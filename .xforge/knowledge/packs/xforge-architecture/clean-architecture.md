# Clean Architecture no XForge

Camadas, regras de dependencia, organizacao de pastas.

## As 4 camadas

```
+------------------+
|     API/Web      |  Controllers, DTOs, Middleware
+------------------+
        |
        v  (depende)
+------------------+
|  Application     |  Use Cases, Commands, Queries, Handlers
+------------------+
        |
        v  (depende)
+------------------+
|     Domain       |  Entities, Value Objects, Events, Domain Services
+------------------+
        ^
        |  (implementa)
+------------------+
|  Infrastructure  |  EF Core, HttpClient, FileSystem, External APIs
+------------------+
```

**Regra de dependencia**: setas apontam para dentro (Domain nao conhece nada).

## Estrutura de pastas

```
src/
  MeuModulo.Domain/
    Entities/
    ValueObjects/
    Events/
    Interfaces/    (ports OUT)
  MeuModulo.Application/
    Commands/
    Queries/
    Handlers/
    Validators/
    Interfaces/    (ports IN)
  MeuModulo.Infrastructure/
    Persistence/
    ExternalApis/
    DependencyInjection.cs
  MeuModulo.Api/
    Endpoints/
    Middleware/
    Program.cs
```

## Exemplo: port + adapter

Domain define a interface:

```csharp
public interface IPedidoRepository {
    Task<Pedido?> ObterAsync(Guid id, CancellationToken ct);
    Task SalvarAsync(Pedido pedido, CancellationToken ct);
}
```

Infrastructure implementa:

```csharp
public class PedidoRepository : IPedidoRepository {
    private readonly AppDbContext _ctx;
    public PedidoRepository(AppDbContext ctx) => _ctx = ctx;

    public async Task<Pedido?> ObterAsync(Guid id, CancellationToken ct) {
        return await _ctx.Pedidos
            .Include(p => p.Itens)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }

    public async Task SalvarAsync(Pedido pedido, CancellationToken ct) {
        _ctx.Pedidos.Update(pedido);
        await _ctx.SaveChangesAsync(ct);
    }
}
```

Application consome via port:

```csharp
public class CriarPedidoHandler {
    private readonly IPedidoRepository _repo;
    public CriarPedidoHandler(IPedidoRepository repo) => _repo = repo;

    public async Task<Guid> HandleAsync(CriarPedidoCommand cmd, CancellationToken ct) {
        var pedido = Pedido.Criar(cmd.ClienteId, cmd.Itens);
        await _repo.SalvarAsync(pedido, ct);
        return pedido.Id;
    }
}
```

API chama handler:

```csharp
app.MapPost("/pedidos", async (CriarPedidoCommand cmd, ISender sender, CancellationToken ct) => {
    var id = await sender.SendAsync(cmd, ct);
    return Results.Created($"/pedidos/{id}", new { id });
});
```

## Regras de dependency

```xml
<!-- Domain.csproj - nao depende de NADA alem de stdlib -->
<ItemGroup>
  <PackageReference Include="XForge.MediatR.Abstractions" Version="1.0.0" />
</ItemGroup>

<!-- Application.csproj -->
<ItemGroup>
  <ProjectReference Include="..\MeuModulo.Domain\MeuModulo.Domain.csproj" />
  <PackageReference Include="XForge.MediatR" Version="1.0.0" />
  <PackageReference Include="FluentValidation" Version="11.*" />
</ItemGroup>

<!-- Infrastructure.csproj -->
<ItemGroup>
  <ProjectReference Include="..\MeuModulo.Application\MeuModulo.Application.csproj" />
  <PackageReference Include="Microsoft.EntityFrameworkCore" Version="9.*" />
</ItemGroup>

<!-- Api.csproj -->
<ItemGroup>
  <ProjectReference Include="..\MeuModulo.Application\MeuModulo.Application.csproj" />
  <ProjectReference Include="..\MeuModulo.Infrastructure\MeuModulo.Infrastructure.csproj" />
</ItemGroup>
```

## Tags

architecture, clean-architecture, ddd, solid, ports-adapters, dotnet
