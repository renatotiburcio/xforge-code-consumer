# OpenCode — Arquitetura

## Visão Geral

OpenCode é um CLI/TUI minimalista escrito em TypeScript. É o projeto base que o Kilo Code forkou.

## Estrutura de Diretórios

```
src/
  index.ts          # Entry point
cmd/                # Comandos CLI
internal/           # Lógica interna
scripts/            # Scripts
```

## Componentes Principais

| Componente | Arquivo | Responsabilidade |
|------------|---------|------------------|
| CLI Entry | `src/index.ts` | Entry point |
| TUI | `internal/` | Terminal UI |
| Commands | `cmd/` | Comandos CLI |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| TypeScript | Linguagem |
| Node.js | Runtime |

## Padrões Arquiteturais

1. **Single-binary** — Instalação simples
2. **TUI** — Terminal UI
3. **Minimalista** — Leve e rápido

## Pontos Fortes

1. Single-binary
2. Rápido
3. Minimalista

## Limitações

1. Funcionalidades limitadas
2. Sem MCP
3. Sem compactação

## Oportunidades para o XForge

1. Single-binary é excelente para distribuição