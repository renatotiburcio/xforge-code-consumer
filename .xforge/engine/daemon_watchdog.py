#!/usr/bin/env python
"""daemon_watchdog.py - Auto-restart watchdog for the XForge production daemon.

Monitors the daemon's state file + PID liveness, and restarts it on crash.
Uses exponential backoff and a max-restart-per-hour cap to avoid tight loops.

State files:
  .xforge/engine/daemon-state.json           (read-only, written by daemon)
  .xforge/engine/daemon-watchdog-state.json  (written by watchdog)
  .xforge/engine/daemon-watchdog.pid         (watchdog pid)
  .xforge/engine/daemon-watchdog.log         (watchdog log)
  .xforge/engine/daemon-watchdog-control.json (sentinel: {"command":"stop"})
"""
import json, os, sys, time, subprocess, signal, argparse
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
DAEMON_SCRIPT = ENGINE_DIR / "daemon.py"
DAEMON_CLI = ENGINE_DIR / "daemon_cli.py"
DAEMON_STATE_FILE = ENGINE_DIR / "daemon-state.json"
WATCHDOG_STATE_FILE = ENGINE_DIR / "daemon-watchdog-state.json"
WATCHDOG_PID_FILE = ENGINE_DIR / "daemon-watchdog.pid"
WATCHDOG_LOG_FILE = ENGINE_DIR / "daemon-watchdog.log"
WATCHDOG_CONTROL_FILE = ENGINE_DIR / "daemon-watchdog-control.json"
PYTHON = sys.executable
VERSION = "1.0.0"
DEFAULT_POLL_INTERVAL = 5
DEFAULT_BACKOFF_INITIAL = 1
DEFAULT_BACKOFF_MAX = 60
DEFAULT_MAX_RESTARTS_PER_HOUR = 10


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


def log(msg):
    line = "{0} [{1}] {2}".format(time.strftime("%Y-%m-%dT%H:%M:%S"), os.getpid(), msg)
    try:
        with open(WATCHDOG_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, flush=True)


def read_daemon_state():
    if not DAEMON_STATE_FILE.exists():
        return None
    try:
        return json.loads(DAEMON_STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_control():
    if not WATCHDOG_CONTROL_FILE.exists():
        return None
    try:
        return json.loads(WATCHDOG_CONTROL_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def spawn_daemon():
    """Spawn a fresh daemon process via daemon_cli.py start (returns pid)."""
    creationflags = 0x00000008 | 0x00000200
    log_fp = open(ENGINE_DIR / "daemon.log", "ab", buffering=0)
    proc = subprocess.Popen(
        [PYTHON, str(DAEMON_SCRIPT), "--mode=daemon"],
        stdout=log_fp, stderr=log_fp, stdin=subprocess.DEVNULL,
        cwd=str(ENGINE_DIR), creationflags=creationflags, close_fds=True,
    )
    return proc.pid

class WatchdogState:
    def __init__(self):
        self.started_at = time.time()
        self.polls = 0
        self.restarts_total = 0
        self.restarts_last_hour = 0
        self.last_restart_at = 0
        self.last_action = "started"
        self.current_backoff = DEFAULT_BACKOFF_INITIAL
        self.last_daemon_pid = 0
        self.last_daemon_status = "unknown"

    def to_dict(self, running=True):
        return {
            "version": VERSION,
            "pid": os.getpid(),
            "running": running,
            "startedAt": self.started_at,
            "uptimeSec": round(time.time() - self.started_at, 2),
            "polls": self.polls,
            "restartsTotal": self.restarts_total,
            "restartsLastHour": self.restarts_last_hour,
            "lastRestartAt": self.last_restart_at,
            "lastAction": self.last_action,
            "currentBackoff": self.current_backoff,
            "lastDaemonPid": self.last_daemon_pid,
            "lastDaemonStatus": self.last_daemon_status,
        }


def prune_restart_history(state):
    """Reset restarts_last_hour if more than 1 hour has passed."""
    if state.last_restart_at == 0:
        state.restarts_last_hour = 0
        return
    if time.time() - state.last_restart_at > 3600:
        state.restarts_last_hour = 0


def write_state(state, running=True):
    try:
        with open(WATCHDOG_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(running=running), f)
    except Exception as e:
        log("write_state error: " + str(e))


def run(poll_interval, max_restarts):
    state = WatchdogState()
    with open(WATCHDOG_PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    log("watchdog starting (pid={0}, poll={1}s, max_restarts={2})".format(os.getpid(), poll_interval, max_restarts))
    write_state(state)
    try:
        while True:
            state.polls += 1
            prune_restart_history(state)
            ctrl = check_control()
            if ctrl and ctrl.get("command") in ("stop", "stop_watchdog"):
                log("control: stop command received")
                try:
                    WATCHDOG_CONTROL_FILE.unlink()
                except Exception:
                    pass
                write_state(state, running=False)
                return {"ok": True, "action": "stopped", "polls": state.polls, "restartsTotal": state.restarts_total}
            dstate = read_daemon_state()
            needs_restart = False
            if dstate is None:
                state.last_daemon_status = "never_started"
                state.last_action = "daemon missing state file"
                needs_restart = True
            else:
                dpid = dstate.get("pid", 0)
                dstatus = dstate.get("status", "unknown")
                state.last_daemon_pid = dpid
                state.last_daemon_status = dstatus
                alive = _is_alive(dpid)
                if dstatus == "running" and alive:
                    state.last_action = "ok"
                    state.current_backoff = DEFAULT_BACKOFF_INITIAL
                else:
                    state.last_action = "needs restart (status=" + str(dstatus) + ", alive=" + str(alive) + ")"
                    log("daemon not healthy: status={0}, pid={1}, alive={2}".format(dstatus, dpid, alive))
                    needs_restart = True
            if needs_restart:
                if state.restarts_last_hour >= max_restarts:
                    state.last_action = "max restarts reached, waiting"
                    log("max restarts ({0}) reached; waiting for backoff".format(max_restarts))
                else:
                    log("restarting daemon (attempt #{0})".format(state.restarts_total + 1))
                    try:
                        new_pid = spawn_daemon()
                        state.restarts_total += 1
                        state.restarts_last_hour += 1
                        state.last_restart_at = time.time()
                        state.current_backoff = min(state.current_backoff * 2, DEFAULT_BACKOFF_MAX)
                        state.last_daemon_pid = new_pid
                        state.last_action = "restarted daemon pid=" + str(new_pid)
                        log("spawned new daemon pid={0}".format(new_pid))
                    except Exception as e:
                        state.last_action = "restart failed: " + str(e)
                        log("restart failed: " + str(e))
            write_state(state)
            time.sleep(poll_interval if state.last_action == "ok" else max(poll_interval, state.current_backoff))
    finally:
        try:
            WATCHDOG_PID_FILE.unlink()
        except Exception:
            pass


def cmd_status():
    if not WATCHDOG_STATE_FILE.exists():
        return {"ok": True, "running": False, "state": None}
    try:
        return {"ok": True, "running": True, "state": json.loads(WATCHDOG_STATE_FILE.read_text(encoding="utf-8"))}
    except Exception as e:
        return {"ok": False, "error": "bad state: " + str(e)}


def cmd_stop():
    if not WATCHDOG_STATE_FILE.exists():
        return {"ok": True, "stopped": True, "note": "watchdog not running"}
    WATCHDOG_CONTROL_FILE.write_text(json.dumps({"command": "stop", "ts": time.time()}), encoding="utf-8")
    deadline = time.time() + 5.0
    while time.time() < deadline:
        time.sleep(0.2)
        s = cmd_status()
        if not s.get("running"):
            try:
                WATCHDOG_CONTROL_FILE.unlink()
            except Exception:
                pass
            return {"ok": True, "stopped": True}
    return {"ok": False, "error": "watchdog did not stop within 5s"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XForge production daemon watchdog")
    parser.add_argument("command", nargs="?", default="run", choices=["run", "status", "stop"])
    parser.add_argument("--poll", type=int, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--max-restarts", type=int, default=DEFAULT_MAX_RESTARTS_PER_HOUR)
    args = parser.parse_args()
    if args.command == "run":
        try:
            print(json.dumps(run(args.poll, args.max_restarts), indent=2))
        except KeyboardInterrupt:
            print(json.dumps({"ok": True, "action": "interrupted"}))
    elif args.command == "status":
        print(json.dumps(cmd_status(), indent=2))
    elif args.command == "stop":
        print(json.dumps(cmd_stop(), indent=2))
