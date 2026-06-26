"""
Tenant tools - multi-tenant management (list, create, use).

Extraido de xforge_engine.py em v3.10.4 per DR-0091.
"""
import json
import re
from .common import _ok, _err, _iso_now, TENANTS_DIR, ROOT


def tool_tenant_list(args):
    if not TENANTS_DIR.exists():
        return _ok(tenants=[])
    tenants = []
    for d in sorted(TENANTS_DIR.iterdir()):
        if not d.is_dir():
            continue
        cfg_path = d / "config.json"
        cfg = {}
        if cfg_path.exists():
            try:
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            except Exception:
                cfg = {"_error": "invalid config.json"}
        kpath = d / "knowledge"
        files = sum(1 for _ in kpath.rglob("*.md")) if kpath.exists() else 0
        tenants.append({"id": d.name, "name": cfg.get("name", d.name),
                        "knowledgePath": str(kpath.relative_to(ROOT)) if kpath.exists() else None,
                        "files": files, "createdAt": cfg.get("createdAt"),
                        "active": cfg.get("active", False)})
    return _ok(count=len(tenants), tenants=tenants)


def tool_tenant_create(args):
    tid = re.sub(r"[^a-z0-9-]", "", (args.get("id") or "").lower())
    name = (args.get("name") or tid).strip()
    if not tid:
        return _err("id required (kebab-case)")
    if not re.match(r"^[a-z][a-z0-9-]*$", tid):
        return _err("id must be kebab-case")
    td = TENANTS_DIR / ("tenant-" + tid)
    if td.exists():
        return _err("tenant 'tenant-" + tid + "' already exists")
    td.mkdir(parents=True)
    (td / "knowledge").mkdir()
    (td / "rag").mkdir()
    (td / "rag" / "indexes").mkdir()
    cfg = {"id": tid, "name": name, "createdAt": _iso_now(), "active": True,
           "isolation": "filesystem",
           "knowledgePath": ".xforge/tenants/tenant-" + tid + "/knowledge/",
           "ragPath": ".xforge/tenants/tenant-" + tid + "/rag/"}
    (td / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    return _ok(tenant={"id": tid, "name": name, "path": str(td.relative_to(ROOT)),
                       "knowledgePath": cfg["knowledgePath"], "createdAt": cfg["createdAt"]})


def tool_tenant_use(args):
    tid = (args.get("id") or "").lower()
    if not tid:
        return _err("id required")
    if not tid.startswith("tenant-"):
        tid = "tenant-" + tid
    td = TENANTS_DIR / tid
    if not td.exists():
        available = [d.name for d in TENANTS_DIR.iterdir() if d.is_dir()] if TENANTS_DIR.exists() else []
        return _err("tenant '" + tid + "' not found", available=available)
    cfg_path = td / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    if TENANTS_DIR.exists():
        for d in TENANTS_DIR.iterdir():
            if not d.is_dir():
                continue
            cp = d / "config.json"
            if cp.exists():
                try:
                    c = json.loads(cp.read_text(encoding="utf-8"))
                    c["active"] = (d.name == tid)
                    cp.write_text(json.dumps(c, indent=2, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass
    return _ok(active=tid, tenant=cfg, knowledgePath=cfg.get("knowledgePath"),
               ragPath=cfg.get("ragPath"))
