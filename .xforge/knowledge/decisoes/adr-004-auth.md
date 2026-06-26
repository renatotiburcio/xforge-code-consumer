---
id: adr-004
type: auth
tags: [JWT, autenticação, autorização, segurança]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-004: JWT + Refresh Tokens + Autorização por Papéis
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: JWT, autenticação, autorização, segurança
- **Tipo**: auth | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-004` |
| Tipo | auth |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-004: JWT + Refresh Tokens + Autorização por Papéis

## Status

Aceito

## Contexto

O ERP terá múltiplas aplicações Blazor (Server e WASM) consumindo APIs. Precisamos de um mecanismo de autenticação seguro, escalável e compatível com o ecossistema .NET.

## Decisão

Implementar autenticação via JWT (JSON Web Tokens) com refresh tokens e autorização baseada em papéis (RBAC - Role-Based Access Control).

## Consequências

### Positivas
- Stateless: facilita escalabilidade horizontal
- Suporte nativo no ecossistema .NET (System.IdentityModel)
- Tokens JWT contêm claims para autorização granular
- Refresh tokens permitem sessões longas sem comprometer segurança

### Negativas
- Complexidade no gerenciamento de tokens (rotação, invalidação)
- Tokens JWT não podem ser facilmente revogados (mitigar com blacklist)
- WASM requer tratamento seguro do storage de tokens

## Alternativas Consideradas

- **Autenticação por sessão**: Estado no servidor dificulta escalabilidade
- **IdentityServer/Duende**: Solução completa, mas com overhead e custo de licenciamento
- **Azure AD B2C**: Ideal para login social/SaaS, mas adiciona dependência externa

## ADRs Relacionados

- ADR-005 (Blazor híbrido)
- ADR-001 (.NET 10 + Blazor)


