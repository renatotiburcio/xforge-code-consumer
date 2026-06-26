---
id: ef-core-patterns
type: pattern
tags: [ef-core, repository, unit-of-work, performance, database, sql]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre EF Core — Padrões de Acesso a Dados
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: ef-core, repository, unit-of-work, performance, database, sql
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `ef-core-patterns` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# EF Core — Padrões de Acesso a Dados

## Propósito

Definir padrões de acesso a dados com EF Core para sistemas ERP, cobrindo Repository, Unit of Work, Specification, compiled queries, split queries, no-tracking e otimizações de performance.

## Descrição do Padrão

### Repository Pattern

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IReadOnlyList<T>> FindAsync(Expression<Func<T, bool>> predicate);
    void Add(T entity);
    void Update(T entity);
    void Delete(T entity);
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _context;
    protected readonly DbSet<T> _dbSet;
    public Repository(AppDbContext context) { _context = context; _dbSet = context.Set(); }
    public virtual async Task<T?> GetByIdAsync(int id) => await _dbSet.FindAsync(id);
    public virtual void Add(T entity) => _dbSet.Add(entity);
    // ...
}
```

### Unit of Work

```csharp
public interface IUnitOfWork : IDisposable
{
    IRepository<Produto> Produtos { get; }
    IRepository<Pedido> Pedidos { get; }
    Task<int> SaveChangesAsync();
}
```

### Specification Pattern

```csharp
public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
}

public class ProdutosAtivosPorCategoriaSpec : ISpecification<Produto>
{
    public Expression<Func<Produto, bool>> Criteria =>
        p => p.Ativo && p.CategoriaId == _categoriaId;
    public List<Expression<Func<Produto, object>>> Includes => new() { p => p.Categoria };
}
```

### Global Query Filters (Multi-tenancy)

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Pedido>().HasQueryFilter(p => p.TenantId == _tenantId);
}
```

### Compiled Queries

```csharp
private static readonly Func<AppDbContext, int, Task<Produto?>> GetProdutoById =
    EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
        ctx.Produtos.FirstOrDefault(p => p.Id == id));
```

### Split Queries vs Single Queries

```csharp
// Use Split Query para múltiplos Includes com grandes volumes
var pedidos = await context.Pedidos
    .Include(p => p.Itens)
    .Include(p => p.Pagamentos)
    .AsSplitQuery()
    .ToListAsync();
```

### No-Tracking para Leitura

```csharp
var produtos = await context.Produtos
    .AsNoTracking()
    .ToListAsync();
```

### Batching (EF Core 7+)

```csharp
// Update em massa sem carregar entidades
await context.Produtos
    .Where(p => p.CategoriaId == 1)
    .ExecuteUpdateAsync(s => s.SetProperty(p => p.Preco, p => p.Preco * 1.1m));
```

## Quando Usar

- **Repository + UoW**: CRUD padrão, separação de camadas.
- **Specification**: Consultas complexas reutilizáveis com Includes dinâmicos.
- **Compiled Queries**: Queries executadas repetidamente (alto throughput).
- **Split Query**: Múltiplos Includes com grandes volumes (evita explosão cartesiana).
- **No-Tracking**: Relatórios, dashboards, APIs GET read-only.
- **Global Filters**: Multi-tenancy, soft delete.

## Exemplo de Uso

```csharp
public class ProdutoService
{
    private readonly IUnitOfWork _uow;
    public async Task<Produto?> ObterPorId(int id) => await _uow.Produtos.GetByIdAsync(id);
    public async Task Criar(Produto produto) { _uow.Produtos.Add(produto); await _uow.SaveChangesAsync(); }
}
```

## Padrões Relacionados

- [[testes]] — testes de repositório com InMemory/SQLite/TestContainers
- [[componentes-blazor.md]] — render modes e acesso a dados
- [[logging.md]] — diagnóstico de queries lentas

