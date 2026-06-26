using Xunit;
using TestProject.Services;

namespace TestProject.Tests;

public class OrderServiceTests
{
    [Fact]
    public void Create_ValidOrder_ReturnsWithId()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        var result = orderService.Create(1, 2);
        Assert.True(result.Id > 0);
        Assert.Equal(2, result.Quantity);
    }

    [Fact]
    public void Create_InvalidProductId_Throws()
    {
        var productService = new ProductService();
        var orderService = new OrderService(productService);
        Assert.Throws<KeyNotFoundException>(() => orderService.Create(999, 1));
    }

    [Fact]
    public void Create_ZeroQuantity_Throws()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        Assert.Throws<ArgumentException>(() => orderService.Create(1, 0));
    }

    [Fact]
    public void GetById_ExistingOrder_ReturnsOrder()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        var created = orderService.Create(1, 3);
        var result = orderService.GetById(created.Id);
        Assert.NotNull(result);
        Assert.Equal(3, result.Quantity);
    }

    [Fact]
    public void GetById_NonExisting_ReturnsNull()
    {
        var productService = new ProductService();
        var orderService = new OrderService(productService);
        Assert.Null(orderService.GetById(999));
    }

    [Fact]
    public void Update_ValidQuantity_UpdatesOrder()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        var created = orderService.Create(1, 2);
        var updated = orderService.Update(created.Id, 5);
        Assert.Equal(5, updated.Quantity);
    }

    [Fact]
    public void Delete_ExistingOrder_ReturnsTrue()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        var created = orderService.Create(1, 1);
        Assert.True(orderService.Delete(created.Id));
        Assert.Null(orderService.GetById(created.Id));
    }

    [Fact]
    public void Delete_NonExisting_ReturnsFalse()
    {
        var productService = new ProductService();
        var orderService = new OrderService(productService);
        Assert.False(orderService.Delete(999));
    }

    [Fact]
    public void GetAll_MultipleOrders_ReturnsAll()
    {
        var productService = new ProductService();
        productService.Create(new Product { Name = "P1", Price = 10m, Stock = 100 });
        var orderService = new OrderService(productService);
        orderService.Create(1, 1);
        orderService.Create(1, 2);
        Assert.Equal(2, orderService.GetAll().Count);
    }
}
