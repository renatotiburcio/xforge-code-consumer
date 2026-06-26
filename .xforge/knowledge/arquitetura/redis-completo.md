---
id: redis-completo
type: conhecimento
tags: [redis, cache, distributed-lock, pub-sub, session, queue, sentinel, cluster]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Redis - Guia Completo
- **Seções principais**: Conceito, Casos de Uso, Setup com .NET, Cache
- **Tags**: redis, cache, distributed-lock, pub-sub, session, queue, sentinel, cluster
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `redis-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 13 |


# Redis - Guia Completo

## Conceito

Redis é um banco de dados em memória multi-modelo, usado para cache, filas, sessões, pub/sub e lock distribuído.

## Casos de Uso

| Caso | Comando | Exemplo |
|------|---------|---------|
| Cache | GET/SET | Cache de consultas |
| Session | SET + TTL | Sessões de usuário |
| Lock distribuído | SET NX | Controle de concorrência |
| Pub/Sub | PUBLISH/SUBSCRIBE | Notificações |
| Filas | LPUSH/BRPOP | Background jobs |
| Contadores | INCR | Rate limiting |
| Geospatial | GEOSEARCH | Busca por localização |

## Setup com .NET

```csharp
// Program.cs
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "xforge_";
});

builder.Services.AddStackExchangeRedisExtensions();
builder.Services.AddSingleton<IConnectionMultiplexer>(
    ConnectionMultiplexer.Connect(builder.Configuration.GetConnectionString("Redis")!));
```

## Cache

### MemoryCache vs Redis

| Aspecto | MemoryCache | Redis |
|---------|-------------|-------|
| Escopo | Instância única | Distribuído |
| Persistência | Não | Sim (RDB/AOF) |
| Performance | Extremamente rápida | Rápida (~1ms) |
| Uso | App single-server | Multi-server |

### Implementação
```csharp
public class RedisCacheService : ICacheService
{
    private readonly IDatabase _db;
    
    public async Task<T?> GetAsync<T>(string key)
    {
        var value = await _db.StringGetAsync(key);
        return value.HasValue ? JsonSerializer.Deserialize<T>(value!) : default;
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
    {
        var json = JsonSerializer.Serialize(value);
        await _db.StringSetAsync(key, json, expiry);
    }
    
    public async Task RemoveAsync(string key)
    {
        await _db.KeyDeleteAsync(key);
    }
    
    public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiry = null)
    {
        var cached = await GetAsync<T>(key);
        if (cached != null) return cached;
        
        var value = await factory();
        await SetAsync(key, value, expiry);
        return value;
    }
}
```

### Cache Patterns

```csharp
// Cache-Aside
public async Task<Product?> GetProductAsync(int id)
{
    var key = $"product:{id}";
    var cached = await _cache.GetAsync<Product>(key);
    if (cached != null) return cached;
    
    var product = await _db.Products.FindAsync(id);
    if (product != null)
        await _cache.SetAsync(key, product, TimeSpan.FromMinutes(5));
    
    return product;
}

// Write-Through
public async Task UpdateProductAsync(Product product)
{
    await _db.Products.UpdateAsync(product);
    await _cache.SetAsync($"product:{product.Id}", product, TimeSpan.FromMinutes(5));
}

// Write-Behind
public async Task UpdateProductAsync(Product product)
{
    await _cache.SetAsync($"product:{product.Id}", product, TimeSpan.FromMinutes(5));
    _ = Task.Run(async () => await _db.Products.UpdateAsync(product));
}
```

## Distributed Lock

```csharp
public class RedisDistributedLock : IDistributedLock
{
    private readonly IConnectionMultiplexer _redis;
    
    public async Task<IDisposable?> AcquireAsync(string key, TimeSpan timeout)
    {
        var db = _redis.GetDatabase();
        var value = Guid.NewGuid().ToString();
        
        var acquired = await db.StringSetAsync(
            $"lock:{key}", value, timeout, When.NotExists);
        
        if (!acquired) return null;
        
        return new LockReleaser(db, key, value);
    }
}

public class LockReleaser : IDisposable
{
    private readonly IDatabase _db;
    private readonly string _key;
    private readonly string _value;
    
    public LockReleaser(IDatabase db, string key, string value)
    {
        _db = db;
        _key = key;
        _value = value;
    }
    
    public void Dispose()
    {
        // Só libera se ainda for o dono
        var script = @"
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('del', KEYS[1])
            end
            return 0";
        
        _db.ScriptEvaluate(script, new RedisKey[] { _key }, new RedisValue[] { _value });
    }
}

// Uso
using var lock = await _distributedLock.AcquireAsync("order:123", TimeSpan.FromSeconds(30));
if (lock == null)
    throw new InvalidOperationException("Could not acquire lock");
    
// Processar...
```

## Pub/Sub

```csharp
// Publisher
public class RedisEventPublisher : IEventPublisher
{
    private readonly ISubscriber _subscriber;
    
    public async Task PublishAsync<T>(string channel, T message)
    {
        var json = JsonSerializer.Serialize(message);
        await _subscriber.PublishAsync(channel, json);
    }
}

// Subscriber
public class RedisEventSubscriber : IHostedService
{
    private readonly ISubscriber _subscriber;
    
    public Task StartAsync(CancellationToken ct)
    {
        _subscriber.Subscribe("order-events", async (channel, message) =>
        {
            var @event = JsonSerializer.Deserialize<OrderEvent>(message!);
            await ProcessEventAsync(@event!);
        });
        
        return Task.CompletedTask;
    }
    
    public Task StopAsync(CancellationToken ct) => Task.CompletedTask;
}
```

## Sessions

```csharp
// Configuração
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Redis como session store
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
    options.InstanceName = "session_";
});
```

## Rate Limiting

```csharp
public class RedisRateLimiter
{
    private readonly IDatabase _db;
    
    public async Task<bool> IsAllowedAsync(string key, int limit, TimeSpan window)
    {
        var current = await _db.StringIncrementAsync($"ratelimit:{key}");
        
        if (current == 1)
        {
            await _db.KeyExpireAsync($"ratelimit:{key}", window);
        }
        
        return current <= limit;
    }
}

// Uso
var allowed = await _rateLimiter.IsAllowedAsync($"api:{ip}", 100, TimeSpan.FromMinutes(1));
if (!allowed)
    return Results.StatusCode(429);
```

## Queues

```csharp
// Producer
public async Task EnqueueAsync(string queue, string message)
{
    var db = _redis.GetDatabase();
    await db.ListRightPushAsync($"queue:{queue}", message);
}

// Consumer
public async Task<string?> DequeueAsync(string queue, TimeSpan? timeout = null)
{
    var db = _redis.GetDatabase();
    var result = await db.ListLeftPopAsync($"queue:{queue}");
    return result.HasValue ? result.ToString() : null;
}

// Blocking consumer
public async Task<string?> BlockingDequeueAsync(string queue, TimeSpan? timeout = null)
{
    var db = _redis.GetDatabase();
    var result = await db.ListLeftPopAsync($"queue:{queue}", timeout ?? TimeSpan.FromSeconds(5));
    return result.HasValue ? result.ToString() : null;
}
```

## Sentinel (Alta Disponibilidade)

```yaml
# redis-sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

```csharp
// Conexão com Sentinel
var options = new ConfigurationOptions
{
    ServiceName = "mymaster",
    AbortOnConnectFail = false
};
options.Endpoints.Add("sentinel1:26379");
options.Endpoints.Add("sentinel2:26379");
options.Endpoints.Add("sentinel3:26379");

var multiplexer = await ConnectionMultiplexer.ConnectAsync(options);
```

## Comandos Úteis

```bash
# Informações
INFO server
INFO memory
INFO clients
DBSIZE

# Gerenciamento
KEYS product:*
DEL product:123
EXISTS product:123
EXPIRE product:123 3600
TTL product:123

# Strings
GET product:123
SET product:123 '{"name":"Test"}'
INCR counter
APPEND key "value"

# Hashes
HSET user:1 name "John"
HGET user:1 name
HGETALL user:1

# Lists
LPUSH queue "task1"
RPOP queue
LRANGE queue 0 -1

# Sets
SADD tags "csharp" "dotnet"
SMEMBERS tags
SISMEMBER tags "csharp"

# Sorted Sets
ZADD leaderboard 100 "player1"
ZRANGE leaderboard 0 -1 WITHSCORES
```

## Performance

### Pipeline
```csharp
var batch = _db.CreateBatch();

var tasks = new List<Task>();
for (int i = 0; i < 1000; i++)
{
    tasks.Add(batch.StringSetAsync($"key:{i}", $"value:{i}"));
}

batch.Execute();
await Task.WhenAll(tasks);
```

### Lua Scripts
```lua
-- Script atômico
local current = redis.call('GET', KEYS[1])
if current == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
```

## Fontes Oficiais
- redis.io
- docs.microsoft.com/azure/azure-cache-for-redis
- StackExchange.Redis documentation
