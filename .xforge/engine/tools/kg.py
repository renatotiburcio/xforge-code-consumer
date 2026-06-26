"""
Knowledge Graph tools - query relationships between XForge entities.

Extraido/CRIADO em v3.11.3 per DR-0097 (Knowledge Graph Expansion per 17-GCF).
Contem: 3 tools (query, path, related) + load_graph helper.
"""
import json
from collections import deque
from .common import _ok, _err


def load_graph():
    """Load knowledge graph from JSON file."""
    from pathlib import Path
    from .common import KNOWLEDGE
    graph_path = KNOWLEDGE / "graph.json"
    if not graph_path.exists():
        return None
    try:
        return json.loads(graph_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _index_by_id(graph):
    """Build node lookup index."""
    return {n["id"]: n for n in graph.get("nodes", [])}


def _adjacency(graph):
    """Build adjacency list (outgoing edges by source)."""
    adj = {}
    for e in graph.get("edges", []):
        adj.setdefault(e["source"], []).append(e)
    return adj


def tool_graph_query(args):
    """Query nodes by type/domain/trustScore."""
    graph = load_graph()
    if graph is None:
        return _err("graph.json not found")
    node_type = args.get("type")
    domain = args.get("domain")
    min_trust = args.get("minTrust", 0)
    results = []
    for n in graph.get("nodes", []):
        if node_type and n.get("type") != node_type:
            continue
        if domain and n.get("domain") != domain:
            continue
        ts = n.get("trustScore", 0)
        if ts < min_trust:
            continue
        results.append(n)
    return _ok(count=len(results), nodes=results)


def tool_graph_related(args):
    """Find nodes related to a given node via direct edges."""
    graph = load_graph()
    if graph is None:
        return _err("graph.json not found")
    nid = args.get("id")
    if not nid:
        return _err("id required")
    adj = _adjacency(graph)
    reverse = {}
    for e in graph.get("edges", []):
        reverse.setdefault(e["target"], []).append(e)
    out = [e for e in adj.get(nid, []) if e["source"] == nid]
    inn = [e for e in reverse.get(nid, []) if e["target"] == nid]
    return _ok(id=nid, outgoing=out, incoming=inn, total=len(out) + len(inn))


def tool_graph_path(args):
    """Find shortest path between two nodes using BFS."""
    graph = load_graph()
    if graph is None:
        return _err("graph.json not found")
    src = args.get("from")
    dst = args.get("to")
    if not src or not dst:
        return _err("from and to required")
    adj = _adjacency(graph)
    visited = {src}
    queue = deque([(src, [src])])
    while queue:
        node, path = queue.popleft()
        if node == dst:
            return _ok(from_=src, to=dst, path=path, length=len(path))
        for e in adj.get(node, []):
            nxt = e["target"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return _ok(from_=src, to=dst, path=None, length=-1, reachable=False)
