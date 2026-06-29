---
id: KILO-AGENT-PATTERNS-001
title: Agent Configuration Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: agent-configuration
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [agent, configuration, kilo, subagent, permissions, modes]
---

# Agent Configuration Patterns

## 1. Subagent Definition (Markdown File)

Location: `.kilo/agents/<name>.md` (project) or `~/.config/kilo/agents/<name>.md` (global)

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

You are a code reviewer. Analyze code for:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

## 2. Subagent Definition (JSON in kilo.jsonc)

```jsonc
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    }
  }
}
```

## 3. Agent Modes

| Mode | Description |
|------|-------------|
| `primary` | User-facing agents you interact with directly |
| `subagent` | Only invocable via Task tool or @ mentions |
| `all` | Can function as both primary and subagent (default for custom) |

## 4. Permission Patterns

### Bash Command Permissions
```yaml
permission:
  bash:
    "*": ask           # Default: ask for all commands
    "git diff": allow  # Allow specific commands
    "git log*": allow
    "npm test": allow
```

### File Edit Permissions
```yaml
permission:
  edit:
    "*": deny          # Deny all edits by default
    "*.md": allow      # Allow markdown edits
    "docs/*": allow    # Allow edits in docs/
```

### Subagent Delegation Control
```yaml
permission:
  task:
    "*": deny
    "code-reviewer": allow
    "docs-writer": allow
```

## 5. Sensitive File Protection

Kilo treats `.env` and `.env.*` as sensitive. Broad read approvals do NOT bypass this.

```yaml
permission:
  read:
    "*": allow
    "*.env": ask
    "*.env.*": ask
    "*.env.example": allow
```

## 6. Agent Configuration Precedence

1. Built-in agent defaults
2. Global config (`~/.config/kilo/config.json`)
3. Project config (`kilo.jsonc` in project root)
4. Global agent markdown files (`~/.config/kilo/agents/*.md`)
5. Project agent markdown files (`.kilo/agents/*.md`)

## 7. Built-in Subagents

| Name | Description |
|------|-------------|
| `general` | General-purpose, full tool access (except todo) |
| `explore` | Fast, read-only codebase exploration |

## 8. Invocation Patterns

### Automatic (via Task tool)
Primary agents invoke subagents when description matches the task.

### Manual (via @ mentions)
```
@code-reviewer review the authentication module for security issues
```

### CLI Interactive Creation
```bash
kilo agent create --path .kilo --description "Reviews code for security" --mode subagent --tools "read,grep,glob"
```

## Key Insights

- **Isolated context**: Each subagent runs in its own session with separate conversation history
- **Results flow back**: When subagent completes, result summary returns to parent
- **Description matching**: Agent LLM decides whether to use a skill based on description field
- **No keyword matching**: The agent evaluates request against all available skill descriptions
- **Permission inheritance**: Unspecified fields use sensible defaults (mode: "all", full permissions)
- **Temperature control**: Lower = more deterministic (0.1 for review, 0.3 for generation)
- **Steps limit**: Maximum agentic iterations before forcing text-only response (cost control)
