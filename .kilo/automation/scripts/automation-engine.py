#!/usr/bin/env python3
# XForge Automation Engine
import json, os, sys, subprocess, argparse, time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent.parent
XFORGE = ROOT / ".xforge"
LEARNING = XFORGE / "learning"
MEMORY = XFORGE / "memory"
SESSIONS = MEMORY / "sessions"
REGISTRIES = ROOT / ".kilo/core/registries"

def ensure_dirs():
    for d in [LEARNING, SESSIONS]:
        d.mkdir(parents=True, exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).isoformat() + "Z"

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_doctor():
    doctor = ROOT / ".kilo/automation/scripts/doctor.ps1"
    if not doctor.exists():
        return 1, "doctor.ps1 not found"
    r = subprocess.run([
        "powershell", "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", str(doctor)],
        capture_output=True, text=True, timeout=60, cwd=str(ROOT))
    return r.returncode, r.stdout + r.stderr

def update_registries():
    ensure_dirs()
    results = {}
    kdir = XFORGE / "knowledge"
    areas = []
    if kdir.exists():
        for d in sorted(kdir.iterdir()):
            if d.is_dir():
                files = [str(f.relative_to(ROOT)) for f in sorted(d.rglob('*')) if f.is_file()]
                if files:
                    areas.append({"path": str(d.relative_to(ROOT)), "files": files, "fileCount": len(files)})
    save_json(REGISTRIES / "knowledge-registry.json", {"knowledgeAreas": areas})
    results["knowledge"] = len(areas)
    arch = {"standards": [
        {"id": "endpoints", "path": ".xforge/knowledge/arquitetura/clean-architecture.md"},
        {"id": "cqrs", "path": ".xforge/knowledge/padroes/ef-core-patterns.md"},
        {"id": "dtos", "path": ".xforge/knowledge/arquitetura/design-patterns-gof.md"},
        {"id": "producer-specs", "path": ".xforge/knowledge/padroes/logging.md"}
    ], "rules": []}
    save_json(REGISTRIES / "architecture-registry.json", arch)
    results["architecture"] = len(arch["standards"])
    return results

def main():
    import argparse
    p = argparse.ArgumentParser(description="XForge Automation Engine")
    p.add_argument("request", nargs="?", help="User request")
    p.add_argument("--output", "-o", help="Output file")
    p.add_argument("--registry-update", action="store_true")
    p.add_argument("--doctor", action="store_true")
    args = p.parse_args()
    if args.doctor:
        code, out = run_doctor()
        print(out)
        sys.exit(code)
    if args.registry_update:
        print(json.dumps(update_registries(), indent=2))
        sys.exit(0)
    if not args.request:
        p.print_help()
        sys.exit(1)
    print("Processing: " + args.request)
    print("Registry: " + str(update_registries()))
    print("Done.")

if __name__ == "__main__":
    main()
