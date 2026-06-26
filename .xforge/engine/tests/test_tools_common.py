"""Tests for tools.common (paths, caches, helpers)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.common import (
    _ok, _err, _iso_now,
    _load_index_cached, _invalidate_index_cache, _index_cache_stats,
    ROOT, WORKFLOWS, KNOWLEDGE, INDEX_JSON,
    _INDEX_CACHE, _INDEX_TTL_SEC,
    _DOCTOR_CACHE, _DOCTOR_TTL_SEC,
    _PYTEST_CACHE, _PYTEST_TTL_SEC,
)

def test_ok_envelope():
    r = _ok(test=1)
    assert r.get("ok") is True
    assert r.get("test") == 1

def test_err_envelope():
    r = _err("oops")
    assert r["ok"] is False
    assert r["error"] == "oops"

def test_iso_now_format():
    s = _iso_now()
    assert "T" in s
    assert s.endswith("Z") or "+" in s

def test_index_cache_stats():
    stats = _index_cache_stats()
    assert "hits" in stats
    assert "misses" in stats
    assert "ttl_sec" in stats
    assert "size_bytes" in stats
    assert stats["ttl_sec"] == _INDEX_TTL_SEC

def test_invalidate_index_cache():
    _load_index_cached()
    _invalidate_index_cache()
    assert _INDEX_CACHE["data"] is None

def test_paths_exist():
    assert ROOT.exists()
    assert WORKFLOWS.exists()
    assert KNOWLEDGE.exists()
    assert INDEX_JSON.exists()

def test_cache_ttl_constants():
    assert _INDEX_TTL_SEC > 0
    assert _DOCTOR_TTL_SEC > 0
    assert _PYTEST_TTL_SEC > 0


# === v3.13.0 additional tests for common module (DR-0103) ===

def test_ok_with_error_key():
    r = _ok(ok=True, custom="value")
    assert r["ok"] is True
    assert r["custom"] == "value"

def test_err_envelope():
    r = _err("something failed")
    assert r["ok"] is False
    assert r["error"] == "something failed"

def test_iso_now_format():
    s = _iso_now()
    assert isinstance(s, str)
    assert "T" in s  # ISO 8601 separator

def test_paths_exist():
    # All root paths should be Path objects
    from pathlib import Path
    assert isinstance(ROOT, Path)
    assert isinstance(KNOWLEDGE, Path)
    assert isinstance(INDEX_JSON, Path)
    assert str(ROOT).endswith("XForge-Development-New")

def test_cache_constants_valid():
    assert isinstance(_INDEX_TTL_SEC, float)
    assert _INDEX_TTL_SEC > 0
    assert isinstance(_DOCTOR_TTL_SEC, float)
    assert _DOCTOR_TTL_SEC > 0
    assert isinstance(_PYTEST_TTL_SEC, float)
    assert _PYTEST_TTL_SEC > 0

def test_cache_invalidation():
    _invalidate_index_cache()
    r = _index_cache_stats()
    assert "hits" in r
    assert "misses" in r
    assert r["ttl_sec"] == _INDEX_TTL_SEC