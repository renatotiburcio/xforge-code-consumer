# Agent Operating Model

## Purpose

Make IA + KiloCode collaboration predictable.

## Operating Sequence

1. Public command receives the user request.
2. Command router identifies intent and risk.
3. Canonical agent is selected.
4. Supporting agents are selected only if needed.
5. Skills are selected by capability, not by title similarity.
6. Memory is retrieved on demand.
7. Work is executed in the workspace.
8. Validation is run.
9. Memory, docs, backlog or roadmap are updated only when relevant.
10. Final answer reports what was done, what was validated and what remains.

## Constraints

- One primary agent per task.
- Prefer canonical agents over legacy agents.
- Prefer small skills over large knowledge files.
- Prefer `.xforge` indexes over loading full `.xforge` directories.
- Use `doctor.ps1` after structural changes to `.kilo`.

