"""Tests for tools.rbac (tool_rbac_check)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.rbac import tool_rbac_check, _role_chain

def test_rbac_check_no_args():
    r = tool_rbac_check({})
    assert r["ok"] is False
    assert "required" in r["error"]

def test_rbac_check_valid():
    r = tool_rbac_check({"role": "admin", "action": "xforge_pack_install"})
    assert "ok" in r
    assert "role" in r
    assert "action" in r
    assert "allowed" in r
    assert "reason" in r

def test_rbac_check_unknown_role():
    r = tool_rbac_check({"role": "unknown_role_xyz", "action": "test"})
    assert r["ok"] is False
    assert "unknown role" in r["error"]

def test_role_chain_helper():
    """Empty config returns single-element chain."""
    rbac = {"roles": {"admin": {"inherits": []}}}
    chain = _role_chain(rbac, "admin")
    assert "admin" in chain
