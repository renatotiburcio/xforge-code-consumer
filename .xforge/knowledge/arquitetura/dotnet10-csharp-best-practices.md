---
id: dotnet10-csharp-best-practices
type: conhecimento
tags: [dotnet, csharp, dotnet10, best-practices, clean-code, performance]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre .NET 10 e C# — Melhores Práticas
- **Seções principais**: Versão Atual, Novidades .NET 10, Padrões de Código, Performance
- **Tags**: dotnet, csharp, dotnet10, best-practices, clean-code, performance
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `dotnet10-csharp-best-practices` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 8 |


# .NET 10 e C# — Melhores Práticas

## Versão Atual

| Componente | Versão | Status |
|------------|--------|--------|
| .NET | 10 (LTS) | Suporte até Nov 2028 |
| C# | 14 | Estável |
| ASP.NET Core | 10 | Estável |
| EF Core | 10 | Estável |

## Novidades .NET 10

### C# 14
- `field` keyword (propriedades com backing field implícito)
- `params` collections (não só arrays)
- `Lock` type nativo
- `Lazy<T>` melhorado
- `SearchValues` para buscas eficientes
- `TimeSpan.From*` overload com `int`

### ASP.NET Core 10
- `Keyed DI` nativo (não precisa de pacote extra)
- `IAsyncEnumerable` melhorado
- `Output Caching` nativo
- `Rate Limiter` nativo
- `Health Checks` melhorados
- `Minimal APIs` maduro

### EF Core 10
- `Bulk Operations` nativo
- `JSON Columns` suporte nativo
- `Custom Conventions` melhoradas
- `Interceptors` mais granulares
- `Raw SQL` com tipagem

## Padrões de Código

### Record Types
```csharp
// Imutabilidade
public record ProductDto(int Id, string Name, decimal Price);

// Value Objects
public record Money(decimal Amount, string Currency)
{
    public static Money BRL(decimal amount) => new(amount, "BRL");
}

// Pattern Matching
public record Discount(decimal Percent, string Reason);
```

### Primary Constructors
```csharp
// Classes
public class ProductService(IProductRepository repo, ILogger<ProductService> logger)
{
    public async Task<Product?> GetByIdAsync(int id)
    {
        logger.LogInformation("Getting product {Id}", id);
        return await repo.GetByIdAsync(id);
    }
}

// Records
public record CreateProductCommand(string Name, decimal Price, int CategoryId);
```

### Collection Expressions
```csharp
// Antes
var numbers = new List<int> { 1, 2, 3 };
var array = new int[] { 1, 2, 3 };

// Agora (C# 12+)
List<int> numbers = [1, 2, 3];
int[] array = [1, 2, 3];
Span<int> span = [1, 2, 3];
```

### Pattern Matching
```csharp
// Switch expression
var description = product switch
{
    { Price: > 1000 } => "Premium",
    { Price: > 100 } => "Standard",
    { Stock: 0 } => "Out of stock",
    _ => "Regular"
};

// Property patterns
if (order is { Status: OrderStatus.Shipped, Items.Count: > 0 })
{
    // Process shipped order
}

// List patterns
if (numbers is [1, 2, .. var rest])
{
    // first is 1, second is 2, rest is remaining
}
```

## Performance

### Span<T> e Memory<T>
```csharp
// Evita alocação de heap
public static bool IsHex(ReadOnlySpan<char> input)
{
    return input.Length > 0 && 
           input.All(c => char.IsDigit(c) || "abcdefABCDEF".Contains(c));
}
```

### Object Pool
```csharp
// Reutilizar objetos custosos
services.AddObjectPoolBuilder()
    .AddStringBuilder()
    .SetPoolMaxSize(100);
```

### Compiled Queries
```csharp
// EF Core compiled queries
private static readonly Func<AppDbContext, int, Task<Product?>> GetProductById =
    EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
        ctx.Products.FirstOrDefault(p => p.Id == id));
```

### ValueTask
```csharp
// Para operações que podem ser síncronas
public async ValueTask<Result> ProcessAsync(Request request)
{
    if (CanProcessSync(request))
        return ProcessSync(request);
    
    return await ProcessAsyncInternal(request);
}
```

## Clean Code

### Naming
```csharp
// ✅ BOM
public async Task<Order> GetOrderByIdAsync(int orderId)
{
    var order = await _context.Orders.FindAsync(orderId);
    return order ?? throw new NotFoundException(nameof(Order), orderId);
}

// ❌ RUIM
public async Task<Order> GetOrder(int id)
{
    var o = await _context.Orders.FindAsync(id);
    return o;
}
```

### Methods
```csharp
// ✅ Método curto e coeso
public bool CanApplyDiscount(Order order, Discount discount)
{
    return order.Status == OrderStatus.Pending
        && order.Total > discount.MinimumOrderValue
        && !discount.IsExpired;
}

// ❌ Método longo e com múltiplas responsabilidades
public void ProcessOrder(...) // 200+ linhas
```

### Exception Handling
```csharp
// ✅ Exceções específicas
public class OrderNotFoundException : NotFoundException
{
    public OrderNotFoundException(int id) 
        : base($"Order {id} not found") { }
}

// Uso
var order = await repo.GetByIdAsync(id)
    ?? throw new OrderNotFoundException(id);
```

## SOLID em .NET

### S - Single Responsibility
```csharp
// Uma classe = uma responsabilidade
public class OrderValidator { }      // Validação
public class OrderCalculator { }     // Cálculos
public class OrderRepository { }     // Persistência
public class OrderNotifier { }       // Notificações
```

### O - Open/Closed
```csharp
// Aberto para extensão, fechado para modificação
public interface IPaymentProcessor
{
    Task<Result> ProcessAsync(PaymentRequest request);
}

public class CreditCardProcessor : IPaymentProcessor { }
public class PixProcessor : IPaymentProcessor { }
public class BoletoProcessor : IPaymentProcessor { }
```

### D - Dependency Inversion
```csharp
// Depender de abstrações
public class OrderService
{
    private readonly IOrderRepository _repo; // Abstração
    private readonly IEventBus _eventBus;    // Abstração
    
    public OrderService(IOrderRepository repo, IEventBus eventBus)
    {
        _repo = repo;
        _eventBus = eventBus;
    }
}
```

## Extensões Úteis

```csharp
public static class StringExtensions
{
    public static bool IsCnpj(this string cnpj)
    {
        cnpj = Regex.Replace(cnpj, @"[^\d]", "");
        return cnpj.Length == 14 && cnpj.All(char.IsDigit);
    }
    
    public static string ToCnpjFormat(this string cnpj)
    {
        cnpj = Regex.Replace(cnpj, @"[^\d]", "");
        return Convert.ToUInt64(cnpj)
            .ToString(@"00\.000\.000\/0000\-00");
    }
}
```

## Fontes Oficiais
- docs.microsoft.com/dotnet
- docs.microsoft.com/aspnet/core
- github.com/dotnet/efcore
- learn.microsoft.com/dotnet/csharp
