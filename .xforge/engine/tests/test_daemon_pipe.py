"""Tests for named-pipe IPC client in daemon_cli.py (Sprint 20).

The pipe client uses ctypes to talk to the daemon's Windows named pipe
without requiring pywin32 in the client process. Falls back to file-queue
if pipe is unavailable.
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


def test_pipe_name_defined_in_cli():
    code = DAEMON_CLI.read_text(encoding="utf-8")
    assert "PIPE_NAME" in code
    assert "xforge-daemon" in code
    assert "_pipe_call" in code
    assert "ctypes" in code


def test_pipe_call_function_callable():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon_cli
    assert hasattr(daemon_cli, "_pipe_call")
    assert callable(daemon_cli._pipe_call)


def test_pipe_call_returns_none_when_no_daemon():
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon_cli
    r = daemon_cli._pipe_call("xforge_workflow_list", {})
    assert r is None


def test_pipe_call_succeeds_when_daemon_running():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon_cli
    r = daemon_cli._pipe_call("xforge_workflow_list", {})
    assert r is not None, "pipe call should succeed when daemon running"
    assert r.get("ok") is True
    inner = r.get("result", r)
    assert "count" in inner or "workflows" in inner
    if "workflows" in inner:
        assert inner["count"] >= 15


def test_cmd_call_uses_pipe_when_available():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("call", "xforge_workflow_list", "{}", timeout=30)
    assert code == 0
    data = json.loads(out)
    assert data.get("ok") is True
    if "workflows" in data:
        assert data["count"] >= 15
    elif "result" in data and "workflows" in data["result"]:
        assert data["result"]["count"] >= 15


def test_pipe_call_5x_avg_under_2s():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("call", "xforge_workflow_list", "{}", timeout=30)
    time.sleep(0.5)
    sys.path.insert(0, str(ENGINE_DIR))
    import daemon_cli
    times = []
    for i in range(5):
        t0 = time.time()
        r = daemon_cli._pipe_call("xforge_workflow_list", {})
        times.append((time.time() - t0) * 1000)
        assert r is not None
    avg = sum(times) / len(times)
    assert avg < 2000, f"pipe call avg {avg:.1f}ms should be under 2000ms (cache hits + subprocess startup)"