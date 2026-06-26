---
id: adr-005
type: frontend
tags: [Blazor, WASM, Server, híbrido, UI]
owner:  Core
version: "1.0"
updated: 2026-06-09
status: accepted
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ADR-005: Blazor Híbrido (Server + WASM)
- **Seções principais**: Status, Contexto, Decisão, Consequências
- **Tags**: Blazor, WASM, Server, híbrido, UI
- **Tipo**: frontend | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `adr-005` |
| Tipo | frontend |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | Core |
| Total de seções | 6 |


# ADR-005: Blazor Híbrido (Server + WASM)

## Status

Aceito

## Contexto

O ERP requer tanto experiências em tempo real (dashboards, notificações) quanto capacidade offline (operações em campo). A equipe possui expertise em C# e buscamos máxima reutilização de código.

## Decisão

Utilizar Blazor de forma híbrida: Blazor Server para módulos que exigem tempo real e Blazor WASM para funcionalidades offline-capazes.

## Consequências

### Positivas
- Reutilização de código C# entre Server e WASM via Shared Library
- SignalR nativo no Blazor Server para atualizações em tempo real
- WASM oferece experiência offline sem dependência de conexão
- Uma única equipe de desenvolvimento com C#

### Negativas
- Payload inicial WASM maior que SPA tradicionais
- Latência perceptível na primeira carga do WASM
- Complexidade de gerenciar dois modos de renderização

## Alternativas Consideradas

- **React**: Comunidade grande, mas exige TypeScript/JavaScript adicional
- **Angular**: Framework maduro, mas curva de aprendizagem separada
- **Vue.js**: Leve e produtivo, mas fora do ecossistema C#

## ADRs Relacionados

- ADR-001 (.NET 10 + Blazor)
- ADR-004 (JWT + Auth)


