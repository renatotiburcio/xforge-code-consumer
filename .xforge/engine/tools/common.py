"""
Common helpers for xforge engine tools.

Extraido de xforge_engine.py em v3.9.1 per DR-0083.
Contem: imports, ROOT constants, cache state + helpers, ok/err/iso helpers.
"""
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
import shutil

ROOT = Path(os.environ.get("XFORGE_ROOT", r"D:\dev\XForge-Development-New")).resolve()
WORKFLOWS = ROOT / ".xforge" / "workflows"
KNOWLEDGE = ROOT / ".xforge" / "knowledge"
BUSINESS = ROOT / ".xforge" / "business"
INDEX_JSON = KNOWLEDGE / "INDEX.json"
RBAC_CONFIG = ROOT / ".xforge" / "policy" / "rbac.json"
TENANTS_DIR = ROOT / ".xforge" / "tenants"
MARKETPLACE = ROOT / ".xforge" / "marketplace" / "packs"
PACKS_INSTALLED = ROOT / ".xforge" / "packs" / "installed.json"
AUTORESEARCH_CFG = ROOT / ".xforge" / "autoresearch" / "config.json"
AUTORESEARCH_RESULTS = ROOT / ".xforge" / "autoresearch" / "results.tsv"
AUTORESEARCH_EXPERIMENTS = ROOT / ".xforge" / "autoresearch" / "experiments"
AUTORESEARCH_SANDBOX = ROOT / ".xforge" / "autoresearch" / "sandbox"
SCHEMA_KNOWLEDGE = ROOT / ".xforge" / "schemas" / "knowledge.schema.json"
SCHEMA_WORKFLOW = ROOT / ".xforge" / "workflows" / "workflow.schema.json"
SCHEMAS_DIR = ROOT / ".xforge" / "schemas"
SCORING_RULE = ROOT / ".kilo" / "rules" / "immutable-scoring.md"
POLICY_ENGINE = ROOT / ".xforge" / "policy" / "engine.json"

# ADR-0015: In-process TTL cache for INDEX.json reads
_INDEX_CACHE = {"data": None, "mtime": 0.0, "loaded_at": 0.0, "hits": 0, "misses": 0}
_INDEX_TTL_SEC = float(os.environ.get("XFORGE_INDEX_CACHE_TTL_SEC", "60"))

# Doctor cache (TTL 5s)
_DOCTOR_CACHE = {"result": None, "expires_at": 0.0, "hits": 0, "misses": 0}
_DOCTOR_TTL_SEC = float(os.environ.get("XFORGE_DOCTOR_CACHE_TTL_SEC", "5"))

# Pytest cache (TTL 300s, disk-persisted)
_PYTEST_CACHE = {"result": None, "expires_at": 0.0, "runs": 0, "hits": 0, "misses": 0}
_PYTEST_TTL_SEC = float(os.environ.get("XFORGE_PYTEST_CACHE_TTL_SEC", "300"))


def _ok(**kw):
    """Standard success envelope."""
    return {"ok": True, **kw}


def _err(msg, **kw):
    """Standard error envelope."""
    return {"ok": False, "error": msg, **kw}


def _iso_now():
    return datetime.now(timezone.utc).isoformat()


def _load_index_cached():
    """Load INDEX.json with TTL+mtime cache (ADR-0015)."""
    now = time.time()
    try:
        if INDEX_JSON.exists():
            mtime = INDEX_JSON.stat().st_mtime
            cached = _INDEX_CACHE["data"]
            if cached is not None and mtime == _INDEX_CACHE["mtime"] and now - _INDEX_CACHE["loaded_at"] < _INDEX_TTL_SEC:
                _INDEX_CACHE["hits"] += 1
                return cached
        data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
        mtime = INDEX_JSON.stat().st_mtime if INDEX_JSON.exists() else 0.0
        _INDEX_CACHE.update(data=data, mtime=mtime, loaded_at=now)
        _INDEX_CACHE["misses"] += 1
        return data
    except (OSError, json.JSONDecodeError):
        return None


def _invalidate_index_cache():
    """Force next load to hit disk."""
    _INDEX_CACHE["data"] = None
    _INDEX_CACHE["mtime"] = 0.0
    _INDEX_CACHE["loaded_at"] = 0.0


def _index_cache_stats():
    return {
        "hits": _INDEX_CACHE["hits"],
        "misses": _INDEX_CACHE["misses"],
        "ttl_sec": _INDEX_TTL_SEC,
        "size_bytes": len(INDEX_JSON.read_text(encoding="utf-8")) if INDEX_JSON.exists() else 0,
    }
