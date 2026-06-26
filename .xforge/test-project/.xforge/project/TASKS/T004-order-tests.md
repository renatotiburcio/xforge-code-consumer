---
id: T004
title: Criar testes unitários OrderService
priority: P0
status: pending
estimated_time: 10min
dependencies: T002
---

# T004: Criar testes unitários OrderService

## Objetivo
Criar testes unitários para OrderService cobrindo todos os métodos CRUD.

## Passos
1. Criar arquivo `tests/OrderServiceTests.cs`
2. Criar testes para: GetById, GetAll, Create, Update, Delete
3. Testar validação de ProductId

## Arquivos
- Criar: `tests/OrderServiceTests.cs`

## Critérios de Aceite
- [ ] Arquivo OrderServiceTests.cs existe
- [ ] Contém 5 testes (1 por método CRUD)
- [ ] Testa validação de ProductId inexistente
- [ ] Testes passam
