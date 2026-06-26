---
id: aspnet-core-minimal-apis
type: conhecimento
tags: [aspnetcore, minimal-apis, webapi, performance, di, middleware]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ASP.NET Core 10 — Minimal APIs
- **Seções principais**: Conceito, Estrutura Básica, Groups, Validação
- **Tags**: aspnetcore, minimal-apis, webapi, performance, di, middleware
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `aspnet-core-minimal-apis` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 11 |


# ASP.NET Core 10 — Minimal APIs

## Conceito

Minimal APIs são o padrão recomendado para APIs no ASP.NET Core, eliminando a necessidade de Controllers para a maioria dos cenários.

## Estrutura Básica

```csharp
var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Endpoints
app.MapGet("/products", async (IProductService svc) =>
    await svc.GetAllAsync())
    .WithName("GetProducts")
    .WithTags("Products")
    .Produces<List<ProductDto>>();

app.MapGet("/products/{id:int}", async (int id, IProductService svc) =>
{
    var product = await svc.GetByIdAsync(id);
    return product is not null ? Results.Ok(product) : Results.NotFound();
})
.WithName("GetProductById")
.WithTags("Products")
.Produces<ProductDto>()
.Produces(404);

app.MapPost("/products", async (CreateProductCommand cmd, IProductService svc) =>
{
    var result = await svc.CreateAsync(cmd);
    return Results.Created($"/products/{result.Id}", result);
})
.WithName("CreateProduct")
.WithTags("Products")
.Produces<ProductDto>(201)
.ProducesValidationProblem();

app.Run();
```

## Groups

```csharp
var products = app.MapGroup("/products")
    .WithTags("Products")
    .RequireAuthorization();

products.MapGet("/", async (IProductService svc) => await svc.GetAllAsync());
products.MapGet("/{id:int}", async (int id, IProductService svc) => ...);
products.MapPost("/", async (CreateProductCommand cmd, IProductService svc) => ...);
products.MapPut("/{id:int}", async (int id, UpdateProductCommand cmd, IProductService svc) => ...);
products.MapDelete("/{id:int}", async (int id, IProductService svc) => ...);
```

## Validação

```csharp
// Usando FluentValidation
public class CreateProductValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Price).GreaterThan(0);
        RuleFor(x => x.CategoryId).GreaterThan(0);
    }
}

// Endpoint com validação automática
app.MapPost("/products", async (CreateProductCommand cmd, IProductService svc) =>
{
    var result = await svc.CreateAsync(cmd);
    return Results.Created($"/products/{result.Id}", result);
})
.WithValidation<CreateProductCommand>();
```

## Middleware Customizado

```csharp
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _logger;

    public async Task InvokeAsync(HttpContext context)
    {
        var sw = Stopwatch.StartNew();
        await _next(context);
        sw.Stop();
        _logger.LogInformation("Request {Method} {Path} took {Elapsed}ms",
            context.Request.Method, context.Request.Path, sw.ElapsedMilliseconds);
    }
}

// Uso
app.UseMiddleware<RequestTimingMiddleware>();
```

## Dependency Injection

```csharp
// Builder pattern para services
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddTransient<IEmailService, SmtpEmailService>();

// Keyed services (.NET 8+)
builder.Services.AddKeyedScoped<ICacheService>("redis", (sp, _) => 
    new RedisCacheService(sp.GetRequiredService<IConnectionMultiplexer>()));
builder.Services.AddKeyedScoped<ICacheService>("memory", (sp, _) => 
    new MemoryCacheService());
```

## Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("fixed", opt =>
    {
        opt.PermitLimit = 100;
        opt.Window = TimeSpan.FromMinutes(1);
    });
    options.AddSlidingWindowLimiter("sliding", opt =>
    {
        opt.PermitLimit = 50;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.SegmentsPerWindow = 4;
    });
});

app.UseRateLimiter();
app.MapGet("/api/data", () => "ok").RequireRateLimiting("fixed");
```

## Output Caching

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromMinutes(5)));
    options.AddPolicy("Products", builder => 
        builder.Expire(TimeSpan.FromMinutes(10))
               .Tag("products"));
});

app.UseOutputCache();
app.MapGet("/products", async (IProductService svc) => await svc.GetAllAsync())
    .CacheOutput("Products");
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddNpgsql(connectionString, name: "postgresql")
    .AddRedis(redisConnection, name: "redis")
    .AddCheck<CustomHealthCheck>("custom");

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
```

## Minimal APIs vs Controllers

| Aspecto | Minimal APIs | Controllers |
|---------|-------------|-------------|
| Setup | Simples | Mais verboso |
| Performance | ~10% mais rápido | Padrão |
| Organização | Groups | Pastas/áreas |
| Testabilidade | Igual | Igual |
| Documentação | Swagger nativo | Swagger nativo |
| Filtros | Endpoint filters | Action filters |

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/fundamentals/minimal-apis
- docs.microsoft.com/aspnet/core/fundamentals/minimal-apis/openapi
