# Kilo Code — Gerenciamento de Contexto

## Arquitetura

O contexto no Kilo Code é montado em camadas:

```mermaid
flowchart TD
    EP[Entry Point] --> CA[Context Assembly]
    CA -->|coleta| IDX[Indexing\npackages/kilo-indexing]
    CA -->|carrega| AG[AGENTS.md]
    CA -->|resolve| REF[@file/@folder]
    CA -->|monta| PROMPT[Prompt]
    PROMPT -->|envia| LLM
```

## Componentes

| Componente | Package | Responsabilidade |
|------------|---------|------------------|
| ContextAssembler | opencode | Monta contexto |
| Indexing | kilo-indexing | Indexação RAG (Qdrant) |
| CompactionEngine | opencode | Comprime contexto |

## Context Assembly Pipeline

1. System prompt (fixo, < 2000 tokens)
2. Tool definitions (fixo, < 1000 tokens)
3. AGENTS.md (root)
4. Arquivos referenciados (@file, @folder)
5. Histórico de mensagens (variável)
6. Resultados de tool calls

## Compaction Strategy

Quando contexto atinge 80% do limite (200k tokens):
1. Sumariza mensagens antigas (mantém decisões)
2. Preserva mensagens recentes (últimas 5)
3. Preserva system prompt e tool definitions
4. Preserva arquivos modificados

## RAG/Indexing

O Kilo Code usa Qdrant para busca semântica:
- Embeddings: Ollama nomic-embed-text
- Collection: project_files
- Chunk size: 1000 tokens
- Overlap: 200 tokens

## Pontos Fortes

1. Compaction inteligente
2. RAG com Qdrant
3. Preserva decisões importantes

## Limitações

1. Sem per-directory AGENTS.md
2. Sem knowledge graph
3. Sem TTL em conhecimento

## Oportunidades para o XForge

1. Adicionar per-directory rules
2. Implementar knowledge graph com TTL
3. Melhorar compaction com LLM