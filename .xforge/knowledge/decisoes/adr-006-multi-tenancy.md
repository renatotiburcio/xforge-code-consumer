---
id: adr-006
type: multi-tenancy
tags: [multi-tenant, SaaS, PostgreSQL, RLS, isolamento]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-006: Banco Compartilhado com Discriminador + RLS
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: multi-tenant, SaaS, PostgreSQL, RLS, isolamento
- **Tipo**: multi-tenancy | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-006` |
| Tipo | multi-tenancy |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-006: Banco Compartilhado com Discriminador + RLS

## Status

Aceito

## Contexto

O ERP será oferecido como SaaS com múltiplos clientes (tenants). Precisamos garantir isolamento de dados eficiente com custo operacional controlado para centenas de tenants.

## Decisão

Adotar banco de dados compartilhado com coluna discriminadora (TenantId) combinado com Row Level Security (RLS) do PostgreSQL para isolamento automático.

## Consequências

### Positivas
- Custo operacional menor: um único banco para todos os tenants
- RLS do PostgreSQL garante isolamento mesmo com bugs na aplicação
- Simplifica backup e manutenção
- Escalável para centenas de tenants com recursos adequados

### Negativas
- Requer filtragem cuidadosa em todas as queries (mitigar com RLS)
- Performance pode degradar sem tuning adequado com muitos tenants
- Incidente pode afetar todos os tenants simultaneamente

## Alternativas Consideradas

- **Database-per-tenant**: Isolamento máximo, mas custo operacional inviável em escala
- **Schema-per-tenant**: Meio-termo entre isolamento e custo, porém complexo de gerenciar

## ADRs Relacionados

- ADR-003 (PostgreSQL 17 + EF Core)
- ADR-002 (Clean Architecture + CQRS)


