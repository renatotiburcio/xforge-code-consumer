namespace TestProject.Services;

public interface IProductService
{
    Product? GetById(int id);
    List<Product> GetAll();
    Product Create(Product product);
    Product Update(int id, Product product);
    bool Delete(int id);
}

public class ProductService : IProductService
{
    private readonly List<Product> _products = new();
    private int _nextId = 1;

    public Product? GetById(int id) => _products.FirstOrDefault(p => p.Id == id);

    public List<Product> GetAll() => _products.ToList();

    public Product Create(Product product)
    {
        product.Id = _nextId++;
        product.CreatedAt = DateTime.UtcNow;
        _products.Add(product);
        return product;
    }

    public Product Update(int id, Product product)
    {
        var existing = GetById(id) ?? throw new KeyNotFoundException($"Product {id} not found");
        existing.Name = product.Name;
        existing.Price = product.Price;
        existing.Stock = product.Stock;
        return existing;
    }

    public bool Delete(int id)
    {
        var product = GetById(id);
        if (product == null) return false;
        _products.Remove(product);
        return true;
    }
}
