#!/usr/bin/env python
"""daemon_installer.py - One-line setup for XForge production daemon."""
import json, os, platform, subprocess, sys
from pathlib import Path
ENGINE_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable
DAEMON_SCRIPT = ENGINE_DIR / "daemon.py"
CLI = ENGINE_DIR / "daemon_cli.py"


def run(args, check=True):
    r = subprocess.run(args, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("command failed: " + " ".join(args) + "\n" + r.stderr)
    return r


def install(autostart=True):
    steps = []
    steps.append({"step": "verify_python", "ok": True, "python": PYTHON, "version": sys.version.split()[0]})
    if not DAEMON_SCRIPT.exists():
        raise FileNotFoundError("daemon.py not found: " + str(DAEMON_SCRIPT))
    steps.append({"step": "verify_daemon_script", "ok": True, "path": str(DAEMON_SCRIPT)})
    if not CLI.exists():
        raise FileNotFoundError("daemon_cli.py not found: " + str(CLI))
    steps.append({"step": "verify_cli", "ok": True, "path": str(CLI)})
    ping = run([PYTHON, str(DAEMON_SCRIPT), "--mode=ping"], check=False)
    steps.append({"step": "ping_test", "ok": ping.returncode == 0, "stdout": ping.stdout.strip()[:200]})
    if platform.system() == "Windows" and autostart:
        reg = run([PYTHON, str(CLI), "install"], check=False)
        try:
            steps.append({"step": "register_autostart", "ok": json.loads(reg.stdout).get("ok", False), "output": reg.stdout.strip()[:200]})
        except Exception:
            steps.append({"step": "register_autostart", "ok": False, "error": reg.stderr.strip()[:200]})
    if platform.system() == "Windows":
        r = run([PYTHON, str(CLI), "start"], check=False)
        try:
            steps.append({"step": "start_daemon", "ok": json.loads(r.stdout).get("ok", False), "output": r.stdout.strip()[:200]})
        except Exception:
            steps.append({"step": "start_daemon", "ok": False, "error": r.stderr.strip()[:200]})
    return {"ok": True, "platform": platform.system(), "python": PYTHON, "engineDir": str(ENGINE_DIR), "steps": steps}


def uninstall():
    steps = []
    if platform.system() == "Windows":
        r = run([PYTHON, str(CLI), "stop"], check=False)
        try:
            steps.append({"step": "stop_daemon", "ok": json.loads(r.stdout).get("ok", False)})
        except Exception:
            pass
        r = run([PYTHON, str(CLI), "uninstall"], check=False)
        try:
            steps.append({"step": "remove_autostart", "ok": json.loads(r.stdout).get("ok", False)})
        except Exception:
            pass
    for fname in ("daemon-state.json", "daemon.pid", "daemon-control.json", "daemon.log"):
        p = ENGINE_DIR / fname
        if p.exists():
            try:
                p.unlink()
                steps.append({"step": "cleanup", "ok": True, "file": fname})
            except Exception as e:
                steps.append({"step": "cleanup", "ok": False, "file": fname, "error": str(e)})
    return {"ok": True, "steps": steps}


def status():
    return json.loads(subprocess.run([PYTHON, str(CLI), "status"], capture_output=True, text=True).stdout)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(json.dumps({"usage": "daemon_installer.py <install|uninstall|status> [--no-autostart]"}, indent=2))
        sys.exit(0)
    cmd = sys.argv[1]
    autostart = "--no-autostart" not in sys.argv
    if cmd == "install":
        print(json.dumps(install(autostart=autostart), indent=2))
    elif cmd == "uninstall":
        print(json.dumps(uninstall(), indent=2))
    elif cmd == "status":
        print(json.dumps(status(), indent=2))
    else:
        print(json.dumps({"ok": False, "error": "unknown command: " + cmd}, indent=2))
        sys.exit(2)