# Consolidação — Gerenciamento de Contexto dos 10 Projetos

## Tabela Comparativa

| Projeto | File Referencing | RAG | Compaction | Per-directory |
|---------|------------------|-----|------------|---------------|
| Kilo Code | @file/@folder | Qdrant | ✅ | ❌ |
| Cline | Manual | ❌ | ❌ | ❌ |
| Continue | @file/@folder/@codebase/@docs | SQLite | ❌ | ❌ |
| Goose | MCP resources | ❌ | ❌ | ❌ |
| Roo-Code | Manual | ❌ | ❌ | ❌ |
| Aider | Repo Map | Repo Map | ❌ | ❌ |
| OpenHands | Sandbox output | ❌ | ❌ | ❌ |
| Twinny | Manual | ❌ | ❌ | ❌ |
| MiMo-Code | Manual | ❌ | ❌ | ❌ |
| OpenCode | Manual | ❌ | ❌ | ❌ |

## @context System (Continue)

O sistema mais avançado:
- `@file src/main.ts` — inclui arquivo
- `@folder src/` — inclui pasta
- `@codebase` — inclui estrutura completa
- `@docs` — inclui documentação

## Repo Mapping (Aider)

Indexação automática da estrutura:
- Entende relações entre arquivos
- Gera contexto relevante
- Atualizado a cada mudança

## Oportunidades para o XForge

1. @context system (inspirado em Continue)
2. Per-directory AGENTS.md (inspirado em Kilo Code)
3. Hybrid RAG (K + Aider)