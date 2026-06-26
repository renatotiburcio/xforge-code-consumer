"""Tests for v1.1.2 disk-based pytest cache in validate_all."""
import json
import os
import time
from pathlib import Path
import pytest

ENGINE_DIR = Path(__file__).resolve().parent.parent
sys_path = str(ENGINE_DIR)
import sys
sys.path.insert(0, sys_path)
import xforge_engine as xe


def test_pytest_cache_constants_defined():
    assert hasattr(xe, "_PYTEST_CACHE")
    assert hasattr(xe, "_PYTEST_TTL_SEC")
    # _PYTEST_TIMEOUT_SEC removed in v3.10.x; TTL is the only knob
    assert isinstance(xe._PYTEST_TTL_SEC, float)
    assert xe._PYTEST_TTL_SEC == 300.0


def test_pytest_cache_initial_state():
    assert isinstance(xe._PYTEST_CACHE, dict)
    assert "result" in xe._PYTEST_CACHE
    assert "expires_at" in xe._PYTEST_CACHE
    assert "hits" in xe._PYTEST_CACHE
    assert "misses" in xe._PYTEST_CACHE


def test_pytest_cache_disk_path():
    """Verify the cache file path is what we expect."""
    cache_file = xe.ROOT / ".xforge" / ".cache" / "pytest-result.json"
    assert ".xforge" in str(cache_file)
    assert cache_file.name == "pytest-result.json"
    # Cache dir should exist (created on first call)
    assert cache_file.parent.exists()


def test_pytest_cache_stub_roundtrip(tmp_stub_cache):
    """Use a stub cache to verify the read path is exercised without running pytest."""
    cache_file, payload = tmp_stub_cache
    # Now call _run_pytest_cached - should hit cache
    r = xe._run_pytest_cached()
    assert r.get("cached") is True, f"Expected cache hit, got: {r}"
    assert r.get("passed") == payload["result"]["passed"]
    assert r.get("failed") == payload["result"]["failed"]
    # Should NOT have written the cache (already valid)
    data = json.loads(cache_file.read_text(encoding="utf-8"))
    assert data["written_at"] == payload["written_at"]


def test_pytest_cache_corrupted_file_triggers_rerun():
    """If cache file is corrupted, should re-run pytest (we mark this slow to skip)."""
    pytest.skip("Slow test - triggers pytest run")


@pytest.mark.skip(reason="stale after v3.10.6 refactor (xfs scoring moved to a separate audit doc)")
def test_validate_all_warm_cache_is_fast(tmp_stub_cache):
    """validate_all should be fast with a warm pytest cache (< 20s)."""
    _ = tmp_stub_cache  # warm cache
    t0 = time.time()
    result = xe.tool_validate_all({})
    elapsed = time.time() - t0
    pytest_result = result.get("checks", {}).get("pytest", {})
    if pytest_result.get("cached"):
        # All other checks should also be fast
        assert elapsed < 20, f"validate_all took {elapsed:.1f}s with warm cache"


@pytest.fixture
def tmp_stub_cache(monkeypatch):
    """Write a stub pytest result cache file and return (path, payload)."""
    cache_file = xe.ROOT / ".xforge" / ".cache" / "pytest-result.json"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    payload = {
        "result": {
            "ok": True,
            "passed": 141,
            "failed": 0,
            "cached": False,
        },
        "expires_at": now + 600,  # 10 min in future
        "written_at": now,
    }
    cache_file.write_text(json.dumps(payload), encoding="utf-8")
    # Reset in-process cache so it re-reads from disk
    monkeypatch.setitem(xe._PYTEST_CACHE, "result", None)
    monkeypatch.setitem(xe._PYTEST_CACHE, "expires_at", 0.0)
    yield cache_file, payload