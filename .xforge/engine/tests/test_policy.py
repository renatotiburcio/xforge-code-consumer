"""Tests for policy engine + RBAC combination."""
def test_developer_fiscal_requires_reviewer(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "developer", "action": "update_file",
        "resource": ".xforge/knowledge/curated-operational/fiscal/nfe/test.md"
    })
    assert r["ok"] is True
    assert r["allowed"] is True
    assert r["decision"] == "allowed_with_requirements"
    assert any(req["required"] == "reviewer" for req in r["requirements"])


def test_reviewer_fiscal_allowed(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "reviewer", "action": "update_file",
        "resource": ".xforge/knowledge/curated-operational/fiscal/nfe/test.md"
    })
    assert r["allowed"] is True
    assert r["decision"] == "allowed"


def test_developer_modify_immutable_scoring_denied(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "developer", "action": "update_file",
        "resource": ".kilo/rules/immutable-scoring.md"
    })
    assert r["allowed"] is False
    assert r["stage"] == "policy:P002"


def test_owner_modify_immutable_scoring_allowed(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "owner", "action": "update_file",
        "resource": ".kilo/rules/immutable-scoring.md"
    })
    assert r["allowed"] is True
    # P002 appliesTo excludes owner, so owner is allowed without escalation


def test_viewer_cannot_publish(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "viewer", "action": "publish", "resource": "any"
    })
    assert r["allowed"] is False
    assert r["stage"] == "rbac"


def test_lgpd_requires_premium_provider(call_tool):
    r = call_tool("xforge_policy_check", {
        "actor_role": "owner", "action": "lgpd_request",
        "resource": "any", "context": {"provider": "local"}
    })
    assert r["allowed"] is True
    assert r["decision"] == "allowed_with_requirements"
    assert any(req["type"] == "provider" and req["required"] == "premium" for req in r["requirements"])