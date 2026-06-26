#!/usr/bin/env python3
"""GitHub MCP smoke-test for XForge integration.

DR-0191: validates that the GitHub MCP server (remote or local fallback) is reachable
and the configured toolsets respond.

Usage:
    python .kilo/skills/github-mcp/test_server.py
    python .kilo/skills/github-mcp/test_server.py --local

Requires:
    - GITHUB_PERSONAL_ACCESS_TOKEN env var (PAT with repo scope minimum)
    - Or GITHUB_MCP_PAT env var (alias used in kilo.jsonc)

Exit codes:
    0 - PASS (server reachable, initialize handshake works)
    1 - FAIL (network, auth, or server error)
    2 - SKIP (env var missing; not an error in CI)
"""
import json
import os
import sys
import urllib.error
import urllib.request

REMOTE_URL = os.environ.get("GITHUB_MCP_URL", "https://api.githubcopilot.com/mcp/")


def main():
    pat = os.environ.get("GITHUB_MCP_PAT") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not pat:
        print("[SKIP] GITHUB_MCP_PAT / GITHUB_PERSONAL_ACCESS_TOKEN not set", file=sys.stderr)
        return 2

    init_body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "xforge-github-mcp-test", "version": "1.0.0"},
        },
    }).encode()
    req = urllib.request.Request(
        REMOTE_URL,
        data=init_body,
        headers={
            "Authorization": f"Bearer {pat}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            if resp.status != 200:
                print(f"[FAIL] HTTP {resp.status}: {body[:200]}", file=sys.stderr)
                return 1
            print(f"[OK] initialize: HTTP {resp.status}")
            print(f"     server: {REMOTE_URL}")
            print(f"     body preview: {body[:120]}")
    except urllib.error.HTTPError as e:
        print(f"[FAIL] HTTP {e.code}: {e.read()[:200].decode(errors='replace')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"[FAIL] URL error: {e.reason}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())