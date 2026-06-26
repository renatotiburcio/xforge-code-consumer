---
id: fluentvalidation-completo
type: conhecimento
tags: [fluentvalidation, validacao, rules, validators, custom, async, inheritance]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre FluentValidation - Validação Completa
- **Seções principais**: Conceito, Setup, Validator Básico, Regras Comuns
- **Tags**: fluentvalidation, validacao, rules, validators, custom, async, inheritance
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fluentvalidation-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# FluentValidation - Validação Completa

## Conceito

FluentValidation é uma biblioteca para criação de regras de validação fluent e tipadas em .NET.

## Setup

```csharp
// Program.cs
builder.Services.AddValidatorsFromAssemblyContaining<ProductValidator>();
// ou
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);
```

## Validator Básico

```csharp
public class ProductValidator : AbstractValidator<Product>
{
    public ProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Nome é obrigatório")
            .MaximumLength(200).WithMessage("Nome muito longo")
            .MinimumLength(2).WithMessage("Nome muito curto");
        
        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Preço deve ser positivo")
            .LessThan(1_000_000).WithMessage("Preço muito alto");
        
        RuleFor(x => x.CategoryId)
            .GreaterThan(0).WithMessage("Categoria é obrigatória");
        
        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("Descrição muito longa")
            .When(x => !string.IsNullOrEmpty(x.Description));
    }
}
```

## Regras Comuns

```csharp
// String
RuleFor(x => x.Name).NotEmpty();
RuleFor(x => x.Name).Length(2, 200);
RuleFor(x => x.Name).MinimumLength(2);
RuleFor(x => x.Name).MaximumLength(200);
RuleFor(x => x.Email).EmailAddress();
RuleFor(x => x.Url).Must(BeAValidUrl);
RuleFor(x => x.Phone).Matches(@"^\+?[1-9]\d{1,14}$");
RuleFor(x => x.CPF).CPF(); // Extensão customizada
RuleFor(x => x.CNPJ).CNPJ();

// Numérico
RuleFor(x => x.Price).GreaterThan(0);
RuleFor(x => x.Price).GreaterThanOrEqualTo(0);
RuleFor(x => x.Price).LessThan(1000000);
RuleFor(x => x.Quantity).InclusiveBetween(1, 1000);
RuleFor(x => x.Rating).InclusiveBetween(1, 5);

// Data
RuleFor(x => x.StartDate).LessThan(x => x.EndDate);
RuleFor(x => x.BirthDate).LessThan(DateTime.Today);
RuleFor(x => x.ExpiryDate).GreaterThan(DateTime.Today);

// Coleção
RuleFor(x => x.Items).NotEmpty().WithMessage("Adicione pelo menos 1 item");
RuleFor(x => x.Items).Must(list => list.Count <= 100);
RuleForEach(x => x.Items).SetValidator(new OrderItemValidator());

// Condicional
RuleFor(x => x.Discount).GreaterThan(0)
    .When(x => x.HasDiscount);

RuleFor(x => x.CouponCode).NotEmpty()
    .When(x => x.CouponApplied);

// Nilable
RuleFor(x => x.NullableField).NotNull()
    .When(x => x.IsNotNullRequired);
```

## Validadores Aninhados

```csharp
public class AddressValidator : AbstractValidator<Address>
{
    public AddressValidator()
    {
        RuleFor(x => x.Street).NotEmpty();
        RuleFor(x => x.City).NotEmpty();
        RuleFor(x => x.State).NotEmpty().Length(2);
        RuleFor(x => x.ZipCode).Matches(@"^\d{5}-?\d{3}$");
    }
}

public class CustomerValidator : AbstractValidator<Customer>
{
    public CustomerValidator()
    {
        RuleFor(x => x.Name).NotEmpty();
        RuleFor(x => x.Address).SetValidator(new AddressValidator());
        RuleForEach(x => x.Addresses).SetValidator(new AddressValidator());
    }
}
```

## Validação Asíncrona

```csharp
public class UserValidator : AbstractValidator<User>
{
    private readonly IUserRepository _repository;
    
    public UserValidator(IUserRepository repository)
    {
        _repository = repository;
        
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MustAsync(async (email, ct) => 
                !await _repository.EmailExistsAsync(email))
            .WithMessage("Email já está em uso");
        
        RuleFor(x => x.Username)
            .NotEmpty()
            .MustAsync(async (username, ct) => 
                !await _repository.UsernameExistsAsync(username))
            .WithMessage("Username já está em uso");
    }
}
```

## Custom Validators

```csharp
// CPF
public static class CpfValidatorExtensions
{
    public static IRuleBuilderOptions<T, string> CPF<T>(this IRuleBuilder<T, string> ruleBuilder)
    {
        return ruleBuilder.Must(cpf =>
        {
            cpf = new string(cpf.Where(char.IsDigit).ToArray());
            if (cpf.Length != 11) return false;
            if (cpf.All(c => c == cpf[0])) return false;
            
            var mult1 = new[] { 10, 9, 8, 7, 6, 5, 4, 3, 2 };
            var mult2 = new[] { 11, 10, 9, 8, 7, 6, 5, 4, 3, 2 };
            
            var sum = 0;
            for (int i = 0; i < 9; i++)
                sum += (cpf[i] - '0') * mult1[i];
            
            var rest = sum % 11;
            if (rest < 2) rest = 0; else rest = 11 - rest;
            if ((cpf[9] - '0') != rest) return false;
            
            sum = 0;
            for (int i = 0; i < 10; i++)
                sum += (cpf[i] - '0') * mult2[i];
            
            rest = sum % 11;
            if (rest < 2) rest = 0; else rest = 11 - rest;
            return (cpf[10] - '0') == rest;
        }).WithMessage("CPF inválido");
    }
}

// CNPJ
public static class CnpjValidatorExtensions
{
    public static IRuleBuilderOptions<T, string> CNPJ<T>(this IRuleBuilder<T, string> ruleBuilder)
    {
        return ruleBuilder.Must(cnpj =>
        {
            cnpj = new string(cnpj.Where(char.IsDigit).ToArray());
            if (cnpj.Length != 14) return false;
            if (cnpj.All(c => c == cnpj[0])) return false;
            
            var mult1 = new[] { 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 };
            var mult2 = new[] { 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 };
            
            var sum = 0;
            for (int i = 0; i < 12; i++)
                sum += (cnpj[i] - '0') * mult1[i];
            
            var rest = sum % 11;
            if (rest < 2) rest = 0; else rest = 11 - rest;
            if ((cnpj[12] - '0') != rest) return false;
            
            sum = 0;
            for (int i = 0; i < 13; i++)
                sum += (cnpj[i] - '0') * mult2[i];
            
            rest = sum % 11;
            if (rest < 2) rest = 0; else rest = 11 - rest;
            return (cnpj[13] - '0') == rest;
        }).WithMessage("CNPJ inválido");
    }
}
```

## Herança de Validators

```csharp
public abstract class EntityValidator<T> : AbstractValidator<T> where T : Entity
{
    protected EntityValidator()
    {
        RuleFor(x => x.Id).GreaterThan(0);
    }
}

public class ProductValidator : EntityValidator<Product>
{
    public ProductValidator()
    {
        RuleFor(x => x.Name).NotEmpty();
        RuleFor(x => x.Price).GreaterThan(0);
    }
}
```

## ValidationResult

```csharp
var validator = new ProductValidator();
var result = validator.Validate(product);

if (!result.IsValid)
{
    var errors = result.Errors.Select(e => new
    {
        Field = e.PropertyName,
        Message = e.ErrorMessage
    });
    
    return BadRequest(errors);
}
```

## Integração com ASP.NET Core

```csharp
// Auto validação via FluentValidation.AspNetCore
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddFluentValidationClientsideAdapters();

// Validação manual
[HttpPost]
public async Task<IActionResult> Create(CreateProductCommand command)
{
    var validator = new CreateProductValidator();
    var result = await validator.ValidateAsync(command);
    
    if (!result.IsValid)
        return ValidationProblem(result.ToDictionary());
    
    var product = await _mediator.Send(command);
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}
```

## Mensagens Customizadas

```csharp
RuleFor(x => x.Email)
    .NotEmpty().WithMessage("Email é obrigatório")
    .EmailAddress().WithMessage("Formato de email inválido")
    .MustAsync(async (email, ct) => !await _repo.EmailExistsAsync(email))
    .WithMessage("Email já está cadastrado")
    .WithErrorCode("DUPLICATE_EMAIL");
```

## Fontes Oficiais
- docs.fluentvalidation.net
- github.com/FluentValidation/FluentValidation
