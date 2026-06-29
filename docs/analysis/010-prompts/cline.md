# Cline — Engenharia de Prompts

## System Prompt

O Cline usa system prompt focado em segurança:

```
You are Cline, an AI coding assistant.

## Rules
- Always explain what you are doing before making changes
- Show diffs before applying changes
- Ask for approval before destructive operations
- Prefer minimal changes
- Follow existing patterns

## Safety
- Never delete files without confirmation
- Never run destructive commands without approval
- Never commit without explicit instruction
```

## Prompt por Modo

| Modo | System Prompt |
|------|---------------|
| Plan | Explore codebase, ask questions, design strategy |
| Act | Execute plan with approval for each change |

## Pontos Fortes

1. Safety-first prompting
2. Plan/Act separation

## Limitações

1. Sem modos especializados
2. Sem few-shot examples

## Oportunidades para o XForge

1. Safety prompts + modos especializados