# Continue — Engenharia de Prompts

## System Prompt

O Continue usa prompts contextuais:

```
You are Continue, an AI coding assistant.

## Context
- File: {file_name}
- Language: {language}
- Project: {project_context}

## Guidelines
- Provide concise explanations
- Show code examples
- Reference documentation
```

## @context Integration

O sistema @context integra referências diretamente no prompt:

 Files
{file_contents}

## Referenced Folders
{folder_contents}

## Codebase Structure
{codebase_summary}
```

## Pontos Fortes

1. Context-aware prompts
2. @context integration

## Limitações

1. Read-only (não mantido)

## Oportunidades para o XForge

1. @context + knowledge graph