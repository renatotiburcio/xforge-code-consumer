# Consolidação — Sistemas Core dos 10 Projetos

## Tabela Comparativa

| Projeto | Agent Loop | Tool System | Compaction | RAG |
|---------|------------|-------------|------------|-----|
| Kilo Code | Tool-calling | Built-in + MCP | ✅ | Qdrant |
| Cline | Tool-calling | Built-in + Browser | ❌ | ❌ |
| Continue | Chat-based | Built-in | ❌ | SQLite |
| Goose | Tool-calling | MCP-only | ❌ | ❌ |
| Roo-Code | Mode-based | Per-mode | ❌ | ❌ |
| Aider | Edit loop | Git tools | ❌ | Repo Map |
| OpenHands | Event-driven | Sandbox | ❌ | ❌ |
| Twinny | Simple | — | ❌ | ❌ |
| MiMo-Code | Simple | — | ❌ | ❌ |
| OpenCode | Simple | — | ❌ | ❌ |

## Router + Worker

Apenas Kilo Code implementa Router + Worker:
- Router (7B): decisões rápidas
- Worker (72B): execução de alta qualidade
- Economia de 70% em custo

## Compaction

Apenas Kilo Code implementa compactação de contexto:
- Sumariza mensagens antigas
- Preserva decisões importantes
- Preserva system prompt e tool definitions

## RAG/Indexing

| Projeto | Tecnologia | Tipo |
|---------|------------|------|
| Kilo Code | Qdrant | Vector store |
| Continue | SQLite | Local embeddings |
| Aider | Repo Map | Structure index |

## Oportunidades para o XForge

1. Router + Worker (inspirado em Kilo Code)
2. Compaction inteligente (inspirado em Kilo Code)
3. Hybrid RAG (Kilo Code + Continue + Aider)