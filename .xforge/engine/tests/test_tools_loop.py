# Tests for Loop Engineer (v3.19.0 per DR-0109)
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools import loop
import xforge_engine as xe

def test_loop_state():
    r = loop.tool_loop_state({})
    assert r.get("ok")
    assert r.get("maxStepsDefault") == 10
    assert r.get("confidenceThreshold") == 0.7
    assert "stateMachine" in r

def test_loop_confidence_ok_with_data():
    r = loop.tool_loop_confidence({"observation": {"ok": True, "data": "x"}})
    assert r.get("ok")
    assert r.get("score") == 0.9
    assert r.get("above") is True

def test_loop_confidence_ok_no_data():
    r = loop.tool_loop_confidence({"observation": {"ok": True}})
    assert r.get("score") == 0.7

def test_loop_confidence_fail():
    r = loop.tool_loop_confidence({"observation": {"ok": False, "error": "x"}})
    assert r.get("score") == 0.1
    assert r.get("above") is False

def test_loop_confidence_empty():
    r = loop.tool_loop_confidence({})
    assert r.get("score") == 0.5

def test_loop_drift_empty():
    r = loop.tool_loop_detect_drift({"history": []})
    assert r.get("ok")
    assert r.get("drift") is False

def test_loop_drift_no_drift():
    history = [{"action": {"tool": "a"}}, {"action": {"tool": "b"}}, {"action": {"tool": "c"}}]
    r = loop.tool_loop_detect_drift({"history": history})
    assert r.get("drift") is False

def test_loop_drift_detected():
    history = [{"action": {"tool": "same"}}] * 3
    r = loop.tool_loop_detect_drift({"history": history})
    assert r.get("drift") is True

def test_loop_run_basic():
    r = loop.tool_loop_run({"goal": "test", "max_steps": 2})
    assert r.get("ok")
    assert r.get("steps", 0) > 0
    assert r.get("maxSteps") == 2
    assert r.get("finalConfidence") is not None
    assert r.get("stopped") is not None

def test_loop_run_in_engine():
    assert "xforge_loop_run" in xe.TOOLS
    assert "xforge_loop_state" in xe.TOOLS
    assert "xforge_loop_detect_drift" in xe.TOOLS
    assert "xforge_loop_confidence" in xe.TOOLS
    assert len(xe.TOOLS) >= 30  # was 34 in v3.19, now 37 in v3.24


# === v3.24.0: Loop Engineer v2 (progressive summarization + span_id) ===

def test_loop_run_v2_basic():
    r = loop.tool_loop_run_v2({"goal": "test", "max_steps": 3})
    assert r.get("ok"), r
    assert "steps" in r
    assert "totalSpans" in r

def test_loop_run_v2_has_span_ids():
    r = loop.tool_loop_run_v2({"goal": "test", "max_steps": 3})
    history = r.get("history", [])
    for step in history:
        assert "spanId" in step
        assert step["spanId"].startswith("span-")

def test_loop_run_v2_summarizes_long_history():
    r = loop.tool_loop_run_v2({"goal": "test", "max_steps": 5, "summarize_after": 2})
    assert r.get("ok")
    assert r.get("summary") is not None
    assert r.get("summary").get("summarizedCount", 0) > 0

def test_loop_run_v2_short_history_no_summary():
    r = loop.tool_loop_run_v2({"goal": "test", "max_steps": 2, "summarize_after": 5})
    assert r.get("ok")
    # short history: no summary needed
    assert r.get("summary") is None

def test_loop_span_id():
    r = loop.tool_loop_span_id({})
    assert r.get("ok")
    assert r["spanId"].startswith("span-")

def test_loop_summarize():
    history = [{"action": {"tool": "a"}, "observation": {"ok": True}}] * 5
    r = loop.tool_loop_summarize({"history": history, "max_steps": 2})
    assert r.get("ok")
    assert r.get("recentCount") == 2
    assert r.get("summary")["summarizedCount"] == 3

def test_loop_v2_in_engine():
    assert "xforge_loop_run_v2" in xe.TOOLS
    assert "xforge_loop_summarize" in xe.TOOLS
    assert "xforge_loop_span_id" in xe.TOOLS
    assert len(xe.TOOLS) == 37