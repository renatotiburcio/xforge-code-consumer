# Integration Tests com Testcontainers

Padroes para testes de integracao reais com Docker.

## PostgreSQL container

```csharp
public class DatabaseFixture : IAsyncLifetime {
    public PostgreSqlContainer Container { get; private set; } = default!;
    public string ConnectionString => Container.GetConnectionString();

    public async Task InitializeAsync() {
        Container = new PostgreSqlBuilder()
            .WithImage("postgres:17-alpine")
            .WithDatabase("xforge_test")
            .WithUsername("test")
            .WithPassword("test")
            .Build();
        await Container.StartAsync();
    }

    public async Task DisposeAsync() {
        await Container.DisposeAsync();
    }
}

[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class ClienteRepositoryTests {
    private readonly DatabaseFixture _fixture;
    public ClienteRepositoryTests(DatabaseFixture fixture) => _fixture = fixture;

    [Fact]
    public async Task Inserir_ClienteValido_PersisteNoBanco() {
        await using var ctx = new AppDbContext(
            new DbContextOptionsBuilder<AppDbContext>()
                .UseNpgsql(_fixture.ConnectionString)
                .Options);
        await ctx.Database.MigrateAsync();
        var repo = new ClienteRepository(ctx);
        var cliente = new Cliente("Renato");

        await repo.InserirAsync(cliente);
        var encontrado = await repo.ObterAsync(cliente.Id);

        encontrado.Should().NotBeNull();
    }
}
```

## Redis container

```csharp
var redis = new RedisBuilder()
    .WithImage("redis:7-alpine")
    .Build();
await redis.StartAsync();

var conn = redis.GetConnectionString();
var multiplexer = ConnectionMultiplexer.Connect(conn);
var db = multiplexer.GetDatabase();
```

## RabbitMQ container

```csharp
var rabbit = new RabbitMqBuilder()
    .WithImage("rabbitmq:3.13-management-alpine")
    .WithPortBinding(5672, true)
    .Build();
```

## Boas praticas

- Reusar container entre tests via `IClassFixture` ou `ICollectionFixture`
- Rodar migrations no `InitializeAsync`
- Limpar dados entre tests (`TRUNCATE TABLE ... CASCADE`)
- Tempo total: containers reutilizados ~1-5s, novo container ~10-30s
- Marcadores `[Trait("Category", "Integration")]` para separar CI

## Tags

testing, testcontainers, docker, postgres, redis, rabbitmq, integration
