# Extended tests for knowledge graph tools (v3.11.5)

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_graph_query_by_type():
    from tools.kg import tool_graph_query
    result = tool_graph_query({"type": "skill"})
    assert result.get("ok"), result
    assert result.get("count", 0) > 0

def test_graph_query_unknown_type():
    from tools.kg import tool_graph_query
    result = tool_graph_query({"type": "nonexistent-xyz"})
    assert result.get("count", 0) == 0

def test_graph_related():
    from tools.kg import tool_graph_related
    result = tool_graph_related({"id": "pack:xforge-blazor"})
    assert result.get("ok"), result
    assert result.get("total", 0) > 0, "should have related nodes"

def test_graph_related_missing_id():
    from tools.kg import tool_graph_related
    result = tool_graph_related({})
    assert not result.get("ok", True), "missing id should return error"

def test_graph_path_real():
    from tools.kg import tool_graph_path
    result = tool_graph_path({"from": "pack:xforge-blazor", "to": "concept:SOLID"})
    assert result.get("ok"), result
    path = result.get("path", [])
    assert path[0] == "pack:xforge-blazor"
    assert path[-1] == "concept:SOLID"

def test_graph_path_missing_args():
    from tools.kg import tool_graph_path
    result = tool_graph_path({})
    assert not result.get("ok", True)

def test_graph_node_count():
    import os, json
    path = os.path.join(os.path.dirname(__file__), "..", "graph.json")
    if not os.path.exists(path):
        return
    with open(path) as f:
        data = json.load(f)
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    assert len(nodes) >= 40, "expected 40+ nodes, got " + str(len(nodes))
    assert len(edges) >= 40, "expected 40+ edges, got " + str(len(edges))

def test_graph_node_types():
    import os, json
    path = os.path.join(os.path.dirname(__file__), "..", "graph.json")
    if not os.path.exists(path):
        return
    with open(path) as f:
        data = json.load(f)
    types = set(n.get("type") for n in data.get("nodes", []))
    assert "skill" in types
    assert "concept" in types
