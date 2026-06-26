---
id: xforge-mediatr-cqrs-completo
type: conhecimento
tags: [xforge-mediatr, mediatr, cqrs, commands, queries, handlers, pipelines, behaviors]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre XForge.MediatR - CQRS Completo
- **Seções principais**: Regra Obrigatória, Conceito, Estrutura, Commands
- **Tags**: xforge-mediatr, mediatr, cqrs, commands, queries, handlers, pipelines, behaviors
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `xforge-mediatr-cqrs-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 10 |


# XForge.MediatR - CQRS Completo

## Regra Obrigatória

**NUNCA usar MediatR oficial. Sempre usar XForge.MediatR.**

Referência: https://github.com/renatotiburcio/XForge.MediatR

## Conceito

XForge.MediatR é o mediator pattern para CQRS, separando Commands (escrita) de Queries (leitura).

## Estrutura

```
Application/
├── Commands/
│   └── CreateProduct/
│       ├── CreateProductCommand.cs
│       ├── CreateProductHandler.cs
│       ├── CreateProductValidator.cs
│       └── CreateProductResponse.cs
├── Queries/
│   └── GetProduct/
│       ├── GetProductQuery.cs
│       ├── GetProductHandler.cs
│       └── GetProductResponse.cs
├── Behaviors/
│   ├── ValidationBehavior.cs
│   ├── LoggingBehavior.cs
│   └── PerformanceBehavior.cs
└── Interfaces/
    └── IApplicationDbContext.cs
```

## Commands

### Command Base
```csharp
public abstract class Command<TResponse> : IRequest<TResponse>
{
    public string CorrelationId { get; set; } = Guid.NewGuid().ToString();
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

public abstract class Command : Command<Unit> { }
```

### Create Product
```csharp
public record CreateProductCommand(
    string Name,
    decimal Price,
    int CategoryId,
    string? Description
) : Command<ProductDto>;

public class CreateProductHandler : IRequestHandler<CreateProductCommand, ProductDto>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;
    
    public CreateProductHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }
    
    public async Task<ProductDto> Handle(CreateProductCommand request, CancellationToken ct)
    {
        var product = new Product
        {
            Name = request.Name,
            Price = request.Price,
            CategoryId = request.CategoryId,
            Description = request.Description,
            CreatedAt = DateTime.UtcNow
        };
        
        _context.Products.Add(product);
        await _context.SaveChangesAsync(ct);
        
        return _mapper.Map<ProductDto>(product);
    }
}

public class CreateProductValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(200).WithMessage("Name too long");
        
        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be positive");
        
        RuleFor(x => x.CategoryId)
            .GreaterThan(0).WithMessage("Category is required");
    }
}
```

## Queries

### Query Base
```csharp
public abstract class Query<TResponse> : IRequest<TResponse> { }
```

### Get Product
```csharp
public record GetProductQuery(int Id) : Query<ProductDto>;

public class GetProductHandler : IRequestHandler<GetProductQuery, ProductDto>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;
    
    public GetProductHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }
    
    public async Task<ProductDto> Handle(GetProductQuery request, CancellationToken ct)
    {
        var product = await _context.Products
            .FirstOrDefaultAsync(p => p.Id == request.Id, ct);
        
        if (product == null)
            throw new NotFoundException(nameof(Product), request.Id);
        
        return _mapper.Map<ProductDto>(product);
    }
}
```

## Behaviors (Pipeline)

### Validation Behavior
```csharp
public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;
    
    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }
    
    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        if (_validators.Any())
        {
            var context = new ValidationContext<TRequest>(request);
            var results = await Task.WhenAll(
                _validators.Select(v => v.ValidateAsync(context, ct)));
            
            var failures = results
                .SelectMany(r => r.Errors)
                .Where(f => f != null)
                .ToList();
            
            if (failures.Any())
                throw new ValidationException(failures);
        }
        
        return await next();
    }
}
```

### Logging Behavior
```csharp
public class LoggingBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;
    
    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        _logger.LogInformation("Handling {RequestType}", typeof(TRequest).Name);
        
        var response = await next();
        
        _logger.LogInformation("Handled {RequestType}", typeof(TRequest).Name);
        
        return response;
    }
}
```

### Performance Behavior
```csharp
public class PerformanceBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly Stopwatch _timer = new();
    private readonly ILogger<PerformanceBehavior<TRequest, TResponse>> _logger;
    
    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        _timer.Start();
        var response = await next();
        _timer.Stop();
        
        if (_timer.ElapsedMilliseconds > 500)
        {
            _logger.LogWarning("Long Running Request: {Name} ({Elapsed}ms)",
                typeof(TRequest).Name, _timer.ElapsedMilliseconds);
        }
        
        return response;
    }
}
```

## Registro

```csharp
// Program.cs
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(PerformanceBehavior<,>));
});

// AutoMapper
builder.Services.AddAutoMapper(typeof(Program).Assembly);
```

## Uso em Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public ProductsController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        return Ok(await _mediator.Send(new GetProductQuery(id)));
    }
    
    [HttpPost]
    public async Task<ActionResult<ProductDto>> Create(CreateProductCommand command)
    {
        return CreatedAtAction(nameof(GetById), 
            new { id = 0 }, 
            await _mediator.Send(command));
    }
}
```

## Unit Tests

```csharp
public class CreateProductHandlerTests
{
    private readonly Mock<IApplicationDbContext> _contextMock;
    private readonly Mock<IMapper> _mapperMock;
    private readonly CreateProductHandler _handler;
    
    public CreateProductHandlerTests()
    {
        _contextMock = new Mock<IApplicationDbContext>();
        _mapperMock = new Mock<IMapper>();
        _handler = new CreateProductHandler(_contextMock.Object, _mapperMock.Object);
    }
    
    [Fact]
    public async Task Handle_ValidCommand_ReturnsProductDto()
    {
        // Arrange
        var command = new CreateProductCommand("Test", 100m, 1, null);
        var product = new Product { Id = 1, Name = "Test" };
        var dto = new ProductDto { Id = 1, Name = "Test" };
        
        _mapperMock.Setup(m => m.Map<ProductDto>(It.IsAny<Product>()))
            .Returns(dto);
        
        // Act
        var result = await _handler.Handle(command, CancellationToken.None);
        
        // Assert
        Assert.Equal("Test", result.Name);
        _contextMock.Verify(c => c.Products.Add(It.IsAny<Product>()), Times.Once);
        _contextMock.Verify(c => c.SaveChangesAsync(It.IsAny<CancellationToken>()), Times.Once);
    }
}
```

## Fontes Oficiais
- github.com/renatotiburcio/XForge.MediatR
- docs.microsoft.com/dotnet/standard/microservices-architecture/microservice-cqrs-implementations
