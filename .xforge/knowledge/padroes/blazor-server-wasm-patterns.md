---
id: blazor-server-wasm-patterns
type: conhecimento
tags: [blazor, server, wasm, componentes, renderizacao, state, signalr]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Blazor Server e WASM — Padrões Enterprise
- **Seções principais**: Comparativo, Estrutura de Componentes, State Management, Comunicação com Servidor
- **Tags**: blazor, server, wasm, componentes, renderizacao, state, signalr
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `blazor-server-wasm-patterns` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 8 |


# Blazor Server e WASM — Padrões Enterprise

## Comparativo

| Aspecto | Blazor Server | Blazor WASM |
|---------|--------------|-------------|
| Execução | Servidor (SignalR) | Cliente (Browser) |
| Latência | Depende da rede | Zero (local) |
| Download inicial | ~3MB | ~5-15MB |
| Acesso a BD | Direto | Via API |
| Offline | Não | Sim (PWA) |
| Segurança | Código no servidor | Código no browser |
| Escalabilidade | Conexões simultâneas | CDN |

## Estrutura de Componentes

### Componente Base
```razor
<div class="@CssClass">
    @ChildContent
</div>

@code {
    [Parameter] public RenderFragment? ChildContent { get; set; }
    [Parameter] public string CssClass { get; set; } = "";
}
```

### Componente com Lógica
```razor
@page "/products"
@inject IProductService ProductService
@inject NavigationManager Nav

<h3>Produtos</h3>

@if (_products is null)
{
    <LoadingSpinner />
}
else if (!_products.Any())
{
    <EmptyState Message="Nenhum produto encontrado" />
}
else
{
    <ProductTable Products="_products" OnEdit="EditProduct" OnDelete="DeleteProduct" />
}

@code {
    private List<ProductDto>? _products;

    protected override async Task OnInitializedAsync()
    {
        _products = await ProductService.GetAllAsync();
    }

    private void EditProduct(int id) => Nav.NavigateTo($"/products/{id}/edit");

    private async Task DeleteProduct(int id)
    {
        await ProductService.DeleteAsync(id);
        _products = await ProductService.GetAllAsync();
    }
}
```

### Cascading Parameters
```razor
<CascadingValue Value="Theme">
    <CascadingValue Value="Culture">
        @ChildContent
    </CascadingValue>
</CascadingValue>

@code {
    [Parameter] public RenderFragment? ChildContent { get; set; }
    [CascadingParameter] public string Theme { get; set; } = "light";
    [CascadingParameter] public CultureInfo Culture { get; set; } = new("pt-BR");
}
```

## State Management

### CascadingValue + StateContainer
```csharp
public class AppState
{
    private readonly ILogger<AppState> _logger;
    
    public string? CurrentUser { get; set; }
    public List<string> Notifications { get; } = new();
    
    public event Action? OnChange;
    
    public void NotifyStateChanged() => OnChange?.Invoke();
}

// Registration
builder.Services.AddScoped<AppState>();

// Usage
@inject AppState State
@implements IDisposable

@code {
    protected override void OnInitialized()
    {
        State.OnChange += StateHasChanged;
    }
    
    public void Dispose()
    {
        State.OnChange -= StateHasChanged;
    }
}
```

### Flux/Redux Pattern
```csharp
public record State(int Count, bool IsLoading);
public record IncrementAction;
public record DecrementAction;
public record FetchDataAction;

public class Reducer
{
    public static State Reduce(State state, object action) => action switch
    {
        IncrementAction => state with { Count = state.Count + 1 },
        DecrementAction => state with { Count = state.Count - 1 },
        FetchDataAction => state with { IsLoading = true },
        _ => state
    };
}
```

## Comunicação com Servidor

### SignalR Hub
```csharp
// Server
public class OrderHub : Hub
{
    public async Task NotifyOrderStatus(int orderId, string status)
    {
        await Clients.All.SendAsync("OrderStatusChanged", orderId, status);
    }
}

// Client (Blazor)
@inject IHubConnectionBuilder HubBuilder

@code {
    private HubConnection? _hubConnection;

    protected override async Task OnInitializedAsync()
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(NavigationManager.ToAbsoluteUri("/orderhub"))
            .WithAutomaticReconnect()
            .Build();

        _hubConnection.On<int, string>("OrderStatusChanged", (orderId, status) =>
        {
            InvokeAsync(StateHasChanged);
        });

        await _hubConnection.StartAsync();
    }
}
```

### HTTP Client
```csharp
// Registration
builder.Services.AddHttpClient<IProductApi, ProductApi>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

// Usage
public class ProductApi : IProductApi
{
    private readonly HttpClient _http;
    
    public async Task<List<ProductDto>> GetAllAsync()
    {
        var response = await _http.GetAsync("/products");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<List<ProductDto>>() ?? new();
    }
}
```

## Renderização

### RenderMode
```razor
<!-- Server -->
@rendermode RenderMode.InteractiveServer

<!-- WASM -->
@rendermode RenderMode.InteractiveWebAssembly

<!-- Auto (decide no server) -->
@rendermode RenderMode.InteractiveAuto

<!-- Static (SSR) -->
@rendermode RenderMode.Static
```

### ForceReRender
```csharp
private async Task RefreshData()
{
    // Força re-renderização
    await InvokeAsync(StateHasChanged);
    
    // Ou via Reference
    await _componentRef.Value?.RefreshAsync();
}
```

## Performance

### Virtualization
```razor
<Virtualize Items="@_products" Context="product" ItemSize="50">
    <div class="product-row">
        @product.Name - @product.Price
    </div>
</Virtualize>
```

### Lazy Loading
```csharp
// Lazy load assemblies
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(Program).Assembly);

// Lazy load route
@page "/heavy"
@attribute [LazyRoute("/heavy")]
```

## Acessibilidade

```razor
<button @onclick="HandleClick"
        aria-label="@($"Remover {Product.Name}")"
        role="button"
        tabindex="0"
        @onkeydown="HandleKeydown">
    <span class="sr-only">Remover</span>
    <Icon Name="trash" />
</button>
```

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/blazor
- docs.microsoft.com/aspnet/core/blazor/components
- docs.microsoft.com/aspnet/core/blazor/state-management
