"""
Validate tools - health/validation checks via subprocesses.

Extraido de xforge_engine.py em v3.9.2 per DR-0084.
Contem: tool_validate_all + 3 _run_*_cached helpers + workflow parallel validator.
"""
from .common import ROOT, _PYTEST_CACHE, _PYTEST_TTL_SEC, _ok
import subprocess, re
import os as _os_v
import time as _t_v


def _run_knowledge_cached():
    r = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile",
         "-File", str(ROOT / ".xforge" / "schemas" / "validate-knowledge.ps1")],
        capture_output=True, text=True, timeout=60, cwd=str(ROOT.resolve()))
    ok = "All knowledge files valid" in r.stdout
    m_total = re.search(r"Total:\s*(\d+)", r.stdout)
    m_valid = re.search(r"Valid:\s*(\d+)", r.stdout)
    m_loose = re.search(r"Loose:\s*(\d+)", r.stdout)
    m_invalid = re.search(r"Invalid:\s*(\d+)", r.stdout)
    return {
        "ok": ok,
        "total": int(m_total.group(1)) if m_total else 0,
        "valid": int(m_valid.group(1)) if m_valid else 0,
        "loose": int(m_loose.group(1)) if m_loose else 0,
        "invalid": int(m_invalid.group(1)) if m_invalid else 0,
    }


def _run_pytest_cached():
    """Run pytest with disk-based TTL cache (v1.1.2)."""
    cache_file = ROOT / ".xforge" / ".cache" / "pytest-result.json"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    now = _t_v.time()
    if cache_file.exists():
        try:
            import json as _json_p
            cached = _json_p.loads(cache_file.read_text(encoding="utf-8"))
            expires_at = float(cached.get("expires_at", 0))
            if now < expires_at and "result" in cached:
                _PYTEST_CACHE["hits"] += 1
                result = dict(cached["result"])
                result["cached"] = True
                result["cache_ttl_sec"] = int(expires_at - now)
                result["cache_path"] = str(cache_file)
                _PYTEST_CACHE["result"] = result
                _PYTEST_CACHE["expires_at"] = expires_at
                return result
        except (OSError, ValueError):
            pass
    _PYTEST_CACHE["misses"] += 1
    _PYTEST_CACHE["runs"] += 1
    try:
        engine_dir = str((ROOT / ".xforge" / "engine").resolve())
        r = subprocess.run(
            ["python", "-m", "pytest", "tests",
             "-q", "--tb=no", "-p", "no:cacheprovider"],
            capture_output=True, text=True, timeout=300,
            cwd=engine_dir)
        last_line = r.stdout.strip().split(chr(10))[-1] if r.stdout.strip() else ""
        m = re.search(r"(\d+) passed", last_line)
        m_failed = re.search(r"(\d+) failed", last_line)
        passed = int(m.group(1)) if m else 0
        failed = int(m_failed.group(1)) if m_failed else 0
        result = {
            "ok": r.returncode == 0 and failed == 0,
            "passed": passed, "failed": failed,
            "cached": False,
        }
    except subprocess.TimeoutExpired:
        result = {"ok": False, "error": "timeout", "cached": False}
    except Exception as e:
        result = {"ok": False, "error": str(e), "cached": False}
    try:
        import json as _json_p
        cache_file.write_text(_json_p.dumps({
            "result": result,
            "expires_at": now + _PYTEST_TTL_SEC,
            "written_at": now,
        }, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    _PYTEST_CACHE["result"] = dict(result)
    _PYTEST_CACHE["expires_at"] = now + _PYTEST_TTL_SEC
    return result


def _run_workflow_validate_parallel(workflows):
    from concurrent.futures import ThreadPoolExecutor
    # Lazy import to avoid circular dependency with engine
    import xforge_engine
    valid_wf = 0
    invalid_wf = []
    def _validate_one(w):
        v = xforge_engine.tool_workflow_validate({"id": w["id"]})
        return w["id"], v.get("valid", False), v.get("errors", [])
    with ThreadPoolExecutor(max_workers=min(8, len(workflows))) as pool:
        for wf_id, valid, errs in pool.map(_validate_one, workflows):
            if valid:
                valid_wf += 1
            else:
                invalid_wf.append({"id": wf_id, "errors": errs})
    return valid_wf, invalid_wf


def tool_validate_all(args):
    """Run comprehensive validation (doctor + knowledge + pytest + workflows + infra + mcp + packs + tenants + xfs)."""
    import time
    import json
    from concurrent.futures import ThreadPoolExecutor
    # Lazy imports para evitar circular dependency
    from .doctor import _run_doctor_cached
    import xforge_engine
    start = time.time()
    result = {"ok": True, "checks": {}, "summary": {}}
    checks = result["checks"]

    # Parallel: 4 checks
    with ThreadPoolExecutor(max_workers=4) as pool:
        f_doctor = pool.submit(_run_doctor_cached)
        f_knowledge = pool.submit(_run_knowledge_cached)
        f_pytest = pool.submit(_run_pytest_cached)
        f_wf_list = pool.submit(xforge_engine.tool_workflow_list, {})
        try:
            checks["doctor"] = f_doctor.result()
        except Exception as e:
            checks["doctor"] = {"ok": False, "error": str(e)}
        try:
            checks["knowledge"] = f_knowledge.result()
        except Exception as e:
            checks["knowledge"] = {"ok": False, "error": str(e)}
        try:
            checks["pytest"] = f_pytest.result()
        except Exception as e:
            checks["pytest"] = {"ok": False, "error": str(e)}
        try:
            wf_res = f_wf_list.result()
        except Exception as e:
            wf_res = {"ok": False, "workflows": []}

    # 3. Workflows (parallel validate)
    if wf_res.get("ok"):
        valid_wf, invalid_wf = _run_workflow_validate_parallel(wf_res["workflows"])
        checks["workflows"] = {
            "ok": len(invalid_wf) == 0,
            "total": len(wf_res["workflows"]),
            "valid": valid_wf,
            "invalid": invalid_wf,
        }
        if invalid_wf:
            result["ok"] = False

    # 4. Infra
    eng = ROOT / ".xforge" / "engine" / "xforge_engine.py"
    srv = ROOT / ".xforge" / "mcp" / "server.js"
    mft = ROOT / ".xforge" / "mcp" / "manifest.json"
    checks["infra"] = {
        "ok": all(p.exists() and p.stat().st_size > 100 for p in (eng, srv, mft)),
        "engine_bytes": eng.stat().st_size if eng.exists() else 0,
        "server_bytes": srv.stat().st_size if srv.exists() else 0,
        "manifest_bytes": mft.stat().st_size if mft.exists() else 0,
    }
    if not checks["infra"]["ok"]:
        result["ok"] = False
    # 5. MCP
    if mft.exists():
        try:
            m = json.loads(mft.read_text(encoding="utf-8"))
            tool_count = len(m.get("tools", []))
            checks["mcp"] = {"ok": tool_count >= 5, "toolCount": tool_count}
            if tool_count < 5:
                result["ok"] = False
        except Exception as e:
            checks["mcp"] = {"ok": False, "error": str(e)}
            result["ok"] = False
    # 6. Packs
    packs = xforge_engine.tool_pack_list({})
    installed = packs.get("packs", [])
    installed_count = sum(1 for p in installed if p.get("installed"))
    checks["packs"] = {
        "ok": True,
        "available": packs.get("count", 0) if packs.get("ok") else 0,
        "installed": installed_count,
    }
    # 7. Tenants
    tenants = xforge_engine.tool_tenant_list({})
    checks["tenants"] = {
        "ok": tenants.get("ok", False),
        "count": tenants.get("count", 0),
    }
    # 8. xfs
    xfs = xforge_engine._measure_xfs()
    checks["xfs"] = {"ok": xfs >= 0.7, "value": xfs}
    if xfs < 0.7:
        result["ok"] = False

    result["summary"] = {
        "totalChecks": len(checks),
        "passedChecks": sum(1 for c in checks.values() if c.get("ok")),
        "failedChecks": sum(1 for c in checks.values() if not c.get("ok")),
        "elapsedMs": int((time.time() - start) * 1000),
    }
    return result
