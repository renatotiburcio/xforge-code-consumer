---
name: playwright-mcp
description: Playwright MCP integration (DR-0196) - 50+ browser automation tools (click/navigate/snapshot/evaluate/route/cookies) via @playwright/mcp. Microsoft-maintained.
applicabilityScope: ["*"]
version: 1.0.0
created: 2026-06-22
---

# Playwright MCP Integration (DR-0196)

## What it is
The Playwright MCP Integration (DR-0196) wraps `@playwright/mcp` (official Microsoft MCP server) as a **native MCP** in XForge. It exposes 50+ browser automation tools using Playwright's accessibility tree (not pixel-based), making it LLM-friendly and deterministic.

Native MCPs in XForge cannot be installed or uninstalled - only **enabled/disabled** via `kilo.jsonc` `mcp.<name>.enabled`. Optional MCPs use the full lifecycle via `/mcp-lifecycle` command.

**Complementary to XForge**:
- Existing: `visual_investigate.py` (Playwright scripts for visual regression)
- New: Playwright MCP (browser tools available to LLM agent)

## When to use
- When you need to interact with a web page (click, type, fill forms, navigate).
- When you need to test web app flows end-to-end.
- When you need to capture accessibility snapshots for analysis.
- When you need to mock network requests (route).
- When you need to manage cookies/localStorage.
- DO NOT use for non-browser tasks (use GitHub MCP for code, Filesystem MCP for files).

## How to use
1. Enable in `kilo.jsonc` -> `mcp.playwright.enabled = true`
2. Restart MCP host (VS Code / Claude / Cursor)
3. npx will auto-download chromium on first use

## Parameters
| Parameter | Type | Default | Description | Required? |
|-----------|------|---------|-------------|-----------|
| `mcp.playwright.enabled` | bool | `false` | Toggle the MCP at host level | No |
| `browser` (CLI) | string | `chromium` | Browser to use (chrome/firefox/webkit/msedge) | No |
| `headless` (CLI) | flag | `false` | Run headless (no GUI) | No |
| `isolated` (CLI) | flag | `false` | No persistent profile (clean state) | No |
| `caps` (CLI) | list | `core` | Capability sets to enable | No |
| `outputDir` (CLI) | path | temp | Where to save output files | No |

## Examples

### Example 1: Navigate and capture snapshot
```
[Agent] Navigate to https://example.com and snapshot
[MCP] browser_navigate(url='https://example.com')
[MCP] browser_snapshot() -> accessibility tree
[Output] page structure with all interactive elements
```

### Example 2: Fill a form
```
[Agent] Fill the login form with user@example.com
[MCP] browser_fill_form(fields=[{name:'email', type:'textbox', value:'user@example.com', target:'email-input'}])
[MCP] browser_click(target='submit-button')
```

### Example 3: Capture console messages
```
[Agent] Check for JS errors on the page
[MCP] browser_console_messages(level='error')
[Output] all error-level console messages
```

### Example 4: Mock API
```
[Agent] Mock the /api/users endpoint to return []
[MCP] browser_route(pattern='**/api/users', status=200, body='[]', contentType='application/json')
```

### Example 5: Disable when offline / not needed
```jsonc
// kilo.jsonc -> mcp.playwright.enabled = false
"mcp": {
  "playwright": { "enabled": false }
}
```

## Troubleshooting

### [SKIP] npx not in PATH
- Install Node.js 18+

### [FAIL] browser not found
- First run downloads chromium (~150MB) to `~/.cache/ms-playwright/`
- Or set `PLAYWRIGHT_BROWSERS_PATH=0` for system browser

### Browser hangs on headless
- Add `--no-sandbox` (only in trusted environments)

### File system access denied
- Default is workspace-root restricted; do NOT pass `--allow-unrestricted-file-access`

## Related
- DR-0196 (this integration)
- DR-0191 (GitHub MCP, similar pattern)
- DR-0194 (Filesystem MCP, complementary for workspace files)
- DR-0195 (Context7 MCP, library docs)
- XForge: `webapp-testing` skill, `e2e-visual-testing-expert` agent, `visual_investigate.py`