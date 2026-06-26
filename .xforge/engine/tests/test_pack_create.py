import json, shutil
from pathlib import Path

ROOT = Path(r"D:\\dev\\XForge-Development-New")


def test_pack_create_scaffolds_new_pack(call_tool):
    """xforge_pack_create must scaffold manifest + content + register."""
    r = call_tool("xforge_pack_create", {
        "name": "xforge-pytest-tmp",
        "version": "1.0.0",
        "trustScore": 75,
        "tags": ["pytest", "tmp"],
        "domain": "test",
        "description": "Pack created by pytest",
        "files": ["a.md", "b.md"],
    })
    assert r["ok"] is True, r
    assert r["pack"] == "xforge-pytest-tmp"
    assert r["filesCreated"] == 2
    assert r["registered"] is True
    # Verify files exist
    assert (ROOT / ".xforge" / "marketplace" / "packs" / "xforge-pytest-tmp.json").exists()
    assert (ROOT / ".xforge" / "knowledge" / "packs" / "xforge-pytest-tmp" / "a.md").exists()


def test_pack_create_rejects_duplicate(call_tool):
    """xforge_pack_create must fail if manifest already exists."""
    r = call_tool("xforge_pack_create", {
        "name": "xforge-fiscal",  # already exists
        "description": "should fail",
    })
    assert r["ok"] is False
    assert "already exists" in r["error"]


def test_pack_create_rejects_bad_name(call_tool):
    """Pack name must start with xforge- prefix."""
    r = call_tool("xforge_pack_create", {"name": "bad-name"})
    assert r["ok"] is False
    assert "xforge-" in r["error"]


def test_pack_create_validates_trust_score(call_tool):
    """trustScore must be 0-100."""
    r = call_tool("xforge_pack_create", {
        "name": "xforge-bad-trust",
        "trustScore": 150,
    })
    assert r["ok"] is False
    assert "trustScore" in r["error"]


def test_pack_create_is_idempotent(call_tool):
    """Running twice on same pack must not overwrite."""
    r1 = call_tool("xforge_pack_create", {
        "name": "xforge-idem-test",
        "files": ["x.md"],
    })
    assert r1["ok"] is True
    # Try again - should fail
    r2 = call_tool("xforge_pack_create", {
        "name": "xforge-idem-test",
        "files": ["x.md"],
    })
    assert r2["ok"] is False


def teardown_module():
    """Cleanup tmp packs created by tests."""
    for name in ["xforge-pytest-tmp", "xforge-idem-test", "xforge-bad-trust"]:
        m = ROOT / ".xforge" / "marketplace" / "packs" / f"{name}.json"
        if m.exists():
            m.unlink()
        d = ROOT / ".xforge" / "knowledge" / "packs" / name
        if d.exists():
            shutil.rmtree(d)
    inst = ROOT / ".xforge" / "packs" / "installed.json"
    if inst.exists():
        data = json.loads(inst.read_text(encoding="utf-8"))
        for name in ["xforge-pytest-tmp", "xforge-idem-test", "xforge-bad-trust"]:
            data.get("packs", {}).pop(name, None)
        inst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")