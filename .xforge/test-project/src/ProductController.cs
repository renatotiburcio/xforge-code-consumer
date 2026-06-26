namespace TestProject.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProductController : ControllerBase
{
    private readonly IProductService _productService;

    public ProductController(IProductService productService)
    {
        _productService = productService;
    }

    [HttpGet]
    public ActionResult<List<Product>> GetAll() => Ok(_productService.GetAll());

    [HttpGet("{id}")]
    public ActionResult<Product> GetById(int id)
    {
        var product = _productService.GetById(id);
        return product == null ? NotFound() : Ok(product);
    }

    [HttpPost]
    public ActionResult<Product> Create([FromBody] Product product)
    {
        var created = _productService.Create(product);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    [HttpPut("{id}")]
    public ActionResult<Product> Update(int id, [FromBody] Product product)
    {
        try { return Ok(_productService.Update(id, product)); }
        catch (KeyNotFoundException) { return NotFound(); }
    }

    [HttpDelete("{id}")]
    public ActionResult Delete(int id)
    {
        return _productService.Delete(id) ? NoContent() : NotFound();
    }
}
