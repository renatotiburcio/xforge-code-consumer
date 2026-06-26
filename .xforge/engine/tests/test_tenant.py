"""Tests for multi-tenant runtime."""
import shutil
from pathlib import Path

def test_tenant_list_initial(call_tool):
    r = call_tool("xforge_tenant_list", {})
    assert r["ok"] is True
    assert r["count"] >= 1
    assert any(t["id"] == "tenant-acme" for t in r["tenants"])


def test_tenant_create_then_use(call_tool):
    tid = "test-tenant-xyz"
    r = call_tool("xforge_tenant_create", {"id": tid, "name": "Test Tenant XYZ"})
    assert r["ok"] is True
    assert r["tenant"]["id"] == tid
    r = call_tool("xforge_tenant_use", {"id": tid})
    assert r["ok"] is True
    assert r["active"] == "tenant-test-tenant-xyz"
    # Cleanup
    target = Path(r"D:\dev\XForge-Development-New\.xforge\tenants\tenant-test-tenant-xyz")
    if target.exists():
        shutil.rmtree(target)


def test_tenant_create_duplicate_fails(call_tool):
    r = call_tool("xforge_tenant_create", {"id": "acme", "name": "Dup"})
    assert r["ok"] is False
    assert "already exists" in r["error"]


def test_tenant_use_unknown(call_tool):
    r = call_tool("xforge_tenant_use", {"id": "nonexistent-zzz"})
    assert r["ok"] is False
    assert "not found" in r["error"]