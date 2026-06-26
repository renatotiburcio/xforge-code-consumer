---
id: T001
title: Criar ProductService com CRUD
priority: P0
status: pending
estimated_time: 10min
dependencies: nenhuma
---

# T001: Criar ProductService com CRUD

## Objetivo
Criar ProductService com operações Create, Read, Update, Delete para a entidade Product.

## Passos
1. Criar arquivo `src/ProductService.cs` com interface IProductService
2. Implementar métodos: GetById, GetAll, Create, Update, Delete
3. Usar padrão Repository (mock, sem banco real)

## Arquivos
- Criar: `src/ProductService.cs`

## Critérios de Aceite
- [ ] Arquivo ProductService.cs existe
- [ ] Contém interface IProductService
- [ ] Implementa 5 métodos CRUD
- [ ] Compila sem erros (dotnet build)
