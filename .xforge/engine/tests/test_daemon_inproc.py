"""Tests for in-process engine dispatch in daemon.py (Sprint 22).

The daemon can dispatch 3 cacheable tools directly in-process
without spawning a subprocess:
  - xforge_knowledge_search: search INDEX.json
  - xforge_workflow_list: list .xforge/workflows/*.yaml
  - xforge_workflow_validate: validate a workflow

This eliminates ~500ms subprocess startup overhead per call,
giving 4-7x speedup over cold start.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
ENGINE_DIR = ROOT / ".xforge" / "engine"
DAEMON_PY = ENGINE_DIR / "daemon.py"
DAEMON_CLI = ENGINE_DIR / "daemon_cli.py"
STATE_FILE = ENGINE_DIR / "daemon-state.json"
PYTHON = sys.executable


def _cli(*args, timeout=30):
    r = subprocess.run([PYTHON, str(DAEMON_CLI), *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def _kill_daemon():
    if STATE_FILE.exists():
        try:
            st = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            pid = st.get("pid")
            if pid:
                try:
                    import ctypes
                    k = ctypes.windll.kernel32
                    h = k.OpenProcess(0x0001, False, pid)
                    if h:
                        k.TerminateProcess(h, 1)
                        k.CloseHandle(h)
                except Exception:
                    pass
        except Exception:
            pass
        try:
            STATE_FILE.unlink()
        except Exception:
            pass
    for f in (ENGINE_DIR / "daemon.pid", ENGINE_DIR / "daemon-control.json"):
        try:
            f.unlink(missing_ok=True)
        except Exception:
            pass
    time.sleep(0.3)


@pytest.fixture(autouse=True)
def cleanup():
    _kill_daemon()
    yield
    _kill_daemon()


def test_inproc_constants_defined():
    code = DAEMON_PY.read_text(encoding="utf-8")
    assert "IN_PROCESS_TOOLS" in code
    assert "xforge_knowledge_search" in code
    assert "xforge_workflow_list" in code
    assert "xforge_workflow_validate" in code
    assert "_in_process_tool" in code


def test_inproc_workflow_list_returns_dict():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_workflow_list({})
    assert result.get("ok") is True
    assert result.get("count", 0) >= 15
    assert "workflows" in result
    assert result["workflows"][0].get("id") in ("W001", "W002", "W003")


def test_inproc_knowledge_search_returns_dict():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_knowledge_search({"query": "blazor", "limit": 5})
    assert result.get("ok") is True
    assert result.get("count", 0) >= 1
    for r in result.get("results", []):
        assert "path" in r
        assert "blazor" in r["path"].lower() or "blazor" in r.get("summary", "").lower() or any("blazor" in k for k in r.get("keywords", []))


def test_inproc_knowledge_search_empty_query():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_knowledge_search({})
    assert result.get("ok") is False
    assert "query" in result.get("error", {}).get("message", "").lower()


def test_inproc_workflow_validate_w001():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_workflow_validate({"id": "W001"})
    assert result.get("ok") is True, f"validate W001: {result}"
    assert result.get("id") == "W001"
    assert result.get("states", 0) > 0
    assert result.get("transitions", 0) > 0
    assert result.get("errors") == []


def test_inproc_workflow_validate_missing_id():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_workflow_validate({})
    assert result.get("ok") is False
    assert result.get("error", {}).get("code") == "BAD_REQUEST"


def test_inproc_workflow_validate_unknown_id():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_workflow_validate({"id": "W999"})
    assert result.get("ok") is False
    assert result.get("error", {}).get("code") == "NOT_FOUND"


def test_inproc_tool_dispatch_returns_none_for_unknown():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon
    result = daemon._in_process_tool("xfs_measure", {})
    assert result is None


def test_inproc_dispatch_via_daemon_call_under_200ms():
    """End-to-end: in-process call via daemon should be < 200ms (was ~565ms subprocess)."""
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    times = []
    for i in range(3):
        t0 = time.time()
        code, out, err = _cli("call", "xforge_workflow_list", "{}", timeout=30)
        elapsed_ms = (time.time() - t0) * 1000
        times.append(elapsed_ms)
        assert code == 0
        data = json.loads(out)
        assert data.get("ok") is True
    avg = sum(times) / len(times)
    assert avg < 200, f"avg {avg:.1f}ms exceeds 200ms (subprocess was ~565ms)"


def test_inproc_knowledge_search_via_daemon_under_200ms():
    args_file = ENGINE_DIR / ".tmp-search-args-blazor.json"
    args_file.write_text(json.dumps({"query": "blazor", "limit": 3}), encoding="utf-8")
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    t0 = time.time()
    code, out, err = _cli("call", "xforge_knowledge_search", "@" + str(args_file), timeout=30)
    elapsed_ms = (time.time() - t0) * 1000
    args_file.unlink(missing_ok=True)
    assert code == 0
    data = json.loads(out)
    assert data.get("ok") is True
    assert elapsed_ms < 200, f"knowledge_search {elapsed_ms:.1f}ms exceeds 200ms (was ~565ms subprocess)"


def test_inproc_validate_via_daemon_under_200ms():
    args_file = ENGINE_DIR / ".tmp-validate-args-w001.json"
    args_file.write_text(json.dumps({"id": "W001"}), encoding="utf-8")
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    t0 = time.time()
    code, out, err = _cli("call", "xforge_workflow_validate", "@" + str(args_file), timeout=30)
    elapsed_ms = (time.time() - t0) * 1000
    args_file.unlink(missing_ok=True)
    assert code == 0
    data = json.loads(out)
    assert data.get("ok") is True
    assert elapsed_ms < 200, f"workflow_validate {elapsed_ms:.1f}ms exceeds 200ms (was ~565ms subprocess)"


def test_cmd_call_supports_at_filepath():
    """cmd_call should accept @filepath for args (not just inline JSON)."""
    args_file = ENGINE_DIR / ".tmp-cmd-call-args.json"
    args_file.write_text(json.dumps({"query": "pix", "limit": 2}), encoding="utf-8")
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("call", "xforge_knowledge_search", "@" + str(args_file), timeout=30)
    args_file.unlink(missing_ok=True)
    assert code == 0
    data = json.loads(out)
    assert data.get("ok") is True
    assert "query" not in str(data.get("error", "")).lower() or "required" not in str(data.get("error", ""))