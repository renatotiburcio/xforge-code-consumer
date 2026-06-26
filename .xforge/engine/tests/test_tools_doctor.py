"""Tests for tools.doctor (tool_doctor_run)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.doctor import tool_doctor_run, _run_doctor_cached
from tools.common import _DOCTOR_CACHE

def test_run_doctor_cached_ok():
    r = _run_doctor_cached()
    assert "ok" in r
    assert "exitCode" in r
    assert "errors" in r
    assert "warnings" in r

def test_tool_doctor_run():
    """Integration test - runs real doctor.ps1."""
    r = tool_doctor_run({})
    assert "ok" in r
    # Cache hit should be True on second call
    r2 = tool_doctor_run({})
    assert r2.get("cached") is True

def test_doctor_cache_structure():
    assert "result" in _DOCTOR_CACHE
    assert "expires_at" in _DOCTOR_CACHE
    assert "hits" in _DOCTOR_CACHE
    assert "misses" in _DOCTOR_CACHE
