---
id: swagger-openapi-net10-completo
type: conhecimento
tags: [swagger, openapi, nswag, api-docs, net10, minimal-apis]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Swagger/OpenAPI para .NET 10
- **Seções principais**: Conceito, Setup, Anotações, Minimal APIs
- **Tags**: swagger, openapi, nswag, api-docs, net10, minimal-apis
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `swagger-openapi-net10-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 11 |


# Swagger/OpenAPI para .NET 10

## Conceito

Swagger/OpenAPI documenta automaticamente APIs REST, gerando UI interativa e specs para clientes.

## Setup

```csharp
// Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "XForge API",
        Version = "v1",
        Description = "API do XForge Enterprise Development OS",
        Contact = new OpenApiContact
        {
            Name = "XForge Team",
            Email = "support@xforge.com"
        }
    });
    
    // JWT Bearer
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Enter your JWT token"
    });
    
    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
    
    // XML Comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);
});

// Swagger UI
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "XForge API v1");
    options.RoutePrefix = "swagger";
    options.DefaultModelsExpandDepth(-1); // Esconder modelos por padrão
});
```

## Anotações

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
[Tags("Products")]
public class ProductsController : ControllerBase
{
    /// <summary>
    /// Lista todos os produtos
    /// </summary>
    /// <param name="categoryId">ID da categoria</param>
    /// <param name="page">Página atual</param>
    /// <param name="pageSize">Tamanho da página</param>
    /// <returns>Lista de produtos</returns>
    /// <response code="200">Sucesso</response>
    /// <response code="400">Parâmetros inválidos</response>
    [HttpGet]
    [ProducesResponseType(typeof(List<ProductDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ErrorResponse), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<List<ProductDto>>> GetAll(
        [FromQuery] int? categoryId,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        return Ok(await _service.GetAllAsync(categoryId, page, pageSize));
    }
    
    /// <summary>
    /// Cria um novo produto
    /// </summary>
    /// <param name="command">Dados do produto</param>
    /// <returns>Produto criado</returns>
    [HttpPost]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ErrorResponse), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductDto>> Create(CreateProductCommand command)
    {
        var product = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
}
```

## Minimal APIs

```csharp
app.MapGet("/products", async (IProductService svc) =>
    await svc.GetAllAsync())
    .WithName("GetProducts")
    .WithTags("Products")
    .Produces<List<ProductDto>>()
    .WithOpenApi();

app.MapPost("/products", async (CreateProductCommand cmd, IProductService svc) =>
{
    var result = await svc.CreateAsync(cmd);
    return Results.Created($"/products/{result.Id}", result);
})
.WithName("CreateProduct")
.WithTags("Products")
.Produces<ProductDto>(StatusCodes.Status201Created)
.ProducesValidationProblem()
.WithOpenApi();
```

## Filtros

```csharp
// Filtro de operação
public class AddRequiredHeaderParameter : IOperationFilter
{
    public void Apply(OpenApiOperation operation, OperationFilterContext context)
    {
        operation.Parameters ??= new List<OpenApiParameter>();
        
        operation.Parameters.Add(new OpenApiParameter
        {
            Name = "X-Request-Id",
            In = ParameterLocation.Header,
            Required = false,
            Schema = new OpenApiSchema { Type = "string" }
        });
    }
}

// Registro
builder.Services.AddSwaggerGen(options =>
{
    options.OperationFilter<AddRequiredHeaderParameter>();
});
```

## Schema Filters

```csharp
// Esconder propriedades internas
public class HideInternalPropertiesFilter : ISchemaFilter
{
    public void Apply(OpenApiSchema schema, SchemaFilterContext context)
    {
        var properties = schema.Properties.Where(p => 
            p.Key.StartsWith("_") || p.Key == "Id").ToList();
        
        foreach (var prop in properties)
        {
            schema.Properties.Remove(prop.Key);
        }
    }
}
```

## NSwag (Alternativa)

```csharp
// Program.cs
builder.Services.AddOpenApiDocument(config =>
{
    config.Title = "XForge API";
    config.Version = "v1";
    config.AddSecurity("Bearer", new OpenApiSecurityScheme
    {
        Type = OpenApiSecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
});

app.UseOpenApi();
app.UseSwaggerUi3();
```

## Geração de Client

```bash
# CLI
nswag openapi2csclient /input:swagger.json /output:ApiClient.cs /namespace:MyApp.Client

# npm
npx openapi-typescript swagger.json -o types.ts
```

## Versionamento

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
});

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "API", Version = "v1" });
    options.SwaggerDoc("v2", new OpenApiInfo { Title = "API", Version = "v2" });
});
```

## ProducesResponseType

```csharp
[HttpPost]
[ProducesResponseType(typeof(ProductDto), 201)]
[ProducesResponseType(typeof(ValidationProblemDetails), 400)]
[ProducesResponseType(401)]
[ProducesResponseType(403)]
[ProducesResponseType(500)]
public async Task<ActionResult<ProductDto>> Create(CreateProductCommand command)
{
    // ...
}
```

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/tutorials/web-api-help-pages
- docs.microsoft.com/aspnet/core/tutorials/web-api-using-openapi
- github.com/domaindrivendev/Swashbuckle.AspNetCore
