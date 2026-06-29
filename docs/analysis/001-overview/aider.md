# Aider

## O que é

Aider é um agente de código AI como CLI Python. Foca em git-native workflow, repo mapping, e pair programming. Diferente de extensões VS Code, roda no terminal. Usa GPT-4/Claude para gerar patches git.

## Qual objetivo

Fornecer um assistente que entende o repositório git completo, gera diffs precisos, e facilita pair programming entre humano e IA.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| CLI[Aider CLI\nPython]
    CLI -->|carrega| REPO[Repo Map\nrepository structure]
    REPO -->|indexa| FILES[Files + structure]
    CLI -->|monta| CTX[Context]
    CTX -->|envia| LLM[GPT-4/Claude]
    LLM -->|decide| EDIT{Edit?}
    EDIT -->|sim| DIFF[Generate Diff]
    DIFF -->|aplica| GIT[Git]
    EDIT -->|não| RESP[Response]
    RESP --> U
\\\

## Funcionalidades Principais

1. **Git-native**: Entende commits, diffs, branches
2. **Repo mapping**: Indexa estrutura do projeto automaticamente
3. **Pair programming**: Modo colaborativo humano-IA
4. **Prompt caching**: Reduz tokens
5. **Multi-model**: GPT-4, Claude, etc.
6. **Auto-commit**: Commits automáticos com mensagens geradas

## Pontos Fortes

1. **Git-native**: Melhor integração com git
2. **Repo mapping**: Indexação automática
3. **Pair programming**: Colaboração natural
4. **Minimal UI**: Foco no terminal

## Limitações

1. **Sem UI rica**: Apenas terminal
2. **Sem multi-agentes**: Apenas um agente
3. **Sem compactação**: Contexto limitado
4. **Sem MCP**: Sem ferramentas externas

## Oportunidades para o XForge

1. Git-native workflow é excelente modelo
2. Repo mapping pode ser integrado com RAG
3. Pair programming pode ser expandido para multi-agentes