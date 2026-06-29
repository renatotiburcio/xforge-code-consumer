# Aider — Sistema de Memória

## Arquitetura

O Aider usa sessões para persistência:

```mermaid
flowchart TD
    AG[Agente] --> SESS[Session Manager]
    SESS -->|salva| DISK[Session Files]
```

## Pontos Fortes

1. Sessões persistentes
2. Git-native

## Limitações

1. Sem error learning
2. Sem compaction

## Oportunidades para o XForge

1. Sessões + error graph