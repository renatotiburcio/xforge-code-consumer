"""Tests for tools.kg (knowledge graph)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.kg import tool_graph_query, tool_graph_related, tool_graph_path, load_graph

def test_load_graph_exists():
    g = load_graph()
    assert g is not None
    assert "nodes" in g
    assert "edges" in g
    assert len(g["nodes"]) > 0
    assert len(g["edges"]) > 0

def test_graph_query_by_type():
    r = tool_graph_query({"type": "skill"})
    assert r["ok"] is True
    assert r["count"] >= 10
    assert all(n["type"] == "skill" for n in r["nodes"])

def test_graph_query_by_domain():
    r = tool_graph_query({"domain": "fiscal"})
    assert r["ok"] is True
    assert r["count"] >= 3
    assert all(n.get("domain") == "fiscal" for n in r["nodes"])

def test_graph_query_by_min_trust():
    r = tool_graph_query({"minTrust": 90})
    assert r["ok"] is True
    for n in r["nodes"]:
        assert n.get("trustScore", 0) >= 90

def test_graph_related():
    r = tool_graph_related({"id": "pack:xforge-fiscal"})
    assert r["ok"] is True
    assert r["total"] > 0
    assert len(r["outgoing"]) > 0  # fiscal requires skills

def test_graph_related_no_id():
    r = tool_graph_related({})
    assert r["ok"] is False
    assert "id required" in r["error"]

def test_graph_path():
    r = tool_graph_path({"from": "pack:xforge-blazor", "to": "concept:SOLID"})
    assert r["ok"] is True
    assert r["length"] > 0
    assert r["path"][0] == "pack:xforge-blazor"
    assert r["path"][-1] == "concept:SOLID"

def test_graph_path_unreachable():
    """fiscal is NOT connected to dotnet-standards, so KISS unreachable."""
    r = tool_graph_path({"from": "pack:xforge-fiscal", "to": "concept:KISS"})
    assert r["ok"] is True
    assert r["reachable"] is False
    assert r["path"] is None
    assert r["length"] == -1

def test_graph_no_graph():
    """If graph.json missing, return error."""
    import tools.kg as kg_mod
    orig_path = kg_mod.__file__
    """We test by mocking load_graph to return None."""
    orig = kg_mod.load_graph
    kg_mod.load_graph = lambda: None
    try:
        r = kg_mod.tool_graph_query({})
        assert r["ok"] is False
    finally:
        kg_mod.load_graph = orig
