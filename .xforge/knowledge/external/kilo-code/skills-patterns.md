---
id: KILO-SKILLS-PATTERNS-001
title: Skills System Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: skills
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [skills, agent-skills, SKILL.md, marketplace, extensibility]
---

# Skills System Patterns

## 1. Skill Structure

```
my-skill/
├── SKILL.md           # Required: instructions + metadata
├── scripts/           # Optional: executable code
├── references/        # Optional: documentation
└── assets/            # Optional: templates, resources
```

## 2. SKILL.md Format

```markdown
---
name: my-skill-name
description: A brief description of what this skill does and when to use it
license: Apache-2.0
metadata:
  author: example-org
  version: 1.0.0
---

# Instructions

Your detailed instructions for the AI agent go here.
The agent will read this content when it decides to use the skill.
```

## 3. Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase, numbers, hyphens only |
| `description` | Yes | Max 1024 chars. When to use the skill |
| `license` | No | License name or reference |
| `compatibility` | No | Environment requirements |
| `metadata` | No | Arbitrary key-value mapping |

## 4. Skill Locations

### Global (User-Level)
- Mac/Linux: `~/.kilo/skills/`
- Windows: `\Users\<user>\.kilo\skills\`

### Project-Level
- `.kilo/skills/`

### Compatibility Directories
- `.agents/skills/` — Open agent standard
- `.claude/skills/` — Claude Code compatibility

### Remote URLs (kilo.jsonc)
```jsonc
{
  "skills": {
    "paths": ["/path/to/shared/skills", "~/my-skills"],
    "urls": ["https://example.com/.well-known/skills/"]
  }
}
```

Remote server must serve `index.json`:
```json
{
  "skills": [
    { "name": "skill-name", "files": ["SKILL.md", "references/file.md"] }
  ]
}
```

## 5. Skill Loading Mechanism

1. **Discovery**: Scanned at session start, only metadata (name, description, path) read
2. **Prompt inclusion**: Relevant skill metadata included in system prompt
3. **On-demand loading**: When agent determines task matches skill description, reads full SKILL.md

## 6. Agent Decision Criteria

The agent (LLM) decides whether to use a skill based on the `description` field:
- **No keyword matching or semantic search**
- Agent evaluates request against all available skill descriptions
- Must "clearly and unambiguously apply"
- **Description wording matters**: Write descriptions matching how users phrase requests
- **Explicit invocation always works**: "use the api-design skill"

## 7. Priority Rules

1. Project skills override global skills (same name)
2. Mode-specific skills override generic skills (in legacy)
3. Additional paths loaded alongside

## 8. When Skills Are Loaded

- CLI: When starting a new session or `kilo run`
- VS Code: When extension connects to CLI server
- Re-scanned at start of each new session
- New session required to pick up changes

## 9. Name Matching Rule

The `name` field MUST match the parent directory name:

```
✅ Correct:
skills/
└── frontend-design/
    └── SKILL.md  # name: frontend-design

❌ Incorrect:
skills/
└── frontend-design/
    └── SKILL.md  # name: my-frontend-skill
```

## Key Insights for XForge

- Skills are self-documenting and interoperable
- Agent decides usage based on description matching (not rigid rules)
- Can include scripts, references, and assets
- Remote URL loading enables centralized skill distribution
- Priority system allows project overrides of global skills
