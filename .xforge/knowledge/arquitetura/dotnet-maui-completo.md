---
id: dotnet-maui-completo
type: conhecimento
tags: [maui, mobile, desktop, xaml, blazor, hybrid, android, ios, windows, macos]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre .NET MAUI - Guia Completo
- **Seções principais**: Conceito, Comparativo, Estrutura do Projeto, MVVM Pattern
- **Tags**: maui, mobile, desktop, xaml, blazor, hybrid, android, ios, windows, macos
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `dotnet-maui-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 13 |


# .NET MAUI - Guia Completo

## Conceito

.NET MAUI (Multi-platform App UI) é o framework para criar aplicações mobile e desktop com C# e .NET, suportando Android, iOS, Windows e macOS com uma única codebase.

## Comparativo

| Framework | Plataforma | Linguagem | UI |
|-----------|-----------|-----------|-----|
| .NET MAUI | Android, iOS, Windows, macOS | C# | XAML/Blazor |
| Xamarin.Forms | Android, iOS (legado) | C# | XAML |
| WPF | Windows | C# | XAML |
| WinForms | Windows | C# | Designer |
| Avalonia | Cross-platform | C# | XAML |
| Flutter | Android, iOS, Web | Dart | Widget |
| React Native | Android, iOS | JavaScript | Components |

## Estrutura do Projeto

```
MyApp/
├── MauiProgram.cs          # Configuração DI e Services
├── App.xaml / App.xaml.cs  # Aplicação
├── AppShell.xaml           # Shell de navegação
├── MainPage.xaml           # Página principal
├── Views/                  # Páginas
├── ViewModels/             # ViewModels (MVVM)
├── Models/                 # Modelos de dados
├── Services/               # Serviços (API, DB, etc.)
├── Platforms/
│   ├── Android/            # Código específico Android
│   ├── iOS/                # Código específico iOS
│   ├── Windows/            # Código específico Windows
│   └── macOS/              # Código específico macOS
└── Resources/
    ├── Fonts/
    ├── Images/
    └── Styles/
```

## MVVM Pattern

### Modelo
```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string ImageUrl { get; set; } = string.Empty;
}
```

### ViewModel
```csharp
public partial class ProductViewModel : ObservableObject
{
    private readonly IProductService _productService;
    
    [ObservableProperty]
    private ObservableCollection<Product> _products = new();
    
    [ObservableProperty]
    private Product? _selectedProduct;
    
    [ObservableProperty]
    private bool _isLoading;
    
    public ProductViewModel(IProductService productService)
    {
        _productService = productService;
    }
    
    [RelayCommand]
    private async Task LoadProductsAsync()
    {
        IsLoading = true;
        try
        {
            var products = await _productService.GetAllAsync();
            Products = new ObservableCollection<Product>(products);
        }
        finally
        {
            IsLoading = false;
        }
    }
    
    [RelayCommand]
    private async Task AddProductAsync()
    {
        await Shell.Current.GoToAsync("addproduct");
    }
    
    [RelayCommand]
    private async Task DeleteProductAsync(Product product)
    {
        if (await Application.Current?.MainPage?.DisplayAlert(
            "Confirm", $"Delete {product.Name}?", "Yes", "No")!)
        {
            await _productService.DeleteAsync(product.Id);
            Products.Remove(product);
        }
    }
}
```

### View (XAML)
```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProductPage"
             Title="Products">
    
    <ShellContent.TitleView>
        <Label Text="Products" FontSize="Large" />
    </Shell.Content>
    
    <Grid>
        <RefreshView IsRefreshing="{Binding IsLoading}"
                     Command="{Binding LoadProductsCommand}">
            <CollectionView ItemsSource="{Binding Products}"
                            SelectionMode="Single"
                            SelectionChanged="OnSelectionChanged">
                <CollectionView.ItemTemplate>
                    <DataTemplate x:DataType="models:Product">
                        <Grid Padding="10" ColumnDefinitions="*,Auto">
                            <Grid.ColumnDefinitions>
                                <ColumnDefinition Width="*" />
                                <ColumnDefinition Width="Auto" />
                            </Grid.ColumnDefinitions>
                            
                            <VerticalStackGrid Grid.Column="0">
                                <Label Text="{Binding Name}" 
                                       FontSize="18" FontAttributes="Bold" />
                                <Label Text="{Binding Price, StringFormat='{0:C}'}"
                                       FontSize="14" TextColor="Gray" />
                            </VerticalStackGrid>
                            
                            <Button Grid.Column="1"
                                    Text="🗑"
                                    Command="{Binding Source={RelativeSource AncestorType={x:Type vm:ProductViewModel}}, 
                                            Path=DeleteProductCommand}"
                                    CommandParameter="{Binding .}" />
                        </Grid>
                    </DataTemplate>
                </CollectionView.ItemTemplate>
            </CollectionView>
        </RefreshView>
        
        <Button Text="+ Add Product"
                Command="{Binding AddProductCommand}"
                HorizontalOptions="End"
                VerticalOptions="End"
                Margin="20"
                BackgroundColor="{AppThemeBinding Light=Blue, Dark=DarkBlue}"
                TextColor="White" />
    </Grid>
</ContentPage>
```

## Navegação

### Shell Navigation
```csharp
// Registrar rotas
Routing.RegisterRoute("productdetail", typeof(ProductDetailPage));
Routing.RegisterRoute("addproduct", typeof(AddProductPage));

// Navegar
await Shell.Current.GoToAsync($"productdetail?id={product.Id}");

// Receber parâmetro
[QueryProperty(nameof(ProductId), "id")]
public partial class ProductDetailViewModel : ObservableObject
{
    [ObservableProperty]
    private string _productId = string.Empty;
    
    partial void OnProductIdChanged(string value)
    {
        LoadProductAsync(int.Parse(value));
    }
}
```

### NavigationPage
```csharp
// AppShell.xaml
<Shell>
    <TabBar>
        <ShellContent Title="Products" ContentTemplate="{DataTemplate views:ProductPage}" />
        <ShellContent Title="Orders" ContentTemplate="{DataTemplate views:OrderPage}" />
        <ShellContent Title="Settings" ContentTemplate="{DataTemplate views:SettingsPage}" />
    </TabBar>
</Shell>
```

## Serviços e Dependency Injection

### MauiProgram.cs
```csharp
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        
        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
            });
        
        // Services
        builder.Services.AddHttpClient<IProductService, ProductService>(client =>
        {
            client.BaseAddress = new Uri("https://api.example.com");
        });
        
        builder.Services.AddSingleton<ISqliteConnection, SqliteConnection>();
        builder.Services.AddScoped<IProductRepository, ProductRepository>();
        
        // ViewModels
        builder.Services.AddTransient<ProductViewModel>();
        builder.Services.AddTransient<ProductDetailViewModel>();
        
        // Pages
        builder.Services.AddTransient<ProductPage>();
        builder.Services.AddTransient<ProductDetailPage>();
        
        return builder.Build();
    }
}
```

## Acesso a Dados Local

### SQLite
```csharp
// Repository
public class ProductRepository : IProductRepository
{
    private readonly ISqliteConnection _connection;
    
    public ProductRepository(ISqliteConnection connection)
    {
        _connection = connection;
        _connection.CreateTableAsync<Product>();
    }
    
    public async Task<List<Product>> GetAllAsync()
    {
        return await _connection.Table<Product>().ToListAsync();
    }
    
    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _connection.Table<Product>()
            .FirstOrDefaultAsync(p => p.Id == id);
    }
    
    public async Task SaveAsync(Product product)
    {
        if (product.Id != 0)
            await _connection.UpdateAsync(product);
        else
            await _connection.InsertAsync(product);
    }
    
    public async Task DeleteAsync(int id)
    {
        var product = await GetByIdAsync(id);
        if (product != null)
            await _connection.DeleteAsync(product);
    }
}
```

## APIs e Conectividade

### HTTP Client
```csharp
public class ProductService : IProductService
{
    private readonly HttpClient _http;
    
    public async Task<List<Product>> GetAllAsync()
    {
        var response = await _http.GetAsync("/products");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<List<Product>>() ?? new();
    }
    
    public async Task<Product> GetByIdAsync(int id)
    {
        var response = await _http.GetAsync($"/products/{id}");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<Product>() 
            ?? throw new NotFoundException();
    }
    
    public async Task<Product> CreateAsync(CreateProductCommand cmd)
    {
        var response = await _http.PostAsJsonAsync("/products", cmd);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<Product>()!;
    }
}
```

### Connectivity
```csharp
// Verificar conectividade
if (Connectivity.Current.NetworkAccess != NetworkAccess.Internet)
{
    await DisplayAlert("Error", "No internet connection", "OK");
    return;
}

// Monitorar mudanças
Connectivity.Current.NetworkAccessChanged += (sender, args) =>
{
    if (args.NetworkAccess == NetworkAccess.Internet)
        SyncDataAsync();
};
```

## Plataforma Específica

### Conditional Compilation
```csharp
// Código específico por plataforma
#if ANDROID
    // Código Android
    public void Vibrate() => Vibration.Vibrate(TimeSpan.FromMilliseconds(200));
#elif IOS
    // Código iOS
    public void Vibrate() => HapticFeedback.PerformClick();
#elif WINDOWS
    // Código Windows
    public void Vibrate() => 
        new Windows.UI.Input.HapticFeedback().Perform(HapticFeedbackKind.Click);
#endif
```

### Permissões
```csharp
// Solicitar permissão de câmera
var status = await Permissions.CheckStatusAsync<Permissions.Camera>();
if (status != PermissionStatus.Granted)
{
    status = await Permissions.RequestAsync<Permissions.Camera>();
}

// Solicitar permissão de localização
var locationStatus = await Permissions.CheckStatusAsync<Permissions.LocationWhenInUse>();
if (locationStatus != PermissionStatus.Granted)
{
    locationStatus = await Permissions.RequestAsync<Permissions.LocationWhenInUse>();
}
```

## Blazor Hybrid

```csharp
// MauiProgram.cs
builder.Services.AddMauiBlazorWebView();

// MainPage.razor
@page "/products"

<h3>Products</h3>

@if (_products is null)
{
    <p>Loading...</p>
}
else
{
    @foreach (var product in _products)
    {
        <div class="product-card">
            <h4>@product.Name</h4>
            <p>@product.Price.ToString("C")</p>
        </div>
    }
}

@code {
    private List<Product>? _products;
    
    protected override async Task OnInitializedAsync()
    {
        _products = await Http.GetFromJsonAsync<List<Product>>("products");
    }
}
```

## Publicação

### Android
```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### iOS
```xml
<!-- Info.plist -->
<key>NSCameraUsageDescription</key>
<string>Need camera for scanning</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Need location for mapping</string>
```

### Windows
- Gerar MSIX para Microsoft Store
- Gerar .exe para distribuição direta

## Performance

### Virtualização
```xml
<CollectionView ItemsSource="{Binding Products}"
                CachingStrategy="RecycleElement">
    <!-- RecycleElement reutiliza elementos da lista -->
</CollectionView>
```

### Lazy Loading
```csharp
// Carregar dados sob demanda
<CollectionView ItemsSource="{Binding Products}"
                RemainingItemsThreshold="5"
                RemainingItemsThresholdReached="OnThresholdReached" />
```

## Fontes Oficiais
- docs.microsoft.com/dotnet/maui
- learn.microsoft.com/dotnet/maui
- github.com/dotnet/maui
