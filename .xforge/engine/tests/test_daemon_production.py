"""Tests for the XForge PRODUCTION daemon (daemon.py + daemon_cli.py).

These tests verify the real production daemon:
  - ping works
  - start/stop/status work
  - file-queue call works
  - cache hit works
  - benchmark works

Each test ensures cleanup so the daemon doesn't leak across runs.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
ENGINE_DIR = ROOT / ".xforge" / "engine"
DAEMON_PY = ENGINE_DIR / "daemon.py"
DAEMON_CLI = ENGINE_DIR / "daemon_cli.py"
STATE_FILE = ENGINE_DIR / "daemon-state.json"
CONTROL_FILE = ENGINE_DIR / "daemon-control.json"
PID_FILE = ENGINE_DIR / "daemon.pid"
LOG_FILE = ENGINE_DIR / "daemon.log"
REQUESTS_DIR = ENGINE_DIR / "daemon-requests"
RESPONSES_DIR = ENGINE_DIR / "daemon-responses"
PYTHON = sys.executable


def _cli(*args, timeout=30):
    r = subprocess.run([PYTHON, str(DAEMON_CLI), *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def _kill_daemon():
    """Force-kill any leftover daemon and clean state."""
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
    for f in (CONTROL_FILE, PID_FILE):
        try:
            f.unlink(missing_ok=True)
        except Exception:
            pass
    time.sleep(0.3)


@pytest.fixture(autouse=True)
def cleanup_before_and_after():
    _kill_daemon()
    yield
    _kill_daemon()


def test_daemon_files_exist():
    assert DAEMON_PY.exists(), f"daemon.py missing: {DAEMON_PY}"
    assert DAEMON_CLI.exists(), f"daemon_cli.py missing: {DAEMON_CLI}"
    code_d = DAEMON_PY.read_text(encoding="utf-8")
    code_c = DAEMON_CLI.read_text(encoding="utf-8")
    assert "TTLCache" in code_d
    assert "DaemonState" in code_d
    assert "serve_file_queue" in code_d
    assert "control_loop" in code_d
    assert "HANDLERS" in code_c
    assert "cmd_start" in code_c
    assert "cmd_stop" in code_c
    assert "cmd_call" in code_c
    assert "cmd_benchmark" in code_c


def test_daemon_ping():
    code, out, err = _cli("ping", timeout=15)
    assert code == 0, f"ping failed: {err}"
    data = json.loads(out)
    assert data["ok"] is True
    assert data["pong"] is True
    assert "version" in data
    assert "latencyMs" in data


def test_daemon_start_status_stop():
    code, out, err = _cli("start", timeout=15)
    assert code == 0, f"start failed: {err}"
    data = json.loads(out)
    assert data["ok"] is True
    pid = data["daemonPid"]
    assert pid > 0
    time.sleep(1)
    code, out, err = _cli("status", timeout=10)
    assert code == 0
    data = json.loads(out)
    assert data["running"] is True
    assert data["state"]["alive"] is True
    code, out, err = _cli("stop", timeout=15)
    assert code == 0
    data = json.loads(out)
    assert data["ok"] is True
    assert data["stopped"] is True
    time.sleep(0.5)
    code, out, err = _cli("status", timeout=10)
    data = json.loads(out)
    assert data["running"] is False


def test_daemon_call_returns_result():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("call", "xforge_workflow_list", "{}", timeout=30)
    assert code == 0, f"call failed: {err}"
    data = json.loads(out)
    assert data.get("ok") is True, f"call returned: {data}"
    if isinstance(data.get("result"), dict) and "workflows" in data["result"]:
        assert data["result"]["count"] >= 15
    elif "count" in data and "workflows" in data:
        assert data["count"] >= 15


def test_daemon_call_caches_repeat():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    _cli("call", "xforge_workflow_list", "{}", timeout=30)
    time.sleep(1)
    _cli("call", "xforge_workflow_list", "{}", timeout=30)
    time.sleep(1)
    code, out, err = _cli("status", timeout=10)
    data = json.loads(out)
    cache = data["state"]["cache"]
    assert cache["hits"] >= 1, f"expected cache hit, got: {cache}"
    assert cache["size"] >= 1


def test_daemon_list_shows_recent():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    _cli("call", "xforge_workflow_list", "{}", timeout=30)
    time.sleep(1)
    code, out, err = _cli("list", timeout=10)
    data = json.loads(out)
    assert data["ok"] is True
    assert data["state"]["requestCount"] >= 1
    assert data["count"] >= 1
    assert data["requests"][0]["tool"] == "xforge_workflow_list"


def test_daemon_benchmark_runs():
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("benchmark", "2", timeout=120)
    assert code == 0, f"benchmark failed: {err}"
    data = json.loads(out)
    assert data["ok"] is True
    assert data["iterations"] == 2
    assert "cold" in data
    assert "warm" in data
    assert "avgMs" in data["cold"]
    assert len(data["cold"]["times"]) == 2
    assert data["warm"] is not None
    assert data["warm"]["avgMs"] > 0


def test_daemon_installer_help():
    code, out, err = subprocess.run([PYTHON, str(ENGINE_DIR / "daemon_installer.py")], capture_output=True, text=True, timeout=10).returncode, subprocess.run([PYTHON, str(ENGINE_DIR / "daemon_installer.py")], capture_output=True, text=True, timeout=10).stdout, ""
    assert code == 0
    data = json.loads(out)
    assert "usage" in data
    assert "install" in data["usage"]
    assert "uninstall" in data["usage"]


def test_daemon_install_dry_run():
    code, out, err = subprocess.run([PYTHON, str(ENGINE_DIR / "daemon_installer.py"), "status"], capture_output=True, text=True, timeout=10).returncode, subprocess.run([PYTHON, str(ENGINE_DIR / "daemon_installer.py"), "status"], capture_output=True, text=True, timeout=10).stdout, ""
    assert code == 0
    data = json.loads(out)
    assert data.get("ok") is True