# Kilo Compatibility Notes

## Fontes oficiais consideradas

- Kilo Custom Rules;
- Kilo Custom Modes/Agents;
- Kilo Skills;
- Kilo Custom Subagents;
- AGENTS.md;
- .kilocodeignore;
- Codebase Indexing.

## Regras aplicadas na REV37

- `kilo.jsonc` não recebe chaves customizadas inválidas.
- Novos roteadores/registries ficam em `core/`.
- Comandos continuam em `.kilo/commands/*.md`.
- Skills continuam em `.kilo/skills/<skill>/SKILL.md`.
- AGENTS.md é usado como instrução de alto nível.
- Regras continuam em `.kilo/rules/*.md`.
- Conhecimento pesado permanece fora de `kilo.jsonc`.
