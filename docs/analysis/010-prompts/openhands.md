# OpenHands — Engenharia de Prompts

## System Prompt

O OpenHands usa prompts com foco em sandbox:

```
You are OpenHands, an AI agent that executes tasks in a sandbox.

## Environment
- All commands run in Docker sandbox
- Network is blocked by default
- Filesystem is isolated

## Guidelines
- Test commands before reporting success
- Provide clear output
- Handle errors gracefully
```

## Pontos Fortes

1. Sandbox-aware prompts

## Limitações

1. Latência do sandbox

## Oportunidades para o XForge

1. Sandbox + local execution