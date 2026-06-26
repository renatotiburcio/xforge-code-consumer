---
id: playbook-perf-n-plus-1-query
type: playbook
title: N+1 Query Problem - Identificar e Resolver
severity: high
status: validated
trustScore: 93
source: dotnet-docs + operacao-real
lastValidated: 2026-06-14
tags: ["performance", "n+1", "orm", "ef-core", "database", "query"]
---

## Sintoma
- Endpoint lento: 2-5s para retornar 100 items
- CPU do banco alta com queries simples
- Log mostra mesmas queries repetidas em loop
- p99 latency degrada com mais dados

## Causa
Loop que executa 1 query por iteracao, ao inves de 1 query batch.
```python
# RUIM: N+1
for cliente in clientes:  # 1 query para clientes
    pedidos = db.query(f"SELECT * FROM pedidos WHERE cliente_id={cliente.id}")  # N queries
# Total: 1 + N queries (N = 1000 clientes = 1001 queries)
```

```python
# BOM: 1 query com JOIN ou IN
clientes_com_pedidos = db.query("""
    SELECT c.*, p.* FROM clientes c
    LEFT JOIN pedidos p ON p.cliente_id = c.id
    WHERE c.id IN (...)
""")  # 1 query
```

## Como Detectar

### 1. Logs SQL (EF Core)
```json
{
  "EventId": 20101,
  "Category": "Microsoft.EntityFrameworkCore.Database.Command",
  "Message": "Executed DbCommand (5ms) [Parameters=[@__id_0='1'], CommandType='Text', CommandTimeout='30']",
  "CommandText": "SELECT * FROM pedidos WHERE cliente_id = @__id_0"
}
```
Procurar: muitas linhas identicas com parametros diferentes.

### 2. EF Core SQL Logging
```csharp
// Program.cs
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseNpgsql(connStr)
       .LogTo(Console.WriteLine, LogLevel.Information)
       .EnableSensitiveDataLogging());  // dev only
```

### 3. EF Core Query Splitting (correto)
```csharp
// Subdivide automaticamente JOINs em queries separadas
var clientes = await _context.Clientes
    .Include(c => c.Pedidos)
    .AsSplitQuery()  // evita cartesian explosion
    .ToListAsync();
```

### 4. Postgres pg_stat_statements
```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
WHERE query ILIKE '%pedidos%'
ORDER BY calls DESC
LIMIT 20;
-- Se calls for 1000+ para query simples = N+1
```

## Solucoes

### 1. Eager Loading (Include)
```csharp
// Carrega cliente + pedidos em 1 (ou 2 com split) query
var clientes = await _context.Clientes
    .Include(c => c.Pedidos)
    .Where(c => c.Ativo)
    .ToListAsync();
```

### 2. Explicit Loading (quando condicional)
```csharp
var clientes = await _context.Clientes.ToListAsync();
foreach (var c in clientes.Where(c => c.Pedidos.Count > 0))
    await _context.Entry(c).Collection(c => c.Pedidos).LoadAsync();
```

### 3. Projection (Select apenas o necessario)
```csharp
// Mais rapido que Include: nao materializa entidades completas
var resultado = await _context.Clientes
    .Where(c => c.Ativo)
    .Select(c => new
    {
        c.Id,
        c.Nome,
        Pedidos = c.Pedidos.Select(p => new { p.Id, p.Total })
    })
    .ToListAsync();
```

### 4. Batch Query (raw SQL ou LINQ)
```csharp
// 1 query com WHERE IN
var clienteIds = clientes.Select(c => c.Id).ToList();
var pedidos = await _context.Pedidos
    .Where(p => clienteIds.Contains(p.ClienteId))
    .ToListAsync();
var pedidosPorCliente = pedidos.ToLookup(p => p.ClienteId);
```

### 5. Dapper (para queries criticas)
```csharp
using var conn = new NpgsqlConnection(connStr);
var result = await conn.QueryAsync<ClienteComPedidos>(@"
    SELECT c.id, c.nome,
           p.id AS pedido_id, p.total, p.data
    FROM clientes c
    LEFT JOIN pedidos p ON p.cliente_id = c.id
    WHERE c.ativo = true
", buffered: false);
```

## Caso Real (2024-09)
Endpoint `GET /api/pedidos` retornava lista paginada.
Carregava 50 pedidos com include de cliente, items, e historico.
**N+1**: 1 + 50 + 50*5 + 50*3 = 351 queries por request.
**Resultado**: 4.5s latency, 90% CPU no banco.
**Fix**: usar projection + Dapper para o caso complexo, ou split query.
**Resultado**: 1 query com JOIN, 80ms latency, 5% CPU.

## Ferramentas de Deteccao

### EF Core Profiler
```csharp
// HibernatingRhinos.Profiler.Appender para EF Core
// Mostra N+1 visualmente
```

### Postgres Slow Query Log
```ini
# postgresql.conf
log_min_duration_statement = 500  # log queries > 500ms
log_statement = 'all'  # dev only
```

### MiniProfiler
```csharp
// Para ASP.NET Core: SqlStoreDiagnosticsListener
// Mostra tempo por query em /miniprofiler
```

## Prevencao

### Code Review
- [ ] Toda query em loop tem justificativa?
- [ ] Include/ThenInclude para navegacoes?
- [ ] Projection ao inves de entidade completa quando possivel?
- [ ] Pagination implementada?

### Testes de Performance
```csharp
[Fact]
public async Task ListarPedidos_DeveExecutarMenosDe5Queries()
{
    var queries = new List<string>();
    using var listener = new SqlClientListener(q => queries.Add(q));
    using var scope = _factory.Services.CreateScope();
    var svc = scope.ServiceProvider.GetRequiredService<IPedidoService>();
    await svc.ListarAsync(novo PageRequest(1, 50));
    Assert.True(queries.Count < 5, $"N+1 detectado: {queries.Count} queries");
}
```

### Limites no Banco
- Connection pool: 100 connections max
- Statement timeout: 30s default
- Slow query log: queries > 1s

## Referencias
- EF Core: Loading Related Data
- Use AsSplitQuery: https://learn.microsoft.com/en-us/ef-core/querying/single-split-queries
- Dapper: https://www.learndapper.com/
- Postgres pg_stat_statements
- Stack Overflow: https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem
