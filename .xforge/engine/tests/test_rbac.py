"""Tests for RBAC enforcement."""
def test_developer_can_create_file(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "developer", "action": "create_file"})
    assert r["ok"] is True
    assert r["allowed"] is True
    assert r["level"] == 2


def test_developer_cannot_publish(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "developer", "action": "publish"})
    assert r["ok"] is True
    assert r["allowed"] is False


def test_viewer_can_read_only(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "viewer", "action": "read"})
    assert r["allowed"] is True
    r = call_tool("xforge_rbac_check", {"role": "viewer", "action": "delete"})
    assert r["allowed"] is False


def test_owner_has_wildcard(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "owner", "action": "any_xyz"})
    assert r["allowed"] is True
    assert r["level"] == 5


def test_reviewer_inherits_developer(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "reviewer", "action": "run_tests"})
    assert r["allowed"] is True


def test_unknown_role(call_tool):
    r = call_tool("xforge_rbac_check", {"role": "hacker", "action": "publish"})
    assert r["ok"] is False
    assert "unknown role" in r["error"]