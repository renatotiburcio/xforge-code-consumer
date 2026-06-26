---
id: razor-pages-mvc-completo
type: conhecimento
tags: [razor, mvc, controllers, views, tag-helpers, view-components, filters]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Razor Pages e ASP.NET Core MVC - Guia Completo
- **Seções principais**: Razor Pages vs MVC, Razor Pages, MVC Controllers, Tag Helpers
- **Tags**: razor, mvc, controllers, views, tag-helpers, view-components, filters
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `razor-pages-mvc-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 9 |


# Razor Pages e ASP.NET Core MVC - Guia Completo

## Razor Pages vs MVC

| Aspecto | Razor Pages | MVC |
|---------|-------------|-----|
| Modelo | Page-based | Controller-based |
| URL | /products | /products/index |
| Organização | Pastas por página | Pastas por controller |
| Complexidade | Simples | Média/Alta |
| Ideal para | CRUD simples | APIs + Views complexas |

## Razor Pages

### Estrutura
```
Pages/
├── Products/
│   ├── Index.cshtml          # GET /products
│   ├── Index.cshtml.cs       # PageModel
│   ├── Create.cshtml         # GET /products/create
│   ├── Create.cshtml.cs
│   ├── Edit.cshtml           # GET /products/edit/1
│   ├── Edit.cshtml.cs
│   ├── Delete.cshtml         # GET /products/delete/1
│   ├── Delete.cshtml.cs
│   └── Details.cshtml        # GET /products/details/1
│   └── Details.cshtml.cs
├── Shared/
│   ├── _Layout.cshtml
│   └── _ValidationScriptsPartial.cshtml
├── _ViewImports.cshtml
└── _ViewStart.cshtml
```

### PageModel
```csharp
public class IndexModel : PageModel
{
    private readonly IProductService _service;
    
    public IndexModel(IProductService service)
    {
        _service = service;
    }
    
    public IList<ProductDto> Products { get; set; } = new();
    
    [BindProperty(SupportsGet = true)]
    public string? SearchTerm { get; set; }
    
    public async Task OnGetAsync()
    {
        Products = string.IsNullOrEmpty(SearchTerm)
            ? await _service.GetAllAsync()
            : await _service.SearchAsync(SearchTerm);
    }
    
    public async Task<IActionResult> OnPostDeleteAsync(int id)
    {
        await _service.DeleteAsync(id);
        return RedirectToPage();
    }
}
```

### View
```html
@page
@model Products.IndexModel
@{
    ViewData["Title"] = "Products";
}

<h1>Products</h1>

<form method="get">
    <input type="text" asp-for="SearchTerm" />
    <button type="submit">Search</button>
</form>

<table class="table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        @foreach (var product in Model.Products)
        {
            <tr>
                <td>@product.Name</td>
                <td>@product.Price.ToString("C")</td>
                <td>
                    <a asp-page="./Edit" asp-route-id="@product.Id">Edit</a>
                    <a asp-page="./Details" asp-route-id="@product.Id">Details</a>
                    <form method="post" asp-page-handler="Delete" asp-route-id="@product.Id">
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
        }
    </tbody>
</table>
```

## MVC Controllers

### Controller
```csharp
[Route("api/[controller]")]
[ApiController]
[Authorize]
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;
    
    public ProductsController(IProductService service)
    {
        _service = service;
    }
    
    [HttpGet]
    [AllowAnonymous]
    public async Task<ActionResult<List<ProductDto>>> GetAll()
    {
        return Ok(await _service.GetAllAsync());
    }
    
    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        return product == null ? NotFound() : Ok(product);
    }
    
    [HttpPost]
    public async Task<ActionResult<ProductDto>> Create(CreateProductCommand command)
    {
        var product = await _service.CreateAsync(command);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
    
    [HttpPut("{id:int}")]
    public async Task<IActionResult> Update(int id, UpdateProductCommand command)
    {
        if (id != command.Id) return BadRequest();
        await _service.UpdateAsync(command);
        return NoContent();
    }
    
    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
    {
        await _service.DeleteAsync(id);
        return NoContent();
    }
}
```

## Tag Helpers

```html
<!-- Form -->
<form asp-action="Create" asp-controller="Products" method="post">
    <div asp-validation-summary="ModelOnly"></div>
    <input asp-for="Name" class="form-control" />
    <span asp-validation-for="Name"></span>
    <button type="submit">Save</button>
</form>

<!-- Links -->
<a asp-page="/Products/Edit" asp-route-id="@product.Id">Edit</a>
<a asp-action="Details" asp-route-id="@product.Id">Details</a>

<!-- Images -->
<img src="~/images/@product.ImageUrl" asp-append-version="true" />

<!-- Environment -->
<environment include="Development">
    <script src="~/js/debug.js"></script>
</environment>
<environment exclude="Development">
    <script src="~/js/site.min.js"></script>
</environment>

<!-- Cache -->
<cache expires-after="TimeSpan.FromMinutes(5)">
    @await Html.PartialAsync("_ProductList")
</cache>
```

## View Components

```csharp
public class ProductSummaryViewComponent : ViewComponent
{
    private readonly IProductService _service;
    
    public ProductSummaryViewComponent(IProductService service)
    {
        _service = service;
    }
    
    public async Task<IViewComponentResult> InvokeAsync(int categoryId)
    {
        var products = await _service.GetByCategoryAsync(categoryId);
        return View(products);
    }
}
```

### View
```html
<!-- Views/Shared/Components/ProductSummary/Default.cshtml -->
@model List<ProductDto>

<div class="product-summary">
    <h3>Products (@Model.Count)</h3>
    <ul>
        @foreach (var product in Model)
        {
            <li>@product.Name - @product.Price.ToString("C")</li>
        }
    </ul>
</div>
```

### Usage
```html
@await Component.InvokeAsync("ProductSummary", new { categoryId = 1 })
```

## Filtros

```csharp
// Action Filter
public class LogActionFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var controller = context.Controller;
        var action = context.ActionDescriptor.RouteValues["action"];
        
        Console.WriteLine($"Executing {controller}.{action}");
        
        var resultContext = await next();
        
        Console.WriteLine($"Executed {controller}.{action} - {resultContext.Result}");
    }
}

// Result Filter
public class CacheResultFilter : IAsyncResultFilter
{
    public async Task OnResultExecutionAsync(ResultExecutingContext context, ResultExecutionDelegate next)
    {
        if (context.Result is ViewResult)
        {
            context.HttpContext.Response.Headers.Append("Cache-Control", "public, max-age=300");
        }
        await next();
    }
}

// Registra globalmente
builder.Services.AddControllersWithViews(options =>
{
    options.Filters.Add<LogActionFilter>();
    options.Filters.Add<CacheResultFilter>();
});
```

## Model Binding

```csharp
public class ProductViewModel
{
    [Required]
    [StringLength(200)]
    public string Name { get; set; } = string.Empty;
    
    [Range(0.01, 999999.99)]
    [DataType(DataType.Currency)]
    public decimal Price { get; set; }
    
    [Display(Name = "Category")]
    public int CategoryId { get; set; }
    
    [EmailAddress]
    public string? ContactEmail { get; set; }
    
    [BindProperty]
    public IFormFile? Image { get; set; }
    
    [FromForm]
    public List<string> Tags { get; set; } = new();
}
```

## Validação

```csharp
// FluentValidation
public class ProductValidator : AbstractValidator<ProductViewModel>
{
    public ProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(200).WithMessage("Name too long");
        
        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be positive");
        
        RuleFor(x => x.CategoryId)
            .GreaterThan(0).WithMessage("Category is required");
        
        RuleFor(x => x.ContactEmail)
            .EmailAddress().When(x => !string.IsNullOrEmpty(x.ContactEmail));
    }
}

// Data Annotations
public class Product
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(200, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;
    
    [Range(0.01, double.MaxValue, ErrorMessage = "Price must be positive")]
    public decimal Price { get; set; }
    
    [Required]
    public int CategoryId { get; set; }
}
```

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/razor-pages
- docs.microsoft.com/aspnet/core/mvc
- docs.microsoft.com/aspnet/core/mvc/controllers/actions
