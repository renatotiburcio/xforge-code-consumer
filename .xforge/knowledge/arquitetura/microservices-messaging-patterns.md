---
id: microservices-messaging-patterns
type: conhecimento
tags: [microservices, rabbitmq, kafka, messaging, event-driven, saga, retry]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Microservices e Padrões de Mensageria
- **Seções principais**: Quando Usar Microservices, Message Brokers, Padrões de Mensageria, Saga Pattern
- **Tags**: microservices, rabbitmq, kafka, messaging, event-driven, saga, retry
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `microservices-messaging-patterns` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# Microservices e Padrões de Mensageria

## Quando Usar Microservices

| Sinal | Monolito Modular | Microservices |
|-------|:----------------:|:-------------:|
| Time pequeno (< 10 devs) | ✅ | ❌ |
| Domínio simples | ✅ | ❌ |
| Escala uniforme | ✅ | ❌ |
| Time grande, múltiplos times | ❌ | ✅ |
| Domínio complexo, bounded contexts | ❌ | ✅ |
| Escala diferenciada por módulo | ❌ | ✅ |

## Message Brokers

### RabbitMQ
```csharp
// Publisher
public class OrderPublisher
{
    private readonly IConnection _connection;
    
    public async Task PublishAsync(OrderCreatedEvent @event)
    {
        using var channel = _connection.CreateModel();
        channel.ExchangeDeclare(exchange: "orders", type: ExchangeType.Topic);
        
        var body = JsonSerializer.SerializeToUtf8Bytes(@event);
        var properties = channel.CreateBasicProperties();
        properties.Persistent = true;
        properties.Headers = new Dictionary<string, object>
        {
            ["event-type"] = nameof(OrderCreatedEvent)
        };
        
        channel.BasicPublish(
            exchange: "orders",
            routingKey: "order.created",
            basicProperties: properties,
            body: body);
    }
}

// Consumer
public class OrderCreatedConsumer : IConsumer<OrderCreatedEvent>
{
    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        var message = context.Message;
        // Processar evento
        await _notificationService.SendAsync(message.CustomerId, "Pedido criado!");
    }
}
```

### Kafka
```csharp
// Producer
var config = new ProducerConfig { BootstrapServers = "localhost:9092" };
using var producer = new ProducerBuilder<string, string>(config).Build();
await producer.ProduceAsync("orders", new Message<string, string>
{
    Key = orderId.ToString(),
    Value = JsonSerializer.Serialize(@event)
});

// Consumer
var config = new ConsumerConfig
{
    BootstrapServers = "localhost:9092",
    GroupId = "order-service",
    AutoOffsetReset = AutoOffsetReset.Earliest
};
using var consumer = new ConsumerBuilder<string, string>(config).Build();
consumer.Subscribe("orders");
var result = consumer.Consume();
```

## Padrões de Mensageria

### Pub/Sub
```
Publisher → Exchange/Topic → Subscriber 1
                           → Subscriber 2
                           → Subscriber 3
```

### Point-to-Point
```
Producer → Queue → Consumer
```

### Request-Reply
```
Client → Request Queue → Service
Client ← Reply Queue ← Service
```

## Saga Pattern

### Choreography-based
```
Order Service → OrderCreated → Payment Service
Payment Service → PaymentProcessed → Inventory Service
Inventory Service → InventoryReserved → Shipping Service
```

### Orchestration-based
```csharp
public class OrderSaga
{
    public async Task ExecuteAsync(CreateOrderCommand cmd)
    {
        try
        {
            var order = await _orderService.CreateAsync(cmd);
            await _paymentService.ChargeAsync(order.Id, order.Total);
            await _inventoryService.ReserveAsync(order.Items);
            await _shippingService.ScheduleAsync(order.Id);
            await _orderService.ConfirmAsync(order.Id);
        }
        catch (Exception ex)
        {
            await CompensateAsync(cmd);
            throw;
        }
    }
}
```

## Retry Policies

```csharp
// Polly
services.AddHttpClient<IApiClient, ApiClient>()
    .AddPolicyHandler(Policy<HttpResponseMessage>
        .Handle<HttpRequestException>()
        .OrResult(r => !r.IsSuccessStatusCode)
        .WaitAndRetryAsync(3, retry => 
            TimeSpan.FromSeconds(Math.Pow(2, retry))));

// Circuit Breaker
services.AddHttpClient<IApiClient, ApiClient>()
    .AddPolicyHandler(Policy<HttpResponseMessage>
        .Handle<HttpRequestException>()
        .CircuitBreakerAsync(
            eventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30)));
```

## Outbox Pattern

```csharp
public class OutboxMessage
{
    public Guid Id { get; set; }
    public string EventType { get; set; }
    public string Payload { get; set; }
    public DateTime CreatedAt { get; set; }
    public bool Processed { get; set; }
}

// Na mesma transação do banco
public async Task CreateOrderAsync(CreateOrderCommand cmd)
{
    using var transaction = await _context.Database.BeginTransactionAsync();
    
    var order = new Order(cmd.CustomerId);
    _context.Orders.Add(order);
    
    _context.OutboxMessages.Add(new OutboxMessage
    {
        EventType = nameof(OrderCreatedEvent),
        Payload = JsonSerializer.Serialize(new OrderCreatedEvent(order.Id)),
        CreatedAt = DateTime.UtcNow
    });
    
    await _context.SaveChangesAsync();
    await transaction.CommitAsync();
}

// Background job processa outbox
public class OutboxProcessor : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var messages = await _context.OutboxMessages
                .Where(m => !m.Processed)
                .Take(100)
                .ToListAsync(ct);
            
            foreach (var msg in messages)
            {
                await _eventBus.PublishAsync(msg.EventType, msg.Payload);
                msg.Processed = true;
            }
            await _context.SaveChangesAsync(ct);
            
            await Task.Delay(TimeSpan.FromSeconds(5), ct);
        }
    }
}
```

## Fontes Oficiais
- docs.microsoft.com/azure/architecture/patterns
- microservices.io/patterns
- rabbitmq.com/tutorials
- confluent.io/kafka
