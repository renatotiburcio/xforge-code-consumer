---
id: validacao
type: pattern
tags: [validation, fluentvalidation, blazor, cpf, cnpj, erp, input]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Validação com FluentValidation
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: validation, fluentvalidation, blazor, cpf, cnpj, erp, input
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `validacao` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Validação com FluentValidation

## Propósito

Padronizar a validação de entidades de negócio em sistemas ERP usando FluentValidation, com suporte a validação assíncrona, cross-field, integração com Blazor e mensagens em português.

## Descrição do Padrão

### Validator Básico

```csharp
public class ClienteValidator : AbstractValidator<Cliente>
{
    public ClienteValidator()
    {
        RuleFor(x => x.Nome)
            .NotEmpty().WithMessage("O nome é obrigatório")
            .MinimumLength(2).WithMessage("O nome deve ter pelo menos 2 caracteres")
            .MaximumLength(150).WithMessage("O nome deve ter no máximo 150 caracteres");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("O e-mail é obrigatório")
            .EmailAddress().WithMessage("E-mail inválido");

        RuleFor(x => x.CpfCnpj)
            .NotEmpty().WithMessage("CPF/CNPJ é obrigatório")
            .Must(CpfCnpjValido).WithMessage("CPF ou CNPJ inválido");

        RuleFor(x => x.Cep)
            .NotEmpty().WithMessage("CEP é obrigatório")
            .Matches(@"^\d{5}-?\d{3}$").WithMessage("CEP inválido");

        RuleFor(x => x.DataCadastro)
            .LessThanOrEqualTo(DateTime.Now).WithMessage("Data de cadastro não pode ser futura");
    }

    private static bool CpfCnpjValido(string? cpfCnpj)
    {
        if (string.IsNullOrWhiteSpace(cpfCnpj)) return false;
        var digitos = new string(cpfCnpj.Where(char.IsDigit).ToArray());
        return digitos.Length == 11 ? ValidarCpf(digitos) : ValidarCnpj(digitos);
    }
}
```

### Validação Assínciona (Banco de Dados)

```csharp
public class ProdutoValidator : AbstractValidator<Produto>
{
    public ProdutoValidator(IProdutoRepositorio repositorio)
    {
        RuleFor(x => x.CodigoBarras)
            .MustAsync(async (prod, code, ct) =>
            {
                var existente = await repositorio.ObterPorCodigoBarrasAsync(code, ct);
                return existente is null || existente.Id == prod.Id;
            })
            .WithMessage("Código de barras já cadastrado");
    }
}
```

### Validação Cross-Field

```csharp
RuleFor(x => x.PrecoVenda)
    .GreaterThan(x => x.PrecoCusto)
    .WithMessage("Preço de venda deve ser maior que o preço de custo");

RuleFor(x => x.DataSaida)
    .GreaterThanOrEqualTo(x => x.DataEmissao)
    .WithMessage("Data de saída deve ser posterior à emissão")
    .When(x => x.DataSaida.HasValue);
```

### Validação em Cascata

```csharp
RuleFor(x => x.Cliente)
    .SetValidator(new ClienteValidator())
    .NotNull().WithMessage("Cliente obrigatório");

RuleForEach(x => x.Itens)
    .SetValidator(new ItemPedidoValidator())
    .NotEmpty().WithMessage("Item obrigatório");
```

### Integração com ASP.NET Core

```csharp
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddFluentValidationClientsideAdapters();
builder.Services.AddValidatorsFromAssemblyContaining<Program>();
```

### Integração com Blazor

```csharp
builder.Services.AddScoped<IValidator<Cliente>, ClienteValidator>();
```

```razor
<EditForm Model="@_cliente" OnValidSubmit="SalvarAsync">
    <FluentValidationValidator @ref="_validator" />
    <ValidationSummary />

    <MudTextField @bind-Value="_cliente.Nome"
                  For="@(() => _cliente.Nome)" />
</EditForm>
```

### Mensagens em Portuguese

Todas as mensagens usam `.WithMessage()` com texto em português:
- `"O nome é obrigatório"` em vez de `"Nome é obrigatório"`
- `"CPF/CNPJ inválido"` em vez de `"Invalid CPF/CNPJ"`

## Quando Usar

- Validação de entidades de negócio (Cliente, Produto, Pedido, NotaFiscal).
- Validação assíncrona que consulta banco (unicidade de código).
- Cross-field validation (datas, preços, ranges).
- Formulários Blazor com feedback imediato.

## Exemplo de Uso

```csharp
[HttpPost]
public async Task<IActionResult> CriarAsync(Cliente cliente, CancellationToken ct)
{
    var result = await _validator.ValidateAsync(cliente, ct);
    if (!result.IsValid)
    {
        var erros = result.Errors.GroupBy(e => e.PropertyName)
            .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
        return BadRequest(new { Mensagem = "Erros de validação", Erros = erros });
    }
    await _repositorio.AdicionarAsync(cliente, ct);
    return CreatedAtAction(nameof(ObterPorId), new { id = cliente.Id }, cliente);
}
```

## Padrões Relacionados

- [[componentes-blazor.md]] — integração com formulários Blazor
- [[testes]] — teste de validators com xUnit + FluentAssertions
- [[seguranca-api.md]] — validação de entrada como camada de segurança

