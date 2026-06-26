#!/usr/bin/env python
"""daemon.py - XForge production daemon (long-lived engine).

Modes:
  --mode=daemon   long-running, listens on Windows named pipe + polls request files
  --mode=ping     one-shot, returns {"ok": True, "pong": True}
"""
import json, os, sys, time, threading, subprocess, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ENGINE_DIR = Path(__file__).resolve().parent
CACHE_DIR = ROOT / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
PID_FILE = ENGINE_DIR / "daemon.pid"
LOG_FILE = ENGINE_DIR / "daemon.log"
STATE_FILE = ENGINE_DIR / "daemon-state.json"
CONTROL_FILE = ENGINE_DIR / "daemon-control.json"
REQUESTS_DIR = ENGINE_DIR / "daemon-requests"
RESPONSES_DIR = ENGINE_DIR / "daemon-responses"
PIPE_NAME = r"\\.\pipe\xforge-daemon"
CACHE_TTL_SEC = 300
CACHE_CLEANUP_INTERVAL_SEC = 60
POLL_INTERVAL_SEC = 0.1
PIPE_TIMEOUT_MS = 5000
VERSION = "1.0.0"
INDEX_JSON = ROOT / ".xforge" / "knowledge" / "INDEX.json"
WORKFLOWS_DIR = ROOT / ".xforge" / "workflows"
IN_PROCESS_TOOLS = {"xforge_knowledge_search", "xforge_workflow_list", "xforge_workflow_validate"}
_in_process_index_cache = None
_in_process_index_mtime = 0

for d in (REQUESTS_DIR, RESPONSES_DIR):
    d.mkdir(parents=True, exist_ok=True)


class TTLCache:
    def __init__(self, default_ttl=CACHE_TTL_SEC):
        self._data = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def get(self, key):
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self.misses += 1
                return None
            value, expires_at = entry
            if time.time() > expires_at:
                del self._data[key]
                self.misses += 1
                return None
            self.hits += 1
            return value

    def set(self, key, value, ttl=None):
        with self._lock:
            self._data[key] = (value, time.time() + (ttl or self.default_ttl))

    def invalidate(self, key=None):
        with self._lock:
            if key is None:
                self._data.clear()
            else:
                self._data.pop(key, None)

    def stats(self):
        with self._lock:
            return {"size": len(self._data), "hits": self.hits, "misses": self.misses, "hitRate": round(self.hits / max(1, self.hits + self.misses), 4)}

class DaemonState:
    def __init__(self):
        self.started_at = time.time()
        self.request_count = 0
        self.cache = TTLCache()
        self.recent_requests = []
        self.last_tick_at = 0
        self.crashes = 0

    def to_dict(self, status="running"):
        return {
            "pid": os.getpid(),
            "status": status,
            "startedAt": self.started_at,
            "uptimeSec": round(time.time() - self.started_at, 2),
            "requestCount": self.request_count,
            "cache": self.cache.stats(),
            "lastTickAt": self.last_tick_at,
            "crashes": self.crashes,
            "version": VERSION,
            "recentRequests": self.recent_requests[-10:],
        }


def log(msg):
    line = "{0} [{1}] {2}".format(time.strftime("%Y-%m-%dT%H:%M:%S"), os.getpid(), msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, flush=True)


def write_state(state, status="running"):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(status), f)
    except Exception as e:
        log("write_state error: " + str(e))


def call_subprocess_tool(tool, args):
    args_file = CACHE_DIR / ".tmp-args-{0}-{1}.json".format(os.getpid(), int(time.time() * 1000))
    try:
        with open(args_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(args or {}, ensure_ascii=False))
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        r = subprocess.run(
            ["python", str(ROOT / ".xforge" / "engine" / "xforge_engine.py"), tool, "@" + str(args_file)],
            capture_output=True, text=True, timeout=30, env=env, cwd=str(ENGINE_DIR),
        )
        if r.returncode != 0:
            return {"ok": False, "error": {"code": "ENGINE_FAIL", "message": r.stderr[:500]}}
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError as e:
            return {"ok": False, "error": {"code": "PARSE_FAIL", "message": str(e)}}
    finally:
        try:
            args_file.unlink()
        except Exception:
            pass


CACHEABLE_TOOLS = {
    "xforge_doctor",
    "xforge_knowledge_search",
    "xforge_workflow_list",
    "xforge_workflow_validate",
    "xfs_measure",
}


def _load_index_inproc():
    global _in_process_index_cache, _in_process_index_mtime
    if not INDEX_JSON.exists():
        return None
    try:
        mtime = INDEX_JSON.stat().st_mtime
        if _in_process_index_cache is None or mtime != _in_process_index_mtime:
            _in_process_index_cache = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
            _in_process_index_mtime = mtime
        return _in_process_index_cache
    except Exception:
        return None


def _in_process_knowledge_search(args):
    q = (args.get("query") or "").strip().lower()
    if not q:
        return {"ok": False, "error": {"code": "BAD_REQUEST", "message": "query required"}}
    limit = int(args.get("limit", 20))
    idx = _load_index_inproc()
    if idx is None:
        return {"ok": False, "error": {"code": "INDEX_MISSING", "message": "INDEX.json not found"}}
    results = []
    for f in idx.get("files", []):
        hay = " ".join([
            f.get("path", ""), f.get("summary", ""), f.get("domain", ""),
            f.get("category", ""), " ".join(f.get("keywords", []))
        ]).lower()
        if q in hay:
            results.append(f)
            if len(results) >= limit:
                break
    return {"ok": True, "count": len(results), "results": results}


def _in_process_workflow_list(args):
    if not WORKFLOWS_DIR.exists():
        return {"ok": True, "count": 0, "workflows": []}
    out = []
    try:
        import yaml
    except ImportError:
        return {"ok": False, "error": {"code": "NO_YAML", "message": "PyYAML not installed"}}
    for yml in sorted(WORKFLOWS_DIR.glob("W*.yaml")):
        try:
            d = yaml.safe_load(yml.read_text(encoding="utf-8"))
            out.append({
                "file": yml.name,
                "id": d.get("id"),
                "name": d.get("name"),
                "version": d.get("version"),
                "description": d.get("description"),
                "states": len(d.get("states", [])) if isinstance(d.get("states"), list) else 0,
                "transitions": len(d.get("transitions", [])) if isinstance(d.get("transitions"), list) else 0,
            })
        except Exception as e:
            out.append({"file": yml.name, "error": str(e)})
    return {"ok": True, "count": len(out), "workflows": out}


def _in_process_workflow_validate(args):
    try:
        import yaml
    except ImportError:
        return {"ok": False, "error": {"code": "NO_YAML", "message": "PyYAML not installed"}}
    wid = (args.get("id") or "").strip()
    if not wid:
        return {"ok": False, "error": {"code": "BAD_REQUEST", "message": "id required"}}
    wf_path = None
    for yml in WORKFLOWS_DIR.glob("W*.yaml"):
        try:
            d = yaml.safe_load(yml.read_text(encoding="utf-8"))
            if d.get("id") == wid:
                wf_path = yml
                wf_data = d
                break
        except Exception:
            continue
    if wf_path is None:
        return {"ok": False, "error": {"code": "NOT_FOUND", "message": "workflow not found"}}
    states = wf_data.get("states", [])
    transitions = wf_data.get("transitions", [])
    errors = []
    if not states:
        errors.append("missing states")
    if not isinstance(states, list):
        errors.append("states must be a list")
    if not isinstance(transitions, list):
        errors.append("transitions must be a list")
    terminal = set(d.get("terminalStates", []))
    referenced = set()
    for t in transitions:
        if isinstance(t, dict):
            f = t.get("from")
            to = t.get("to")
            if f:
                referenced.add(f)
            if to:
                referenced.add(to)
    unreachable = set(states) - referenced - terminal if isinstance(states, list) else set()
    return {
        "ok": len(errors) == 0 and not unreachable,
        "id": wf_data.get("id"),
        "name": wf_data.get("name"),
        "states": len(states) if isinstance(states, list) else 0,
        "transitions": len(transitions) if isinstance(transitions, list) else 0,
        "errors": errors,
        "unreachable": sorted(unreachable) if unreachable else [],
    }


IN_PROCESS_DISPATCH = {
    "xforge_knowledge_search": _in_process_knowledge_search,
    "xforge_workflow_list": _in_process_workflow_list,
    "xforge_workflow_validate": _in_process_workflow_validate,
}


def _in_process_tool(tool, args):
    """Try in-process dispatch; return None if tool not supported in-process."""
    handler = IN_PROCESS_DISPATCH.get(tool)
    if handler is None:
        return None
    try:
        return handler(args or {})
    except Exception as e:
        log("in-process {0} failed: {1}".format(tool, e))
        return None


def handle_request(state, request):
    state.request_count += 1
    tool = request.get("tool")
    args = request.get("args") or {}
    req_id = request.get("id")
    if not tool:
        return {"ok": False, "id": req_id, "error": {"code": "BAD_REQUEST", "message": "missing tool"}}
    if tool in CACHEABLE_TOOLS:
        cache_key = "{0}:{1}".format(tool, json.dumps(args, sort_keys=True, ensure_ascii=False))
        cached = state.cache.get(cache_key)
        if cached is not None:
            state.recent_requests.append({"id": req_id, "tool": tool, "cached": True, "ts": time.time()})
            try:
                write_state(state, "running")
            except Exception:
                pass
            return {"ok": True, "id": req_id, "result": cached, "cached": True}
        result = _in_process_tool(tool, args)
        if result is None:
            result = call_subprocess_tool(tool, args)
        if result.get("ok"):
            state.cache.set(cache_key, result.get("result"))
        state.recent_requests.append({"id": req_id, "tool": tool, "cached": False, "ts": time.time()})
        try:
            write_state(state, "running")
        except Exception:
            pass
        return result
    if tool == "xforge_daemon_status":
        return {"ok": True, "id": req_id, "result": state.to_dict()}
    if tool == "xforge_daemon_ping":
        return {"ok": True, "id": req_id, "result": "pong"}
    if tool == "xforge_daemon_invalidate":
        state.cache.invalidate(args.get("key"))
        return {"ok": True, "id": req_id, "result": {"invalidated": args.get("key") or "all"}}
    if tool == "xforge_daemon_stop":
        threading.Thread(target=lambda: (time.sleep(0.3), os._exit(0))).start()
        return {"ok": True, "id": req_id, "result": {"action": "stop", "scheduled": True}}
    state.recent_requests.append({"id": req_id, "tool": tool, "cached": False, "ts": time.time()})
    result = call_subprocess_tool(tool, args)
    try:
        write_state(state, "running")
    except Exception:
        pass
    return result


def check_control_file():
    if not CONTROL_FILE.exists():
        return None
    try:
        return json.loads(CONTROL_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def serve_pipe(state):
    try:
        import win32pipe, win32file, pywintypes
    except ImportError:
        log("pywin32 not available; pipe disabled, using file queue only")
        return False
    log("Windows named pipe: " + PIPE_NAME)
    while True:
        try:
            handle = win32pipe.CreateNamedPipe(
                PIPE_NAME,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES,
                65536, 65536, PIPE_TIMEOUT_MS, None,
            )
            try:
                win32pipe.ConnectNamedPipe(handle, None)
            except pywintypes.error as e:
                if e.args[0] != 535:
                    raise
            try:
                _, data = win32file.ReadFile(handle, 64 * 1024)
                try:
                    request = json.loads(data.decode("utf-8"))
                except Exception as e:
                    win32file.WriteFile(handle, json.dumps({"ok": False, "error": {"code": "PARSE_FAIL", "message": str(e)}}).encode("utf-8"))
                    continue
                response = handle_request(state, request)
                win32file.WriteFile(handle, json.dumps(response).encode("utf-8"))
            finally:
                win32file.CloseHandle(handle)
        except Exception as e:
            log("pipe error: " + str(e))
            time.sleep(1)
    return True


def serve_file_queue(state):
    log("File queue polling: " + str(REQUESTS_DIR))
    while True:
        try:
            for req_file in REQUESTS_DIR.glob("*.json"):
                try:
                    request = json.loads(req_file.read_text(encoding="utf-8"))
                    req_id = request.get("id") or req_file.stem
                    response = handle_request(state, request)
                    resp_file = RESPONSES_DIR / (req_id + ".json")
                    resp_file.write_text(json.dumps(response, default=str), encoding="utf-8")
                    req_file.unlink(missing_ok=True)
                except Exception as e:
                    log("file_queue handler error: " + str(e))
                    try:
                        req_file.unlink(missing_ok=True)
                    except Exception:
                        pass
        except Exception as e:
            log("file_queue error: " + str(e))
        time.sleep(POLL_INTERVAL_SEC)


def control_loop(state):
    while True:
        time.sleep(CACHE_CLEANUP_INTERVAL_SEC)
        state.last_tick_at = time.time()
        ctrl = check_control_file()
        if ctrl and ctrl.get("command") == "stop":
            log("control: stop command received")
            try:
                CONTROL_FILE.unlink()
            except Exception:
                pass
            write_state(state, "stopped")
            os._exit(0)
        try:
            write_state(state, "running")
        except Exception:
            pass


def serve():
    state = DaemonState()
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    log("daemon starting (pid={0}, root={1}, mode={2})".format(os.getpid(), ROOT, MODE))
    write_state(state, "starting")
    pipe_thread = None
    if sys.platform == "win32":
        pipe_thread = threading.Thread(target=serve_pipe, args=(state,), daemon=True)
        pipe_thread.start()
    else:
        log("non-Windows platform; file queue only")
    threads = [
        threading.Thread(target=control_loop, args=(state,), daemon=False),
        threading.Thread(target=serve_file_queue, args=(state,), daemon=True),
    ]
    for t in threads:
        t.start()
    write_state(state, "running")
    log("daemon ready (pid={0}, pipe={1}, file_queue=active, control=active)".format(os.getpid(), "active" if pipe_thread else "n/a"))
    while True:
        time.sleep(60)


def cmd_ping():
    print(json.dumps({"ok": True, "pong": True, "version": VERSION, "pid": os.getpid(), "ts": time.time()}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XForge production daemon")
    parser.add_argument("--mode", default="daemon", choices=["daemon", "ping"])
    args, _ = parser.parse_known_args()
    global MODE
    MODE = args.mode
    if MODE == "ping":
        cmd_ping()
    else:
        serve()
