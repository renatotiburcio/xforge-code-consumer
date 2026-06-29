# Roo-Code — Sistema de Ferramentas

## Arquitetura

O Roo-Code tem ferramentas por modo:

```mermaid
flowchart TD
    AG[Agente] --> MD[Mode Detector]
    MD -->|Code| TOOLS_C[Tools Code]
    MD -->|Architect| TOOLS_A[Tools Architect]
    MD -->|Debug| TOOLS_D[Tools Debug]
```

## Tools por Modo

| Modo | Tools |
|------|-------|
| Code | read, write, edit, bash |
| Architect | plan, search, write |
| Ask | search, read |
| Debug | read, bash, debug |

## Pontos Fortes

1. Tools especializadas por modo

## Limitações

1. Descontinuado
2. Sem MCP tools

## Oportunidades para o XForge

1. Tools por modo + MCP