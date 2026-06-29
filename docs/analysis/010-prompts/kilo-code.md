# Kilo Code — Engenharia de Prompts

## System Prompt

O Kilo Code usa system prompt estruturado por modo:

```
You are Kilo Code, an AI coding agent.

## Capabilities
- Read, write, edit files
- Execute bash commands
- Search codebase
- Use MCP tools

## Guidelines
- Always read files before editing
- Prefer minimal changes
- Follow existing patterns
- Run tests after changes

## Code Style
- Single word variable names
- Avoid unnecessary destructuring
- Prefer early returns
- Use const by default
- Avoid try/catch where possible
```

## Prompt por Modo

| Modo | System Prompt |
|------|---------------|
| Code | Expert developer, focus on implementation |
| Plan | Architect + Planner, focus on design |
| Ask | Code reviewer, focus on analysis |
| Debug | Debugger, focus on root cause |
| Review | Security + Quality, focus on issues |

## Dynamic Prompts

O Kilo Code ajusta prompts baseado em:
- Stack detectada (.NET 10, Node.js, Python, Go, Rust)
- Tipo de arquivo (.ts, .cs, .py, etc.)
- Complexidade da tarefa

## Pontos Fortes

1. System prompt bem estruturado
2. Modos com prompts especializados
3. Ajuste dinâmico por stack

## Limitações

1. Sem few-shot examples
2. Sem chain-of-thought explícito

## Oportunidades para o XForge

1. Few-shot examples por stack
2. Chain-of-thought para tarefas complexas