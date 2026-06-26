---
id: T007
title: Criar validações FluentValidation
priority: P1
status: pending
estimated_time: 10min
dependencies: T001, T002
---

# T007: Criar validações FluentValidation

## Objetivo
Criar validadores para Product e Order.

## Passos
1. Criar `src/ProductValidator.cs`
2. Criar `src/OrderValidator.cs`
3. Validar: Nome obrigatório, Preço > 0, Quantidade > 0

## Arquivos
- Criar: `src/ProductValidator.cs`
- Criar: `src/OrderValidator.cs`

## Critérios de Aceite
- [ ] 2 arquivos de validação criados
- [ ] Product: Nome não vazio, Price > 0
- [ ] Order: Quantity > 0, ProductId válido
