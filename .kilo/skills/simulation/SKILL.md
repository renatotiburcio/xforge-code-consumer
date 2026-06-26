---
name: simulation
description: Use before risky refactors, migrations, package updates, breaking changes, architecture changes, or integration changes.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# simulation

## Objetivo

Simular impactos antes de executar mudanças de risco.

## Quando Simular

- Refactor de mais de 10 arquivos
- Atualização de package com breaking changes
- Migração de banco de dados
- Mudança de arquitetura (monolito → modular)
- Alteração de API pública
- Mudança de autenticação/autorização

## Procedimento

### 1. Mapear Impacto
- Quais arquivos são afetados?
- Quais dependências mudam?
- Quais testes precisam de update?

### 2. Simular Cenários
- **Melhor caso**: tudo funciona
- **Pior caso**: quebras em cadeia
- **Caso realista**: issues menores

### 3. Estimar Esforço
- Arquivos a modificar: N
- Testes a atualizar: N
- Tempo estimado: X horas
- Risco: baixo/médio/alto/crítico

### 4. Decidir
- Risco baixo → executar com monitoramento
- Risco médio → criar branch, testar, depois merge
- Risco alto → criar spike/POC primeiro
- Risco crítico → exigir review humano

## Saída

```json
{
  "scenario": "refactor-auth",
  "filesAffected": 15,
  "testsAffected": 8,
  "estimatedHours": 4,
  "riskLevel": "medium",
  "recommendation": "create-branch-and-test",
  "rollbackPlan": "git revert commit-hash"
}
```
