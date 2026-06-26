---
id: bdd-completo
type: conhecimento
tags: [bdd, specflow, cucumber, gherkin, scenarios, acceptance, behave]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre BDD (Behavior-Driven Development) - Guia Completo
- **Seções principais**: Conceito, Ciclo BDD, Gherkin, SpecFlow (.NET)
- **Tags**: bdd, specflow, cucumber, gherkin, scenarios, acceptance, behave
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `bdd-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 9 |


# BDD (Behavior-Driven Development) - Guia Completo

## Conceito

BDD é uma abordagem de desenvolvimento que usa linguagem natural (Gherkin) para descrever comportamento do sistema, alinhando desenvolvimento, teste e negócio.

## Ciclo BDD

```
1. Discovery: Business + Dev + QA discutem cenários
2. Formulation: Cenários escritos em Gherkin
3. Automation: Step definitions implementadas
4. Development: Código para passar nos cenários
5. Review: Cenários como documentação viva
```

## Gherkin

### Sintaxe

```gherkin
Feature: Gestão de Produtos
  
  Como usuário do sistema
  Quero gerenciar produtos
  Para manter o catálogo atualizado

  Scenario: Criar produto válido
    Given eu estou na página de produtos
    When eu preencho o nome "Produto Teste"
    And eu preencho o preço "99.99"
    And eu clico em "Salvar"
    Then o produto deve ser criado
    And eu devo ver a mensagem "Produto criado com sucesso"

  Scenario: Tentar criar produto sem nome
    Given eu estou na página de produtos
    When eu deixo o nome vazio
    And eu preencho o preço "99.99"
    And eu clico em "Salvar"
    Then eu devo ver o erro "Nome é obrigatório"

  Scenario Outline: Validação de preços
    Given eu estou na página de produtos
    When eu preencho o preço "<preço>"
    And eu clico em "Salvar"
    Then eu devo ver "<resultado>"

    Examples:
      | preço   | resultado                    |
      | 99.99   | Produto criado com sucesso   |
      | -10     | Preço deve ser positivo      |
      | 0       | Preço deve ser positivo      |
      | 1000001 | Preço muito alto             |
```

### Palavras-Chave

| Palavra | Uso |
|---------|-----|
| **Feature** | Funcionalidade sendo testada |
| **Scenario** | Caso de teste |
| **Given** | Estado inicial (arrange) |
| **When** | Ação executada (act) |
| **Then** | Resultado esperado (assert) |
| **And** | Passo adicional |
| **But** | Resultado negativo |
| **Background** | Passos comuns a todos os cenários |
| **Scenario Outline** | Cenário parametrizado |
| **Examples** | Dados para Scenario Outline |

## SpecFlow (.NET)

### Setup

```xml
<PackageReference Include="SpecFlow" Version="3.9.0" />
<PackageReference Include="SpecFlow.NUnit" Version="3.9.0" />
<PackageReference Include="SpecFlow.Tools.MsBuild.Generation" Version="3.9.0" />
```

### Feature File

```gherkin
# Features/ProductManagement.feature
Feature: Product Management
  
  Background:
    Given the following products exist:
      | Name         | Price  | Category |
      | Laptop       | 2500   | Eletrônicos |
      | Mouse        | 50     | Eletrônicos |
      | Desk         | 500    | Móveis     |

  Scenario: List all products
    Given I am on the products page
    When I view the product list
    Then I should see 3 products
    And the first product should be "Laptop"

  Scenario: Search products by name
    Given I am on the products page
    When I search for "Mouse"
    Then I should see 1 product
    And the product should be "Mouse"

  Scenario: Create a new product
    Given I am on the new product page
    When I fill in:
      | Field    | Value        |
      | Name     | Keyboard     |
      | Price    | 150          |
      | Category | Eletrônicos  |
    And I submit the form
    Then I should see "Product created successfully"
    And the product list should have 4 products
```

### Step Definitions

```csharp
[Binding]
public class ProductSteps
{
    private readonly ScenarioContext _scenarioContext;
    private readonly IProductService _productService;
    
    public ProductSteps(ScenarioContext scenarioContext, IProductService productService)
    {
        _scenarioContext = scenarioContext;
        _productService = productService;
    }
    
    [Given(@"the following products exist:")]
    public void GivenTheFollowingProductsExist(Table table)
    {
        foreach (var row in table.Rows)
        {
            var product = new Product
            {
                Name = row["Name"],
                Price = decimal.Parse(row["Price"]),
                Category = row["Category"]
            };
            _productService.CreateAsync(product).Wait();
        }
    }
    
    [Given(@"I am on the products page")]
    public void GivenIAmOnTheProductsPage()
    {
        _scenarioContext["CurrentPage"] = "Products";
    }
    
    [When(@"I view the product list")]
    public void WhenIViewTheProductList()
    {
        var products = _productService.GetAllAsync().Result;
        _scenarioContext["Products"] = products;
    }
    
    [Then(@"I should see (\d+) products")]
    public void ThenIShouldSeeProducts(int expectedCount)
    {
        var products = _scenarioContext["Products"] as List<Product>;
        products.Should().HaveCount(expectedCount);
    }
    
    [Then(@"the first product should be ""(.*)""")]
    public void ThenTheFirstProductShouldBe(string expectedName)
    {
        var products = _scenarioContext["Products"] as List<Product>;
        products!.First().Name.Should().Be(expectedName);
    }
}
```

### Hooks

```csharp
[Binding]
public class TestHooks
{
    [BeforeScenario]
    public void BeforeScenario()
    {
        Console.WriteLine($"Starting: {ScenarioContext.Current.ScenarioInfo.Title}");
    }
    
    [AfterScenario]
    public void AfterScenario()
    {
        Console.WriteLine($"Finished: {ScenarioContext.Current.ScenarioInfo.Title}");
    }
    
    [BeforeFeature]
    public static void BeforeFeature(FeatureContext featureContext)
    {
        Console.WriteLine($"Feature: {featureContext.FeatureInfo.Title}");
    }
    
    [AfterFeature]
    public static void AfterFeature(FeatureContext featureContext)
    {
        // Cleanup
    }
}
```

## Playwright + BDD

```csharp
// Step definitions com Playwright
[Given(@"I am on the products page")]
public async Task GivenIAmOnTheProductsPage()
{
    await _page.GotoAsync("http://localhost:5000/products");
}

[When(@"I search for ""(.*)""")]
public async Task WhenISearchFor(string searchTerm)
{
    await _page.FillAsync("[data-testid='search-input']", searchTerm);
    await _page.ClickAsync("[data-testid='search-button']");
}

[Then(@"I should see (\d+) products")]
public async Task ThenIShouldSeeProducts(int expectedCount)
{
    var rows = await _page.QuerySelectorAllAsync("[data-testid='product-row']");
    rows.Should().HaveCount(expectedCount);
}
```

## BDD com xUnit

```csharp
public class ProductFeatureTests
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;
    
    public ProductFeatureTests()
    {
        _factory = new WebApplicationFactory<Program>();
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task Create_Product_With_Valid_Data_Should_Succeed()
    {
        // Given
        var command = new CreateProductCommand("Test Product", 99.99m, 1, null);
        
        // When
        var response = await _client.PostAsJsonAsync("/api/products", command);
        
        // Then
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var product = await response.Content.ReadFromJsonAsync<ProductDto>();
        product!.Name.Should().Be("Test Product");
    }
    
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task Create_Product_With_Invalid_Price_Should_Fail(decimal price)
    {
        // Given
        var command = new CreateProductCommand("Test", price, 1, null);
        
        // When
        var response = await _client.PostAsJsonAsync("/api/products", command);
        
        // Then
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }
}
```

## Benefícios do BDD

1. **Comunicação**: Linguagem natural entendida por todos
2. **Documentação**: Cenários vivos como documentação
3. **Alinhamento**: Business + Dev + QA na mesma página
4. **Regresão**: Cenários automatizados detectam quebras
5. **Confiança**: Cobertura comportamental completa

## Quando Usar BDD

| Cenário | Recomendação |
|---------|-------------|
| Features complexas | ✅ BDD |
| CRUD simples | ⚠️ Opcional |
| Integrações | ✅ BDD |
| APIs | ✅ BDD |
| UI complexa | ✅ BDD |
| Bug fixes | ⚠️ Opcional |

## Fontes Oficiais
- specflow.org
- docs.specflow.org
- cucumber.io
- github.com/cucumber
