---
id: KILO-CUSTOM-RULES-001
title: Custom Rules Patterns from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: rules
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [custom-rules, guardrails, coding-standards, security-rules, markdown-rules]
---

# Custom Rules Patterns

## 1. Rule Types

- **Project Rules**: Apply only to current project workspace
- **Global Rules**: Apply across all projects

## 2. Rule Location (VSCode/CLI)

### Via kilo.jsonc
```jsonc
{
  "instructions": [".kilo/rules/formatting.md", ".kilo/rules/*.md"]
}
```

### File Structure
```
project/
├── .kilo/
│   ├── rules/
│   │   ├── formatting.md
│   │   ├── restricted_files.md
│   │   └── naming_conventions.md
```

## 3. Rule Format

```markdown
# Restricted files

Files in the list contain sensitive data, they MUST NOT be read

- supersecrets.txt
- credentials.json
- .env
```

### Table Formatting Rule
```markdown
# Tables

When printing tables, always add an exclamation mark to each column header
```

## 4. Loading Priority

1. Global rules from `~/.kilocode/rules/`
2. Project rules from `.kilocode/rules/`
3. Legacy fallback: `.roorules`, `.clinerules`

Project rules take precedence over global for conflicts.

## 5. Mode-Specific Rules

### Directory Pattern
```
.kilocode/rules-${mode}/
```

Example:
```
.kilocode/rules-code/          # Code mode only
.kilocode/rules-architect/     # Architect mode only
```

Checked first, falls back to `.kilocoderules-${mode}`.

## 6. Managing Rules via kilo.jsonc

```jsonc
{
  "instructions": [
    ".kilo/rules/formatting.md",
    // ".kilo/rules/experimental.md",  -- temporarily disabled
    ".kilo/rules/naming_conventions.md"
  ]
}
```

JSONC supports comments for temporary disabling.

## 7. Use Cases

- Code Style: Enforce formatting, naming conventions
- Security Controls: Prevent access to sensitive files
- Project Structure: Define where files should be created
- Documentation Requirements: Specify formats
- Testing Patterns: Define test structure
- API Usage: Specify how APIs should be documented
- Error Handling: Define error handling conventions

## 8. Example Rules

- "Strictly follow code style guide"
- "Always use spaces for indentation, with a width of 4 spaces"
- "Use camelCase for variable names"
- "Write unit tests for all new functions"
- "Explain your reasoning before providing code"
- "Focus on code readability and maintainability"
- "Prioritize using the most common library in the community"

## Key Insights

- Rules are markdown-based (not code)
- Project rules override global (not merge)
- Mode-specific via directory naming
- Can be temporarily disabled via comments
- Legacy file support for backward compatibility
- Security use case: deny access to specific files
