"""
AutoResearch tools - autonomous experiment loop (run, run_mutate, daemon).

Extraido de xforge_engine.py em v3.10.6 per DR-0093 (ULTIMO).
Contem: 3 tools + 5 helpers.
"""
import json
import re
import subprocess
import time
import shutil
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from .common import (
    _ok, _err, _iso_now, ROOT, KNOWLEDGE, INDEX_JSON, WORKFLOWS, BUSINESS,
    _load_index_cached, _invalidate_index_cache,
    AUTORESEARCH_CFG, AUTORESEARCH_RESULTS, AUTORESEARCH_EXPERIMENTS, AUTORESEARCH_SANDBOX,
    SCORING_RULE, SCHEMA_KNOWLEDGE, SCHEMA_WORKFLOW, SCHEMAS_DIR,
    POLICY_ENGINE, RBAC_CONFIG,
)

def _hash_row(row):
    import hashlib
    return hashlib.sha256("\t".join(row).encode("utf-8")).hexdigest()


def _measure_xfs():
    score = 0.0
    if KNOWLEDGE.exists():
        kcount = sum(1 for _ in KNOWLEDGE.rglob("*.md"))
        score += min(kcount / 200, 1.0) * 0.30
    if WORKFLOWS.exists():
        wcount = sum(1 for _ in WORKFLOWS.glob("W*.yaml"))
        score += min(wcount / 15, 1.0) * 0.20
    eng = ROOT / ".xforge" / "engine" / "xforge_engine.py"
    srv = ROOT / ".xforge" / "mcp" / "server.js"
    mft = ROOT / ".xforge" / "mcp" / "manifest.json"
    infra = sum(1 for p in (eng, srv, mft) if p.exists() and p.stat().st_size > 100)
    score += (infra / 3) * 0.20
    qa = sum(1 for p in (POLICY_ENGINE, RBAC_CONFIG, AUTORESEARCH_CFG)
             if p.exists() and p.stat().st_size > 50)
    score += (qa / 3) * 0.15
    empty = 0
    for d in (ROOT / ".xforge").iterdir():
        if d.is_dir() and not any(d.iterdir()):
            empty += 1
    score += max(0, (1 - empty * 0.1)) * 0.15
    return round(min(score, 1.0), 4)


def _exp_count_knowledge():
    kcount = sum(1 for _ in KNOWLEDGE.rglob("*.md")) if KNOWLEDGE.exists() else 0
    return "knowledge_files", kcount


def _exp_count_transitions():
    total = 0
    for yml in (WORKFLOWS.glob("W*.yaml") if WORKFLOWS.exists() else []):
        try:
            d = yaml.safe_load(yml.read_text(encoding="utf-8"))
            total += len(d.get("transitions", []))
        except Exception:
            pass
    return "transitions", total


def _exp_check_documented():
    if not (KNOWLEDGE.exists() and WORKFLOWS.exists()):
        return "undocumented", []
    klow = {p.name.lower() for p in KNOWLEDGE.rglob("*.md")}
    missing = []
    for yml in WORKFLOWS.glob("W*.yaml"):
        wf_id = yml.stem.split("-")[0].lower()
        if not any(wf_id in n for n in klow):
            missing.append(yml.name)
    return "undocumented_workflows", missing


def _exp_check_empty_dirs():
    if not (ROOT / ".xforge").exists():
        return "empty_dirs", []
    empties = []
    for d in (ROOT / ".xforge").rglob("*"):
        if d.is_dir() and not any(d.iterdir()):
            empties.append(str(d.relative_to(ROOT)))
    return "empty_dirs", empties


def _exp_check_dup_types():
    if not KNOWLEDGE.exists():
        return "duplicates", []
    seen = {}
    dups = []
    for f in KNOWLEDGE.rglob("*.md"):
        c = f.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"(?s)^---\r?\n(.+?)\r?\n---", c)
        if not m:
            continue
        fm = m.group(1)
        fid, ftype = "", ""
        for ln in fm.splitlines():
            if ln.startswith("id:"):
                fid = ln.split(":", 1)[1].strip()
            if ln.startswith("type:"):
                ftype = ln.split(":", 1)[1].strip()
        if fid and ftype:
            key = (ftype, fid)
            if key in seen:
                dups.append({"id": fid, "type": ftype,
                             "files": [seen[key], str(f.relative_to(ROOT))]})
            else:
                seen[key] = str(f.relative_to(ROOT))
    return "duplicates", dups



def tool_autoresearch_run(args):
    if not AUTORESEARCH_CFG.exists():
        return _err("autoresearch/config.json not found")
    try:
        cfg = json.loads(AUTORESEARCH_CFG.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return _err("config invalid: " + str(e))
    iterations = int(args.get("iterations", 3))
    iterations = min(iterations, cfg.get("loop", {}).get("maxIterations", 20))
    protected = [str(SCORING_RULE.relative_to(ROOT))] if SCORING_RULE.exists() else []
    baseline = _measure_xfs()
    results = [{"step": 0, "xfs": baseline, "status": "baseline",
                "description": "initial measurement", "timestamp": _iso_now()}]
    experiments = [
        ("count_knowledge_files", _exp_count_knowledge, "Count .md files in knowledge"),
        ("count_workflow_transitions", _exp_count_transitions, "Count total transitions"),
        ("check_documented_workflows", _exp_check_documented, "Find workflows without docs"),
        ("check_empty_dirs", _exp_check_empty_dirs, "Find empty .xforge dirs"),
        ("check_duplicate_types", _exp_check_dup_types, "Find knowledge duplicates"),
    ]
    for i in range(1, iterations + 1):
        name, fn, desc = experiments[(i - 1) % len(experiments)]
        try:
            metric, value = fn()
        except Exception as e:
            metric, value = None, "error: " + str(e)
        new_xfs = _measure_xfs()
        keep = new_xfs >= baseline
        results.append({"step": i, "experiment": name, "value": value,
                        "xfs": new_xfs, "baseline": baseline,
                        "status": "keep" if keep else "discard",
                        "description": desc, "timestamp": _iso_now()})
        if keep:
            baseline = new_xfs
    AUTORESEARCH_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    header = ["step", "experiment", "xfs", "baseline", "status", "value",
              "description", "timestamp", "sha256"]
    write_header = not AUTORESEARCH_RESULTS.exists()
    with AUTORESEARCH_RESULTS.open("a", encoding="utf-8") as f:
        if write_header:
            f.write("\t".join(header) + "\n")
        for r in results:
            row = [str(r.get(h, "")) for h in header[:-1]]
            sha = _hash_row(row)
            row.append(sha[:16])
            f.write("\t".join(row) + "\n")
    return _ok(iterations=iterations, currentXfs=baseline, protectedPaths=protected,
               results=results, historyFile=str(AUTORESEARCH_RESULTS.relative_to(ROOT)))



# ============================================================== HEALTH CHECK




    invalid_wf = []
    def _validate_one(w):
        v = tool_workflow_validate({"id": w["id"]})
        return w["id"], v.get("valid", False), v.get("errors", [])
    with ThreadPoolExecutor(max_workers=min(8, len(workflows))) as pool:
        for wf_id, valid, errs in pool.map(_validate_one, workflows):
            if valid:
                valid_wf += 1
            else:
                invalid_wf.append({"id": wf_id, "errors": errs})
    return valid_wf, invalid_wf




def _measure_sandbox_xfs(sandbox_knowledge):
    """Heuristic xfs for a sandbox knowledge copy."""
    sb = Path(sandbox_knowledge)
    k_count = sum(1 for _ in sb.rglob("*.md")) if sb.exists() else 0
    wf_count = 15
    infra = 3
    qa = 3
    empty = sum(1 for d in sb.rglob("*") if d.is_dir() and not any(d.iterdir())) if sb.exists() else 0
    xfs = 0.30 * (k_count / 200) + 0.20 * (wf_count / 15) + 0.20 * (infra / 3) + 0.15 * (qa / 3) - 0.15 * (empty * 0.1)
    return min(max(xfs, 0.0), 1.0)



def tool_autoresearch_run_mutate(args):
    """Real AutoResearch loop: copy knowledge to sandbox, run experiments, measure, keep/discard."""
    if not AUTORESEARCH_EXPERIMENTS.exists():
        return _err(f"experiments dir not found: {AUTORESEARCH_EXPERIMENTS}")
    iterations = int(args.get("iterations", 3))
    iterations = min(iterations, 20)
    experiments = sorted(AUTORESEARCH_EXPERIMENTS.glob("E*.py"))
    if not experiments:
        return _err("no experiment scripts (E*.py) found in experiments/")

    # prepare sandbox
    if AUTORESEARCH_SANDBOX.exists():
        shutil.rmtree(AUTORESEARCH_SANDBOX)
    AUTORESEARCH_SANDBOX.mkdir(parents=True)
    sandbox_knowledge = AUTORESEARCH_SANDBOX / "knowledge"
    if KNOWLEDGE.exists():
        shutil.copytree(KNOWLEDGE, sandbox_knowledge)
    # Copy .xforge/business/ so experiments can see realistic business context.
    # xfs formula is GUARDED: only counts .md inside sandbox/knowledge/.
    # Business files are NOT included in xfs calculation (see _measure_sandbox_xfs).
    business_copied = 0
    sandbox_business = AUTORESEARCH_SANDBOX / "business"
    if BUSINESS.exists():
        shutil.copytree(BUSINESS, sandbox_business)
        business_copied = sum(1 for _ in sandbox_business.rglob("*")) if sandbox_business.exists() else 0


    baseline_xfs = _measure_sandbox_xfs(sandbox_knowledge)
    results = [{
        "step": 0, "experiment": "(baseline)", "xfs": baseline_xfs,
        "status": "baseline", "description": "initial sandbox copy of knowledge",
        "business_copied": business_copied,
        "timestamp": _iso_now()
    }]

    for i in range(1, iterations + 1):
        exp = experiments[(i - 1) % len(experiments)]
        try:
            r = subprocess.run(
                [sys.executable, str(exp)],
                env={**os.environ, "SANDBOX": str(sandbox_knowledge)},
                capture_output=True, text=True, timeout=120
            )
            output = (r.stdout or r.stderr or "(no output)").strip()
        except Exception as e:
            output = f"error: {e}"
        new_xfs = _measure_sandbox_xfs(sandbox_knowledge)
        keep = new_xfs >= baseline_xfs
        results.append({
            "step": i, "experiment": exp.stem, "xfs": new_xfs,
            "baseline": baseline_xfs, "status": "keep" if keep else "discard",
            "description": output.split(chr(10))[-1][:200] if output else "",
            "timestamp": _iso_now()
        })
        if keep:
            baseline_xfs = new_xfs

    # append to results.tsv
    AUTORESEARCH_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    header = ["step", "experiment", "xfs", "baseline", "status", "value", "description", "timestamp", "sha256"]
    write_header = not AUTORESEARCH_RESULTS.exists()
    with AUTORESEARCH_RESULTS.open("a", encoding="utf-8") as f:
        if write_header:
            f.write(chr(9).join(header) + chr(10))
        for r in results:
            row = [str(r.get(h, "")) for h in header[:-1]]
            sha = _hash_row(row)
            row.append(sha[:16])
            f.write(chr(9).join(row) + chr(10))

    return _ok(
        iterations=iterations,
        experimentsAvailable=len(experiments),
        sandboxPath=str(AUTORESEARCH_SANDBOX.relative_to(ROOT)),
        currentXfs=baseline_xfs,
        results=results,
        historyFile=str(AUTORESEARCH_RESULTS.relative_to(ROOT))
    )






# ---------------------------------------------------------------- DAEMON

AUTORESEARCH_DAEMON = ROOT / ".xforge" / "autoresearch" / "daemon.py"
AUTORESEARCH_DAEMON_STATE = ROOT / ".xforge" / "autoresearch" / "daemon-state.json"
AUTORESEARCH_DAEMON_CONTROL = ROOT / ".xforge" / "autoresearch" / "daemon-control.json"


def _pid_alive(pid: int) -> bool:
    """Return True if a process with this pid is alive (best-effort, cross-platform)."""
    if pid is None or pid <= 0:
        return False
    try:
        if os.name == "nt":
            # Windows: use tasklist via subprocess (cheaper than ctypes import)
            r = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True, text=True, timeout=5,
            )
            return str(pid) in r.stdout
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False


def _daemon_read_state():
    if AUTORESEARCH_DAEMON_STATE.exists():
        try:
            with open(AUTORESEARCH_DAEMON_STATE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "pid": None,
        "startedAt": None,
        "iterationsCompleted": 0,
        "currentXfs": None,
        "lastTickAt": None,
        "status": "never_started",
        "crashes": 0,
    }



def tool_autoresearch_daemon(args):
    """Start/stop/status the AutoResearch background daemon.

    Args:
      action: "start" | "stop" | "status" (default "status")
      iterationsPerTick: int (default 7) - budget per loop iteration when started
      detach: bool (default True) - run as detached background process on Windows

    Returns:
      - start: {ok, pid, startedAt, stateFile}
      - stop:  {ok, previousStatus, pid, killed}
      - status: {ok, state, pidAlive, lastTickAt, iterationsCompleted, currentXfs}
    """
    import time
    action = (args.get("action") or "status").lower().strip()
    iterations_per_tick = int(args.get("iterationsPerTick") or 7)
    detach = bool(args.get("detach", True))

    state = _daemon_read_state()
    pid = state.get("pid")
    pid_alive = _pid_alive(pid) if pid else False

    if action == "status":
        return _ok(
            action="status",
            state=state,
            pidAlive=pid_alive,
            stateFile=str(AUTORESEARCH_DAEMON_STATE.relative_to(ROOT)),
            controlFile=str(AUTORESEARCH_DAEMON_CONTROL.relative_to(ROOT)),
        )

    if action == "start":
        if pid_alive:
            return _ok(
                action="start",
                alreadyRunning=True,
                pid=pid,
                state=state,
                message="daemon already running, use status to inspect",
            )
        # Reset control file (no stop command)
        AUTORESEARCH_DAEMON_CONTROL.write_text(
            json.dumps({"command": "run"}, indent=2), encoding="utf-8"
        )
        # Spawn detached subprocess
        kwargs = {
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "stdin": subprocess.DEVNULL,
            "close_fds": True,
        }
        if os.name == "nt" and detach:
            kwargs["creationflags"] = (
                subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            kwargs["start_new_session"] = True
        proc = subprocess.Popen(
            [sys.executable, str(AUTORESEARCH_DAEMON)], **kwargs
        )
        # Write initial state immediately (the daemon will overwrite)
        initial_state = {
            "pid": proc.pid,
            "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "iterationsCompleted": 0,
            "currentXfs": None,
            "lastTickAt": None,
            "status": "spawned",
            "crashes": 0,
        }
        AUTORESEARCH_DAEMON_STATE.write_text(
            json.dumps(initial_state, indent=2), encoding="utf-8"
        )
        return _ok(
            action="start",
            spawned=True,
            pid=proc.pid,
            stateFile=str(AUTORESEARCH_DAEMON_STATE.relative_to(ROOT)),
            iterationsPerTick=iterations_per_tick,
            state=initial_state,
        )

    if action == "stop":
        # Tell daemon to stop on next tick
        AUTORESEARCH_DAEMON_CONTROL.write_text(
            json.dumps({"command": "stop"}, indent=2), encoding="utf-8"
        )
        killed = False
        if pid_alive and pid:
            try:
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/PID", str(pid), "/F"],
                        capture_output=True, timeout=5,
                    )
                else:
                    os.kill(pid, 15)  # SIGTERM
                killed = True
            except Exception:
                pass
        # Update state
        state["status"] = "stopped"
        AUTORESEARCH_DAEMON_STATE.write_text(
            json.dumps(state, indent=2), encoding="utf-8"
        )
        return _ok(
            action="stop",
            previousState=state,
            pid=pid,
            killed=killed,
            message="control file set to stop; PID terminated if alive",
        )

    return _ok(error="unknown action", action=action, valid=["start", "stop", "status"])
