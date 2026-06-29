---
id: KILO-PERMISSIONS-PATTERNS-001
title: Permissions and Security Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: security
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [permissions, security, rbac, agent-permissions, bash-permissions]
---

# Permissions and Security Patterns

## 1. Permission Actions

| Action | Behavior |
|--------|----------|
| `allow` | Run without asking |
| `ask` | Prompt before running |
| `deny` | Block entirely |

## 2. Permission Structure

```yaml
permission:
  read: allow
  edit:
    "*": deny
    "*.md": allow
  bash:
    "*": ask
    "git status *": allow
    "git diff *": allow
```

## 3. Rule Precedence

Rules evaluated in config order. **Last matching rule wins.**

```yaml
# Correct: specific after broad
permission:
  bash:
    "*": ask        # broad fallback first
    "uv *": allow    # exception after

# Wrong: broad overrides specific
permission:
  bash:
    "uv *": allow
    "*": ask        # this wins, uv still asks
```

## 4. Glob Pattern Matching

| Pattern | Matches |
|---------|---------|
| `*` | Any target |
| `git *` | `git`, `git status`, `git log --oneline` |
| `git status *` | `git status` with/without args |
| `src/*` | Paths under `src/` |
| `*.env` | Files ending in `.env` (including nested) |

## 5. Shell Command Parsing

Multi-command blocks: each command must be permitted. Single denied command rejects entire request.

```bash
cd "/project"; git status
# If git * is denied, entire block is denied
```

## 6. Read-Only Agent Pattern

```yaml
permission:
  bash:
    "*": deny
    "cat *": allow
    "grep *": allow
    "git status *": allow
    "git diff *": allow
```

## 7. Sensitive File Protection

Kilo treats `.env` and `.env.*` as sensitive. Broad read approvals do NOT bypass this.

## 8. Subagent Delegation Control

```yaml
permission:
  task:
    "*": deny
    "code-reviewer": allow
    "docs-writer": allow
```

## 9. Top-Level Override

```yaml
# bash overrides global fallback
permission:
  "*": ask
  bash: allow
```

## Key Insights

- Permission model is deny-by-default with explicit allows
- Glob patterns evaluated in order (last match wins)
- Sensitive files (.env) always require explicit approval
- Subagent delegation can be restricted per-agent
- Windows paths normalized to forward slashes for matching
- Home directory expansion: `~`, `~/...`, `$HOME`
