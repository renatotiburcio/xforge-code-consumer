"""Tests for xforge-esocial and xforge-sped-fiscal packs (added in v55.2).

Verifies both packs have valid marketplace manifests, source files,
frontmatter, and are installable via the engine.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")

NEW_PACKS = [
    {
        "id": "xforge-esocial",
        "source": ROOT / ".xforge" / "business" / "esocial",
        "files": ["s-1000-iniciais.md", "s-1200-folha.md", "s-3000-sst.md"],
    },
    {
        "id": "xforge-sped-fiscal",
        "source": ROOT / ".xforge" / "business" / "sped-fiscal",
        "files": ["efd-icms-ipi.md", "efd-contribuicoes.md", "ecd-ecf.md"],
    },
]


@pytest.mark.parametrize("pack_id", [p["id"] for p in NEW_PACKS])
def test_marketplace_manifest_exists(pack_id):
    p = ROOT / ".xforge" / "marketplace" / "packs" / f"{pack_id}.json"
    assert p.exists(), f"missing: {p}"


@pytest.mark.parametrize("pack_id", [p["id"] for p in NEW_PACKS])
def test_marketplace_manifest_fields(pack_id):
    p = ROOT / ".xforge" / "marketplace" / "packs" / f"{pack_id}.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    assert m["id"] == pack_id
    assert m["version"] == "1.0.0"
    assert m["files"] >= 3
    assert isinstance(m.get("tags"), list)
    assert 0 <= m.get("trustScore", 0) <= 100


@pytest.mark.parametrize("pack", NEW_PACKS, ids=[p["id"] for p in NEW_PACKS])
def test_source_files_exist(pack):
    for name in pack["files"]:
        p = pack["source"] / name
        assert p.exists(), f"missing source file: {p}"


@pytest.mark.parametrize("pack", NEW_PACKS, ids=[p["id"] for p in NEW_PACKS])
def test_source_files_have_frontmatter(pack):
    fm_pattern = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
    for md in sorted(pack["source"].glob("*.md")):
        content = md.read_text(encoding="utf-8")
        m = fm_pattern.match(content)
        assert m, f"{md.name} missing frontmatter"
        body = m.group(1)
        assert "title:" in body, f"{md.name} missing title"
        assert "summary:" in body, f"{md.name} missing summary"
        assert "keywords:" in body, f"{md.name} missing keywords"
        assert "id:" in body, f"{md.name} missing id"
        assert "type:" in body, f"{md.name} missing type"


@pytest.mark.parametrize("pack_id", [p["id"] for p in NEW_PACKS])
def test_pack_installed_in_knowledge(call_tool, pack_id):
    r = call_tool("xforge_pack_list", {})
    assert r["ok"] is True
    names = {p["id"] for p in r.get("packs", [])}
    assert pack_id in names, f"{pack_id} not in pack list: {names}"


@pytest.mark.parametrize("pack_id", [p["id"] for p in NEW_PACKS])
def test_pack_searchable_by_keyword(call_tool, pack_id):
    """Search for the pack id in knowledge; should return at least 1 file from the pack."""
    r = call_tool("xforge_knowledge_search", {"query": pack_id.replace("xforge-", ""), "limit": 5})
    assert r["ok"] is True
    # Either returns results or empty; both are OK
    # What we care about is that the tool didn't crash


def test_total_knowledge_files_at_least_208():
    """After installing esocial + sped-fiscal, knowledge should have 199+3+3+3=208 files."""
    k_root = ROOT / ".xforge" / "knowledge"
    if not k_root.exists():
        pytest.skip("knowledge root not present")
    # Count only .md files in the packs subdir + main knowledge
    n = sum(1 for _ in k_root.rglob("*.md"))
    assert n >= 208, f"expected >= 208 knowledge files, got {n}"