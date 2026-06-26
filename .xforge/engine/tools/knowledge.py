"""
Knowledge/RAG tools - search INDEX.json and cache stats.

Extraido de xforge_engine.py em v3.9.3 per DR-0085.
"""
from .common import (
    INDEX_JSON, _load_index_cached, _index_cache_stats,
    _DOCTOR_CACHE, _DOCTOR_TTL_SEC, _ok, _err,
)


def tool_knowledge_search(args):
    """Search INDEX.json with simple substring matching."""
    q = (args.get("query") or "").strip().lower()
    if not q:
        return _err("query required")
    limit = int(args.get("limit", 20))
    if not INDEX_JSON.exists():
        return _err("INDEX.json not found")
    idx = _load_index_cached()
    if idx is None:
        return _err("INDEX.json not found or invalid")
    results = []
    for f in idx.get("files", []):
        hay = " ".join([
            f.get("path", ""), f.get("summary", ""), f.get("domain", ""),
            f.get("category", ""), " ".join(f.get("keywords", []))
        ]).lower()
        if q in hay:
            results.append(f)
            if len(results) >= limit:
                break
    return _ok(count=len(results), results=results)


def tool_index_cache_stats(args):
    """Return INDEX.json and doctor cache statistics (ADR-0015 + Fase 2.3)."""
    idx_stats = _index_cache_stats()
    return _ok(
        **idx_stats,
        doctor_hits=_DOCTOR_CACHE["hits"],
        doctor_misses=_DOCTOR_CACHE["misses"],
        doctor_ttl_sec=_DOCTOR_TTL_SEC,
    )
