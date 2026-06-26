---
id: T003
title: Criar testes unitários ProductService
priority: P0
status: pending
estimated_time: 10min
dependencies: T001
---

# T003: Criar testes unitários ProductService

## Objetivo
Criar testes unitários para ProductService cobrindo todos os métodos CRUD.

## Passos
1. Criar arquivo `tests/ProductServiceTests.cs`
2. Criar testes para: GetById, GetAll, Create, Update, Delete
3. Cada teste deve ser independente

## Arquivos
- Criar: `tests/ProductServiceTests.cs`

## Critérios de Aceite
- [ ] Arquivo ProductServiceTests.cs existe
- [ ] Contém 5 testes (1 por método CRUD)
- [ ] Usa xUnit e Assert
- [ ] Testes passam (dotnet test)
