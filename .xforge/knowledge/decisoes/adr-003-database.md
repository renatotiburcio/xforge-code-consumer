---
id: adr-003
type: database
tags: [PostgreSQL, EF Core, banco-dados, ORM]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-003: PostgreSQL 17 + EF Core 10
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: PostgreSQL, EF Core, banco-dados, ORM
- **Tipo**: database | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-003` |
| Tipo | database |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-003: PostgreSQL 17 + EF Core 10

## Status

Aceito

## Contexto

O sistema requer um banco de dados relacional confiável com suporte avançado a JSON (para documentos fiscais e configurações flexíveis), com bom custo-benefício para operação em nuvem ou on-premise.

## Decisão

Adotar PostgreSQL 17 como banco de dados principal e EF Core 10 como ORM para acesso a dados.

## Consequências

### Positivas
- Open source com licença permissiva e sem custo de licenciamento
- Suporte avançado a JSON/JSONB ideal para documentos eletrônicos (NFe, CFe)
- Excelente ecossistema e comunidade ativa
- Funcionalidades avançadas: particionamento, full-text search, replication
- EF Core 10 com suporte nativo a .NET 10

### Negativas
- Integração menos nativa com Azure comparado ao SQL Server
- Algumas ferramentas Microsoft priorizam SQL Server
- Requer conhecimento específico para administração

## Alternativas Consideradas

- **SQL Server**: Integração nativa Azure, mas custo de licenciamento elevado
- **MySQL**: Alternativa open source, mas com menos funcionalidades avançadas

## ADRs Relacionados

- ADR-002 (Clean Architecture + CQRS)
- ADR-006 (Multi-tenancy com RLS)


