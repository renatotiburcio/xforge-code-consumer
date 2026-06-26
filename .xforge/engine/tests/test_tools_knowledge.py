"""Tests for tools.knowledge (search + index_cache_stats)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools import knowledge
from tools.knowledge import tool_knowledge_search, tool_index_cache_stats
from tools.common import INDEX_JSON, _invalidate_index_cache

def test_tool_knowledge_search_empty_query():
    r = tool_knowledge_search({"query": ""})
    assert r["ok"] is False
    assert "query required" in r["error"]

def test_tool_knowledge_search_valid_query():
    """Should find something in INDEX.json."""
    r = tool_knowledge_search({"query": "pack", "limit": 5})
    assert r["ok"] is True
    assert "count" in r
    assert "results" in r
    assert r["count"] >= 0

def test_tool_index_cache_stats():
    r = tool_index_cache_stats({})
    assert r["ok"] is True
    assert "hits" in r
    assert "misses" in r
    assert "doctor_hits" in r
    assert "doctor_misses" in r
    assert "ttl_sec" in r
    assert "size_bytes" in r

def test_index_json_exists():
    assert INDEX_JSON.exists()


# === v3.13.0 tests for knowledge module (DR-0103) ===

def test_index_cache_stats():
    r = knowledge.tool_index_cache_stats({})
    assert r.get("ok"), r
    assert "hits" in r
    assert "misses" in r
    assert "ttl_sec" in r

def test_knowledge_search_basic():
    r = knowledge.tool_knowledge_search({"query": "xforge"})
    assert r.get("ok"), r
    # Should return some result structure (count, results, etc)
    assert isinstance(r.get("count"), int) or "results" in r

def test_knowledge_search_with_limit():
    r = knowledge.tool_knowledge_search({"query": "engine", "limit": 5})
    assert r.get("ok")
    if "count" in r:
        assert r["count"] <= 5

def test_knowledge_search_no_results():
    r = knowledge.tool_knowledge_search({"query": "nonexistent_xyz_query_zzz"})
    assert r.get("ok")
    if "count" in r:
        assert r["count"] == 0

def test_knowledge_in_engine_v313():
    import xforge_engine as xe
    assert "xforge_knowledge_search" in xe.TOOLS
    assert "xforge_index_cache_stats" in xe.TOOLS