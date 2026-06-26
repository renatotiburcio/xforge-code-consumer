# Command Router

## Objective

Reduce operational complexity and keep KiloCode routing predictable.

## Rule

The user should use canonical public commands. Specialized commands remain available as internal routes or compatibility aliases.

## Flow

```text
public command
-> intent
-> domain
-> primary agent
-> skills
-> internal commands
-> workflows
-> gates
-> result
```

## Canonical Public Commands

See `.kilo/core/registries/command-registry.json`.

The official public surface is:

- `/xforge`
- `/analisar-projeto`
- `/criar-projeto`
- `/desenvolver`
- `/qualidade`
- `/seguranca`
- `/conhecimento`
- `/memoria`
- `/documentacao`
- `/release`

## Compatibility

Old commands are not removed. They remain available for backward compatibility, automation and direct expert use.
