namespace TestProject.Models;

public class Order
{
    public int Id { get; set; }
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal Total => Product?.Price * Quantity ?? 0;
    public DateTime OrderDate { get; set; } = DateTime.UtcNow;
    public Product? Product { get; set; }
}
