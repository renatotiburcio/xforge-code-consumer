---
id: automapper-completo
type: conhecimento
tags: [automapper, mapping, profiles, dto, entity, project, reverse]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre AutoMapper - Mapeamento Completo
- **Seções principais**: Regra Obrigatória, Conceito, Setup, Profile
- **Tags**: automapper, mapping, profiles, dto, entity, project, reverse
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `automapper-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 16 |


# AutoMapper - Mapeamento Completo

## Regra Obrigatória

**NUNCA usar Mapster. Sempre usar AutoMapper.**

## Conceito

AutoMapper mapeia objetos de um tipo para outro, eliminando código repetitivo de conversão.

## Setup

```csharp
// Program.cs
builder.Services.AddAutoMapper(typeof(Program).Assembly);
// ou
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());
```

## Profile

```csharp
public class MappingProfile : Profile
{
    public MappingProfile()
    {
        // Entity → DTO
        CreateMap<Product, ProductDto>()
            .ForMember(dest => dest.CategoryName, 
                opt => opt.MapFrom(src => src.Category.Name))
            .ForMember(dest => dest.CreatedAt, 
                opt => opt.MapFrom(src => src.CreatedAt.ToString("dd/MM/yyyy")));

        // DTO → Entity
        CreateMap<CreateProductCommand, Product>()
            .ForMember(dest => dest.Id, opt => opt.Ignore())
            .ForMember(dest => dest.CreatedAt, opt => opt.MapFrom(_ => DateTime.UtcNow));

        // Update
        CreateMap<UpdateProductCommand, Product>()
            .ForMember(dest => dest.Id, opt => opt.Ignore())
            .ForMember(dest => dest.CreatedAt, opt => opt.Ignore());

        // Reverse
        CreateMap<ProductDto, Product>().ReverseMap();
    }
}
```

## Mapeamentos

### Básico
```csharp
// Entity → DTO
var dto = _mapper.Map<ProductDto>(product);

// DTO → Entity
var product = _mapper.Map<Product>(dto);

// Lista
var dtos = _mapper.Map<List<ProductDto>>(products);
```

### Com Configuração
```csharp
var dto = _mapper.Map<ProductDto>(product, opt =>
{
    opt.BeforeMap((src, dest) =>
    {
        // Antes do mapeamento
    });
    opt.AfterMap((src, dest) =>
    {
        // Depois do mapeamento
    });
});
```

### Mapeamento Condicional
```csharp
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.ImageUrl, 
        opt => opt.Condition(src => !string.IsNullOrEmpty(src.ImageUrl)))
    .ForMember(dest => dest.Discount, 
        opt => opt.Condition(src => src.HasDiscount));
```

### Ignorar Propriedades
```csharp
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.InternalCode, opt => opt.Ignore())
    .ForMember(dest => dest.CreatedBy, opt => opt.Ignore());
```

### Valores Customizados
```csharp
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.Status, 
        opt => opt.MapFrom(src => src.IsActive ? "Active" : "Inactive"))
    .ForMember(dest => dest.FullDescription, 
        opt => opt.MapFrom(src => $"{src.Name} - {src.Description}"));
```

## ProjectTo (IQueryable)

```csharp
// EF Core otimizado - gera SQL otimizado
var dtos = await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ProjectTo<ProductDto>(_mapper.ConfigurationProvider)
    .ToListAsync();

// Vs
var products = await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync();
var dtos = _mapper.Map<List<ProductDto>>(products); // Mapeia tudo em memória
```

## Null Handling

```csharp
// Mapear null para null
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.ImageUrl, 
        opt => opt.Condition(src => src.ImageUrl != null));

// Valor padrão para null
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.Description, 
        opt => opt.MapFrom(src => src.Description ?? "Sem descrição"));
```

## Coleções

```csharp
// Lista
CreateMap<List<Product>, List<ProductDto>>();

// Array
CreateMap<Product[], ProductDto[]>();

// Dictionary
CreateMap<Dictionary<int, Product>, Dictionary<int, ProductDto>>();
```

## Custom Value Resolver

```csharp
public class ProductImageUrlResolver : IValueResolver<Product, ProductDto, string>
{
    private readonly IConfiguration _config;
    
    public ProductImageUrlResolver(IConfiguration config)
    {
        _config = config;
    }
    
    public string Resolve(Product source, ProductDto dest, string destMember, ResolutionContext context)
    {
        if (string.IsNullOrEmpty(source.ImageUrl))
            return $"{_config["ImageDefaults:NoImage"]}";
        
        return $"{_config["ImageBaseUrl"]}/{source.ImageUrl}";
    }
}

// Uso
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.ImageUrl, 
        opt => opt.MapFrom<ProductImageUrlResolver>());
```

## BeforeMap / AfterMap

```csharp
CreateMap<Product, ProductDto>()
    .BeforeMap((src, dest) =>
    {
        // Antes do mapeamento
        dest.CreatedAt = src.CreatedAt.ToString("dd/MM/yyyy HH:mm");
    })
    .AfterMap((src, dest) =>
    {
        // Depois do mapeamento
        dest.FullName = $"{dest.Name} ({dest.Id})";
    });
```

## ForPath (Propriedades Aninhadas)

```csharp
CreateMap<Order, OrderDto>()
    .ForPath(dest => dest.Customer.Name, 
        opt => opt.MapFrom(src => src.Customer.FullName))
    .ForPath(dest => dest.Customer.Email, 
        opt => opt.MapFrom(src => src.Customer.EmailAddress));
```

## ReverseMap

```csharp
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.CategoryName, 
        opt => opt.MapFrom(src => src.Category.Name))
    .ReverseMap()
    .ForMember(dest => dest.Category, opt => opt.Ignore());
```

## Unit Tests

```csharp
public class MappingProfileTests
{
    private readonly IMapper _mapper;
    
    public MappingProfileTests()
    {
        var config = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<MappingProfile>();
        });
        _mapper = config.CreateMapper();
    }
    
    [Fact]
    public void Should_Map_Product_To_ProductDto()
    {
        var product = new Product { Id = 1, Name = "Test", Price = 100m };
        var dto = _mapper.Map<ProductDto>(product);
        
        Assert.Equal(1, dto.Id);
        Assert.Equal("Test", dto.Name);
        Assert.Equal(100m, dto.Price);
    }
    
    [Fact]
    public void Should_Map_ProductDto_To_Product()
    {
        var dto = new ProductDto { Name = "Test", Price = 100m };
        var product = _mapper.Map<Product>(dto);
        
        Assert.Equal("Test", product.Name);
        Assert.Equal(100m, product.Price);
    }
    
    [Fact]
    public void Configuration_Should_Be_Valid()
    {
        var config = new MapperConfiguration(cfg =>
        {
            cfg.AddProfile<MappingProfile>();
        });
        
        config.AssertConfigurationIsValid(); // Verifica se todos os mapeamentos estão OK
    }
}
```

## Configuração Global

```csharp
// Program.cs
builder.Services.AddAutoMapper(config =>
{
    config.AllowNullDestinationValues = true;
    config.AllowNullCollections = true;
    config.CreateMissingTypeMaps = false;
}, typeof(Program).Assembly);
```

## Performance

```csharp
// Usar ProjectTo para queries EF Core
var dtos = await _context.Products
    .ProjectTo<ProductDto>(_mapper.ConfigurationProvider)
    .ToListAsync();

// Compilar mapeamentos em produção
var config = new MapperConfiguration(cfg =>
{
    cfg.AddProfile<MappingProfile>();
});

// Em produção, usar config.CreateMapper()
// Em dev, usar config.AssertConfigurationIsValid()
```

## Fontes Oficiais
- docs.automapper.org
- github.com/AutoMapper/AutoMapper
