"""Tests for the xforge-banking pack (added in v55.1).

Verifies:
  - Pack manifest exists in marketplace
  - All declared files exist in business/banking/
  - Pack is installable via the engine tool
  - All files have valid frontmatter
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
MARKETPLACE_MANIFEST = ROOT / ".xforge" / "marketplace" / "packs" / "xforge-banking.json"
SOURCE_DIR = ROOT / ".xforge" / "business" / "banking"


def test_banking_manifest_exists():
    assert MARKETPLACE_MANIFEST.exists(), f"missing: {MARKETPLACE_MANIFEST}"


def test_banking_manifest_fields():
    m = json.loads(MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
    assert m["id"] == "xforge-banking"
    assert m["version"] == "1.0.0"
    assert m["files"] >= 3
    assert isinstance(m.get("tags"), list)
    assert any(t in {"banking", "pix", "open-finance", "cnab"} for t in m["tags"])
    assert 0 <= m.get("trustScore", 0) <= 100


def test_banking_source_files_exist():
    expected = ["open-finance.md", "pix.md", "conciliacao.md"]
    for name in expected:
        p = SOURCE_DIR / name
        assert p.exists(), f"missing source file: {p}"


def test_banking_files_have_frontmatter():
    fm_pattern = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
    for md in sorted(SOURCE_DIR.glob("*.md")):
        content = md.read_text(encoding="utf-8")
        m = fm_pattern.match(content)
        assert m, f"{md.name} missing frontmatter"
        body = m.group(1)
        assert "title:" in body, f"{md.name} missing title in frontmatter"
        assert "summary:" in body, f"{md.name} missing summary in frontmatter"
        assert "keywords:" in body, f"{md.name} missing keywords in frontmatter"


def test_banking_pack_installed(call_tool):
    r = call_tool("xforge_pack_list", {})
    assert r["ok"] is True
    names = {p["id"] for p in r.get("packs", [])}
    assert "xforge-banking" in names, f"xforge-banking not in pack list: {names}"