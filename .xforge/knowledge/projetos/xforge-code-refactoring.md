# XForge Code — Refatoração Kilo Code → VSCode Extension

## Visão Geral
Projeto de refatoração do Kilo Code (monorepo 22 packages) para XForge Code (extensão VSCode focada).

## Análise da Estrutura Atual

### Packages a MANTER (VSCode-compatíveis)
| Package | Path | Motivo |
|---------|------|--------|
| kilo-vscode | src/packages/kilo-vscode | Core da extensão → renomear para xforge-vscode |
| opencode (core) | src/packages/opencode | Orquestração LLM |
| llm | src/packages/llm | Providers de IA |
| ui | src/packages/ui | Componentes compartilhados |
| sdk | src/packages/sdk | SDK público |
| plugin | src/packages/plugin | Sistema de plugins |
| extensions | src/packages/extensions | Extensões VSCode |
| script | src/packages/script | Build scripts |

### Packages a REMOVER
| Package | Path | Motivo |
|---------|------|--------|
| kilo-web-ui | src/packages/kilo-web-ui | Web UI standalone |
| kilo-console | src/packages/kilo-console | Console terminal |
| kilo-jetbrains | src/packages/kilo-jetbrains | Plugin IntelliJ |
| kilo-gateway | src/packages/kilo-gateway | API gateway |
| kilo-sandbox | src/packages/kilo-sandbox | Sandboxing |
| kilo-docs | src/packages/kilo-docs | Docs viewer |
| kilo-indexing | src/packages/kilo-indexing | Code indexing |
| kilo-telemetry | src/packages/kilo-telemetry | Telemetry |
| kilo-i18n | src/packages/kilo-i18n | i18n separado |
| containers | src/packages/containers | Dev containers |
| http-recorder | src/packages/http-recorder | HTTP recording |
| storybook | src/packages/storybook | Dev stories |
| plugin-atomic-chat | src/packages/plugin-atomic-chat | Chat plugin |
| effect-drizzle-sqlite | src/packages/effect-drizzle-sqlite | DB local |

## Logos Disponíveis
- implement/logo/XForge All.png — logo principal
- implement/logo/XForge All.svg — logo vetorial
- implement/logo/XForge-All.icns — ícone macOS

## Decisões Técnicas
1. Foco exclusivo VSCode (D001)
2. Renomeação estruturada Kilo → XForge (D002)
3. Manter SolidJS (D003)
4. Manter Bun + Turbo (D004)
5. System prompt parametrizável (D005)

## Referência VSCode
- Pasta: referencia/vscode/
- Contém: src/vs/workbench/, src/vs/code/, test/, vscode-dts/
- APIs relevantes: vscode.d.ts, contribChat, contribLanguageModel, etc.

## Backlog
- 34 tarefas identificadas (P0: 7, P1: 12, P2: 10, P3: 5)
- Estimativa total: ~55h
- Documentação completa em .xforge/project/

## Status
- Análise: completa
- Implementação: pendente (aguardando aprovação)
