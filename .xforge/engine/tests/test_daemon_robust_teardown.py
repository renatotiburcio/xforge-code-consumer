"""Robust teardown fixture for daemon tests (Sprint 11).

NOTE: All tests in this file are marked `flaky` because they exercise
the daemon start/stop lifecycle, which has inherent timing variability
on Windows (kill is async, state file write is async).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
STATE_FILE = ROOT / ".xforge" / "autoresearch" / "daemon-state.json"
CONTROL_FILE = ROOT / ".xforge" / "autoresearch" / "daemon-control.json"


@pytest.fixture(autouse=True)
def _daemon_robust_teardown():
    """Kill any leftover daemons and clean state files before AND after each test."""
    _kill_all_daemons()
    for f in (STATE_FILE, CONTROL_FILE):
        if f.exists():
            try: f.unlink()
            except: pass
    yield
    _kill_all_daemons()
    for f in (STATE_FILE, CONTROL_FILE):
        if f.exists():
            try: f.unlink()
            except: pass


def _kill_all_daemons():
    if sys.platform != "win32":
        return
    ps = "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -like '*daemon.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=10)
    except: pass
    time.sleep(0.5)


@pytest.mark.flaky
def test_robust_teardown_helper_waits_for_status(call_tool):
    """Verify the polling helper works for daemon stop."""
    r = call_tool("xforge_autoresearch_daemon", {"action": "start", "iterationsPerTick": 1})
    assert r["ok"] is True
    pid = r.get("pid")
    assert pid and pid > 0
    time.sleep(1)
    s = call_tool("xforge_autoresearch_daemon", {"action": "stop"})
    assert s["ok"] is True
    # Poll for up to 10s
    deadline = time.time() + 10
    while time.time() < deadline:
        s2 = call_tool("xforge_autoresearch_daemon", {"action": "status"})
        if s2.get("state", {}).get("status") in ("stopped", "crashed", "never_started"):
            return  # success
        time.sleep(0.5)
    pytest.fail("daemon did not stop within 10s")


@pytest.mark.flaky
def test_daemon_double_stop_is_idempotent(call_tool):
    """Calling stop twice should not raise."""
    call_tool("xforge_autoresearch_daemon", {"action": "start", "iterationsPerTick": 1})
    time.sleep(1)
    r1 = call_tool("xforge_autoresearch_daemon", {"action": "stop"})
    assert r1["ok"] is True
    time.sleep(2)
    r2 = call_tool("xforge_autoresearch_daemon", {"action": "stop"})
    assert r2["ok"] is True