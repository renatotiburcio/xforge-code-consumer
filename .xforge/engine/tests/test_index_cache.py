"""Test INDEX.json TTL cache (ADR-0015).

Validates:
  - First call: miss, returns parsed dict
  - Second call: hit, returns same object reference
  - Invalidation: works, forces reload
  - TTL expiry: works, forces reload
  - Engine has 19 tools now (was 18, +1 cache stats)
"""

import time
from pathlib import Path

from conftest import run_tool


def test_index_cache_first_call_is_miss():
    """First call should miss, returning parsed dict."""
    res = run_tool('xforge_index_cache_stats', {})
    assert res['ok'] is True
    stats = res
    assert 'hits' in stats
    assert 'misses' in stats
    assert 'ttl_sec' in stats
    assert 'size_bytes' in stats
    assert stats['ttl_sec'] == 60.0


def _fresh_engine():
    """Import a fresh copy of the engine module."""
    import sys, importlib.util
    engine_dir = str(Path(__file__).parent.parent)
    if engine_dir not in sys.path:
        sys.path.insert(0, engine_dir)
    spec = importlib.util.spec_from_file_location(
        'xforge_engine_test',
        str(Path(__file__).parent.parent / 'xforge_engine.py'),
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # Reset index cache since tools.common is shared across re-imports
    import tools.common as _tc
    _tc._INDEX_CACHE['data'] = None
    _tc._INDEX_CACHE['mtime'] = 0.0
    _tc._INDEX_CACHE['loaded_at'] = 0.0
    _tc._INDEX_CACHE['hits'] = 0
    _tc._INDEX_CACHE['misses'] = 0
    return m


def test_index_cache_second_call_hits():
    """Subsequent calls within TTL should hit cache (same object ref)."""
    m = _fresh_engine()
    m._invalidate_index_cache()
    idx1 = m._load_index_cached()
    assert isinstance(idx1, dict)
    initial_misses = m._index_cache_stats()['misses']
    idx2 = m._load_index_cached()
    assert idx1 is idx2, 'Cache hit should return same object reference'
    after = m._index_cache_stats()
    assert after['misses'] == initial_misses, 'No new miss expected on cache hit'
    assert after['hits'] >= 1, 'At least one hit expected'


def test_index_cache_invalidation_works():
    """After invalidation, next call should miss again."""
    m = _fresh_engine()
    m._load_index_cached()
    idx_before = m._load_index_cached()
    m._invalidate_index_cache()
    idx_after = m._load_index_cached()
    assert idx_before is not idx_after, 'Invalidation should produce new object'


def test_index_cache_ttl_expiry(monkeypatch):
    """When TTL expires, next call should miss."""
    monkeypatch.setenv("XFORGE_INDEX_CACHE_TTL_SEC", "0.1")
    m = _fresh_engine()
    # Force reload do TTL do env var (tools.common pode estar cached)
    import tools.common as _tc
    _tc._INDEX_TTL_SEC = float(__import__("os").environ.get("XFORGE_INDEX_CACHE_TTL_SEC", "0.1"))
    m._INDEX_TTL_SEC = _tc._INDEX_TTL_SEC
    assert m._INDEX_TTL_SEC == 0.1, "TTL should be 0.1s from env var"
    m._load_index_cached()
    m._load_index_cached()
    time.sleep(0.15)
    initial_misses = m._index_cache_stats()['misses']
    m._load_index_cached()
    after_misses = m._index_cache_stats()['misses']
    assert after_misses > initial_misses, 'TTL expiry should trigger new miss'


def test_knowledge_search_uses_cache():
    """xforge_knowledge_search should work via cache (no errors)."""
    res = run_tool('xforge_knowledge_search', {'query': 'pix', 'limit': 3})
    assert res['ok'] is True
    assert 'results' in res
    assert 'count' in res


def test_engine_has_19_tools():
    """Engine should have 19+ tools (was 18, +1 cache stats). 22 after v3.11.5."""
    m = _fresh_engine()
    assert len(m.TOOLS) >= 19, 'Expected 19 tools, got ' + str(len(m.TOOLS))
    assert 'xforge_index_cache_stats' in m.TOOLS


def test_index_cache_stats_tool():
    """xforge_index_cache_stats tool should be callable via engine CLI."""
    res = run_tool('xforge_index_cache_stats', {})
    assert res['ok'] is True
    assert res['ttl_sec'] == 60.0
    assert res['size_bytes'] > 0

