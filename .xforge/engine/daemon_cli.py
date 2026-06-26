#!/usr/bin/env python
"""daemon_cli.py - Real CLI for XForge production daemon."""
import json, os, subprocess, sys, time, uuid
from pathlib import Path
ENGINE_DIR = Path(__file__).resolve().parent
DAEMON_SCRIPT = ENGINE_DIR / "daemon.py"
STATE_FILE = ENGINE_DIR / "daemon-state.json"
CONTROL_FILE = ENGINE_DIR / "daemon-control.json"
REQUESTS_DIR = ENGINE_DIR / "daemon-requests"
RESPONSES_DIR = ENGINE_DIR / "daemon-responses"
LOG_FILE = ENGINE_DIR / "daemon.log"
PID_FILE = ENGINE_DIR / "daemon.pid"
VERSION = "1.0.0"


PIPE_NAME = r"\\.\\pipe\\xforge-daemon"


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


def _pipe_call(tool, args, timeout_ms=10000):
    """Send a request to the daemon via Windows named pipe. Returns response dict or None on failure."""
    import ctypes
    from ctypes import wintypes
    GENERIC_READ_WRITE = 0xC0000000
    OPEN_EXISTING = 3
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateFileW(
        PIPE_NAME, GENERIC_READ_WRITE, 0, None, OPEN_EXISTING, 0, None,
    )
    if not handle or handle == INVALID_HANDLE_VALUE:
        return None
    try:
        req_id = uuid.uuid4().hex
        request = json.dumps({"id": req_id, "tool": tool, "args": args or {}}, ensure_ascii=False)
        data = request.encode("utf-8")
        written = wintypes.DWORD()
        if not kernel32.WriteFile(handle, data, len(data), ctypes.byref(written), None):
            return None
        if written.value != len(data):
            return None
        buf = ctypes.create_string_buffer(65536)
        read = wintypes.DWORD()
        if not kernel32.ReadFile(handle, buf, 65536, ctypes.byref(read), None):
            return None
        if read.value == 0:
            return None
        return json.loads(buf.raw[:read.value].decode("utf-8"))
    except Exception:
        return None
    finally:
        try:
            kernel32.CloseHandle(handle)
        except Exception:
            pass
for d in (REQUESTS_DIR, RESPONSES_DIR):
    d.mkdir(parents=True, exist_ok=True)

def _read_state():
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None

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
def cmd_start(args):
    state = _read_state()
    if state and state.get("status") == "running":
        pid = state.get("pid")
        if _is_alive(pid):
            return {"ok": False, "error": "daemon already running", "pid": pid, "state": state}
    if STATE_FILE.exists():
        try:
            STATE_FILE.unlink()
        except Exception:
            pass
    cf = 0x00000008 | 0x00000200
    log_fp = open(LOG_FILE, "ab", buffering=0)
    proc = subprocess.Popen(
        [sys.executable, str(DAEMON_SCRIPT), "--mode=daemon"],
        stdout=log_fp, stderr=log_fp, stdin=subprocess.DEVNULL,
        cwd=str(ENGINE_DIR), creationflags=cf, close_fds=True,
    )
    deadline = time.time() + 5.0
    while time.time() < deadline:
        if STATE_FILE.exists():
            st = _read_state()
            if st:
                return {"ok": True, "pid": proc.pid, "daemonPid": st.get("pid"), "state": st}
        time.sleep(0.1)
    return {"ok": False, "error": "daemon did not start within 5s", "pid": proc.pid}

def cmd_stop(args):
    state = _read_state()
    if not state:
        return {"ok": False, "error": "no state file; daemon not running"}
    pid = state.get("pid")
    if not _is_alive(pid):
        STATE_FILE.unlink(missing_ok=True)
        return {"ok": True, "stopped": True, "note": "process was already dead"}
    CONTROL_FILE.write_text(json.dumps({"command": "stop", "ts": time.time()}), encoding="utf-8")
    deadline = time.time() + 5.0
    while time.time() < deadline:
        time.sleep(0.2)
        s = _read_state()
        if not s or s.get("status") in ("stopped", "crashed"):
            CONTROL_FILE.unlink(missing_ok=True)
            return {"ok": True, "stopped": True, "finalState": s}
    if _is_alive(pid):
        try:
            import ctypes
            k = ctypes.windll.kernel32
            k.TerminateProcess(k.OpenProcess(1, False, pid), 1)
        except Exception:
            pass
    STATE_FILE.unlink(missing_ok=True)
    CONTROL_FILE.unlink(missing_ok=True)
    return {"ok": True, "stopped": True, "note": "force-killed after timeout"}

def cmd_status(args):
    state = _read_state()
    if not state:
        return {"ok": True, "running": False, "state": None}
    pid = state.get("pid")
    state["alive"] = _is_alive(pid)
    return {"ok": True, "running": state.get("status") == "running" and state["alive"], "state": state}

def cmd_ping(args):
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(DAEMON_SCRIPT), "--mode=ping"],
        capture_output=True, text=True, timeout=10, cwd=str(ENGINE_DIR),
    )
    latency = round((time.time() - t0) * 1000, 2)
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout.strip())
            data["latencyMs"] = latency
            return data
        except Exception:
            return {"ok": True, "pong": True, "latencyMs": latency, "raw": proc.stdout.strip()}
    return {"ok": False, "error": "ping failed", "stderr": proc.stderr.strip(), "latencyMs": latency}

def cmd_list(args):
    state = _read_state()
    if not state:
        return {"ok": True, "requests": [], "note": "daemon never started"}
    recent = state.get("recentRequests", [])
    return {"ok": True, "count": len(recent), "requests": recent[-20:], "state": {"status": state.get("status"), "pid": state.get("pid"), "requestCount": state.get("requestCount")}}

def cmd_call(args):
    if not args:
        return {"ok": False, "error": "usage: call <tool> [args-json]"}
    tool = args[0]
    raw = args[1] if len(args) > 1 else "{}"
    try:
        if raw.startswith("@"):
            with open(raw[1:], "r", encoding="utf-8") as f:
                raw = f.read().strip()
        tool_args = json.loads(raw) if raw.startswith("{") else {"path": raw}
    except Exception as e:
        return {"ok": False, "error": "invalid JSON args: " + str(e)}
    if sys.platform == "win32":
        try:
            resp = _pipe_call(tool, tool_args)
            if resp is not None:
                return resp
        except Exception:
            pass
    req_id = uuid.uuid4().hex
    REQUESTS_DIR.joinpath(req_id + ".json").write_text(
        json.dumps({"id": req_id, "tool": tool, "args": tool_args, "ts": time.time()}),
        encoding="utf-8",
    )
    resp_path = RESPONSES_DIR.joinpath(req_id + ".json")
    deadline = time.time() + 30.0
    while time.time() < deadline:
        if resp_path.exists():
            try:
                data = json.loads(resp_path.read_text(encoding="utf-8"))
                REQUESTS_DIR.joinpath(req_id + ".json").unlink(missing_ok=True)
                resp_path.unlink(missing_ok=True)
                return data
            except Exception as e:
                return {"ok": False, "error": "bad response: " + str(e)}
        time.sleep(0.1)
    return {"ok": False, "error": "timeout waiting for response", "requestId": req_id, "transport": "file-queue"}

def cmd_benchmark(args):
    iterations = 5
    if args:
        try:
            iterations = int(args[0])
        except Exception:
            pass
    cold_times = []
    for i in range(iterations):
        t0 = time.time()
        subprocess.run(
            [sys.executable, str(DAEMON_SCRIPT), "--mode=ping"],
            capture_output=True, text=True, timeout=10, cwd=str(ENGINE_DIR),
        )
        cold_times.append(round((time.time() - t0) * 1000, 2))
    state = _read_state()
    warm_times = []
    if state and state.get("status") == "running" and _is_alive(state.get("pid")):
        for i in range(iterations):
            t0 = time.time()
            cmd_call(["xfs_measure", "{}"])
            warm_times.append(round((time.time() - t0) * 1000, 2))
    return {
        "ok": True,
        "iterations": iterations,
        "cold": {"times": cold_times, "avgMs": round(sum(cold_times)/max(1,len(cold_times)),2)},
        "warm": {"times": warm_times, "avgMs": round(sum(warm_times)/max(1,len(warm_times)),2)} if warm_times else None,
        "speedup": round(sum(cold_times)/max(1,sum(warm_times)),2) if warm_times else None,
    }

def cmd_install(args):
    import winreg
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "XForgeDaemon"
    cmd = chr(34) + sys.executable + chr(34) + " " + chr(34) + str(DAEMON_SCRIPT) + chr(34) + " --mode=daemon"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, name, 0, winreg.REG_SZ, cmd)
        return {"ok": True, "installed": True, "registryKey": key_path, "valueName": name, "command": cmd}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def cmd_uninstall(args):
    import winreg
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "XForgeDaemon"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
            winreg.DeleteValue(k, name)
        return {"ok": True, "uninstalled": True, "registryKey": key_path, "valueName": name}
    except FileNotFoundError:
        return {"ok": True, "uninstalled": True, "note": "registry value did not exist"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def cmd_watchdog_start(args):
    """Start the watchdog as a detached process. Returns immediately."""
    import subprocess as sp
    poll = 5
    maxr = 10
    i = 0
    while i < len(args):
        if args[i] == "--poll":
            poll = int(args[i + 1]); i += 2
        elif args[i] == "--max-restarts":
            maxr = int(args[i + 1]); i += 2
        else:
            i += 1
    script = str(ENGINE_DIR / "daemon_watchdog.py")
    if (ENGINE_DIR / "daemon-watchdog-state.json").exists():
        try:
            st = json.loads((ENGINE_DIR / "daemon-watchdog-state.json").read_text(encoding="utf-8"))
            if st.get("running") and _is_alive(st.get("pid")):
                return {"ok": False, "error": "watchdog already running", "pid": st.get("pid"), "state": st}
        except Exception:
            pass
    cf = 0x00000008 | 0x00000200
    proc = sp.Popen(
        [sys.executable, script, "run", "--poll", str(poll), "--max-restarts", str(maxr)],
        stdout=open(ENGINE_DIR / "daemon-watchdog.log", "ab", buffering=0),
        stderr=sp.STDOUT, stdin=sp.DEVNULL, cwd=str(ENGINE_DIR), creationflags=cf, close_fds=True,
    )
    deadline = time.time() + 5.0
    while time.time() < deadline:
        if (ENGINE_DIR / "daemon-watchdog-state.json").exists():
            try:
                st = json.loads((ENGINE_DIR / "daemon-watchdog-state.json").read_text(encoding="utf-8"))
                return {"ok": True, "pid": proc.pid, "watchdogPid": st.get("pid"), "state": st, "poll": poll, "maxRestarts": maxr}
            except Exception:
                pass
        time.sleep(0.1)
    return {"ok": False, "error": "watchdog did not start within 5s", "pid": proc.pid}


def cmd_watchdog_stop(args):
    if not (ENGINE_DIR / "daemon-watchdog-state.json").exists():
        return {"ok": True, "stopped": True, "note": "watchdog not running"}
    CONTROL = ENGINE_DIR / "daemon-watchdog-control.json"
    CONTROL.write_text(json.dumps({"command": "stop", "ts": time.time()}), encoding="utf-8")
    deadline = time.time() + 5.0
    while time.time() < deadline:
        time.sleep(0.2)
        try:
            st = json.loads((ENGINE_DIR / "daemon-watchdog-state.json").read_text(encoding="utf-8"))
            if not st.get("running"):
                CONTROL.unlink(missing_ok=True)
                return {"ok": True, "stopped": True, "finalState": st}
        except Exception:
            pass
    return {"ok": False, "error": "watchdog did not stop within 5s"}


def cmd_watchdog_status(args):
    if not (ENGINE_DIR / "daemon-watchdog-state.json").exists():
        return {"ok": True, "running": False, "state": None}
    try:
        st = json.loads((ENGINE_DIR / "daemon-watchdog-state.json").read_text(encoding="utf-8"))
        st["alive"] = _is_alive(st.get("pid"))
        return {"ok": True, "running": st.get("running", False) and st["alive"], "state": st}
    except Exception as e:
        return {"ok": False, "error": "bad state: " + str(e)}


HANDLERS = {
    "start": cmd_start, "stop": cmd_stop, "status": cmd_status,
    "ping": cmd_ping, "list": cmd_list, "call": cmd_call,
    "benchmark": cmd_benchmark, "install": cmd_install,
    "uninstall": cmd_uninstall,
    "watchdog.start": cmd_watchdog_start,
    "watchdog.stop": cmd_watchdog_stop,
    "watchdog.status": cmd_watchdog_status,
    "help": lambda a: {"ok": True, "commands": sorted(HANDLERS.keys())},
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(json.dumps({"ok": True, "usage": "daemon_cli.py <command> [args...]", "commands": sorted(HANDLERS.keys())}, indent=2))
        return 0
    cmd = sys.argv[1]
    if cmd not in HANDLERS:
        print(json.dumps({"ok": False, "error": "unknown command: " + cmd, "available": sorted(HANDLERS.keys())}, indent=2))
        return 2
    try:
        result = HANDLERS[cmd](sys.argv[2:])
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get("ok") else 1
    except Exception as e:
        print(json.dumps({"ok": False, "error": "exception: " + str(e), "type": type(e).__name__}, indent=2))
        return 1

if __name__ == "__main__":
    sys.exit(main())
