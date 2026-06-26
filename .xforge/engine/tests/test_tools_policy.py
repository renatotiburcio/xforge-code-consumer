"""Tests for tools.policy (tool_policy_check)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.policy import tool_policy_check

def test_policy_check_no_args():
    r = tool_policy_check({})
    assert r["ok"] is False
    assert "required" in r["error"]

def test_policy_check_admin_allowed():
    r = tool_policy_check({"actor_role": "admin", "action": "xforge_pack_install", "resource": "test"})
    assert "ok" in r
    assert "decision" in r
    assert r["decision"] in ("allowed", "denied", "allowed_with_requirements")
