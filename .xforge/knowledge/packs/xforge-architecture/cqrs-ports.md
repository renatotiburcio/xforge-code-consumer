# CQRS + Ports & Adapters com XForge.MediatR

Padroes de Commands, Queries, Handlers e Ports no XForge.

## Command (write)

```csharp
public record CriarPedidoCommand(
    Guid ClienteId,
    List<ItemPedidoDto> Itens
) : IRequest<Result<Guid>>;

public class CriarPedidoValidator : AbstractValidator<CriarPedidoCommand> {
    public CriarPedidoValidator() {
        RuleFor(c => c.ClienteId).NotEmpty();
        RuleFor(c => c.Itens).NotEmpty().Must(i => i.Count <= 100);
    }
}

public class CriarPedidoHandler : IRequestHandler<CriarPedidoCommand, Result<Guid>> {
    private readonly IPedidoRepository _repo;
    private readonly IValidator<CriarPedidoCommand> _validator;
    private readonly IUnitOfWork _uow;

    public async Task<Result<Guid>> HandleAsync(CriarPedidoCommand cmd, CancellationToken ct) {
        var validation = await _validator.ValidateAsync(cmd, ct);
        if (!validation.IsValid) return Result.Failure<Guid>(validation.Errors);

        var pedido = Pedido.Criar(cmd.ClienteId, cmd.Itens.Select(i => (i.ProdutoId, i.Quantidade)));
        await _repo.SalvarAsync(pedido, ct);
        await _uow.CommitAsync(ct);
        return Result.Success(pedido.Id);
    }
}
```

## Query (read)

```csharp
public record ObterPedidoQuery(Guid Id) : IRequest<Result<PedidoView>>;

public class ObterPedidoHandler : IRequestHandler<ObterPedidoQuery, Result<PedidoView>> {
    private readonly IPedidoReadRepository _repo;

    public async Task<Result<PedidoView>> HandleAsync(ObterPedidoQuery q, CancellationToken ct) {
        var pedido = await _repo.ObterViewAsync(q.Id, ct);
        return pedido is null
            ? Result.Failure<PedidoView>("Pedido nao encontrado")
            : Result.Success(pedido);
    }
}
```

## Port (abstracao)

```csharp
public interface IPedidoRepository {
    Task<Pedido?> ObterAsync(Guid id, CancellationToken ct);
    Task SalvarAsync(Pedido pedido, CancellationToken ct);
}

public interface IPedidoReadRepository {
    Task<PedidoView?> ObterViewAsync(Guid id, CancellationToken ct);
    Task<List<PedidoView>> ListarAsync(ClienteId cliente, int page, int size, CancellationToken ct);
}
```

## Adapter (implementacao)

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
        if (await _ctx.Pedidos.AnyAsync(p => p.Id == pedido.Id, ct)) {
            _ctx.Pedidos.Update(pedido);
        } else {
            await _ctx.Pedidos.AddAsync(pedido, ct);
        }
    }
}
```

## Pipeline behaviors (XForge.MediatR)

```csharp
public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse> {
    public async Task<TResponse> HandleAsync(TRequest req, RequestHandlerDelegate<TResponse> next, CancellationToken ct) {
        _logger.LogInformation("Handling {Request}", typeof(TRequest).Name);
        var sw = Stopwatch.StartNew();
        var response = await next();
        _logger.LogInformation("Handled {Request} in {Ms}ms", typeof(TRequest).Name, sw.ElapsedMilliseconds);
        return response;
    }
}

// Register in Program.cs
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(UnitOfWorkBehavior<,>));
```

## Tags

cqrs, xforge-mediatr, commands, queries, handlers, ports, adapters, validation
