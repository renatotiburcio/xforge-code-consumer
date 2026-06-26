---
id: performance-optimization-dotnet
type: conhecimento
tags: [performance, benchmark, memory, cache, pooling, async, dotnet]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Performance e Otimização em .NET
- **Seções principais**: Object Pooling, Compiled Queries (EF Core), Batch Operations (EF Core 7+), Async/Await
- **Tags**: performance, benchmark, memory, cache, pooling, async, dotnet
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `performance-optimization-dotnet` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 11 |


# Performance e Otimização em .NET

## Object Pooling

```csharp
// Reutilizar objetos custosos
services.AddObjectPoolBuilder()
    .AddStringBuilder()
    .SetPoolMaxSize(100);

// Uso
public class MyService
{
    private readonly ObjectPool<StringBuilder> _pool;
    
    public string ProcessLargeData(IEnumerable<string> items)
    {
        var sb = _pool.Get();
        try
        {
            foreach (var item in items)
                sb.AppendLine(item);
            return sb.ToString();
        }
        finally
        {
            _pool.Return(sb);
        }
    }
}
```

## Compiled Queries (EF Core)

```csharp
// Para queries executadas milhares de vezes
private static readonly Func<AppDbContext, int, Task<Order?>> GetOrderById =
    EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
        ctx.Orders
            .Include(o => o.Items)
            .FirstOrDefault(o => o.Id == id));

// Uso
var order = await GetOrderById(_context, orderId);
```

## Batch Operations (EF Core 7+)

```csharp
// Bulk update
await context.Products
    .Where(p => p.CategoryId == categoryId)
    .ExecuteUpdateAsync(s => s
        .SetProperty(p => p.Discount, 0.1m));

// Bulk delete
await context.Products
    .Where(p => p.IsDiscontinued)
    .ExecuteDeleteAsync();
```

## Async/Await

```csharp
// ✅ BOM: Async em chain completa
public async Task<Order?> GetOrderAsync(int id)
{
    return await _context.Orders
        .FirstOrDefaultAsync(o => o.Id == id);
}

// ❌ RUIM: Block em async
public Order GetOrder(int id)
{
    return _context.Orders
        .FirstOrDefault(o => o.Id == id)
        .GetAwaiter().GetResult(); // DEADLOCK RISK
}

// ❌ RUIM: async em methods síncronas
public async Task<int> CountAsync()
{
    return await Task.FromResult(42); // Sem necessidade
}
```

## Caching

### Memory Cache
```csharp
builder.Services.AddMemoryCache();

public class ProductService
{
    private readonly IMemoryCache _cache;
    
    public async Task<Product?> GetByIdAsync(int id)
    {
        var key = $"product_{id}";
        if (_cache.TryGetValue(key, out Product? cached))
            return cached;
        
        var product = await _db.Products.FindAsync(id);
        _cache.Set(key, product, TimeSpan.FromMinutes(5));
        return product;
    }
}
```

### Redis Cache
```csharp
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
    options.InstanceName = "erp_";
});

// Distributed lock
public class DistributedLockService
{
    private readonly IDistributedCache _cache;
    
    public async Task<bool> TryLockAsync(string key, TimeSpan expiry)
    {
        var value = Guid.NewGuid().ToString();
        var existing = await _cache.GetAsync(key);
        if (existing != null) return false;
        
        await _cache.SetAsync(key, Encoding.UTF8.GetBytes(value), 
            new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = expiry });
        return true;
    }
}
```

## Span<T> e Memory<T>

```csharp
// Evita alocação de heap
public static bool IsHex(ReadOnlySpan<char> input)
{
    return input.Length > 0 && 
           input.All(c => char.IsDigit(c) || "abcdefABCDEF".Contains(c));
}

// String interpolation handler
[InterpolatedStringHandler]
public ref struct LogInterpolatedStringHandler
{
    // Performance otimizada para logging
}
```

## StringBuilder vs String Concatenation

```csharp
// ❌ RUIM: O(n²) por alocação
string result = "";
for (int i = 0; i < 10000; i++)
    result += i.ToString(); // Nova string a cada concatenação

// ✅ BOM: O(n)
var sb = new StringBuilder();
for (int i = 0; i < 10000; i++)
    sb.Append(i);
var result = sb.ToString();
```

## ValueTask

```csharp
// Para operações que podem ser síncronas
public async ValueTask<Result> ProcessAsync(Request request)
{
    if (CanProcessSync(request))
        return ProcessSync(request); // Sem async overhead
    
    return await ProcessAsyncInternal(request);
}
```

## Benchmarking

```csharp
[MemoryDiagnoser]
[SimpleJob(RuntimeMoniker.Net10)]
public class MyBenchmark
{
    [Benchmark(Baseline = true)]
    public string StringConcat()
    {
        string result = "";
        for (int i = 0; i < 1000; i++)
            result += i;
        return result;
    }

    [Benchmark]
    public string StringBuilder()
    {
        var sb = new StringBuilder();
        for (int i = 0; i < 1000; i++)
            sb.Append(i);
        return sb.ToString();
    }
}
```

## Checklist de Performance

- [ ] Async/await em toda a chain
- [ ] Compiled queries para queries quentes
- [ ] Batch operations para updates em massa
- [ ] Caching para dados que mudam pouco
- [ ] Span<T> para operações de string
- [ ] Object pooling para objetos custosos
- [ ] Lazy loading apenas quando necessário
- [ ] Pagination para listas grandes
- [ ] No-tracking para leituras
- [ ] Index em colunas de WHERE/JOIN

## Fontes Oficiais
- docs.microsoft.com/dotnet/core/performance
- benchmarkdotnet.org
- github.com/davidfowl/Performance
