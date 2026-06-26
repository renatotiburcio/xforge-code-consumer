---
name: manager-event-bus
description: Gerente do barramento de eventos interno.
color: info
mode: subagent
steps: 25
temperature: 0.2
permission:
  read: allow
  edit:
    "*.md": allow
    "*": deny
  bash: deny
---

# manager-event-bus

## Eventos principais

- PROJECT_RECOGNIZED
- MEMORY_UPDATED
- QUALITY_FAILED
- KNOWLEDGE_PROMOTED
- INCIDENT_RECORDED
- SNAPSHOT_CREATED

## Responsabilidades

Emitir eventos rastreáveis para conectar workflows, memória, GitHub e servidor.
