"""Test xforge_doctor TTL cache (Fase 2.3 optimization).
Doctor.ps1 is slow (~2.5s per call due to PowerShell startup).
Cache: 5s default TTL, configurable via XFORGE_DOCTOR_CACHE_TTL_SEC.
"""

import time
from pathlib import Path

from conftest import run_tool


def _fresh_engine():
    import sys, importlib.util
    engine_dir = str(Path(__file__).parent.parent)
    if engine_dir not in sys.path:
        sys.path.insert(0, engine_dir)
    spec = importlib.util.spec_from_file_location(
        'xforge_engine_doc',
        str(Path(__file__).parent.parent / 'xforge_engine.py'),
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # Reset cache state since tools.common._DOCTOR_CACHE persists across re-imports
    import tools.common as _tc
    _tc._DOCTOR_CACHE['result'] = None
    _tc._DOCTOR_CACHE['expires_at'] = 0.0
    return m


def test_doctor_first_call_is_miss():
    """First call should miss, invoking PowerShell."""
    m = _fresh_engine()
    res = m.tool_doctor_run({})
    assert res['ok'] is True
    assert res.get('cached') is False, 'First call should not be cached'
    assert res.get('cache_ttl_sec') == 5.0, 'Default TTL should be 5s'
    assert res.get('exitCode') == 0, 'Doctor should pass'


def test_doctor_second_call_is_hit():
    """Second call within TTL should hit cache, no PowerShell."""
    m = _fresh_engine()
    r1 = m.tool_doctor_run({})
    assert r1.get('cached') is False
    r2 = m.tool_doctor_run({})
    assert r2.get('cached') is True, 'Second call should be cached'
    assert r1.get('exitCode') == r2.get('exitCode')
    assert r1.get('stdout') == r2.get('stdout')


def test_doctor_cache_faster_than_miss():
    """Cache hit should be significantly faster than miss."""
    m = _fresh_engine()
    t0 = time.time()
    m.tool_doctor_run({})  # miss
    miss_ms = (time.time() - t0) * 1000
    t0 = time.time()
    m.tool_doctor_run({})  # hit
    hit_ms = (time.time() - t0) * 1000
    assert hit_ms * 10 < miss_ms, ('Hit ({:.1f}ms) should be >= 10x faster than miss ({:.1f}ms)').format(hit_ms, miss_ms)


def test_doctor_cache_expiry():
    """After manual cache invalidation, next call should miss again.

    Uses manual invalidation (not TTL) because doctor.ps1 takes ~2.5s
    which races with short TTLs.
    """
    m = _fresh_engine()
    r1 = m.tool_doctor_run({})
    assert r1.get("cached") is False, "First call must miss"
    r2 = m.tool_doctor_run({})
    assert r2.get("cached") is True, "Second call should hit"
    # Manually invalidate the cache
    m._DOCTOR_CACHE["result"] = None
    m._DOCTOR_CACHE["expires_at"] = 0.0
    r3 = m.tool_doctor_run({})
    assert r3.get("cached") is False, "After manual invalidation, should miss again"


def test_doctor_stats_in_cache_stats():
    """Doctor cache stats should be exposed via xforge_index_cache_stats."""
    res = run_tool('xforge_index_cache_stats', {})
    assert res['ok'] is True
    assert 'doctor_hits' in res
    assert 'doctor_misses' in res
    assert 'doctor_ttl_sec' in res
    assert res['doctor_ttl_sec'] == 5.0


def test_doctor_via_subprocess():
    """Doctor should be callable via subprocess (cache miss OK)."""
    res = run_tool('xforge_doctor', {})
    assert res['ok'] is True
    assert res.get('exitCode') == 0

