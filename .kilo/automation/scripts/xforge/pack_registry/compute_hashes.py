"""Compute real SHA256 hashes for bundled packs."""
import hashlib
import json
from pathlib import Path

REG_DIR = Path("D:/dev/XForge-Development-New/.kilo/automation/scripts/xforge/pack_registry")
PACKS_DIR = REG_DIR / "packs"
REGISTRY_FILE = REG_DIR / "registry.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))

for p in reg["packs"]:
    pack_id = p["id"]
    slug = f"{pack_id}-{p['version']}"
    tarball = PACKS_DIR / f"{slug}.tar.gz"
    if not tarball.exists():
        print(f"SKIP: {tarball.name} not found")
        continue
    digest = sha256_file(tarball)
    p["sha256"] = digest
    p["sizeBytes"] = tarball.stat().st_size
    print(f"{pack_id:<28} v{p['version']:<8} sha256={digest[:16]}... size={tarball.stat().st_size}B")

REGISTRY_FILE.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nRegistry updated")
