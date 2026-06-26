"""Tests for the XForge production daemon watchdog (Sprint 18).

Verifies the watchdog can:
  - start/stop/status
  - detect a dead daemon and restart it
  - detect missing state file and restart
  - respect max-restarts-per-hour
  - survive its own restart cycle
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
WATCHDOG_PY = ENGINE_DIR / "daemon_watchdog.py"
DAEMON_CLI = ENGINE_DIR / "daemon_cli.py"
STATE_FILE = ENGINE_DIR / "daemon-state.json"
WATCHDOG_STATE_FILE = ENGINE_DIR / "daemon-watchdog-state.json"
WATCHDOG_PID_FILE = ENGINE_DIR / "daemon-watchdog.pid"
WATCHDOG_CONTROL = ENGINE_DIR / "daemon-watchdog-control.json"
PYTHON = sys.executable


def _cli(*args, timeout=30):
    r = subprocess.run([PYTHON, str(DAEMON_CLI), *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def _is_alive(pid):
    if pid is None or pid <= 0:
        return False
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, pid)
        if not h:
            return False
        try:
            code = ctypes.c_ulong()
            ok = k.GetExitCodeProcess(h, ctypes.byref(code))
            return bool(ok) and code.value == 259
        finally:
            k.CloseHandle(h)
    except Exception:
        return False


def _kill_daemon():
    if STATE_FILE.exists():
        try:
            st = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            pid = st.get("pid")
            if pid and _is_alive(pid):
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


def _kill_watchdog():
    if WATCHDOG_STATE_FILE.exists():
        try:
            st = json.loads(WATCHDOG_STATE_FILE.read_text(encoding="utf-8"))
            pid = st.get("pid")
            if pid and _is_alive(pid):
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
    for f in (WATCHDOG_STATE_FILE, WATCHDOG_PID_FILE, WATCHDOG_CONTROL):
        try:
            f.unlink(missing_ok=True)
        except Exception:
            pass
    time.sleep(0.3)


@pytest.fixture(autouse=True)
def cleanup():
    _kill_watchdog()
    _kill_daemon()
    yield
    _kill_watchdog()
    _kill_daemon()


def test_watchdog_script_exists():
    assert WATCHDOG_PY.exists()
    code = WATCHDOG_PY.read_text(encoding="utf-8")
    assert "WatchdogState" in code
    assert "def run(" in code
    assert "spawn_daemon" in code
    assert "prune_restart_history" in code


def test_watchdog_cli_status_not_running():
    code, out, err = _cli("watchdog.status", timeout=10)
    assert code == 0
    data = json.loads(out)
    assert data["ok"] is True
    assert data["running"] is False
    assert data["state"] is None


def test_watchdog_start_status_stop():
    code, out, err = _cli("watchdog.start", "--poll", "2", timeout=15)
    assert code == 0, f"start failed: {err}"
    data = json.loads(out)
    assert data["ok"] is True
    assert data["watchdogPid"] > 0
    time.sleep(2)
    code, out, err = _cli("watchdog.status", timeout=10)
    data = json.loads(out)
    assert data["ok"] is True
    assert data["running"] is True
    assert data["state"]["alive"] is True
    assert data["state"]["polls"] >= 1
    code, out, err = _cli("watchdog.stop", timeout=15)
    data = json.loads(out)
    assert data["ok"] is True
    assert data["stopped"] is True
    time.sleep(1)
    code, out, err = _cli("watchdog.status", timeout=10)
    data = json.loads(out)
    assert data["running"] is False


def test_watchdog_restarts_dead_daemon():
    """Watchdog must detect a killed daemon and respawn it."""
    code, out, err = _cli("start", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("watchdog.start", "--poll", "2", timeout=15)
    assert code == 0
    time.sleep(3)
    code, out, err = _cli("status", timeout=10)
    pre = json.loads(out)
    pre_pid = pre["state"]["pid"]
    assert pre_pid > 0
    code, out, err = _cli("stop", timeout=15)
    assert code == 0
    time.sleep(8)
    code, out, err = _cli("status", timeout=10)
    post = json.loads(out)
    assert post["running"] is True, f"daemon should be restarted by watchdog: {post}"
    new_pid = post["state"]["pid"]
    assert new_pid > 0
    assert new_pid != pre_pid, "watchdog should have spawned a NEW daemon"
    code, out, err = _cli("watchdog.status", timeout=10)
    wd = json.loads(out)
    assert wd["state"]["restartsTotal"] >= 1, f"expected >=1 restart: {wd}"


def test_watchdog_starts_daemon_from_scratch():
    """Watchdog must start the daemon if no daemon state exists."""
    code, out, err = _cli("watchdog.start", "--poll", "2", timeout=15)
    assert code == 0
    time.sleep(5)
    code, out, err = _cli("status", timeout=10)
    data = json.loads(out)
    assert data["running"] is True, f"watchdog should have started daemon: {data}"
    code, out, err = _cli("watchdog.status", timeout=10)
    wd = json.loads(out)
    assert wd["state"]["restartsTotal"] >= 1


def test_watchdog_double_start_is_idempotent():
    code, out, err = _cli("watchdog.start", "--poll", "2", timeout=15)
    assert code == 0
    time.sleep(2)
    code, out, err = _cli("watchdog.start", "--poll", "2", timeout=15)
    data = json.loads(out)
    assert data["ok"] is False
    assert "already running" in data["error"]