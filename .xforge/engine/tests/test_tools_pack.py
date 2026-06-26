"""Tests for tools.pack (list, install, uninstall, create)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.pack import tool_pack_list, tool_pack_install, tool_pack_uninstall, tool_pack_create
from tools.common import MARKETPLACE, PACKS_INSTALLED

def test_pack_list_returns_list():
    r = tool_pack_list({})
    assert r["ok"] is True
    assert "packs" in r
    assert isinstance(r["packs"], list)
    assert "count" in r
    assert r["count"] >= 0

def test_pack_list_marketplace():
    """Should have 20+ packs in marketplace."""
    r = tool_pack_list({})
    assert r["count"] >= 20, "expected 20+ marketplace packs"

def test_pack_install_no_id():
    r = tool_pack_install({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_pack_install_not_found():
    r = tool_pack_install({"id": "xforge-nonexistent-xyz"})
    assert r["ok"] is False
    assert "not found" in r["error"]

def test_pack_uninstall_no_id():
    r = tool_pack_uninstall({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_pack_create_no_name():
    r = tool_pack_create({})
    assert r["ok"] is False
    assert "name required" in r["error"]

def test_pack_create_invalid_prefix():
    r = tool_pack_create({"name": "invalid-pack"})
    assert r["ok"] is False
    assert "xforge-" in r["error"]

def test_pack_paths():
    assert str(MARKETPLACE).endswith("packs")
    assert str(PACKS_INSTALLED).endswith("installed.json")
