---
id: KILO-CUSTOM-INSTRUCTIONS-001
title: Custom Instructions Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: instructions
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [custom-instructions, system-prompt, AGENTS.md, CLAUDE.md, context-configuration]
---

# Custom Instructions Patterns

## 1. Auto-Discovered Files

Kilo automatically discovers these files at project root (via `findUp`):

- **`AGENTS.md`** — Primary instruction file
- **`CLAUDE.md`** — Claude compatibility
- **`CONTEXT.md`** — Additional project context

## 2. Per-Directory Instructions

Place `AGENTS.md` in any subdirectory — loaded dynamically when Read tool accesses a file in that directory. Contents injected as `<system-reminder>` tags.

Useful for monorepo context-specific guidance.

## 3. Global vs Project Instructions

### Global
- Kilo: `~/.config/kilo/AGENTS.md`
- Claude: `~/.claude/CLAUDE.md`

### Project
- Project root `AGENTS.md`
- Loaded before global instructions

## 4. Additional Sources (kilo.jsonc)

```jsonc
{
  "instructions": [
    "./docs/coding-standards.md",
    "./teams/frontend-rules.md",
    "https://example.com/team-instructions.md"
  ]
}
```

URL sources fetched at session start (5-second timeout, silently skipped if unreachable).

## 5. Mode-Specific Instructions

### Via Settings UI
- Global custom instructions: apply to all modes
- Mode-specific: apply only to selected mode

### Via Files
- Preferred: `.kilo/rules-{mode-slug}/` (directory)
- Fallback: `.kilocoderules-{mode-slug}` (single file)

## 6. Per-Agent Prompts

```jsonc
{
  "agent": {
    "code": {
      "prompt": "You are a Python specialist. Follow PEP8 strictly."
    }
  }
}
```

Or in markdown agent file:
```markdown
---
description: Python specialist
---
You are a Python specialist. Follow PEP8 strictly.
```

## 7. Loading Order

1. Global instructions from global `kilo.jsonc`
2. Project instructions from project `kilo.jsonc`
3. Files matched by glob patterns (filesystem order)
4. Project-level takes precedence over global for conflicts

## Key Insights

- AGENTS.md is the primary instruction file (auto-discovered)
- Per-directory AGENTS.md enables monorepo context
- URL-based instructions enable centralized team configs
- Mode-specific rules via directory naming convention
- Instructions are injected into system prompt
- kilo.jsonc `instructions` array supports paths, globs, and URLs
