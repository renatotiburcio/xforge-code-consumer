using Xunit;
using TestProject.Services;

namespace TestProject.Tests;

public class ProductServiceTests
{
    [Fact]
    public void GetById_ExistingProduct_ReturnsProduct()
    {
        var service = new ProductService();
        var created = service.Create(new Product { Name = "Test", Price = 10m, Stock = 5 });
        var result = service.GetById(created.Id);
        Assert.NotNull(result);
        Assert.Equal("Test", result.Name);
    }

    [Fact]
    public void GetById_NonExistingProduct_ReturnsNull()
    {
        var service = new ProductService();
        var result = service.GetById(999);
        Assert.Null(result);
    }

    [Fact]
    public void GetAll_Empty_ReturnsEmptyList()
    {
        var service = new ProductService();
        var result = service.GetAll();
        Assert.Empty(result);
    }

    [Fact]
    public void GetAll_WithProducts_ReturnsAll()
    {
        var service = new ProductService();
        service.Create(new Product { Name = "A", Price = 1m, Stock = 1 });
        service.Create(new Product { Name = "B", Price = 2m, Stock = 2 });
        var result = service.GetAll();
        Assert.Equal(2, result.Count);
    }

    [Fact]
    public void Create_Product_ReturnsWithId()
    {
        var service = new ProductService();
        var result = service.Create(new Product { Name = "New", Price = 5m, Stock = 10 });
        Assert.True(result.Id > 0);
        Assert.Equal("New", result.Name);
    }

    [Fact]
    public void Update_ExistingProduct_UpdatesFields()
    {
        var service = new ProductService();
        var created = service.Create(new Product { Name = "Old", Price = 1m, Stock = 1 });
        var updated = service.Update(created.Id, new Product { Name = "New", Price = 99m, Stock = 50 });
        Assert.Equal("New", updated.Name);
        Assert.Equal(99m, updated.Price);
    }

    [Fact]
    public void Update_NonExistingProduct_Throws()
    {
        var service = new ProductService();
        Assert.Throws<KeyNotFoundException>(() => service.Update(999, new Product()));
    }

    [Fact]
    public void Delete_ExistingProduct_ReturnsTrue()
    {
        var service = new ProductService();
        var created = service.Create(new Product { Name = "Del", Price = 1m, Stock = 1 });
        var result = service.Delete(created.Id);
        Assert.True(result);
        Assert.Null(service.GetById(created.Id));
    }

    [Fact]
    public void Delete_NonExistingProduct_ReturnsFalse()
    {
        var service = new ProductService();
        var result = service.Delete(999);
        Assert.False(result);
    }
}
