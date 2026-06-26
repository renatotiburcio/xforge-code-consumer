# TestProject

Projeto simples para validar o sistema /research + /document-execute.

## Stack
- C# / .NET 8
- FluentValidation
- xUnit

## Estrutura
```
src/
  Product.cs           — Entidade de produto
  Order.cs             — Entidade de pedido
  ProductService.cs    — Service CRUD produto
  OrderService.cs      — Service CRUD pedido
  ProductController.cs — API endpoints produto
  OrderController.cs   — API endpoints pedido
  ProductValidator.cs  — Validação produto
  OrderValidator.cs    — Validação pedido
tests/
  ProductServiceTests.cs — Testes ProductService (9 testes)
  OrderServiceTests.cs   — Testes OrderService (9 testes)
```

## Build e Teste
```bash
dotnet build
dotnet test
```
