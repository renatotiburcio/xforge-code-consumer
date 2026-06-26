---
id: unit-testing-completo
type: conhecimento
tags: [testes, xunit, nunit, moq, nsubstitute, fluentassertions, testcontainers, bdd, tdd]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Testes Unitários - Guia Completo
- **Seções principais**: Frameworks, xUnit + NSubstitute + FluentAssertions, TDD, Cobertura
- **Tags**: testes, xunit, nunit, moq, nsubstitute, fluentassertions, testcontainers, bdd, tdd
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `unit-testing-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 5 |


# Testes Unitários - Guia Completo

## Frameworks

| Framework | assertions | Mocking | Uso |
|-----------|-----------|---------|-----|
| xUnit | Built-in | Moq/NSubstitute | Mais popular |
| NUnit | Fluent | NSubstitute | Clássico |
| MSTest | Built-in | Moq | Microsoft |

## xUnit + NSubstitute + FluentAssertions

### Setup
```xml
<PackageReference Include="xunit" Version="2.9.0" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.9.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.10.0" />
<PackageReference Include="NSubstitute" Version="5.2.0" />
<PackageReference Include="FluentAssertions" Version="6.12.0" />
<PackageReference Include="AutoFixture" Version="4.18.1" />
```

### Teste Básico
```csharp
public class ProductTests
{
    [Fact]
    public void Product_Should_Have_Correct_Properties()
    {
        // Arrange
        var product = new Product
        {
            Id = 1,
            Name = "Test Product",
            Price = 99.99m
        };
        
        // Act & Assert
        product.Id.Should().Be(1);
        product.Name.Should().Be("Test Product");
        product.Price.Should().Be(99.99m);
    }
    
    [Fact]
    public void Product_Price_Should_Be_Positive()
    {
        var product = new Product { Price = -10 };
        
        product.Price.Should().BeGreaterThan(0);
    }
    
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public void Product_Invalid_Price_Should_Throw(decimal price)
    {
        Action act = () => new Product { Price = price };
        
        act.Should().Throw<ArgumentException>()
            .WithMessage("*positive*");
    }
}
```

### Mocking com NSubstitute

```csharp
public class ProductServiceTests
{
    private readonly IProductRepository _repoMock;
    private readonly ILogger<ProductService> _loggerMock;
    private readonly ProductService _sut;
    
    public ProductServiceTests()
    {
        _repoMock = Substitute.For<IProductRepository>();
        _loggerMock = Substitute.For<ILogger<ProductService>>();
        _sut = new ProductService(_repoMock, _loggerMock);
    }
    
    [Fact]
    public async Task GetById_ExistingProduct_ReturnsProduct()
    {
        // Arrange
        var product = new Product { Id = 1, Name = "Test" };
        _repoMock.GetByIdAsync(1).Returns(product);
        
        // Act
        var result = await _sut.GetByIdAsync(1);
        
        // Assert
        result.Should().NotBeNull();
        result!.Name.Should().Be("Test");
        await _repoMock.Received(1).GetByIdAsync(1);
    }
    
    [Fact]
    public async Task GetById_NonExistingProduct_ReturnsNull()
    {
        _repoMock.GetByIdAsync(999).Returns((Product?)null);
        
        var result = await _sut.GetByIdAsync(999);
        
        result.Should().BeNull();
    }
    
    [Fact]
    public async Task Create_ValidProduct_AddsToRepository()
    {
        var command = new CreateProductCommand("Test", 100m, 1, null);
        
        await _sut.CreateAsync(command);
        
        await _repoMock.Received(1).AddAsync(Arg.Is<Product>(p => 
            p.Name == "Test" && p.Price == 100m));
    }
}
```

### FluentAssertions

```csharp
// Valores
result.Should().Be(expected);
result.Should().BeGreaterThan(0);
result.Should().BeInRange(1, 100);
result.Should().BeOneOf(1, 2, 3);

// Strings
name.Should().NotBeNullOrEmpty();
name.Should().StartWith("Test");
name.Should().Contain("product");
name.Should().MatchRegex(@"^[A-Z]");

// Coleções
list.Should().NotBeEmpty();
list.Should().HaveCount(3);
list.Should().Contain(x => x.Name == "Test");
list.Should().ContainItems(x => x.Price > 0);
list.Should().BeInAscendingOrder(x => x.Name);

// Objetos
result.Should().NotBeNull();
result.Should().BeOfType<Product>();
result.Should().BeEquivalentTo(expected);

// Exceções
Action act = () => service.Delete(999);
act.Should().Throw<NotFoundException>();
act.Should().Throw<NotFoundException>()
    .WithMessage("*999*");

// DateTime
date.Should().BeAfter(DateTime.MinValue);
date.Should().BeBefore(DateTime.UtcNow);
date.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
```

### Test Data Builders

```csharp
public class ProductBuilder
{
    private int _id = 1;
    private string _name = "Test Product";
    private decimal _price = 100m;
    private int _categoryId = 1;
    
    public ProductBuilder WithId(int id) { _id = id; return this; }
    public ProductBuilder WithName(string name) { _name = name; return this; }
    public ProductBuilder WithPrice(decimal price) { _price = price; return this; }
    public ProductBuilder WithCategory(int categoryId) { _categoryId = categoryId; return this; }
    
    public Product Build() => new()
    {
        Id = _id,
        Name = _name,
        Price = _price,
        CategoryId = _categoryId
    };
}

// Uso
var product = new ProductBuilder()
    .WithName("Premium Product")
    .WithPrice(299.99m)
    .Build();
```

### AutoFixture

```csharp
public class ProductServiceTests
{
    private readonly Fixture _fixture = new();
    
    [Fact]
    public async Task Create_ValidProduct_ReturnsDto()
    {
        // AutoFixture gera dados aleatórios
        var command = _fixture.Create<CreateProductCommand>();
        
        var result = await _sut.CreateAsync(command);
        
        result.Should().NotBeNull();
        result.Name.Should().Be(command.Name);
    }
}
```

### Integration Tests com TestContainers

```csharp
public class ProductRepositoryTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _dbContainer;
    private AppDbContext _context = null!;
    private ProductRepository _repository = null!;
    
    public ProductRepositoryTests()
    {
        _dbContainer = new PostgreSqlBuilder()
            .WithImage("postgres:16")
            .WithDatabase("testdb")
            .WithUsername("test")
            .WithPassword("test")
            .Build();
    }
    
    public async Task InitializeAsync()
    {
        await _dbContainer.StartAsync();
        
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(_dbContainer.GetConnectionString())
            .Options;
        
        _context = new AppDbContext(options);
        await _context.Database.EnsureCreatedAsync();
        
        _repository = new ProductRepository(_context);
    }
    
    public async Task DisposeAsync()
    {
        await _dbContainer.DisposeAsync();
    }
    
    [Fact]
    public async Task Add_Should_Persist_Product()
    {
        var product = new Product { Name = "Test", Price = 100m };
        
        await _repository.AddAsync(product);
        await _context.SaveChangesAsync();
        
        var saved = await _context.Products.FindAsync(product.Id);
        saved.Should().NotBeNull();
        saved!.Name.Should().Be("Test");
    }
}
```

### BDD com FluentAssertions

```csharp
public class OrderFeature
{
    [Fact]
    public void Customer_Should_Be_Able_To_Place_Order()
    {
        // Given
        var customer = new CustomerBuilder().Build();
        var product = new ProductBuilder().WithStock(10).Build();
        var order = new OrderBuilder().WithCustomer(customer).Build();
        
        // When
        order.AddItem(product, 2);
        
        // Then
        order.Items.Should().HaveCount(1);
        order.Total.Should().Be(product.Price * 2);
        product.Stock.Should().Be(8);
    }
}
```

### Async Testing

```csharp
[Fact]
public async Task Should_Create_Product_Async()
{
    var result = await _sut.CreateAsync(command);
    
    result.Should().NotBeNull();
}

[Fact]
public async Task Should_Throw_When_Product_Not_Found()
{
    Func<Task> act = async () => await _sut.GetByIdAsync(999);
    
    await act.Should().ThrowAsync<NotFoundException>();
}
```

### Moq (Alternativa)

```csharp
var repoMock = new Mock<IProductRepository>();
repoMock.Setup(x => x.GetByIdAsync(1))
    .ReturnsAsync(new Product { Id = 1, Name = "Test" });

var sut = new ProductService(repoMock.Object);
var result = await sut.GetByIdAsync(1);

repoMock.Verify(x => x.GetByIdAsync(1), Times.Once);
```

## TDD

### Ciclo
```
1. Red: Escrever teste que falha
2. Green: Escrever código mínimo para passar
3. Refactor: Melhorar código mantendo testes verdes
```

### Exemplo
```csharp
// 1. RED - Teste falha
[Fact]
public void CalculateDiscount_Should_Return_10_Percent()
{
    var calc = new DiscountCalculator();
    var result = calc.Calculate(100m, 0.1m);
    result.Should().Be(10m);
}

// 2. GREEN - Código mínimo
public class DiscountCalculator
{
    public decimal Calculate(decimal price, decimal discountPercent)
    {
        return price * discountPercent;
    }
}

// 3. REFACTOR - Melhorar
public class DiscountCalculator
{
    public decimal Calculate(decimal price, decimal discountPercent)
    {
        if (price < 0) throw new ArgumentException("Price cannot be negative");
        if (discountPercent < 0 || discountPercent > 1) 
            throw new ArgumentException("Discount must be between 0 and 1");
        
        return Math.Round(price * discountPercent, 2);
    }
}
```

## Cobertura

```xml
<!-- cobertura do pacote -->
<PackageReference Include="coverlet.collector" Version="6.0.0" />
```

```bash
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura
dotnet reportgenerator -reports:coverage.cobertura.xml -targetdir:coverage
```

## Fontes Oficiais
- docs.microsoft.com/dotnet/core/testing
- xunit.net
- nsubstitute.net
- fluentassertions.com
