"""Tests for Sprint 21 knowledge reindex (Sprint 16 packs now have real content)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
ENGINE_DIR = ROOT / ".xforge" / "engine"
PACKS_DIR = ROOT / ".xforge" / "knowledge" / "packs"
INDEX_JSON = ROOT / ".xforge" / "knowledge" / "INDEX.json"
PYTHON = sys.executable

SPRINT16_PACKS = [
    "xforge-blazor",
    "xforge-pix",
    "xforge-cnab",
    "xforge-testing",
    "xforge-architecture",
]


def test_sprint16_pack_directories_exist():
    for pack in SPRINT16_PACKS:
        assert (PACKS_DIR / pack).is_dir(), f"missing pack dir: {pack}"


def test_sprint16_pack_files_exist():
    """Each Sprint 16 pack should have at least 3 real .md files."""
    for pack in SPRINT16_PACKS:
        md_files = list((PACKS_DIR / pack).glob("*.md"))
        assert len(md_files) >= 3, f"{pack} has only {len(md_files)} files: {[f.name for f in md_files]}"


def test_sprint16_pack_files_have_real_content():
    """Each file should be non-trivial (>= 500 bytes)."""
    for pack in SPRINT16_PACKS:
        for md_file in (PACKS_DIR / pack).glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            assert len(content) >= 500, f"{md_file.name} too small: {len(content)} bytes"


def test_index_json_files_field_includes_sprint16_packs():
    idx = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    files = idx.get("files", [])
    paths = [f["path"] for f in files]
    for pack in SPRINT16_PACKS:
        pack_files = [p for p in paths if pack in p]
        assert len(pack_files) >= 3, f"{pack} has {len(pack_files)} files in INDEX, expected >=3: {pack_files}"


def test_engine_knowledge_search_finds_blazor():
    args_file = ROOT / ".xforge" / "engine" / ".tmp-search-args.json"
    args_file.write_text(json.dumps({"query": "blazor", "limit": 10}), encoding="utf-8")
    r = subprocess.run(
        [PYTHON, str(ENGINE_DIR / "xforge_engine.py"), "xforge_knowledge_search", "@" + str(args_file)],
        capture_output=True, text=True, timeout=30,
    )
    args_file.unlink(missing_ok=True)
    assert r.returncode == 0, f"engine failed: {r.stderr}"
    data = json.loads(r.stdout)
    assert data.get("ok") is True
    assert data.get("count", 0) >= 3, f"expected >=3 blazor hits, got {data.get('count')}"


def test_engine_knowledge_search_finds_pix():
    args_file = ROOT / ".xforge" / "engine" / ".tmp-search-args.json"
    args_file.write_text(json.dumps({"query": "pix", "limit": 10}), encoding="utf-8")
    r = subprocess.run(
        [PYTHON, str(ENGINE_DIR / "xforge_engine.py"), "xforge_knowledge_search", "@" + str(args_file)],
        capture_output=True, text=True, timeout=30,
    )
    args_file.unlink(missing_ok=True)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("count", 0) >= 3


def test_engine_knowledge_search_finds_cnab():
    args_file = ROOT / ".xforge" / "engine" / ".tmp-search-args.json"
    args_file.write_text(json.dumps({"query": "cnab", "limit": 10}), encoding="utf-8")
    r = subprocess.run(
        [PYTHON, str(ENGINE_DIR / "xforge_engine.py"), "xforge_knowledge_search", "@" + str(args_file)],
        capture_output=True, text=True, timeout=30,
    )
    args_file.unlink(missing_ok=True)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("count", 0) >= 3


def test_engine_knowledge_search_finds_architecture():
    args_file = ROOT / ".xforge" / "engine" / ".tmp-search-args.json"
    args_file.write_text(json.dumps({"query": "bounded context", "limit": 10}), encoding="utf-8")
    r = subprocess.run(
        [PYTHON, str(ENGINE_DIR / "xforge_engine.py"), "xforge_knowledge_search", "@" + str(args_file)],
        capture_output=True, text=True, timeout=30,
    )
    args_file.unlink(missing_ok=True)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data.get("count", 0) >= 1