---
name: oops-design-patterns-expert
description: Expert em design patterns GoF, enterprise patterns, SOLID, clean code e refactoring.
metadata:
  version: "1.0.0"
  xforge-category: "technical-expert"
---

# oops-design-patterns-expert

## Objetivo

Aplicar design patterns corretos em cada cenário de design.

## Creational Patterns

| Pattern | Quando Usar | Exemplo .NET |
|---------|-------------|--------------|
| **Singleton** | Uma instância global | DbContext, Logger |
| **Factory** | Criar objetos sem expor lógica | MediatR handlers |
| **Abstract Factory** | Famílias de objetos | Provider patterns |
| **Builder** | Objetos complexos passo-a-passo | Query builders |
| **Prototype** | Copiar objetos existentes | Config cloning |

## Structural Patterns

| Pattern | Quando Usar | Exemplo .NET |
|---------|-------------|--------------|
| **Adapter** | Interface incompatível | Repository pattern |
| **Decorator** | Adicionar comportamento | Middleware pipeline |
| **Facade** | Simplificar subsistemas | Service facades |
| **Proxy** | Controle de acesso | Lazy loading, caching |
| **Composite** | Estrutura em árvore | Menu hierárquico |

## Behavioral Patterns

| Pattern | Quando Usar | Exemplo .NET |
|---------|-------------|--------------|
| **Strategy** | Algoritmos intercambiáveis | Payment processors |
| **Observer** | Notificar mudanças | Event handlers |
| **Chain of Responsibility** | Pipeline de processamento | Middleware ASP.NET |
| **Command** | Encapsular ações | CQRS commands |
| **Template Method** | Esqueleto de algoritmo | Base services |

## SOLID

```
S - Single Responsibility: 1 classe = 1 responsabilidade
O - Open/Closed: aberto para extensão, fechado para modificação
L - Liskov Substitution: subclasses substituem superclasses
I - Interface Segregation: interfaces pequenas e específicas
D - Dependency Inversion: depender de abstrações, não implementações
```

## Exemplos em .NET

### Strategy Pattern
```csharp
public interface IPaymentStrategy
{
    Task<Result> ProcessAsync(PaymentRequest request);
}

public class CreditCardPayment : IPaymentStrategy { ... }
public class PixPayment : IPaymentStrategy { ... }

// Uso
var strategy = _strategies[request.Type];
var result = await strategy.ProcessAsync(request);
```

### Repository Pattern
```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}
```

### Decorator Pattern
```csharp
public class CachedProductService : IProductService
{
    private readonly IProductService _inner;
    private readonly IDistributedCache _cache;

    public async Task<Product?> GetByIdAsync(int id)
    {
        var cached = await _cache.GetAsync<Product>($"product:{id}");
        if (cached != null) return cached;
        
        var product = await _inner.GetByIdAsync(id);
        await _cache.SetAsync($"product:{id}", product);
        return product;
    }
}
```

## Procedimento

1. Identificar o problema de design
2. Verificar qual pattern se aplica
3. Implementar com interfaces
4. Configurar DI
5. Criar testes
6. Documentar decisão (ADR)
