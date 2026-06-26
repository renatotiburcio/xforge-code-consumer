---
id: adr-001
type: tech-stack
tags: [.NET, Blazor, stack,-frontend, backend]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-001: .NET 10 + Blazor como Stack Principal
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: .NET, Blazor, stack,-frontend, backend
- **Tipo**: tech-stack | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-001` |
| Tipo | tech-stack |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-001: .NET 10 + Blazor como Stack Principal

## Status

Aceito

## Contexto

Estamos desenvolvendo um sistema ERP brasileiro que requer robustez, manutenibilidade e produtividade. A equipe possui experiência consolidada em C# e o ecossistema Microsoft oferece ferramentas integradas para o domínio do problema.

## Decisão

Adotar .NET 10 e Blazor como stack principal de desenvolvimento, unificando frontend e backend em uma única linguagem.

## Consequências

### Positivas
- Única linguagem (C#) em toda a pilha de desenvolvimento
- Ecossistema rico com bibliotecas maduras para domínio corporativo
- Produtividade elevada graças à experiência existente da equipe
- Integração nativa com Azure e ferramentas Microsoft

### Negativas
- Comunidade frontend menor comparada a React/Angular
- Menor número de componentes UI prontos no ecossistema
- Dependência em maior grau do ecossistema Microsoft

## Alternativas Consideradas

- **React + API**: Comunidade grande, mas exigiria divisão de conhecimento entre TypeScript e C#
- **Angular + API**: Framework maduro, porém com curva de aprendizagem adicional
- **Java/Spring**: Ecossistema robusto, mas sem aproveitamento da expertise atual

## ADRs Relacionados

- ADR-002 (Arquitetura Clean + CQRS)
- ADR-005 (Blazor híbrido)


