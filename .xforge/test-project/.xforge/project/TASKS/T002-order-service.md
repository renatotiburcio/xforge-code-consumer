---
id: T002
title: Criar OrderService com CRUD
priority: P0
status: pending
estimated_time: 10min
dependencies: nenhuma
---

# T002: Criar OrderService com CRUD

## Objetivo
Criar OrderService com operações Create, Read, Update, Delete para a entidade Order.

## Passos
1. Criar arquivo `src/OrderService.cs` com interface IOrderService
2. Implementar métodos: GetById, GetAll, Create, Update, Delete
3. OrderService deve usar ProductRepository para validar ProductId

## Arquivos
- Criar: `src/OrderService.cs`

## Critérios de Aceite
- [ ] Arquivo OrderService.cs existe
- [ ] Contém interface IOrderService
- [ ] Implementa 5 métodos CRUD
- [ ] Valida ProductId ao criar pedido
- [ ] Compila sem erros
