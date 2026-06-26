"""
Pack tools - marketplace pack management (list, install, uninstall, create).

Extraido de xforge_engine.py em v3.10.5 per DR-0092.
Contem: 4 tools + 3 helpers.
Imports de pack.py (engine side) para marketplace operations.
"""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from .common import (_ok, _err, _iso_now, ROOT, MARKETPLACE, PACKS_INSTALLED, INDEX_JSON, KNOWLEDGE, _load_index_cached, _invalidate_index_cache)


def _read_installed_packs():
    if not PACKS_INSTALLED.exists():
        return {}
    try:
        return json.loads(PACKS_INSTALLED.read_text(encoding="utf-8")).get("packs", {})
    except Exception:
        return {}


def _reindex_pack(pid, file_paths):
    idx = _load_index_cached()
    if idx is None:
        return
    _invalidate_index_cache()  # ensure we read fresh after write below
    idx = json.loads(INDEX_JSON.read_text(encoding="utf-8"))  # reload fresh
    files = idx.setdefault("files", [])
    for fp in file_paths:
        abs_p = ROOT / fp
        if not abs_p.exists():
            continue
        try:
            content = abs_p.read_text(encoding="utf-8")
            m = re.match(r"(?s)^---\r?\n(.+?)\r?\n---", content)
            fm = m.group(1) if m else ""
            lines = len(content.splitlines())
            kw = []
            for ln in fm.splitlines():
                if ln.startswith("tags:"):
                    kw = re.findall(r"[A-Za-z][A-Za-z0-9-]+", ln)
                    break
            if any(f.get("path") == fp for f in files):
                continue
            files.append({"domain": "pack", "relevance": "medium", "path": fp,
                          "summary": "From pack " + pid + " - " + str(lines) + " lines",
                          "category": "pack", "keywords": kw + [pid],
                          "lines": lines, "pack": pid})
        except Exception:
            continue
    idx["files"] = files
    INDEX_JSON.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")
    _invalidate_index_cache()


def _unindex_pack(pid):
    idx = _load_index_cached()
    if idx is None:
        return
    _invalidate_index_cache()  # ensure we read fresh after write below
    idx = json.loads(INDEX_JSON.read_text(encoding="utf-8"))  # reload fresh
    idx["files"] = [f for f in idx.get("files", []) if f.get("pack") != pid]
    INDEX_JSON.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")
    _invalidate_index_cache()


def tool_pack_list(args):
    if not MARKETPLACE.exists():
        return _ok(packs=[])
    installed = _read_installed_packs()
    packs = []
    for p in sorted(MARKETPLACE.glob("*.json")):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            packs.append({"file": p.name, "error": str(e)})
            continue
        pid = m.get("id")
        packs.append({"id": pid, "name": m.get("name"), "version": m.get("version"),
                      "description": m.get("description"), "trustScore": m.get("trustScore"),
                      "tags": m.get("tags", []), "source": m.get("source"),
                      "dependencies": m.get("dependencies", []),
                      "installed": pid in installed})
    return _ok(count=len(packs), packs=packs)


def tool_pack_install(args):
    pid = (args.get("id") or "").lower()
    if not pid:
        return _err("id required")
    manifest = MARKETPLACE / (pid + ".json")
    if not manifest.exists():
        return _err("pack '" + pid + "' not found in marketplace")
    try:
        m = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as e:
        return _err("manifest invalid: " + str(e))
    src_rel = m.get("source", ".xforge/business/" + pid.replace("xforge-", "") + "/")
    src = ROOT / src_rel
    if not src.exists():
        return _err("pack source directory not found: " + src_rel)
    files = list(src.rglob("*.md"))
    if not files:
        return _err("pack source has no .md files: " + src_rel)
    dest = KNOWLEDGE / "packs" / pid
    dest.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in files:
        rel = f.relative_to(src)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
        copied.append(str(target.relative_to(ROOT)))
    installed = _read_installed_packs()
    installed[pid] = {"name": m.get("name"), "version": m.get("version"),
                      "trustScore": m.get("trustScore"),
                      "installedAt": _iso_now(), "files": len(copied)}
    PACKS_INSTALLED.parent.mkdir(parents=True, exist_ok=True)
    PACKS_INSTALLED.write_text(json.dumps({"version": "1.0.0", "packs": installed},
                                          indent=2, ensure_ascii=False), encoding="utf-8")
    _reindex_pack(pid, copied)
    return _ok(pack=pid, filesInstalled=len(copied),
               destination=str(dest.relative_to(ROOT)), registered=True,
               installedAt=installed[pid]["installedAt"])


def tool_pack_uninstall(args):
    pid = (args.get("id") or "").lower()
    if not pid:
        return _err("id required")
    installed = _read_installed_packs()
    if pid not in installed:
        return _err("pack '" + pid + "' is not installed")
    dest = KNOWLEDGE / "packs" / pid
    removed = 0
    if dest.exists():
        for f in dest.rglob("*.md"):
            f.unlink()
            removed += 1
        for d in sorted(dest.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        if dest.exists() and not any(dest.iterdir()):
            dest.rmdir()
    del installed[pid]
    PACKS_INSTALLED.write_text(json.dumps({"version": "1.0.0", "packs": installed},
                                          indent=2, ensure_ascii=False), encoding="utf-8")
    _unindex_pack(pid)
    return _ok(pack=pid, filesRemoved=removed)

def tool_pack_create(args):
    """Scaffold a new knowledge pack (idempotent, never overwrites)."""
    name = (args.get("name") or args.get("id") or "").lower().strip()
    if not name:
        return _err("name required")
    if not name.startswith("xforge-"):
        return _err("pack name must start with xforge- (got: " + name + ")")
    version = args.get("version") or "1.0.0"
    trustScore = int(args.get("trustScore") or 80)
    if trustScore < 0 or trustScore > 100:
        return _err("trustScore must be 0-100")
    tags = args.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    domain = args.get("domain") or "general"
    description = args.get("description") or ("Knowledge pack: " + name)
    files = args.get("files") or ["overview.md", "details.md"]
    if isinstance(files, str):
        files = [f.strip() for f in files.split(",") if f.strip()]

    manifest_dir = MARKETPLACE
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / (name + ".json")
    if manifest_path.exists():
        return _err("pack manifest already exists: " + str(manifest_path))
    manifest = {
        "name": name, "version": version,
        "author": args.get("author") or "XForge Engineer",
        "trustScore": trustScore, "tags": tags,
        "domain": domain, "description": description,
        "files": files, "dependencies": args.get("dependencies") or [],
        "kbVersion": "1.0", "lastUpdated": "2026-06-13",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")

    pack_dir = KNOWLEDGE / "packs" / name
    pack_dir.mkdir(parents=True, exist_ok=True)
    created_files = []
    for fname in files:
        fpath = pack_dir / fname
        if fpath.exists():
            continue
        fm_lines = [
            "---",
            "id: knowledge-" + name + "-" + fname.replace(".md", ""),
            "type: knowledge",
            "title: " + name + " - " + fname.replace(".md", "").replace("-", " ").title(),
            "domain: " + domain,
            "trustScore: " + str(trustScore),
            "source: " + (args.get("source") or "autoresearch-authored"),
            "tags: [" + ", ".join(tags) + "]",
            "status: stub", "priority: medium", "coverage: minimal",
            "lastReviewed: 2026-06-13",
            "---", "",
            "# " + name + " - " + fname.replace(".md", "").replace("-", " ").title(),
            "", "_Stub content. Replace with real content before promoting._", "",
        ]
        fpath.write_text(chr(10).join(fm_lines), encoding="utf-8")
        created_files.append(str(fpath.relative_to(ROOT)))

    installed = _read_installed_packs()
    if name not in installed:
        installed[name] = {
            "name": name, "version": version, "trustScore": trustScore,
            "installedAt": _iso_now(), "files": len(files), "domain": domain,
        }
        PACKS_INSTALLED.write_text(
            json.dumps({"version": "1.0.0", "packs": installed}, ensure_ascii=False, indent=2) + chr(10),
            encoding="utf-8",
        )
    return _ok(
        pack=name,
        manifest=str(manifest_path.relative_to(ROOT)),
        contentDir=str(pack_dir.relative_to(ROOT)),
        filesCreated=len(created_files),
        files=created_files,
        registered=True,
    )

