"""Tests for workflow validation and execution."""
def test_workflow_list_returns_18(call_tool):
    r = call_tool("xforge_workflow_list", {})
    assert r["ok"] is True
    assert r["count"] == 18
    ids = [w["id"] for w in r["workflows"]]
    assert "W001" in ids and "W018" in ids


def test_workflow_validate_w001_ok(call_tool):
    r = call_tool("xforge_workflow_validate", {"id": "W001"})
    assert r["ok"] is True
    assert r["valid"] is True
    assert r["errors"] == []
    assert r["entrypoint"] == "recognized"
    assert "done" in r["terminalStates"]


def test_workflow_validate_w002_w011_after_fix(call_tool):
    """W002 had missing memorizing->done transition; W011 had typo. Both fixed."""
    for wid in ("W002", "W011"):
        r = call_tool("xforge_workflow_validate", {"id": wid})
        assert r["ok"] is True
        assert r["valid"] is True, f"{wid} errors: {r['errors']}"


def test_workflow_run_w001_full_path(call_tool):
    r = call_tool("xforge_workflow_run", {
        "id": "W001",
        "events": ["plan_created", "design_approved", "code_started", "build_passed",
                  "tests_passed", "review_approved", "docs_complete", "memory_saved", "index_updated"]
    })
    assert r["ok"] is True
    assert r["currentState"] == "done"
    assert r["terminal"] is True
    assert r["steps"] == 9


def test_workflow_run_w002_after_fix(call_tool):
    r = call_tool("xforge_workflow_run", {
        "id": "W002",
        "events": ["triage_complete", "repro_started", "repro_confirmed", "fix_applied",
                  "unit_tests_passed", "regression_test_passed", "review_approved", "memory_saved"]
    })
    assert r["ok"] is True
    assert r["currentState"] == "done"
    assert r["terminal"] is True


def test_workflow_run_invalid_event(call_tool):
    r = call_tool("xforge_workflow_run", {"id": "W001", "events": ["nonexistent_event"]})
    assert r["ok"] is False
    assert "no transition" in r["error"]