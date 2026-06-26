# DDD Bounded Contexts + Context Mapping

Como dividir dominios grandes em contextos independentes.

## Conceitos chave

- **Bounded Context (BC)**: limite de um modelo. Dentro do BC, termos tem significado unico. Fora, o mesmo termo pode significar outra coisa.
- **Context Map**: diagrama de como BCs se relacionam.
- **Shared Kernel**: parte do modelo compartilhada por 2+ BCs.
- **Anti-Corruption Layer (ACL)**: tradutor que protege um BC de mudancas em outro.
- **Conformist**: BC que aceita o modelo de outro sem questionar.
- **Customer-Supplier**: relacao clara de dependencia.

## Exemplo: ERP

```
+----------------+      +----------------+
|   Vendas       |----->|   Estoque      |
|   (BC)         | ACL  |   (BC)         |
+----------------+      +----------------+
        |                       |
        v                       v
+----------------+      +----------------+
|   Fiscal       |      |   Compras      |
|   (BC)         |      |   (BC)         |
+----------------+      +----------------+
        |
        v
+----------------+
|   Financeiro   |
|   (BC)         |
+----------------+
```

## Anti-Corruption Layer

Quando Vendas precisa consultar Estoque, nao importa a entidade Produto do Estoque. Cria um DTO no ACL:

```csharp
public class EstoqueACL : IEstoqueConsulta {
    private readonly IEstoqueClient _client;

    public async Task<EstoqueView> ConsultarAsync(Guid produtoId, CancellationToken ct) {
        var estoque = await _client.ObterAsync(produtoId, ct);
        return new EstoqueView(
            produtoId,
            estoque.QuantidadeDisponivel,
            estoque.PrecoCusto
        );
    }
}
```

Vendas depende apenas de IEstoqueConsulta (port), nao do Estoque.

## Shared Kernel

Quando 2+ BCs precisam do mesmo value object (ex: Cnpj):

```csharp
public record Cnpj(string Valor) {
    public static Cnpj Parse(string valor) {
        if (!IsValid(valor)) throw new ArgumentException("CNPJ invalido");
        return new Cnpj(valor);
    }
    public static bool IsValid(string valor) { /* algoritmo */ }
}
```

**Regra**: Shared Kernel deve ser PEQUENO. Se crescer, vira outro BC.

## Domain Events

BCs se comunicam via eventos (nao chamada direta):

```csharp
public record PedidoCriado(Guid PedidoId, Guid ClienteId, decimal Total) : IDomainEvent;

public class ReservarEstoqueOnPedidoCriado : IEventHandler<PedidoCriado> {
    public async Task HandleAsync(PedidoCriado evento, CancellationToken ct) {
        await _estoqueService.ReservarAsync(evento.PedidoId, ct);
    }
}
```

Vendas NAO sabe que Estoque consome o evento. Estoque eh autonomo.

## Tags

ddd, bounded-context, context-map, anti-corruption-layer, shared-kernel, events
