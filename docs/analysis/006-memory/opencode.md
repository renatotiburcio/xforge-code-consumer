# OpenCode — Sistema de Memória

## Arquitetura

O OpenCode tem memória mínima:

```mermaid
flowchart TD
    AG[Agente] --> MEM[Memory]
    MEM -->|salva| DISK[Local Storage]
```

## Limitações

1. Funcionalidades limitadas