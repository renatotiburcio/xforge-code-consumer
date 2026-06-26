"""
Doctor tool - health check via doctor.ps1 with TTL cache.

Extraido de xforge_engine.py em v3.9.2 per DR-0084.
"""
from .common import ROOT, _DOCTOR_CACHE, _DOCTOR_TTL_SEC, _ok, _err
import subprocess


def tool_doctor_run(args):
    """Run doctor.ps1 with TTL cache to avoid PowerShell startup overhead."""
    import time as _time
    now = _time.time()
    cached = _DOCTOR_CACHE["result"]
    if cached is not None and now < _DOCTOR_CACHE["expires_at"]:
        _DOCTOR_CACHE["hits"] += 1
        return _ok(**cached, cached=True, cache_ttl_sec=_DOCTOR_TTL_SEC)
    doctor_script = ROOT / ".kilo" / "automation" / "scripts" / "doctor.ps1"
    if not doctor_script.exists():
        return _err("doctor.ps1 not found")
    try:
        r = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile",
             "-File", str(doctor_script)],
            capture_output=True, text=True, timeout=120, cwd=str(ROOT))
        result_payload = {"exitCode": r.returncode, "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:]}
        _DOCTOR_CACHE["result"] = result_payload
        _DOCTOR_CACHE["expires_at"] = now + _DOCTOR_TTL_SEC
        _DOCTOR_CACHE["misses"] += 1
        return _ok(**result_payload, cached=False, cache_ttl_sec=_DOCTOR_TTL_SEC)
    except Exception as e:
        return _err(str(e))


def _run_doctor_cached():
    """Run doctor.ps1 subprocess returning structured result."""
    r = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile",
         "-File", str(ROOT / ".kilo" / "automation" / "scripts" / "doctor.ps1")],
        capture_output=True, text=True, timeout=120, cwd=str(ROOT))
    doctor_errs = sum(1 for line in r.stdout.splitlines() if line.startswith("[ERROR]"))
    doctor_warns = sum(1 for line in r.stdout.splitlines() if line.startswith("[WARN]"))
    return {
        "ok": r.returncode == 0 and doctor_errs == 0,
        "exitCode": r.returncode,
        "errors": doctor_errs, "warnings": doctor_warns,
    }
