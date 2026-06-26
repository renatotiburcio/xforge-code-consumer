---
id: adr-002
type: architecture
tags: [clean-architecture, CQRS, XForge.MediatR, design-patterns]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-002: Arquitetura Limpa + CQRS com XForge.MediatR
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: clean-architecture, CQRS, XForge.MediatR, design-patterns
- **Tipo**: architecture | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-002` |
| Tipo | architecture |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-002: Arquitetura Limpa + CQRS com XForge.MediatR

## Status

Aceito

## Contexto

O ERP possui regras de negócio complexas e múltiplos módulos (financeiro, estoque, vendas, fiscal). Precisamos de uma arquitetura que garanta testabilidade, manutenibilidade e separação clara de responsabilidades.

## Decisão

Adotar Arquitetura Limpa (Clean Architecture) combinada com padrão CQRS (Command Query Responsibility Segregation) utilizando XForge.MediatR para orquestração.

## Consequências

### Positivas
- Separação clara entre regras de negócio e infraestrutura
- Alta testabilidade com injeção de dependências natural
- Commands e Queries isolados facilitam evolução independente
- XForge.MediatR simplifica pipeline de middlewares (validação, logging, cache)

### Negativas
- Mais código boilerplate comparado a abordagens tradicionais
- Curva de aprendizagem para desenvolvedores novos
- Possível over-engineering para casos simples de CRUD

## Alternativas Consideradas

- **Arquitetura em camadas tradicional**: Simples, mas acopla regras de negócio à infraestrutura
- **DDD completo**: Poderoso, mas complexo demais para a maturidade atual do projeto
- **Microserviços**: Escalabilidade independente, mas overhead operacional significativo

## ADRs Relacionados

- ADR-001 (.NET 10 + Blazor)
- ADR-006 (Multi-tenancy)


