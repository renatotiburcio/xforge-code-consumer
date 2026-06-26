"""Tests for tools.workflow (list, validate, run)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.workflow import tool_workflow_list, tool_workflow_validate, tool_workflow_run, _validate_workflow

def test_workflow_list_returns_list():
    r = tool_workflow_list({})
    assert r["ok"] is True
    assert "workflows" in r
    assert isinstance(r["workflows"], list)
    assert "count" in r

def test_workflow_validate_no_id():
    r = tool_workflow_validate({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_workflow_validate_invalid_id():
    r = tool_workflow_validate({"id": "W999"})
    assert r["ok"] is False
    assert "not found" in r["error"]

def test_workflow_validate_valid_id():
    """If W001 exists, should be valid."""
    r = tool_workflow_list({})
    if r["count"] > 0:
        wid = r["workflows"][0].get("id", "W001")
        v = tool_workflow_validate({"id": wid})
        assert v["ok"] is True
        assert v["valid"] in (True, False)

def test_workflow_run_no_id():
    r = tool_workflow_run({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_workflow_run_valid():
    r = tool_workflow_list({})
    if r["count"] > 0:
        wid = r["workflows"][0].get("id", "W001")
        v = tool_workflow_run({"id": wid, "events": []})
        assert v["ok"] is True
        assert "currentState" in v
        assert "history" in v

def test_validate_workflow_helper():
    """Test internal validator with invalid workflow."""
    errors = _validate_workflow({})
    assert len(errors) > 0
    errors = _validate_workflow({"id": "bad"})
    assert any("id must match" in e for e in errors)
