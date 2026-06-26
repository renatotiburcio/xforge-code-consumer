---
name: linear-mcp
description: Linear MCP integration (DR-0206) - issue tracking for Linear. OPTIONAL Node-based MCP, requires LINEAR_API_KEY per workspace.
applicabilityScope: ["*"]
version: 1.0.0
created: 2026-06-22
---

# Linear MCP (DR-0206)

## What it is
**OPTIONAL MCP** wrapping the official Linear MCP server (@linear/mcp-server, MIT, TypeScript, stdio). Bridges Linear issue tracking into the agent via MCP protocol.

## Why OPTIONAL
- **Project-specific**: each project has its own Linear workspace + API key
- **Paid SaaS**: Linear is a commercial product, not part of the open core
- **Same pattern** as markitdown (DR-0205) and memory (DR-0198): install lifecycle via /mcp-lifecycle command

## Install
```bash
bash .kilo/mcp/optional/linear-mcp/install.sh
# Get API key at: https://linear.app/settings/api
export LINEAR_API_KEY=lin_api_xxxxxxxxxxxx
/mcp-lifecycle install linear
/mcp-lifecycle activate linear
```

## Tools (~12)
- `list_issues` / `get_issue` / `create_issue` / `update_issue`
- `list_teams` / `list_projects` / `create_project`
- `list_cycles` / `list_users`
- `search_issues`
- `add_comment` / `list_comments`

## Security
- **API key NEVER committed** - only via env var LINEAR_API_KEY or .kilo/mcp/optional/linear.json (gitignored)
- Token-based: revoke at any time at https://linear.app/settings/api
- Server is read+write capable - protect LINEAR_API_KEY with same care as GitHub PAT

## Jira (parallel pattern, NOT bundled)
Atlassian Jira MCP server (`mcp-server-jira`) follows the same OPTIONAL pattern:
install `@atlassian/mcp-server-jira` via similar install.sh, env `ATLASSIAN_TOKEN`.
Not bundled by default to avoid scope creep (one issue tracker per install).

## Related
- DR-0206 (this integration)
- DR-0205 (markitdown - same OPTIONAL pattern)
- DR-0198 (memory - first OPTIONAL MCP)
- .kilo/commands/mcp-lifecycle.md (install/activate/deactivate/uninstall)
