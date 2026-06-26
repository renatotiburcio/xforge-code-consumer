using FluentValidation;

namespace TestProject.Validators;

public class OrderValidator : AbstractValidator<Order>
{
    public OrderValidator()
    {
        RuleFor(o => o.ProductId)
            .GreaterThan(0).WithMessage("ProductId must be valid");

        RuleFor(o => o.Quantity)
            .GreaterThan(0).WithMessage("Quantity must be greater than zero");
    }
}
