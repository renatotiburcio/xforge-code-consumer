---
id: design-patterns-erp
type: knowledge
tags: [design-patterns, erp, repository, cqrs, domain-events, aggregate, dotnet]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Design Patterns ERP
- **Principais responsabilidades**: Definir contratos de repositório no Domain; Implementar CQRS com XForge.MediatR; Gerenciar ciclo de vida de agregados e eventos de domínio
- **Seções principais**: Propósito, Responsabilidades, Repository, Unit of Work
- **Tags**: design-patterns, erp, repository, cqrs, domain-events, aggregate, dotnet
- **Tipo**: knowledge | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `design-patterns-erp` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 10 |


# Design Patterns ERP

## Propósito
Padrões de projeto específicos para sistemas ERP, com foco em persistência, separação leitura/escrita, eventos de domínio e agregados. Estes padrões complementam os GoF no contexto de domínio rico.

## Responsabilidades
- Definir contratos de repositório no Domain
- Implementar CQRS com XForge.MediatR
- Gerenciar ciclo de vida de agregados e eventos de domínio
- Garantir consistência transacional via Unit of Work

## Repository

```csharp
public interface IRepository<T> where T : AggregateRoot {
    Task<T?> GetByIdAsync(Guid id, CancellationToken ct);
    Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct);
    Task AddAsync(T entity, CancellationToken ct);
    void Update(T entity);
    void Remove(T entity);
}

public interface ISaleRepository : IRepository<Sale> {
    Task<IReadOnlyList<Sale>> GetByCustomerAsync(Guid customerId, CancellationToken ct);
    Task<IReadOnlyList<Sale>> GetByDateRangeAsync(DateTime start, DateTime end, CancellationToken ct);
    Task<decimal> GetTotalSalesAsync(DateTime month, CancellationToken ct);
}

public interface IProductRepository : IRepository<Product> {
    Task<IReadOnlyList<Product>> GetActiveAsync(CancellationToken ct);
    Task<Product?> GetBySkuAsync(string sku, CancellationToken ct);
}
```

## Unit of Work

```csharp
public interface IUnitOfWork : IDisposable {
    ISaleRepository Sales { get; }
    IProductRepository Products { get; }
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}

// EF Core DbContext implementa IUnitOfWork
public class ErpDbContext : DbContext, IUnitOfWork {
    ISaleRepository IUnitOfWork.Sales => new SaleRepository(this);
    IProductRepository IUnitOfWork.Products => new ProductRepository(this);
}
```

## CQRS (Command Query Responsibility Segregation)

```
Commands (Escrita)          Queries (Leitura)
      |                           |
      v                           v
+----------+              +----------+
| Command  |              |  Query   |
| Handler  |              |  Handler |
+-----+----+              +-----+----+
      |                         |
      v                         v
+----------+              +----------+
|  Domain  |              |  Read    |
|  Model   |              |  Model   |
+-----+----+              +-----+----+
      |                         |
      v                         v
+----------+              +----------+
|  Write   |              |  Read    |
|  DB      |              |  DB      |
+----------+              +----------+
```

**Quando usar:** Domínio complexo, volume de leitura >> escrita, equipes separadas.
**Quando NÃO usar:** CRUD simples, projetos pequenos, MVPs.

## Aggregate Root — Sale

```csharp
public class Sale : AggregateRoot {
    public Guid CustomerId { get; private set; }
    public SaleStatus Status { get; private set; }
    public Money Total { get; private set; } = null!;
    private readonly List<SaleItem> _items = new();
    public IReadOnlyCollection<SaleItem> Items => _items.AsReadOnly();

    public Sale(Guid customerId) {
        CustomerId = customerId;
        Status = SaleStatus.Pending;
        AddDomainEvent(new SaleCreatedEvent(Id, customerId));
    }

    public void AddItem(Product product, int quantity) {
        if (Status != SaleStatus.Pending)
            throw new DomainException("Não é possível alterar venda confirmada.");
        var existing = _items.FirstOrDefault(i => i.ProductId == product.Id);
        if (existing is not null) existing.IncreaseQuantity(quantity);
        else _items.Add(new SaleItem(product.Id, product.Name, product.Price, quantity));
        RecalculateTotal();
    }

    public void Confirm() {
        if (!_items.Any()) throw new DomainException("Venda sem itens.");
        Status = SaleStatus.Confirmed;
        AddDomainEvent(new SaleConfirmedEvent(Id, Total));
    }
}
```

## Domain Events

```csharp
public sealed record SaleCreatedEvent(Guid SaleId, Guid CustomerId) : DomainEventBase;
public sealed record SaleConfirmedEvent(Guid SaleId, Money Total) : DomainEventBase;
public sealed record SaleCancelledEvent(Guid SaleId, string Reason) : DomainEventBase;

public abstract record DomainEventBase : IDomainEvent {
    public DateTime OccurredOn { get; init; } = DateTime.UtcNow;
}

// Publicação automática no SaveChanges do DbContext
public override async Task<int> SaveChangesAsync(CancellationToken ct = default) {
    var entities = ChangeTracker.Entries<Entity>()
        .Where(e => e.Entity.DomainEvents.Any()).Select(e => e.Entity).ToList();
    var events = entities.SelectMany(e => e.DomainEvents).ToList();
    entities.ForEach(e => e.ClearDomainEvents());
    foreach (var evt in events) await _mediator.Publish(evt, ct);
    return await base.SaveChangesAsync(ct);
}
```

## Specification

```csharp
public abstract class Specification<T> {
    public abstract Expression<Func<T, bool>> ToExpression();
    public bool IsSatisfiedBy(T entity) => ToExpression().Compile()(entity);
    public Specification<T> And(Specification<T> other) => new AndSpecification<T>(this, other);
}

public class ActiveProductsSpec : Specification<Product> {
    public override Expression<Func<Product, bool>> ToExpression() => p => p.IsActive;
}

public class HighValueSaleSpec : Specification<Sale> {
    private readonly decimal _threshold;
    public HighValueSaleSpec(decimal threshold = 1000m) { _threshold = threshold; }
    public override Expression<Func<Sale, bool>> ToExpression()
        => s => s.Total.Amount >= _threshold;
}
```

## Dependências
- [clean-architecture.md](clean-architecture.md) — Estrutura de camadas
- [design-patterns-gof.md](design-patterns-gof.md) — GoF patterns complementares

## Restrições
- Agregados devem ser pequenos e consistentes transacionalmente
- Domain Events são disparados após SaveChanges, não antes
- Read Models são projeções eventualmente consistentes — não contêm regras de negócio

