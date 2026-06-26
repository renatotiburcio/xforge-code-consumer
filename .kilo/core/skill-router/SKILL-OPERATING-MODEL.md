# Skill Operating Model

## Purpose

Make skills actionable and lightweight.

## Rules

- A skill is a reusable capability, not a long article.
- A skill should tell the IA what to do, what to read and what to produce.
- Heavy domain knowledge belongs in `.xforge/knowledge`, not in every skill.
- New skills must include `SKILL.md` with frontmatter `name` and `description`.
- Skill names should match their directory names.
- Prefer canonical skills when choosing capabilities.

## Lifecycle

1. Create from `.kilo/skills/_template/SKILL.md`.
2. Keep the skill short.
3. Link to knowledge packs instead of embedding them.
4. Validate with `.kilo/automation/scripts/doctor.ps1`.
5. Promote only after successful use.

