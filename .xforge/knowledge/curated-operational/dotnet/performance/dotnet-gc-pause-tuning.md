---
id: playbook-dotnet-gc-pause-tuning
type: playbook
title: .NET GC Pauses Longas - Diagnosticar e Tunar
severity: medium
status: validated
trustScore: 89
source: dotnet-docs + maoni-blog
lastValidated: 2026-06-14
tags: ["dotnet", "gc", "performance", "tuning", "memory"]
---

## Sintoma
- Latency p99 com picos inexplicaveis (50-500ms)
- Logs mostram "GC pause" ou "Gen 2 collection"
- Application pool recicla com OutOfMemoryException
- Throughput varia mesmo com CPU baixa

## Causas Comuns

### 1. Large Object Heap (LOH) fragmentation
- Objetos > 85KB vao para LOH
- LOH nao compacta por padrao (.NET < 5)
- LOH fragments = full GC para alocar

```csharp
// Ativ ar LOH compaction (.NET 5+)
GCSettings.LargeObjectHeapCompactionMode = GCLargeObjectHeapCompactionMode.CompactOnce;

// Ou forcar manualmente
GC.Collect(2, GCCollectionMode.Forced, blocking: true, compacting: true);
```

### 2. Async/await com state machines pesados
- Cada `await` aloca um state machine
- Multi-await em loop = milhares de allocs

```csharp
// RUIM: state machine por iteracao
foreach (var id in ids)
    await ProcessAsync(id);

// BOM: ProcessAllAsync sem state machine por item
await Task.WhenAll(ids.Select(id => ProcessAsync(id)));
```

### 3. Boxing de value types
- `int.ToString()` em loop = alloc
- Dictionary<int, T> com lookups = alloc

```csharp
// BOM: ArrayPool para buffers
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try { /* use */ } finally { ArrayPool<byte>.Shared.Return(buffer); }
```

### 4. LINQ com allocations
- `Where().Select().ToList()` = 3 enumerators + 1 list
- Em hot path: 10K items = 40K allocs

```csharp
// RUIM (em hot path)
var result = items.Where(x => x.Ativo).Select(x => x.Nome).ToList();

// BOM (manual loop)
var result = new List<string>(items.Count);
for (int i = 0; i < items.Count; i++)
    if (items[i].Ativo) result.Add(items[i].Nome);
```

### 5. Strings concatenadas
- `s1 + s2 + s3` = 3 allocs
- Em loop: O(n^2) allocs

```csharp
// RUIM
string result = "";
for (int i = 0; i < 1000; i++)
    result += items[i].ToString();

// BOM
var sb = new StringBuilder(16384);
for (int i = 0; i < 1000; i++)
    sb.Append(items[i]);
string result = sb.ToString();
```

## Diagnosticar GC

### 1. dotnet-counters
```bash
dotnet-counters monitor -p <PID> System.Runtime
# Mostra: GC heap size, Gen 0/1/2 collections, allocation rate
```

### 2. GC Stats
```csharp
// Habilitar GC stats detalhados
AppContext.SetSwitch("System.GC.Concurrent", true);
AppContext.SetSwitch("System.GC.Server", true);  // server GC

// Latency mode
GCSettings.LatencyMode = GCLatencyMode.SustainedLowLatency;
```

### 3. dotnet-trace (ETW events)
```bash
dotnet-trace collect -p <PID> --providers gc
# Gera arquivo .nettrace
# Abrir em PerfView ou VS
```

### 4. EventCounters (custom)
```csharp
public class GcMonitor
{
    private static readonly Meter _meter = new("MyApp.GC");
    private static readonly Counter<long> _allocCounter = _meter.CreateCounter<long>("allocations");
    private static readonly Histogram<double> _gcPause = _meter.CreateHistogram<double>("gc_pause_ms");
    
    public static void Register()
    {
        AppDomain.CurrentDomain.FirstChanceException += (s, e) => { /* ... */ };
        GC.RegisterForFullGCNotification(10, 10);
    }
}
```

## Tuning de GC

### 1. Workstation vs Server GC
```xml
<!-- .csproj ou runtimeconfig.json -->
<ServerGarbageCollection>true</ServerGarbageCollection>  <!-- server GC: throughput -->
<ConcurrentGarbageCollection>true</ConcurrentGarbageCollection>  <!-- background -->
```

### 2. Heap Sizes
```xml
<GCHeapAffinitizeMask>15</GCHeapAffinitizeMask>  <!-- usa 4 primeiros cores -->
<GCHeapAffinitizeMask>255</GCHeapAffinitizeMask> <!-- usa 8 cores -->
<GCHeapCount>4</GCHeapCount>  <!-- 4 heaps (1 per core) -->
<GCNoAffinitize>0</GCNoAffinitize>
```

### 3. Latency Modes
```csharp
// Para sistemas low-latency (trading, gaming)
GCSettings.LatencyMode = GCLatencyMode.SustainedLowLatency;
// Trade-off: mais CPU (GCs mais frequentes), menos pausas
```

### 4. Tiered Compilation
```xml
<TieredCompilation>true</TieredCompilation>  <!-- .NET Core 3.0+ default -->
<TieredPGO>true</TieredPGO>  <!-- Profile-Guided Optimization -->
```

## Caso Real (2024-11)
API com 1000 RPS, latencia p99 = 1.2s. Picos a 5s inexplicaveis.
**Diagnostico**: 
- dotnet-counters mostrou Gen 2 collections 2x/min
- Cada Gen 2 GC = 800ms pause
- Allocation rate: 50 MB/s
**Root cause**:
- `StringBuilder.ToString()` em hot path de logging
- LOH fragmentation (return de listas grandes como JSON)
**Fix**:
1. `ArrayPool` para buffers de log
2. `GC.TryStartNoGCRegion` durante serializacao
3. `[MemoryDiagnoser]` em benchmarks para validar
**Resultado**: p99 = 150ms, sem picos.

## Padroes de Allocacao

### Object Pool
```csharp
public class ParserPool
{
    private readonly ObjectPool<Parser> _pool;
    
    public ParserPool()
    {
        _pool = new DefaultObjectPool<Parser>(new ParserPolicy(), maxSize: 50);
    }
    
    public async Task<Resultado> ExecutarAsync(string input)
    {
        var parser = _pool.Get();
        try
        {
            return await parser.ParseAsync(input);
        }
        finally
        {
            _pool.Return(parser);
        }
    }
}
```

### Span<T> / Memory<T>
```csharp
// Zero-alloc string parsing
public static int ParseInt(ReadOnlySpan<char> input)
{
    return int.Parse(input);  // Span overload, no alloc
}

// Zero-alloc JSON (System.Text.Json)
public static T Deserialize<T>(ReadOnlySpan<byte> utf8)
{
    return JsonSerializer.Deserialize<T>(utf8);  // no string alloc
}
```

### String.Create
```csharp
// Em .NET 6+: aloca string direto, sem copia intermediaria
string result = string.Create(length: 10, state: (value, format), action: (span, state) =>
{
    var (v, f) = state;
    v.TryFormat(span, out _, f);
});
```

## Prevencao

### 1. Benchmarking em CI
```csharp
[MemoryDiagnoser]
public class MyBench
{
    [Benchmark]
    public List<Item> OldWay() { /* old code */ }
    
    [Benchmark]
    public List<Item> NewWay() { /* new code */ }
}
```

### 2. Profiling Regular
- Profiling de 1h a cada deploy
- Flame graph: identificar top 5 hot paths
- Allocation rate: manter < 10MB/s em codepath de request

### 3. Code Review
- [ ] Sem `new List()` em hot path (usar `ArrayPool` ou pool)
- [ ] Sem `StringBuilder.ToString()` em loop (usar `string.Create` ou cached buffer)
- [ ] Sem LINQ com ToList em hot path
- [ ] Sem boxing de value types
- [ ] Sem string concatenation em loop
- [ ] Sem async sem await (gera warning CS1998)

### 4. Allocation Rate Targets
| Tipo | Alocacao Max |
|------|-------------:|
| Request handler | 1 KB |
| Business logic | 5 KB |
| Background job | 50 KB |
| Report generation | 1 MB |

## Referencias
- .NET docs: Garbage Collection
- Maoni Stephens (MS GC dev): https://maoni0.medium.com/
- Konrad Kokosa: Pro .NET Memory Management
- BenchmarkDotNet: https://benchmarkdotnet.org/
- ADR-0022 XForge: Observability
