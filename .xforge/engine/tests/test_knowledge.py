"""Tests for knowledge search."""


def test_knowledge_search_finds_results(call_tool):
    r = call_tool("xforge_knowledge_search", {"query": "nfe", "limit": 5})
    assert r["ok"] is True
    assert r["count"] >= 1


def test_knowledge_search_empty_query_fails(call_tool):
    r = call_tool("xforge_knowledge_search", {"query": ""})
    assert r["ok"] is False


def test_knowledge_search_finds_pack_content(call_tool):
    call_tool("xforge_pack_install", {"id": "xforge-fiscal"})
    r = call_tool("xforge_knowledge_search", {"query": "sped"})
    assert r["ok"] is True
    paths = [res["path"] for res in r["results"]]
    assert any("xforge-fiscal" in p for p in paths)