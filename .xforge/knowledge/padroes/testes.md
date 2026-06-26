---
id: testes
type: pattern
tags: [testes, xunit, nsubstitute, fluent-assertions, testcontainers, integration]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Testes — Padrões para ERP .NET
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: testes, xunit, nsubstitute, fluent-assertions, testcontainers, integration
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `testes` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Testes — Padrões para ERP .NET

## Propósito

Definir padrões de testes unitários e de integração para sistemas ERP, cobrindo xUnit, NSubstitute, FluentAssertions, Testcontainers, fixture pattern e test data builders.

## Descrição do Padrão

### Testes Unitários (xUnit + NSubstitute + FluentAssertions)

```csharp
public class PedidoServiceTests
{
    private readonly IProdutoRepositorio _produtoRepo;
    private readonly IEstoqueServico _estoqueSvc;
    private readonly PedidoService _service;

    public PedidoServiceTests()
    {
        _produtoRepo = Substitute.For<IProdutoRepositorio>();
        _estoqueSvc = Substitute.For<IEstoqueServico>();
        _service = new PedidoService(_produtoRepo, _estoqueSvc);
    }

    [Fact]
    public async Task CriarPedido_ComEstoqueSuficiente_DeveReservar()
    {
        _estoqueSvc.VerificarDisponibilidadeAsync(1, 2).Returns(true);

        var resultado = await _service.CriarPedidoAsync(1, 2);

        resultado.Should().NotBeNull();
        await _estoqueSvc.Received(1).ReservarAsync(1, 2);
    }

    [Theory]
    [InlineData(100, 10, 110)]
    [InlineData(200, 15, 230)]
    public void CalcularPrecoComImposto_DeveRetornarCorreto(
        @FromBase<ImpostoData> decimal base, decimal pct, decimal esperado)
    {
        var resultado = Produto.CalcularPrecoComImposto(base, pct);
        resultado.Should().Be(esperado);
    }
}
```

### Fixture Pattern (Compartilhamento de Contexto)

```csharp
[CollectionDefinition("DatabaseCollection")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("DatabaseCollection")]
public class ProdutoTests
{
    private readonly DatabaseFixture _fixture;
    public ProdutoTests(DatabaseFixture fixture) => _fixture = fixture;
}
```

### Test Data Builders (Bogus)

```csharp
public static class DadosTeste
{
    public static Faker<Produto> ProdutoFaker =>
        new Faker<Produto>("pt_BR")
            .CustomInstantiator(f => new Produto(f.Commerce.ProductName(), f.Random.Decimal(10, 5000)))
            .RuleFor(p => p.Codigo, f => f.Random.AlphaNumeric(10).ToUpper())
            .RuleFor(p => p.Ativo, f => f.Random.Bool(0.9f));
}
```

### Testes de Integração (Testcontainers)

```csharp
public class SqlServerFixture : IAsyncLifetime
{
    private readonly MsSqlContainer _container = new MsSqlBuilder()
        .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
        .Build();

    public string ConnectionString => _container.GetConnectionString();
    public async Task InitializeAsync() => await _container.StartAsync();
    public async Task DisposeAsync() => await _container.DisposeAsync();
}

public class RepositorioTests : IAsyncLifetime
{
    private readonly SqlServerFixture _fixture;
    private MeuDbContext _context;

    public RepositorioTests(SqlServerFixture fixture) => _fixture = fixture;

    public async Task InitializeAsync()
    {
        var options = new DbContextOptionsBuilder<MeuDbContext>()
            .UseSqlServer(_fixture.ConnectionString).Options;
        _context = new MeuDbContext(options);
        await _context.Database.EnsureCreatedAsync();
    }
}
```

### WebApplicationFactory (Testes de API)

```csharp
public class ApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Substituir DbContext por InMemory
                services.AddDbContext<MeuDbContext>(o => o.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }
}
```

### Metas de Cobertura

| Camada | Meta |
|--------|------|
| Domínio/Regras de negócio | 90%+ |
| Serviços de aplicação | 80%+ |
| Repositórios | 70%+ |
| Controllers | 60%+ |
| Total do projeto | 80%+ |

## Quando Usar

- **Unitários**: Regras de negócio, cálculos de impostos, validações.
- **Integração**: Repositórios com banco real (Testcontainers), fluxos completos de API.
- **TDD**: Ciclo Red → Green → Refactor para novas funcionalidades.

## Exemplo de Uso

```csharp
[Fact]
public void CalcularIcms_Base1000_Aliquota18_DeveRetornar180()
{
    var resultado = CalculadoraImpostos.CalcularIcms(1000m, 18m);
    resultado.Should().Be(180m);
}
```

## Padrões Relacionados

- [[ef-core-patterns]] — teste de repositórios com InMemory/SQLite
- [[validacao]] — teste de validators FluentValidation
- [[logging.md]] — verificação de logs em testes

