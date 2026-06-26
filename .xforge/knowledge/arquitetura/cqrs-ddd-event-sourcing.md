---
id: cqrs-ddd-event-sourcing
type: conhecimento
tags: [cqrs, ddd, event-sourcing, domain-events, aggregates, value-objects]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre CQRS, DDD e Event Sourcing
- **Seções principais**: DDD (Domain-Driven Design), CQRS (Command Query Responsibility Segregation), Event Sourcing, Quando Usar Cada Um
- **Tags**: cqrs, ddd, event-sourcing, domain-events, aggregates, value-objects
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `cqrs-ddd-event-sourcing` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 5 |


# CQRS, DDD e Event Sourcing

## DDD (Domain-Driven Design)

### Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Entity** | Objeto com identidade única (ex: Pedido, Cliente) |
| **Value Object** | Objeto sem identidade, imutável (ex: Dinheiro, Endereço) |
| **Aggregate** | Grupo de objetos com uma raiz (ex: Pedido + Itens) |
| **Aggregate Root** | Entidade raiz do aggregate (ex: Pedido) |
| **Domain Event** | Evento que aconteceu no domínio (ex: PedidoCriado) |
| **Repository** | Interface para persistência de aggregates |
| **Domain Service** | Lógica que não pertence a nenhuma entidade |

### Value Object
```csharp
public record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (amount < 0) throw new ArgumentException("Amount cannot be negative");
        Amount = amount;
        Currency = currency;
    }

    public static Money BRL(decimal amount) => new(amount, "BRL");
    public static Money USD(decimal amount) => new(amount, "USD");

    public Money Add(Money other)
    {
        if (Currency != other.Currency) throw new InvalidOperationException("Different currencies");
        return new Money(Amount + other.Amount, Currency);
    }
}
```

### Aggregate Root
```csharp
public class Order : AggregateRoot
{
    private readonly List<OrderItem> _items = new();
    
    public int CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money Total => _items.Aggregate(Money.BRL(0), (acc, i) => acc.Add(i.Subtotal));
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();

    public Order(int customerId)
    {
        CustomerId = customerId;
        Status = OrderStatus.Created;
        AddDomainEvent(new OrderCreatedEvent(Id, customerId));
    }

    public void AddItem(Product product, int quantity)
    {
        if (Status != OrderStatus.Created)
            throw new InvalidOperationException("Cannot add items to non-created order");
        
        var item = new OrderItem(product.Id, quantity, product.Price);
        _items.Add(item);
        AddDomainEvent(new OrderItemAddedEvent(Id, product.Id, quantity));
    }

    public void Confirm()
    {
        if (Status != OrderStatus.Created)
            throw new InvalidOperationException("Only created orders can be confirmed");
        
        Status = OrderStatus.Confirmed;
        AddDomainEvent(new OrderConfirmedEvent(Id));
    }
}
```

### Domain Events
```csharp
public record OrderCreatedEvent(int OrderId, int CustomerId) : IDomainEvent;
public record OrderConfirmedEvent(int OrderId) : IDomainEvent;
public record OrderItemAddedEvent(int OrderId, int ProductId, int Quantity) : IDomainEvent;

// Handler
public class OrderCreatedHandler : IDomainEventHandler<OrderCreatedEvent>
{
    public async Task HandleAsync(OrderCreatedEvent domainEvent)
    {
        // Enviar notificação, atualizar cache, etc.
    }
}
```

## CQRS (Command Query Responsibility Segregation)

### Separar Leitura e Escrita

```csharp
// Commands (Escrita)
public record CreateOrderCommand(int CustomerId, List<OrderItemDto> Items) : IRequest<OrderDto>;
public record ConfirmOrderCommand(int OrderId) : IRequest;
public record CancelOrderCommand(int OrderId, string Reason) : IRequest;

// Queries (Leitura)
public record GetOrderByIdQuery(int OrderId) : IRequest<OrderDto>;
public record GetOrdersByCustomerQuery(int CustomerId) : IRequest<List<OrderDto>>;

// Handlers
public class CreateOrderHandler : IRequestHandler<CreateOrderCommand, OrderDto>
{
    public async Task<OrderDto> HandleAsync(CreateOrderCommand cmd, CancellationToken ct)
    {
        var order = new Order(cmd.CustomerId);
        foreach (var item in cmd.Items)
            order.AddItem(/* ... */);
        
        await _repo.AddAsync(order);
        return order.ToDto();
    }
}

public class GetOrderByIdHandler : IRequestHandler<GetOrderByIdQuery, OrderDto>
{
    public async Task<OrderDto> HandleAsync(GetOrderByIdQuery query, CancellationToken ct)
    {
        // Leitura de read model (projeção)
        return await _readDb.GetOrderDtoAsync(query.OrderId);
    }
}
```

### Write Model vs Read Model

```csharp
// Write Model (Normalizado)
public class Order
{
    public int Id { get; set; }
    public int CustomerId { get; set; }
    public OrderStatus Status { get; set; }
    public List<OrderItem> Items { get; set; }
}

// Read Model (Desnormalizado para consulta)
public class OrderDto
{
    public int Id { get; set; }
    public string CustomerName { get; set; }
    public decimal Total { get; set; }
    public string Status { get; set; }
    public int ItemCount { get; set; }
    public DateTime CreatedAt { get; set; }
}
```

## Event Sourcing

### Conceito
- Salvar eventos, não estado
- Estado é reconstruído a partir dos eventos
- Histórico completo preservado

### Implementação
```csharp
public abstract class EventStore
{
    public async Task SaveAsync(string streamId, IEnumerable<IDomainEvent> events)
    {
        foreach (var @event in events)
        {
            await AppendAsync(streamId, @event);
        }
    }

    public async Task<T> LoadAsync<T>(string streamId) where T : AggregateRoot, new()
    {
        var aggregate = new T();
        var events = await GetEventsAsync(streamId);
        foreach (var @event in events)
        {
            aggregate.Apply(@event);
        }
        return aggregate;
    }
}

// Aggregate com Apply
public class Order : AggregateRoot
{
    public void Apply(IDomainEvent @event)
    {
        switch (@event)
        {
            case OrderCreatedEvent e:
                Id = e.OrderId;
                CustomerId = e.CustomerId;
                break;
            case OrderConfirmedEvent:
                Status = OrderStatus.Confirmed;
                break;
        }
    }
}
```

## Quando Usar Cada Um

| Padrão | Quando Usar |
|--------|-------------|
| **DDD** | Domínio complexo, muitas regras de negócio |
| **CQRS** | Performance de leitura crítica, múltiplas views |
| **Event Sourcing** | Audit trail completo, undo/redo, debugging |
| **Todos juntos** | ERP complexo com muitas integrações |

## Fontes Oficiais
- Domain-Driven Design (Eric Evans)
- Microsoft eShopOnContainers
- Marten (Event Sourcing for .NET)
