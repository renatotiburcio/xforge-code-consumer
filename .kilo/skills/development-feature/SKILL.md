---
name: development-feature
description: Use when creating new features, endpoints, services, components, or any new functionality in the codebase.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# development-feature

## Objetivo

Criar novas funcionalidades seguindo padrões do projeto.

## Procedimento

### 1. Entender
- Ler requisitos/issue
- Verificar se já existe algo similar
- Identificar módulos afetados

### 2. Planejar
- Arquivos a criar/modificar
- Dependências necessárias
- Testes a escrever
- Estimativa de esforço

### 3. Implementar
- Criar arquivos seguindo Clean Architecture
- Separar: modelo, service, handler, DTO, validação
- Extension methods para Program.cs
- FluentValidation para inputs

### 4. Testar
- Unit tests para lógica de negócio
- Integration tests para endpoints
- Arrange-Act-Assert pattern
- Coverage mínimo 85%

### 5. Documentar
- XML docs em métodos públicos
- Atualizar README se aplicável
- CHANGELOG entry

### 6. Validar
- Rodar quality-gates
- Verificar SOLID/SRP
- Sem preview packages
- XForge.MediatR para CQRS

## Golden Rules

- Um arquivo = uma responsabilidade
- Separação: modelo ≠ service ≠ handler ≠ DTO
- Nunca misturar regra de negócio com persistência
- Program.cs limpo via extensions
- Pacotes sempre versão estável
