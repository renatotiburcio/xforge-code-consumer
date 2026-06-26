# AGENTS.md - XForge Enterprise Development OS

## Mission

Transform a project into living, usable organizational knowledge.

## 🧠 Core Rule #0: Genius Council Framework (Regra de Ouro Suprema)

> **Desde 2026-06-17**, TODA decisao nao-trivial passa pelo **Conselho dos Genios**.

Antes de qualquer implementacao, refatoracao, correcao, melhoria, decisao arquitetural, nova funcionalidade, skill, agent, command, rule, ADR, SDD, documento, conteudo, recurso, opcao, nome, padrao, processo, workflow ou fluxo de trabalho:

1. **Descoberto** (Turing) — o que esta implicito?
2. **Analisado** (3-8 Genios relevantes ao topico)
3. **Debatido** (Devil''s Advocate — 7 perguntas)
4. **Validado** (5 Guardioes: Architecture, Simplicity, Security, Quality, Documentation)
5. **Documentado** (Decision Record canonico)
6. **Consolidado** (Documentation Governor atualiza docs)

**A documentacao e a fonte oficial da verdade.**

Ver:
- Regra: `.kilo/rules/02-genius-council-framework.md`
- Skill: `.kilo/skills/genius-council/SKILL.md`
- Manual: `docs/index.html` (landing visual) ou `docs/SUMMARY.md` (TOC Markdown)

## Core Rule

Recognize before creating.
Understand before changing.
Validate before finishing.
Document before shipping.

## CRITICAL: Tool Usage Rules

### ALWAYS Write Code to Files Directly

When the task requires creating or modifying code, you MUST use the edit or write tools.
Do NOT just describe what to do. Do NOT output code in chat that the user must copy.
Write the actual file, to the actual path, with the actual code.

### ALWAYS Document Before Implementing

Following GCF (Core Rule #0):
1. Create Decision Record (DR-XXXX) first
2. Get consensus from Conselho dos Genios
3. THEN write the code
4. Update documentation (backlog, manual, ADRs)

### Git Safety Protocol

- NEVER update the git config
- NEVER run destructive git commands (force push, hard reset) without explicit request
- NEVER skip hooks unless explicitly requested
- Use commit messages that explain WHY, not just WHAT
- See `.kilo/rules/git-safety.md` for full rules

## GCF Quick Reference

### When to Invoke the Council

Use the Conselho dos Genios when:
- Architectural decisions (stack, pattern, framework)
- Security decisions (auth, cryptography, LGPD)
- UX/UI decisions (flow, design system, component)
- Product decisions (scope, priority, ROI)
- Creating/modifying skills, agents, commands, rules
- Refactoring, breaking changes, migrations
- Bug investigation or incident analysis
- Sprint planning or roadmap

### How to Invoke

```markdown
## Conselho dos Genios: [Topic]

### 1. Discovery (Turing)
[What''s implicit]

### 2. Multi-Perspective Analysis
[3-8 relevant geniuses with their opinions]

### 3. Devil''s Advocate (AG999)
[7 questions answered]

### 4. 5 Guardians Validation
[OK/FAIL for each]

### 5. Consensus (AG100)
[Decision + justification]

### 6. Decision Record
[DR-XXXX summary]

### 7. Next Steps (AG102)
[Executable spec]
```

### Quick Genius Selection

| Topic | Geniuses |
|-------|----------|
| Architecture | Turing, von Neumann, Martin, Dijkstra, Torvalds |
| Security | Schneier, OWASP, Diffie, Cavoukian |
| UX/UI | Norman, Nielsen, Frost, Shneiderman |
| Performance | Knuth, Ritchie, Stroustrup |
| Product | Jobs, Gates, Wozniak, Norman |

## Project Structure

See `.kilo/rules/active-project-root-rules.md` for canonical structure.

## Memory Protocol

See `.kilo/rules/session-memory.md` for memory rules.

## Quality Gates

See `.kilo/rules/proactive-quality-gates.md` for quality gates.

## See Also

- `docs/SUMMARY.md` - Manual index (Markdown)
- `docs/index.html` - Manual landing (HTML visual)
- `.kilo/rules/00-xforge-rule-index.md` - Rules index
- `.xforge/decisions/ADR-INDEX.md` - ADRs index
- `CHANGELOG.md` - Version history
