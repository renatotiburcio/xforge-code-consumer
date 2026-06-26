# Blazor State Management

Padroes para gerenciar estado em apps Blazor enterprise.

## Sem state container (simples)

Para apps pequenos, `[Parameter]` + `EventCallback` bastam.

## CascadingParameter (medio)

Compartilha estado em uma sub-arvore de componentes.

```razor
<CascadingValue Value="@usuarioLogado">
    <Layout>
        <Sidebar />
        <MainContent />
    </Layout>
</CascadingValue>

@code {
    private Usuario usuarioLogado = new("renato", "admin");
}
```

## Service injetado + EventCallback (recomendado)

```csharp
public class CarrinhoState {
    private readonly List<Item> _itens = new();
    public IReadOnlyList<Item> Itens => _itens;
    public event Action? OnChange;

    public void Adicionar(Item item) {
        _itens.Add(item);
        OnChange?.Invoke();
    }
}

builder.Services.AddScoped<CarrinhoState>();
```

```razor
@inject CarrinhoState Carrinho
@implements IDisposable

<span>@Carrinho.Itens.Count itens</span>

@code {
    protected override void OnInitialized() {
        Carrinho.OnChange += StateHasChanged;
    }
    public void Dispose() {
        Carrinho.OnChange -= StateHasChanged;
    }
}
```

## Fluxor (grande escala)

Para apps com 20+ telas e 5+ features cross-cutting.

```csharp
[FeatureState]
public class CarrinhoFeature : Feature<CarrinhoState> {
    public override string GetName() => "Carrinho";
    protected override CarrinhoState GetInitialState() => new();
}

public record AdicionarItemAction(Item Item);
public class AdicionarItemReducer : Reducer<CarrinhoState, AdicionarItemAction> {
    public override CarrinhoState Reduce(CarrinhoState state, AdicionarItemAction action) {
        return state with { Itens = new List<Item>(state.Itens) { action.Item } };
    }
}
```

## Tags

blazor, state, cascadingparameter, fluxor, redux, persistence
