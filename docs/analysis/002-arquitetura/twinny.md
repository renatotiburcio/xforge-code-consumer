# Twinny — Arquitetura

## Visão Geral

Twinny é uma extensão VS Code minimalista com foco em local-first (Ollama) e privacidade.

## Estrutura de Diretórios

```
src/
  extension.ts      # Entry point
  provider.ts       # Provider principal
  context/          # Context assembly
  memory/           # Sistema de memória
  tools/            # Ferramentas
models/             # Modelos LLM
docs/               # Documentação
scripts/            # Scripts
assets/             # Assets
```

## Componentes Principais

| Componente | Arquivo | Responsabilidade |
|------------|---------|------------------|
| TwinnyProvider | `src/extension.ts` | Entry point |
| OllamaClient | `src/provider.ts` | Cliente Ollama local |
| ChatWebview | `src/` | Interface de chat |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| TypeScript | Linguagem |
| VS Code API | Extensão |
| Ollama | Modelos locais |

## Padrões Arquiteturais

1. **Local-first** — Sem cloud, máxima privacidade
2. **Minimalista** — Leve e rápido
3. **Ollama integration** — Modelos locais

## Pontos Fortes

1. Local-first
2. Minimalista
3. Privacidade

## Limitações

1. Sem tools avançadas
2. Sem MCP
3. Sem compactação

## Oportunidades para o XForge

1. Local-first é excelente para privacidade