# Consolidação — Arquitetura dos 10 Projetos

## Tabela Comparativa

| Projeto | Arquitetura | Monorepo | Entry Point | Linguagem |
|---------|-------------|----------|-------------|-----------|
| Kilo Code | Packages modulares (20+) | Turborepo + Bun | extension.ts / CLI | TypeScript |
| Cline | Shared core + produtos | npm workspaces | extension.ts / CLI | TypeScript |
| Continue | Packages modulares (15+) | pnpm workspaces | extension.ts / CLI | TypeScript |
| Goose | Rust Crates (6+) | Cargo workspace | main.rs (CLI/Server) | Rust |
| Roo-Code | Apps/packages/src | pnpm workspaces | extension.ts | TypeScript |
| Aider | Single package | — | main.py | Python |
| OpenHands | Modular (microservices) | — | main.py | Python |
| Twinny | Simple src/ | npm workspaces | extension.ts | TypeScript |
| MiMo-Code | Packages/sdks | npm workspaces | extension.ts | TypeScript |
| OpenCode | Simple cmd/internal | npm workspaces | index.ts | TypeScript |

## Padrões Arquiteturais Comuns

1. **Shared Core** — Kilo Code, Cline, Continue compartilham
2. **Monorepo** — 8 de 10 usam monorepo
3. **VS Code Extension** — 7 de 10 são extensões
4. **CLI + Extension** — 6 de 10 oferecem CLI e extensão

## Padrões Divergentes

1. **Rust** — Apenas Goose
2. **Python** — Aider e OpenHands
3. **Desktop App** — Apenas Goose (Electron)
4. **Web App** — Apenas OpenHands (React)
5. **MCP-first** — Apenas Goose

## Estruturas de Diretórios

| Projeto | Estrutura Principal |
|---------|---------------------|
| Kilo Code | `packages/` (20+ packages) |
| Cline | `apps/`, `sdk/`, `src/` |
| Continue | `packages/` (15+ packages) |
| Goose | `crates/` (6+ crates) |
| Roo-Code | `apps/`, `packages/`, `src/` |
| Aider | `aider/` (single package) |
| OpenHands | `openhands/`, `frontend/` |
| Twinny | `src/` (simple) |
| MiMo-Code | `packages/`, `sdks/` |
| OpenCode | `cmd/`, `internal/` |

## Dependências Principais

| Dependência | Projetos |
|-------------|----------|
| TypeScript | 8 de 10 |
| React (UI) | Kilo Code, Cline, Continue, Goose, Roo-Code |
| MCP SDK | Kilo Code, Cline, Goose, Roo-Code |
| Docker | OpenHands |
| Electron | Goose |

## Oportunidades para o XForge

1. Monorepo bem organizado (inspirado em Kilo Code)
2. Shared core (inspirado em Cline/Continue)
3. Rust performance (inspirado em Goose)
4. Desktop + CLI + Extension (inspirado em Goose)