# OpenCode

## O que é

OpenCode é um agente de código AI como CLI/TUI open-source. Foca em ser minimalista, single-binary, e rápido. É o projeto base que o Kilo Code forkou.

## Qual objetivo

Fornecer um assistente de terminal que roda em qualquer lugar sem dependências complexas.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| TUI[Terminal UI]
    TUI -->|envia| LLM[LLM Provider]
    LLM -->|responde| TUI
    TUI --> U
\\\

## Funcionalidades Principais

1. **Single-binary**: Instalação simples
2. **Rápido**: Startup instantâneo
3. **Multi-provedor**: Suporte a vários LLMs
4. **TUI**: Interface terminal

## Pontos Fortes

1. **Single-binary**: Fácil distribuição
2. **Rápido**: Startup rápido
3. **Multi-provedor**: Flexível

## Limitações

1. **Sem tools**: Funcionalidades limitadas
2. **Sem MCP**: Sem ferramentas externas
3. **Sem compactação**: Contexto limitado

## Oportunidades para o XForge

1. Single-binary é excelente para distribuição
2. TUI pode complementar extensão VS Code