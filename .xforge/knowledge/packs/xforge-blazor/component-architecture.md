# Blazor Component Architecture

Guia de design de componentes Blazor para apps enterprise.

## Anatomia de um componente

```razor
@page "/produtos/{Id:int}"
@inject IProdutoService ProdutoService
@implements IAsyncDisposable

<PageTitle>Produto @Id</PageTitle>

<h1>@produto?.Nome</h1>

@if (produto is null) {
    <p>Carregando...</p>
} else {
    <EditForm Model="produto" OnValidSubmit="Salvar">
        <InputText @bind-Value="produto.Nome" />
        <button type="submit">Salvar</button>
    </EditForm>
}

@code {
    [Parameter] public int Id { get; set; }
    private Produto? produto;
    private CancellationTokenSource? cts;

    protected override async Task OnInitializedAsync() {
        cts = new CancellationTokenSource();
        produto = await ProdutoService.ObterAsync(Id, cts.Token);
    }

    private async Task Salvar() {
        if (produto is null) return;
        await ProdutoService.SalvarAsync(produto, cts!.Token);
    }

    public ValueTask DisposeAsync() {
        cts?.Cancel();
        cts?.Dispose();
        return ValueTask.CompletedTask;
    }
}
```

## Lifecycle (ordem de execucao)

1. `OnInitialized` / `OnInitializedAsync`
2. `OnParametersSet` / `OnParametersSetAsync` (em cada render se params mudaram)
3. `OnAfterRender` / `OnAfterRenderAsync` (apos cada render)
4. `Dispose` / `DisposeAsync` (quando removido da arvore)

## Parametros

```razor
<MeuComponente Titulo="Vendas" MaxItens="50" OnSalvar="HandleSalvar" />

@code {
    [Parameter, EditorRequired] public string Titulo { get; set; } = "";
    [Parameter] public int MaxItens { get; set; } = 100;
    [Parameter] public EventCallback<Produto> OnSalvar { get; set; }
}
```

## Otimizacoes

- `[StreamRendering]` para streaming SSR
- `<Virtualize>` para listas longas
- `@key` explicito em loops para diff correto
- `[Parameter(CaptureUnmatchedValues = true)]` para dict generico

## Anti-patterns

- Logica de negocio dentro de `@code` (usar service injetado)
- Chamadas async sem `CancellationToken`
- `StateHasChanged()` manual (sinal de fluxo assincrono mal feito)

## Tags

blazor, components, razor, lifecycle, performance, srp
