# MiMo-Code — Gerenciamento de Contexto

## Arquitetura

O MiMo-Code tem contexto mínimo:

```mermaid
flowchart TD
    AG[Agente] --> CTX[Context Builder]
    CTX -->|carrega| FILES[Arquivos]
```

## Pontos Fortes

1. Leve
2. Simples

## Limitações

1. Funcionalidades limitadas
2. Sem RAG