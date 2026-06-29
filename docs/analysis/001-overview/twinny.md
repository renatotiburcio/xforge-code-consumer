# Twinny

## O que é

Twinny é um agente de código AI como extensão VS Code. Foca em local-first (Ollama), minimalismo, e privacidade.

## Qual objetivo

Fornecer um assistente leve que roda localmente sem dependências de cloud, respeitando a privacidade do desenvolvedor.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| EXT[VS Code Extension]
    EXT -->|envia| OLL[Ollama Local]
    OLL -->|responde| EXT
    EXT --> U
\\\

## Funcionalidades Principais

1. **Local-first**: Sem cloud, máxima privacidade
2. **Minimalista**: Leve e rápido
3. **Simples**: Fácil de usar e configurar
4. **Ollama integration**: Modelos locais

## Pontos Fortes

1. **Local-first**: Privacidade
2. **Minimalista**: Leve
3. **Simples**: Fácil

## Limitações

1. **Sem tools**: Apenas chat
2. **Sem MCP**: Sem ferramentas externas
3. **Sem compactação**: Contexto limitado

## Oportunidades para o XForge

1. Local-first é excelente para privacidade
2. Minimalismo pode inspirar modo 'lite'