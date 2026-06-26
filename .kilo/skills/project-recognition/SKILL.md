---
name: project-recognition
description: Use when the user asks to analyze, recognize, map, reverse engineer, or learn an existing or new project before making changes.
metadata:
  version: "7.1.0"
  xforge-category: "enterprise-engineer"
---

# project-recognition

## Objetivo

Reconhecer completamente um projeto antes de fazer qualquer alteração.

## Procedimento

### 1. Estrutura
- Listar diretórios e arquivos principais
- **DR-0180**: rodar `.xforge/scripts/purify.ps1 -WhatIf -ProjectRoot <path>` para detectar stack do projeto ativo
- Identificar framework/language/patterns
- Mapear dependências (package.json, .csproj, etc.)

### 2. Código
- Identificar arquitetura (Clean, MVC, etc.)
- Mapear camadas (domain, infrastructure, API)
- Verificar padrões de naming
- Identificar testes existentes

### 3. Banco
- Identificar ORM (EF Core, Dapper, etc.)
- Mapear entidades/models
- Verificar migrations
- Identificar connection strings

### 4. Infra
- Verificar Docker/docker-compose
- CI/CD pipelines
- Environment configs
- Deploy strategy

### 5. Documentação
- README existente
- API docs (Swagger/OpenAPI)
- Decisões registradas (ADR)
- Knowledge existente

### 6. Saída
- Criar PROJECT-DNA em .xforge/project-dna/
- Atualizar memory intelligence
- Atualizar knowledge graph
- Criar backlog inicial

## Output

```json
{
  "project": "nome",
  "language": "stack-agnostic (detectado via purify.ps1)",
  "architecture": "Clean Architecture",
  "database": "stack-specific",
  "tests": "stack-specific",
  "status": "recognized",
  "recommendations": []
}
```