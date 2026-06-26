---
name: github-mcp
description: GitHub MCP integration (DR-0191) — 21 toolsets (~100+ tools) covering Actions, Code Scanning, Dependabot, Discussions, Gists, Issues, PRs, Repos, etc.
applicabilityScope: ["*"]
version: 1.0.0
created: 2026-06-22
---

# GitHub MCP Integration (DR-0191)
The GitHub MCP Integration (DR-0191) wraps the official `github-mcp-server` (https://github.com/github/github-mcp-server) as a **native MCP** in XForge. It exposes 21 toolsets (~100+ tools) covering the full GitHub API surface: Actions, Code Scanning, Copilot, Dependabot, Discussions, Gists, Git, Issues, Labels, Notifications, Orgs, Projects, Pull Requests, Repos, Secret Scanning, Security Advisories, Stargazers, Users, plus context and code quality.

Native MCPs in XForge cannot be installed or uninstalled — only **enabled/disabled** via `kilo.jsonc` `mcp.<name>.enabled`. Optional (community) MCPs use the full lifecycle via `/mcp-lifecycle` command (install, activate, deactivate, uninstall).

## When to use
- When you need to read/write GitHub repos, issues, PRs, actions, security findings, discussions, or projects from inside XForge.
- When you want project DNA + memory context alongside GitHub operations (XForge wrapper enriches tool calls).
- When OAuth or PAT auth is available (`GITHUB_MCP_PAT` env var).
- When MCP host supports HTTP transport (VS Code 1.101+, Claude Desktop, Cursor, Windsurf, OpenCode, Zed, etc.).
- DO NOT use for non-GitHub operations (use gh CLI or XForge native tooling instead).

## How to use
Canonical syntax:

```bash
# 1. Enable the MCP (one-time setup)
# Edit kilo.jsonc -> mcp.github.enabled = true
# Or via command: /mcp-lifecycle activate github

# 2. Set the PAT (one-time)
export GITHUB_MCP_PAT="ghp_xxxxxxxxxxxxxxxxxxxx"

# 3. Smoke-test the connection
python .kilo/skills/github-mcp/test_server.py
# Expected: [OK] initialize: HTTP 200

# 4. Use via MCP host (VS Code Copilot, Claude, etc.)
# In agent mode, tools like get_me, issue_read, create_pull_request become available.
```

XForge-specific wrappers (use these instead of calling MCP tools directly when working with the project):

- `github_pr_review` — PR review with project DNA context (RAG-augmented)
- `github_issue_triage` — issue triage with knowledge applicability filter
- `github_actions_debug` — workflow debugging with quality-gate correlation
- `github_release_notes` — release notes generation from merged PRs (with CHANGELOG append)

## Parameters
| Parameter | Type | Default | Description | Required? |
|-----------|------|---------|-------------|-----------|
| `GITHUB_MCP_PAT` | env var | (none) | GitHub PAT with `repo` scope minimum | Yes |
| `GITHUB_MCP_URL` | env var | `https://api.githubcopilot.com/mcp/` | Remote server URL (override for GHES) | No |
| `mcp.github.enabled` | bool (kilo.jsonc) | `false` | Toggle the MCP at host level | No |
| `toolsets` | server flag | `context, repos, issues, pull_requests, users` | Comma-separated toolsets to load | No |

## Examples

### Example 1: Triage open issues in current repo
```
[Agent mode] List open issues in renatotiburcio/xforge-enterprise-development-os with label 'bug'
[MCP] list_issues(owner='renatotiburcio', repo='xforge-enterprise-development-os', state='OPEN', labels=['bug'])
[Output] 3 issues found: #42, #47, #51
```

### Example 2: Read a specific issue with XForge DNA context
```
[Agent] Get details on issue #42 and correlate with project DRs
[MCP] issue_read(method='get', owner='renatotiburcio', repo='xforge-enterprise-development-os', issue_number=42)
[XForge] queries .xforge/decisions/ for related DRs, .xforge/rag/ for similar issues
[Output] issue #42 references DR-0190 (uncommitted scaffolding fix); tagged 'area:release-process'
```

### Example 3: Create a PR with auto-generated branch name
```
[Agent] Open a PR with title 'v50.10.0: GitHub MCP integration (DR-0191)' from branch 'feature/github-mcp'
[MCP] create_pull_request(owner='renatotiburcio', repo='xforge-enterprise-development-os',
                          title='v50.10.0: GitHub MCP integration (DR-0191)',
                          head='feature/github-mcp', base='master',
                          body='Implements DR-0191. Resolves user request for native GitHub MCP.')
```

### Example 4: GitHub Enterprise Server
```
# Set host override
export GITHUB_MCP_URL="https://ghes.example.com/api/v3/"
export GITHUB_MCP_PAT="ghp_..."
python .kilo/skills/github-mcp/test_server.py
# Note: GHES does not support remote MCP server; use Docker local fallback
```

### Example 5: Smoke-test CI gate
```yaml
# .github/workflows/mcp-smoke.yml
- name: Test GitHub MCP
  env:
    GITHUB_MCP_PAT: ${{ secrets.GITHUB_TOKEN }}
  run: python .kilo/skills/github-mcp/test_server.py
```

### Example 6: Switch off when offline / not needed
```jsonc
// kilo.jsonc -> mcp.github.enabled = false
"mcp": {
  "github": { "enabled": false }
}
```

## Troubleshooting

### [FAIL] HTTP 401
- **Cause**: PAT invalid, expired, or missing scope
- **Fix**: Regenerate PAT at https://github.com/settings/tokens with `repo` scope minimum

### [SKIP] GITHUB_MCP_PAT not set
- **Cause**: env var not exported in shell or CI
- **Fix**: `export GITHUB_MCP_PAT="ghp_..."` before running. In MCP host config, ensure `env.GITHUB_MCP_PAT` is wired to your secret store.

### [FAIL] URL error: [Errno 11001] getaddrinfo failed
- **Cause**: No DNS / offline
- **Fix**: Use Docker local fallback (`ghcr.io/github/github-mcp-server`) or wait for connectivity

### Tools not appearing in agent mode
- **Cause**: MCP host doesn't enable remote MCP servers, or `mcp.github.enabled=false`
- **Fix**: Check MCP host docs (VS Code 1.101+ required). Verify `enabled: true` in kilo.jsonc. Restart MCP host.