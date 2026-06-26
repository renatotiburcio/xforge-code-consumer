---
id: wpf-winforms-desktop-completo
type: conhecimento
tags: [wpf, winforms, xaml, data-binding, mvvm, desktop, windows]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre WPF e WinForms - Desktop .NET
- **Seções principais**: Comparativo, WPF, WinForms, Quando Usar Cada Um
- **Tags**: wpf, winforms, xaml, data-binding, mvvm, desktop, windows
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `wpf-winforms-desktop-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 5 |


# WPF e WinForms - Desktop .NET

## Comparativo

| Aspecto | WPF | WinForms | MAUI |
|---------|-----|----------|------|
| UI Engine | XAML + DirectX | Win32 GDI+ | XAML/Hybrid |
| Plataforma | Windows | Windows | Multi |
| MVVM | Nativo | Manual | Nativo |
| Data Binding | Rico | Simples | Rico |
| Performace | Alta | Média | Alta |
| Moderno | ✅ 2006+ | ⚠️ 2002+ | ✅ 2022+ |

## WPF

### Estrutura
```
MyApp/
├── App.xaml / App.xaml.cs
├── MainWindow.xaml / MainWindow.xaml.cs
├── ViewModels/
│   ├── MainViewModel.cs
│   └── ProductViewModel.cs
├── Views/
│   ├── ProductView.xaml
│   └── ProductView.xaml.cs
├── Models/
│   └── Product.cs
├── Services/
│   └── ProductService.cs
└── Converters/
    └── BoolToVisibilityConverter.cs
```

### MVVM Pattern

#### Model
```csharp
public class Product : INotifyPropertyChanged
{
    private string _name = string.Empty;
    private decimal _price;
    
    public int Id { get; set; }
    
    public string Name
    {
        get => _name;
        set
        {
            _name = value;
            OnPropertyChanged();
        }
    }
    
    public decimal Price
    {
        get => _price;
        set
        {
            _price = value;
            OnPropertyChanged();
        }
    }
    
    public event PropertyChangedEventHandler? PropertyChanged;
    
    protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

#### ViewModel (Base)
```csharp
public abstract class ViewModelBase : INotifyPropertyChanged
{
    private bool _isBusy;
    
    public bool IsBusy
    {
        get => _isBusy;
        set
        {
            _isBusy = value;
            OnPropertyChanged();
        }
    }
    
    public event PropertyChangedEventHandler? PropertyChanged;
    
    protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
    
    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value)) return false;
        field = value;
        OnPropertyChanged(propertyName);
        return true;
    }
}
```

#### ViewModel Específica
```csharp
public class MainViewModel : ViewModelBase
{
    private readonly IProductService _service;
    private ObservableCollection<Product> _products = new();
    private Product? _selectedProduct;
    
    public ObservableCollection<Product> Products
    {
        get => _products;
        set => SetProperty(ref _products, value);
    }
    
    public Product? SelectedProduct
    {
        get => _selectedProduct;
        set => SetProperty(ref _selectedProduct, value);
    }
    
    public ICommand LoadCommand { get; }
    public ICommand AddCommand { get; }
    public ICommand DeleteCommand { get; }
    public ICommand SaveCommand { get; }
    
    public MainViewModel(IProductService service)
    {
        _service = service;
        LoadCommand = new AsyncRelayCommand(LoadAsync);
        AddCommand = new RelayCommand(Add);
        DeleteCommand = new AsyncRelayCommand(DeleteAsync, CanDelete);
        SaveCommand = new AsyncRelayCommand(SaveAsync);
    }
    
    private async Task LoadAsync()
    {
        IsBusy = true;
        try
        {
            Products = new ObservableCollection<Product>(await _service.GetAllAsync());
        }
        finally
        {
            IsBusy = false;
        }
    }
    
    private void Add()
    {
        var product = new Product { Name = "New Product", Price = 0 };
        Products.Add(product);
        SelectedProduct = product;
    }
    
    private bool CanDelete() => SelectedProduct != null;
    
    private async Task DeleteAsync()
    {
        if (SelectedProduct == null) return;
        await _service.DeleteAsync(SelectedProduct.Id);
        Products.Remove(SelectedProduct);
    }
    
    private async Task SaveAsync()
    {
        if (SelectedProduct == null) return;
        await _service.UpdateAsync(SelectedProduct);
    }
}
```

### View (XAML)
```xml
<Window x:Class="MyApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Products" Height="450" Width="800">
    
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
            <RowDefinition Height="Auto" />
        </Grid.RowDefinitions>
        
        <!-- Toolbar -->
        <ToolBar Grid.Row="0">
            <Button Content="Load" Command="{Binding LoadCommand}" />
            <Button Content="Add" Command="{Binding AddCommand}" />
            <Button Content="Delete" Command="{Binding DeleteCommand}" />
            <Button Content="Save" Command="{Binding SaveCommand}" />
        </ToolBar>
        
        <!-- DataGrid -->
        <DataGrid Grid.Row="1"
                  ItemsSource="{Binding Products}"
                  SelectedItem="{Binding SelectedProduct}"
                  AutoGenerateColumns="False"
                  IsReadOnly="True">
            <DataGrid.Columns>
                <DataGridTextColumn Header="ID" Binding="{Binding Id}" Width="50" />
                <DataGridTextColumn Header="Name" Binding="{Binding Name}" Width="200" />
                <DataGridTextColumn Header="Price" Binding="{Binding Price, StringFormat=C}" Width="100" />
            </DataGrid.Columns>
        </DataGrid>
        
        <!-- Status Bar -->
        <StatusBar Grid.Row="2">
            <StatusBarItem>
                <TextBlock Text="{Binding Products.Count, StringFormat='Items: {0}'}" />
            </StatusBarItem>
            <StatusBarItem>
                <ProgressBar IsIndeterminate="{Binding IsBusy}" Width="100" />
            </StatusBarItem>
        </StatusBar>
    </Grid>
</Window>
```

### Data Binding
```xml
<!-- One-Way -->
<TextBlock Text="{Binding Name}" />

<!-- Two-Way -->
<TextBox Text="{Binding Name, Mode=TwoWay}" />

<!-- Update Source Trigger -->
<TextBox Text="{Binding Name, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" />

<!-- Converter -->
<TextBlock Text="{Binding Price, Converter={StaticResource PriceConverter}}" />

<!-- Relative Source -->
<TextBlock Text="{Binding DataContext.Title, RelativeSource={RelativeSource AncestorType=Window}}" />

<!-- Multi Binding -->
<TextBlock>
    <TextBlock.Text>
        <MultiBinding StringFormat="{}{0} - {1}">
            <Binding Path="FirstName" />
            <Binding Path="LastName" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

### Commands (CommunityToolkit.Mvvm)
```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string _name = string.Empty;
    
    [ObservableProperty]
    private decimal _price;
    
    [RelayCommand]
    private async Task SaveAsync()
    {
        await _service.SaveAsync(new Product { Name = Name, Price = Price });
    }
    
    [RelayCommand(CanExecute = nameof(CanDelete))]
    private async Task DeleteAsync()
    {
        await _service.DeleteAsync(SelectedProduct.Id);
    }
    
    private bool CanDelete => SelectedProduct != null;
}
```

## WinForms

### Estrutura
```
MyApp/
├── Program.cs
├── MainForm.cs / MainForm.Designer.cs
├── Models/
├── Services/
└── Controls/
```

### Data Binding
```csharp
// Simple Binding
textBox1.DataBindings.Add("Text", product, "Name");

// Complex Binding
dataGridView1.DataSource = products;
dataGridView1.Columns["Id"].Visible = false;
dataGridView1.Columns["Name"].HeaderText = "Product Name";
```

### BackgroundWorker
```csharp
private readonly BackgroundWorker _worker = new();

public MainForm()
{
    InitializeComponent();
    
    _worker.DoWork += Worker_DoWork;
    _worker.RunWorkerCompleted += Worker_RunWorkerCompleted;
    _worker.ProgressChanged += Worker_ProgressChanged;
    _worker.WorkerReportsProgress = true;
}

private void btnLoad_Click(object sender, EventArgs e)
{
    _worker.RunWorkerAsync();
}

private void Worker_DoWork(object? sender, DoWorkEventArgs e)
{
    var worker = (BackgroundWorker)sender!;
    for (int i = 0; i <= 100; i++)
    {
        Thread.Sleep(50);
        worker.ReportProgress(i);
    }
    e.Result = _service.GetAllAsync().Result;
}

private void Worker_ProgressChanged(object? sender, ProgressChangedEventArgs e)
{
    progressBar1.Value = e.ProgressPercentage;
}

private void Worker_RunWorkerCompleted(object? sender, RunWorkerCompletedEventArgs e)
{
    dataGridView1.DataSource = e.Result;
}
```

## Quando Usar Cada Um

| Cenário | Recomendação |
|---------|-------------|
| App Windows moderna | WPF ou MAUI |
| App Windows legada | WinForms |
| App mobile | MAUI |
| App desktop + mobile | MAUI |
| Dashboard interno | WPF |
| App simples | WinForms |
| App multi-plataforma | MAUI |

## Fontes Oficiais
- docs.microsoft.com/dotnet/desktop/wpf
- docs.microsoft.com/dotnet/desktop/winforms
- learn.microsoft.com/dotnet/communitytoolkit/mvvm
