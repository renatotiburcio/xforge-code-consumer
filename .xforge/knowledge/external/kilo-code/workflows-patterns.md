---
id: KILO-WORKFLOWS-PATTERNS-001
title: Workflow and Slash Command Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: workflows
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [workflows, slash-commands, automation, composable-commands]
---

# Workflow and Slash Command Patterns

## 1. Command File Structure

Location: `.kilo/commands/<name>.md` (project) or `~/.config/kilo/commands/<name>.md` (global)

```markdown
---
description: Submit a pull request with full checks
agent: code
model: anthropic/claude-sonnet-4-20250514
subtask: true
---

# Submit PR Workflow

1. First, use `grep` to check for TODO comments or console.log statements
2. Run tests using `bash` with `npm test`
3. If tests pass, stage and commit changes
4. Push branch and create PR using `gh pr create`
5. Use `question` to get PR title and description

Parameters needed (ask if not provided):
- Branch name
- Reviewers to assign
```

## 2. Frontmatter Fields

| Field | Description |
|-------|-------------|
| `description` | Shown in command picker |
| `agent` | Which agent to use when invoking |
| `model` | Model override for this command |
| `subtask` | When true, runs as sub-agent session |

## 3. Common Workflow Patterns

### Release Management
```markdown
1. Gather merged PRs since last release
2. Generate changelog from commit messages
3. Update version numbers
4. Create release branch and tag
5. Deploy to staging environment
```

### Project Setup
```markdown
1. Clone repository template
2. Install dependencies (npm install, pip install)
3. Configure environment files
4. Initialize database/services
5. Run initial tests
```

### Code Review Preparation
```markdown
1. Search for TODO comments and debug statements
2. Run linting and formatting
3. Execute test suite
4. Generate PR description from recent commits
```

## 4. Invocation

```
/command-name    # invokes the workflow (without .md extension)
```

## 5. Migration from Legacy

Legacy: `.kilocode/workflows/` → New: `.kilo/commands/`
Legacy invoked with `/filename.md` → New invoked with `/filename`
Automatic migration on startup for VS Code extension.

## Key Insights

- Workflows are markdown files with YAML frontmatter
- Can specify agent, model, and subtask flag
- Invoked via slash command syntax
- Support parameter prompting
- All built-in tools available: read, glob, grep, edit, write, bash, webfetch, MCP
- CLI tools (gh, docker, npm) also available
- Composable: can chain multiple steps in single workflow
