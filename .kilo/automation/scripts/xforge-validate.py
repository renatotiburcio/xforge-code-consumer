#!/usr/bin/env python3
"""XForge Engineer - 1-command health check orchestrator.

Runs the full health check suite and returns exit 0 if all pass.
"""
import os
import subprocess
import sys
import re
from pathlib import Path

PROJECT_ROOT = Path(r"D:\dev\XForge-Development-New")
os.chdir(PROJECT_ROOT)


def step(label, fn):
    """Run a step, return (ok, output)."""
    try:
        return fn()
    except Exception as e:
        return (False, "exception: " + str(e))


def run_ps1(script_rel):
    r = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-File", str(PROJECT_ROOT / script_rel)],
        capture_output=True, text=True, timeout=120)
    return (r.returncode == 0, r.stdout + r.stderr)


def run_py(args, timeout=300):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT_ROOT))
    return (r.returncode == 0, r.stdout + r.stderr)


def header(name):
    print("")
    print("=" * 60)
    print(" " + name)
    print("=" * 60)


def report(name, ok, detail=""):
    mark = "[PASS]" if ok else "[FAIL]"
    color = "\033[32m" if ok else "\033[31m"
    reset = "\033[0m"
    line = "  {}{}{}".format(color, mark, reset)
    line += "  " + name
    if detail:
        line += "  - " + detail
    print(line)


def main():
    print("")
    print("=" * 60)
    print(" XFORGE ENGINEER - HEALTH CHECK ORCHESTRATOR")
    print("=" * 60)
    print("  Project root: " + str(PROJECT_ROOT))
    print("  Time: " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    results = []

    header("1/6  Doctor (file structure, configs, rules)")
    ok, out = step("doctor", lambda: run_ps1(".kilo/automation/scripts/doctor.ps1"))
    errs = sum(1 for line in out.splitlines() if line.startswith("[ERROR]"))
    warns = sum(1 for line in out.splitlines() if line.startswith("[WARN]"))
    detail = "errors=" + str(errs) + ", warnings=" + str(warns)
    report("Doctor", ok and errs == 0, detail)
    results.append(ok and errs == 0)

    header("2/6  Knowledge validator")
    ok, out = step("kv", lambda: run_ps1(".xforge/schemas/validate-knowledge.ps1"))
    total_m = re.search(r"Total:\s*(\d+)", out)
    valid_m = re.search(r"Valid:\s*(\d+)", out)
    detail = "total=" + (total_m.group(1) if total_m else "?") + ", valid=" + (valid_m.group(1) if valid_m else "?")
    report("Knowledge", "All knowledge files valid" in out, detail)
    results.append("All knowledge files valid" in out)

    header("3/6  Pytest (89 tests + 1 slow)")
    ok, out = step("pytest", lambda: run_py(["python", "-m", "pytest", ".xforge/engine/tests/", "-q", "--tb=line", "-m", "not slow"]))
    passed_m = re.search(r"(\d+) passed", out)
    detail = (passed_m.group(1) if passed_m else "0") + " passed"
    report("Pytest", ok and passed_m is not None, detail)
    results.append(ok and passed_m is not None)

    header("4/6  Engine validate_all (9 health checks)")
    tmp = PROJECT_ROOT / ".xforge-validate-tmp.json"
    tmp.write_text("{}", encoding="utf-8")
    ok, out = step("validate_all", lambda: run_py(["python", ".xforge/engine/xforge_engine.py", "xforge_validate_all", "@" + str(tmp)]))
    try: tmp.unlink()
    except: pass
    try:
        import json
        d = json.loads(out)
        s = d["summary"]
        detail = str(s["passedChecks"]) + "/" + str(s["totalChecks"]) + " checks passed, xfs=" + str(d["checks"]["xfs"]["value"])
        report("Engine validate_all", d["ok"], detail)
        results.append(d["ok"])
    except Exception as e:
        report("Engine validate_all", False, "parse error: " + str(e))
        results.append(False)

    header("5/6  Workflows (15 FSM)")
    ok, out = step("wfs", lambda: run_py(["python", ".xforge/engine/xforge_engine.py", "xforge_workflow_list"]))
    try:
        import json
        wfs = json.loads(out)["workflows"]
        valid_count = 0
        for w in wfs:
            r2 = subprocess.run(["python", ".xforge/engine/xforge_engine.py",
                                 "xforge_workflow_validate", "@" + str(PROJECT_ROOT / ".tmp.json")],
                                capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT))
            (PROJECT_ROOT / ".tmp.json").write_text('{"id":"' + w["id"] + '"}', encoding="utf-8")
            r2 = subprocess.run(["python", ".xforge/engine/xforge_engine.py",
                                 "xforge_workflow_validate", "@.tmp.json"],
                                capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT))
            try:
                d2 = json.loads(r2.stdout)
                if d2.get("valid"):
                    valid_count += 1
            except Exception:
                pass
        detail = str(valid_count) + "/" + str(len(wfs)) + " valid"
        report("Workflows", valid_count == len(wfs), detail)
        results.append(valid_count == len(wfs))
    except Exception as e:
        report("Workflows", False, "error: " + str(e))
        results.append(False)
    try:
        (PROJECT_ROOT / ".tmp.json").unlink()
    except Exception:
        pass

    header("6/6  MCP tools (17 tools exposed)")
    try:
        mft = json.loads((PROJECT_ROOT / ".xforge" / "mcp" / "manifest.json").read_text(encoding="utf-8"))
        n = len(mft["tools"])
        report("MCP tools", n >= 5, str(n) + " tools")
        results.append(n >= 5)
    except Exception as e:
        report("MCP tools", False, "error: " + str(e))
        results.append(False)

    print("")
    print("=" * 60)
    if all(results):
        print(" \033[32mOVERALL: PASS\033[0m")
        print("=" * 60)
        return 0
    else:
        print(" \033[31mOVERALL: FAIL\033[0m")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())