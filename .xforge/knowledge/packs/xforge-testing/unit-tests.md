# Unit Tests com xUnit + FluentAssertions + Moq

Padrao XForge para testes unitarios em .NET.

## Estrutura AAA (Arrange, Act, Assert)

```csharp
[Fact]
public async Task ObterCliente_ClienteExiste_RetornaCliente() {
    // Arrange
    var id = Guid.NewGuid();
    var cliente = new Cliente(id, "Renato");
    var repo = new Mock<IClienteRepository>();
    repo.Setup(r => r.ObterAsync(id, It.IsAny<CancellationToken>()))
        .ReturnsAsync(cliente);
    var sut = new ClienteService(repo.Object, NullLogger<ClienteService>.Instance);

    // Act
    var resultado = await sut.ObterAsync(id);

    // Assert
    resultado.Should().NotBeNull();
    resultado!.Nome.Should().Be("Renato");
    resultado.Id.Should().Be(id);
    repo.Verify(r => r.ObterAsync(id, It.IsAny<CancellationToken>()), Times.Once);
}
```

## FluentAssertions

```csharp
resultado.Should().NotBeNull();
resultado.Should().BeOfType<Cliente>();
resultado.Nome.Should().StartWith("Ren").And.EndWith("to");
lista.Should().HaveCount(3).And.Contain(x => x.Ativo);
excecao.Message.Should().Contain("not found");
```

## Moq - comportamentos comuns

```csharp
mock.Setup(x => x.MetodoAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()))
    .ReturnsAsync(novo Valor());

mock.Setup(x => x.Metodo(It.Is<string>(s => s.StartsWith("X"))))
    .Throws(new InvalidOperationException());

mock.SetupSequence(x => x.Contador())
    .Returns(1).Returns(2).Returns(3);

mock.Verify(x => x.MetodoAsync(It.IsAny<int>(), It.IsAny<CancellationToken>()),
            Times.Exactly(2));

mock.VerifyNoOtherCalls();
```

## Bogus (faker)

```csharp
var faker = new Faker("pt_BR");
var cliente = new Cliente(
    Guid.NewGuid(),
    faker.Person.FullName,
    faker.Person.Email
);

var lista = faker.Make(50, () => new Produto(
    Guid.NewGuid(),
    faker.Commerce.ProductName(),
    decimal.Parse(faker.Commerce.Price(10, 1000))
)).ToList();
```

## Tags

testing, xunit, moq, fluentassertions, aaa, faker, dotnet
