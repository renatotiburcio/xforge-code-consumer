# Continue — Gerenciamento de Contexto

## Arquitetura

O Continue tem o sistema de contexto mais avançado:

```mermaid
flowchart TD
    EP[Entry Point] --> CA[Context Provider]
    CA -->|resolve| REF[Reference Resolver]
    REF -->|@file| FILE[File Content]
    REF -->|@folder| FOLDER[Folder Files]
    REF -->|@codebase| IDX[Semantic Index\nSQLite]
    REF -->|@docs| DOCS[Documentation]
    CA -->|monta| PROMPT[Prompt]
```

## Componentes

| Componente | Package | Responsabilidade |
|------------|---------|------------------|
| ContextProvider | core | Resolve referências |
| SemanticIndexer | core | Indexação SQLite |
| RAGRetriever | core semântica |

## @context System

| Comando | Ação | Implementação |
|---------|------|---------------|
| `@file src/main.ts` | Inclui arquivo | File read + content |
| `@folder src/` | Inclui pasta | Glob + file contents |
| `@codebase` | Inclui estrutura | Semantic search |
| `@docs` | Inclui documentação | Doc search |

## RAG Local

O Continue usa SQLite para embeddings locais:
- Modelo: local embeddings
- Storage: SQLite database
- Indexação: automática
- Busca: semântica + full-text

## Pontos Fortes

1. @context system único
2. RAG local sem cloud
3. Multi-type referencing

## Limitações

1. Read-only (não mantido)
2. Sem compaction
3. Sem knowledge graph

## Oportunidades para o XForge

1. @context system é modelo ideal
2. RAG local como base para híbrido