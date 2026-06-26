"""Tests for tools.tenant (list, create, use)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.tenant import tool_tenant_list, tool_tenant_create, tool_tenant_use
from tools.common import TENANTS_DIR

def test_tenant_list_returns_list():
    r = tool_tenant_list({})
    assert r["ok"] is True
    assert "tenants" in r
    assert isinstance(r["tenants"], list)
    assert "count" in r

def test_tenant_create_no_id():
    r = tool_tenant_create({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_tenant_create_invalid_id():
    """Invalid id (starts with number) should be rejected."""
    r = tool_tenant_create({"id": "123-bad"})
    assert r["ok"] is False
    assert r["error"]  # may be kebab-case OR already-exists

def test_tenant_use_no_id():
    r = tool_tenant_use({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_tenants_dir_path():
    assert str(TENANTS_DIR).endswith("tenants")
