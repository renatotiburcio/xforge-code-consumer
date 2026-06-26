namespace TestProject.Services;

public interface IOrderService
{
    Order? GetById(int id);
    List<Order> GetAll();
    Order Create(int productId, int quantity);
    Order Update(int id, int quantity);
    bool Delete(int id);
}

public class OrderService : IOrderService
{
    private readonly IProductService _productService;
    private readonly List<Order> _orders = new();
    private int _nextId = 1;

    public OrderService(IProductService productService)
    {
        _productService = productService;
    }

    public Order? GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);

    public List<Order> GetAll() => _orders.ToList();

    public Order Create(int productId, int quantity)
    {
        var product = _productService.GetById(productId)
            ?? throw new KeyNotFoundException($"Product {productId} not found");

        if (quantity <= 0)
            throw new ArgumentException("Quantity must be greater than zero");

        var order = new Order
        {
            Id = _nextId++,
            ProductId = productId,
            Quantity = quantity,
            Product = product,
            OrderDate = DateTime.UtcNow
        };
        _orders.Add(order);
        return order;
    }

    public Order Update(int id, int quantity)
    {
        var existing = GetById(id) ?? throw new KeyNotFoundException($"Order {id} not found");
        if (quantity <= 0)
            throw new ArgumentException("Quantity must be greater than zero");
        existing.Quantity = quantity;
        return existing;
    }

    public bool Delete(int id)
    {
        var order = GetById(id);
        if (order == null) return false;
        _orders.Remove(order);
        return true;
    }
}
