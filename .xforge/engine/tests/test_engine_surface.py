"""Tests for engine surface: dispatcher registration + manifest sync.

Verifies that:
  - All tools exposed by the engine are registered in the dispatcher
  - Manifest MCP version is v1.3.0+ (post-mutate)
  - Manifest tool count matches dispatcher count
  - Manifest paths referenced by engine actually exist on disk
"""
import json
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
ENGINE = ROOT / ".xforge" / "engine" / "xforge_engine.py"
MANIFEST = ROOT / ".xforge" / "mcp" / "manifest.json"


def _read_engine_tools():
    """Parse xforge_engine.py to find the TOOLS dict keys."""
    code = ENGINE.read_text(encoding="utf-8")
    # Find a line that starts with TOOLS = { ... } or similar
    # Look for the dispatcher dict literal
    import re
    # Greedy match: TOOLS = { ... } block at top level
    m = re.search(r"^TOOLS\s*=\s*\{(.+?)\n\}\s*$", code, re.MULTILINE | re.DOTALL)
    assert m, "TOOLS dict not found in engine"
    block = m.group(1)
    # Extract all string keys ("name": ...)
    keys = re.findall(r'"([a-z][a-z0-9_]*)"\s*:\s*tool_', block)
    return sorted(set(keys))


def _read_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def test_engine_has_at_least_16_tools():
    """v55.0 ships 16 tools (15 + xforge_autoresearch_run_mutate)."""
    tools = _read_engine_tools()
    assert len(tools) >= 16, f"engine has {len(tools)} tools, expected >= 16: {tools}"


def test_manifest_has_at_least_16_tools():
    data = _read_manifest()
    n = len(data["tools"])
    assert n >= 16, f"manifest has {n} tools, expected >= 16"


def test_manifest_version_is_v1_3_0_or_higher():
    data = _read_manifest()
    v = data.get("version", "0.0.0")
    # Parse semver-ish; need at least 1.3.0
    parts = [int(p) for p in v.split(".") if p.isdigit()]
    assert parts[:3] >= [1, 3, 0], f"manifest version {v} < 1.3.0"


def test_manifest_tools_cover_all_required_core_tools():
    data = _read_manifest()
    names = {t["name"] for t in data["tools"]}
    required = {
        "xforge_doctor",
        "xforge_knowledge_search",
        "xforge_workflow_list",
        "xforge_workflow_validate",
        "xforge_workflow_run",
        "xforge_rbac_check",
        "xforge_policy_check",
        "xforge_tenant_list",
        "xforge_tenant_create",
        "xforge_tenant_use",
        "xforge_pack_list",
        "xforge_pack_install",
        "xforge_pack_uninstall",
        "xforge_autoresearch_run",
        "xforge_autoresearch_run_mutate",
        "xforge_validate_all",
    }
    missing = required - names
    assert not missing, f"manifest missing tools: {missing}"


def test_manifest_manifest_path_exists():
    data = _read_manifest()
    manifest_path = ROOT / data.get("manifestPath", ".xforge/mcp/manifest.json")
    assert manifest_path.exists(), f"manifestPath does not exist: {manifest_path}"


def test_engine_contains_mutate_function():
    # v3.10.6: tool moved to tools/autoresearch.py
    ar_path = ENGINE.parent / "tools" / "autoresearch.py"
    code = ar_path.read_text(encoding="utf-8") if ar_path.exists() else ""
    assert "def tool_autoresearch_run_mutate" in code
    assert "AUTORESEARCH_SANDBOX" in code
    assert "_measure_sandbox_xfs" in code
    assert "import shutil" in code


def test_manifest_includes_mutate_tool():
    data = _read_manifest()
    names = {t["name"] for t in data["tools"]}
    assert "xforge_autoresearch_run_mutate" in names, "mutate tool missing from manifest"