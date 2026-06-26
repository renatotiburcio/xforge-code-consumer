---
id: playbook-dotnet-memory-leak
type: playbook
title: .NET Memory Leak - Diagnosticar e Resolver
severity: high
status: validated
trustScore: 92
source: dotnet-docs + operacao-real
lastValidated: 2026-06-14
tags: ["dotnet", "memory-leak", "performance", "gc", "diagnostic"]
---

## Sintoma
- Memoria do processo subindo continuamente (nao retorna ao baseline)
- OOM killed eventualmente (Linux) ou `OutOfMemoryException`
- GC pauses cada vez mais frequentes
- Latencia p99 degradando ao longo do tempo (ate reciclar)

## Causas Comuns (.NET)

### 1. Event Handlers nao removidos
```csharp
// RUIM
public class MyService
{
    public MyService()
    {
        SomeStaticEvent.Source += OnSomething;  // segura referencia para sempre
    }
}

// BOM
public class MyService : IDisposable
{
    public MyService()
    {
        SomeStaticEvent.Source += OnSomething;
    }
    public void Dispose()
    {
        SomeStaticEvent.Source -= OnSomething;
    }
}
```

### 2. Singleton com referencia a Scoped/Transient
```csharp
// RUIM: cache guarda referencia a DbContext
public class CacheService
{
    private static readonly Dictionary<int, MyEntity> _cache = new();
    public void Add(MyEntity e) { _cache.Add(e.Id, e); }  // e eh scoped!
}

// BOM: usar ID + factory
public class CacheService
{
    private readonly Dictionary<int, Func<MyEntity>> _factories = new();
}
```

### 3. HttpClient mal usado
```csharp
// RUIM: cria novo HttpClient a cada request (socket exhaustion)
public async Task<string> CallAsync()
{
    using var client = new HttpClient();  // socket leak
    return await client.GetStringAsync(...);
}

// BOM: IHttpClientFactory
services.AddHttpClient<MyService>(c => c.BaseAddress = new Uri("..."));
```

### 4. Streams nao fechados
```csharp
// RUIM
var stream = new FileStream("file.txt", FileMode.Open);
var data = await stream.ReadAsync(buffer);  // stream nunca fechado

// BOM: using
using var stream = new FileStream("file.txt", FileMode.Open);
var data = await stream.ReadAsync(buffer);
```

### 5. Timer / Background Service segurando referencia
```csharp
// RUIM: timer nunca disposed
public class MyService
{
    private readonly Timer _timer = new Timer(DoWork, null, 0, 1000);
    // Singleton, vive para sempre, retem tudo que acessar
}

// BOM: implementa IDisposable corretamente
```

## Como Diagnosticar

### 1. Capturar memory dump
```bash
# dotnet-dump (Linux)
dotnet-dump collect -p <PID> --type Heap
# Gera arquivo .dump

# ou (Windows)
procdump -ma <PID> dump.dmp
```

### 2. Analisar com dotnet-dump
```bash
dotnet-dump analyze dump.core

# Comandos uteis:
dumpheap -stat              # visao geral por tipo
dumpheap -stat -type System.String  # strings
dumpheap -mt <method_table>  # detalhes de um tipo
gcroot <address>            # quem segura esta referencia
threads                    # listar threads
setthread <tid>             # focar em thread
```
- `dot Memory` (JetBrains) - GUI
- PerfView (Microsoft) - gratuito, GUI

### 3. Analise rapida
```bash
# Top 10 tipos em memoria
dumpheap -stat | sort -k 2 -n -r | head -20

# Procura tipos esperados vazando (ex: HttpClient, DbContext)
dumpheap -stat -type System.Net.Http.HttpClient
dumpheap -stat -type Microsoft.EntityFrameworkCore.DbContext
```

### 4. Memory Profiler (visual)
- dotMemory (JetBrains)
- ANTS Memory Profiler (Red Gate)
- Visual Studio Diagnostic Tools (F5 debug)

## Solucoes por Padrao

### 1. WeakReference / WeakEvent
```csharp
public class WeakEvent<T>
{
    private readonly List<WeakReference<Action<T>>> _handlers = new();
    public void Subscribe(Action<T> handler) => _handlers.Add(new WeakReference<Action<T>>(handler));
    public void Raise(T arg)
    {
        foreach (var w in _handlers.ToList())
        {
            if (w.TryGetTarget(out var h)) h(arg);
            else _handlers.Remove(w);  // limpa dead refs
        }
    }
}
```

### 2. MemoryCache com eviction
```csharp
services.AddMemoryCache(opt =>
{
    opt.SizeLimit = 1024;  // MB
});

// Ou usar Redis com TTL
services.AddStackExchangeRedisCache(opt => { ... });
```

### 3. ArrayPool para buffers
```csharp
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try
{
    await stream.ReadAsync(buffer.AsMemory());
}
finally
{
    ArrayPool<byte>.Shared.Return(buffer);
}
```

### 4. ConfigureAwait(false) em libraries
```csharp
public async Task<string> DoWorkAsync()
{
    var result = await SomeCallAsync().ConfigureAwait(false);
    // nao segura SynchronizationContext
    return result;
}
```

## Caso Real (2025-01)
API com memory leak. Memoria subia 50MB/hora ate OOM.
**Causa**: Background service injetava `IServiceProvider` em singleton, recriava DbContext a cada tick.
**Fix**: usar `IServiceScopeFactory` para criar scope novo a cada iteracao.
**Resultado**: memoria estavel em 200MB por semanas.

## Prevencao

### 1. Testes de Stress com Memory Tracking
```csharp
[Fact]
public async Task StressTest_NaoDeveTerMemoryLeak()
{
    var baseline = GC.GetTotalMemory(true);
    for (int i = 0; i < 1000; i++)
        await _service.ProcessAsync(new Request());
    var after = GC.GetTotalMemory(true);
    Assert.True(after < baseline * 1.5, $"Memory grew {(after - baseline) / 1024.0 / 1024.0:F1}MB");
}
```

### 2. Monitoring em Producao
```csharp
// OpenTelemetry meter
var memCounter = Meter.CreateUpDownCounter<long>("process.memory.working_set");
services.AddSingleton(memCounter);

// Job periodico (60s)
public class MemoryReporter : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var mem = Process.GetCurrentProcess().WorkingSet64;
            memCounter.Record(mem);
            await Task.Delay(60000, ct);
        }
    }
}
```

Alerta: `process.memory.working_set > 1GB for 30min`

### 3. Code Review Checklist
- [ ] IDisposable implementado quando classe tem recursos?
- [ ] Event handlers removidos em Dispose?
- [ ] HttpClient via IHttpClientFactory?
- [ ] Streams em `using`?
- [ ] Sem referencias estaticas a scoped/transient?
- [ ] ConfigureAwait(false) em libraries?
- [ ] Sem loops infinitos acumulando dados?

## Referencias
- .NET docs: Memory management
- dotnet-dump: https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-dump
- Profiling .NET: https://learn.microsoft.com/en-us/dotnet/core/diagnostics/
- JetBrains dotMemory
- ADR-0022 XForge: Observability Stack
