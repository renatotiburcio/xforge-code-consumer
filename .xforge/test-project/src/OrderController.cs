namespace TestProject.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrderController(IOrderService orderService)
    {
        _orderService = orderService;
    }

    [HttpGet]
    public ActionResult<List<Order>> GetAll() => Ok(_orderService.GetAll());

    [HttpGet("{id}")]
    public ActionResult<Order> GetById(int id)
    {
        var order = _orderService.GetById(id);
        return order == null ? NotFound() : Ok(order);
    }

    [HttpPost]
    public ActionResult<Order> Create([FromBody] CreateOrderRequest request)
    {
        try { return Ok(_orderService.Create(request.ProductId, request.Quantity)); }
        catch (KeyNotFoundException) { return BadRequest("Product not found"); }
        catch (ArgumentException e) { return BadRequest(e.Message); }
    }

    [HttpPut("{id}")]
    public ActionResult<Order> Update(int id, [FromBody] UpdateOrderRequest request)
    {
        try { return Ok(_orderService.Update(id, request.Quantity)); }
        catch (KeyNotFoundException) { return NotFound(); }
        catch (ArgumentException e) { return BadRequest(e.Message); }
    }

    [HttpDelete("{id}")]
    public ActionResult Delete(int id)
    {
        return _orderService.Delete(id) ? NoContent() : NotFound();
    }
}

public record CreateOrderRequest(int ProductId, int Quantity);
public record UpdateOrderRequest(int Quantity);
