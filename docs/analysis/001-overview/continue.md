# Continue

## O que é

Continue é um agente de código open-source (Apache 2.0) disponível como CLI, extensão VS Code e plugin JetBrains. Foi pioneiro em @context system e RAG integrado. O repositório agora é read-only (manutenção encerrada).

## Qual objetivo

Fornecer um assistente que entende o contexto completo do projeto através de indexação semântica, referências explícitas (@file, @folder, @codebase), e autocomplete baseado em contexto.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|@file/@folder| EXT[VS Code / JetBrains / CLI]
    EXT -->|resolve| CTX[Context Provider]
    CTX -->|busca| IDX[Semantic Index\nSQLite]
    IDX -->|retorna| CTX
    CTX -->|monta| PROMPT[Prompt Assembly]
    PROMPT -->|envia| LLM[LLM]
    LLM -->|responde| EXT
    EXT --> U
\\\

## Produtos

| Produto | Localização | Descrição |
|---------|-------------|-----------|
| **CLI** | extensions/cli | Terminal interface |
| **VS Code** | extensions/vscode | Extensão Marketplace |
| **JetBrains** | extensions/intellij | Plugin IntelliJ |
| **Core** | packages/core | Sistemas centrais (RAG, model, context) |
| **GUI** | packages/gui | Interface gráfica |
| **Binary** | packages/binary | CLI standalone |

## Funcionalidades Principais

1. **@context system** — Referência explícita: @file, @folder, @codebase, @docs
2. **RAG integrado** — Indexação semântica com SQLite local
3. **Autocomplete** — Sugestões baseadas em contexto
4. **Chat** — Conversa com contexto do projeto
5. **Edit** — Edição de código inline
6. **Multi-IDE** — VS Code + JetBrains

## Pontos Fortes

1. **@context system**: Melhor sistema de referência de arquivos
2. **RAG local**: Sem dependência de cloud
3. **Autocomplete**: Context-aware
4. **Pioneiro**: Um primeiros open-source coding agents

## Limitações

1. **Read-only**: Projeto não é mais mantido
2. **Sem multi-agentes**: Apenas chat/autocomplete
3. **Sem compactação**: Contexto limitado
4. **Sem memória**: Sem persistência entre sessões

## Oportunidades para o XForge

1. @context system é excelente — integrar com knowledge graph
2. RAG local + embeddings = base para busca híbrida
3. Autocomplete + error learning = sugestões que evitam erros