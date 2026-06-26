"""Tests for knowledge pack install/uninstall."""
from pathlib import Path

def test_pack_list_has_11(call_tool):
    r = call_tool("xforge_pack_list", {})
    assert r["ok"] is True
    assert r["count"] >= 11
    ids = [p["id"] for p in r["packs"]]
    assert "xforge-fiscal" in ids
    assert "xforge-hr" in ids
    assert "xforge-erp" in ids


def test_pack_install_fiscal(call_tool):
    r = call_tool("xforge_pack_install", {"id": "xforge-fiscal"})
    assert r["ok"] is True
    assert r["filesInstalled"] >= 1
    assert r["registered"] is True
    dest = Path(r"D:\dev\XForge-Development-New\.xforge\knowledge\packs\xforge-fiscal")
    assert dest.exists()
    assert any(dest.rglob("*.md"))


def test_pack_uninstall_removes_files(call_tool):
    call_tool("xforge_pack_install", {"id": "xforge-erp"})
    r = call_tool("xforge_pack_uninstall", {"id": "xforge-erp"})
    assert r["ok"] is True
    assert r["filesRemoved"] >= 1


def test_pack_install_nonexistent(call_tool):
    r = call_tool("xforge_pack_install", {"id": "xforge-nonexistent"})
    assert r["ok"] is False