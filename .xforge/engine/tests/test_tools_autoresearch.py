"""Tests for tools.autoresearch (run, _measure_xfs)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.autoresearch import tool_autoresearch_run, _measure_xfs, _hash_row
from tools.common import AUTORESEARCH_CFG, AUTORESEARCH_RESULTS

def test_autoresearch_run_returns_result():
    r = tool_autoresearch_run({})
    assert "ok" in r

def test_measure_xfs_returns_float():
    xfs = _measure_xfs()
    assert isinstance(xfs, float)
    assert 0.0 <= xfs <= 1.0

def test_hash_row_consistent():
    """Same input should produce same hash."""
    h1 = _hash_row(["test", "a", "b", "c"])
    h2 = _hash_row(["test", "a", "b", "c"])
    assert h1 == h2

def test_hash_row_different():
    """Different input should produce different hash."""
    h1 = _hash_row(["test1"])
    h2 = _hash_row(["test2"])
    assert h1 != h2

def test_autoresearch_paths():
    assert str(AUTORESEARCH_CFG).endswith("config.json")
    assert str(AUTORESEARCH_RESULTS).endswith("results.tsv")
