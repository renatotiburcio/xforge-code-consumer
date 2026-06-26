"""pack.py - Marketplace pack registry, search, install.

Pack format:
    pack_id-version.tar.gz contains:
        <pack_id>-<version>/manifest.json   (required)
        <pack_id>-<version>/...             (files to install)

manifest.json schema:
    {
        "id": "xforge-fiscal",
        "name": "Brazilian Fiscal Pack",
        "version": "1.2.0",
        "description": "...",
        "trustScore": 95,
        "files": ["knowledge/icms.md", ...]  (optional, computed if absent)
    }
"""
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

MIN_TRUST_SCORE = 60
REGISTRY_LOCAL = Path(__file__).resolve().parent / "pack_registry" / "registry.json"


def load_registry(registry_path=None):
    """Load pack registry. Returns dict with packs list."""
    path = registry_path or REGISTRY_LOCAL
    if not path.exists():
        return {"version": "1.0", "packs": []}
    return json.loads(path.read_text(encoding="utf-8"))


def search_packs(query=None, tag=None, min_trust=MIN_TRUST_SCORE, registry_path=None):
    """Search packs in registry."""
    reg = load_registry(registry_path)
    results = []
    for p in reg.get("packs", []):
        if p.get("trustScore", 0) < min_trust:
            continue
        if query:
            q = query.lower()
            text = (p.get("name", "") + " " + p.get("description", "") + " " + " ".join(p.get("tags", []))).lower()
            if q not in text:
                continue
        if tag and tag.lower() not in [t.lower() for t in p.get("tags", [])]:
            continue
        results.append(p)
    return results


def resolve_pack(pack_id, registry_path=None):
    """Find a pack in registry by id. Returns dict or None."""
    reg = load_registry(registry_path)
    for p in reg.get("packs", []):
        if p.get("id") == pack_id:
            return p
    return None


def compute_sha256(path):
    """Compute SHA256 of file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_pack(pack_meta, dest_dir):
    """Download pack from URL to dest_dir. Returns path to downloaded tarball.

    Supports:
      - file://<path>  (local file - default for bundled packs)
      - https://<url>  (remote HTTPS)
    """
    url = pack_meta.get("downloadUrl", "")
    if not url:
        raise ValueError(f"Pack {pack_meta.get('id')} has no downloadUrl")

    dest_dir.mkdir(parents=True, exist_ok=True)
    fname = url.rsplit("/", 1)[-1] if "/" in url else f"{pack_meta['id']}.tar.gz"
    target = dest_dir / fname

    if url.startswith("file://"):
        src = url[7:]
        if src.startswith("xforge/registry/"):
            src = str(Path(__file__).resolve().parent / "pack_registry" / "packs" / src.rsplit("/", 1)[-1])
        if not Path(src).exists():
            raise FileNotFoundError(f"Local pack not found: {src}")
        shutil.copy2(src, target)
    elif url.startswith("https://"):
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        target.write_bytes(data)
    else:
        raise ValueError(f"Unsupported URL scheme: {url}")

    return target


def verify_pack(tarball_path, expected_sha256):
    """Verify pack SHA256. expected_sha256 is None to skip check."""
    if not expected_sha256 or expected_sha256.startswith("placeholder-"):
        return True, "skipped (placeholder hash)"
    actual = compute_sha256(tarball_path)
    if actual == expected_sha256:
        return True, "ok"
    return False, f"hash mismatch (expected {expected_sha256[:16]}..., got {actual[:16]}...)"


class UnsafePackError(ValueError):
    """Raised when pack contains unsafe paths (zip-slip, absolute, etc.)."""
    pass


def _validate_member_path(member_name, target_root):
    """Validate tar member path to prevent zip-slip attacks.

    Returns safe relative path or raises UnsafePackError.
    """
    parts = member_name.split("/", 1)
    rel = parts[1] if len(parts) == 2 else parts[0]
    if not rel or rel.startswith("/"):
        raise UnsafePackError(f"Absolute or empty path: {member_name!r}")
    if rel.startswith("..") or "/.." in ("/" + rel):
        raise UnsafePackError(f"Path traversal attempt: {member_name!r}")
    if "\\" in rel or rel.startswith("\\"):
        raise UnsafePackError(f"Backslash path: {member_name!r}")
    target_resolved = (target_root / rel).resolve()
    root_resolved = target_root.resolve()
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError:
        raise UnsafePackError(f"Resolved path escapes target: {member_name!r}")
    return rel


def extract_pack(tarball_path, target_root):
    """Extract pack to target_root. Returns manifest dict + list of installed files.

    Validates every member path against zip-slip attacks.
    """
    files = []
    manifest = None
    target_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tarball_path, "r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            f = tar.extractfile(member)
            if f is None:
                continue
            content = f.read()
            rel = _validate_member_path(member.name, target_root)
            if rel == "manifest.json":
                manifest = json.loads(content.decode("utf-8"))
                continue
            dest = target_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            files.append(rel)
    if manifest is None:
        raise ValueError("Pack has no manifest.json")
    if "files" not in manifest:
        manifest["files"] = files
    return manifest, files


def install_pack(pack_id, project_root, registry_path=None, force=False):
    """Install a pack by id. Returns (manifest, error_msg)."""
    pack = resolve_pack(pack_id, registry_path)
    if pack is None:
        return None, f"Pack '{pack_id}' not found in registry"

    trust = pack.get("trustScore", 0)
    if trust < MIN_TRUST_SCORE and not force:
        return None, f"Trust score {trust} < minimum {MIN_TRUST_SCORE}. Use --force para instalar mesmo assim."

    xforge_packs = project_root / ".xforge" / "packs"
    installed_file = xforge_packs / "installed.json"
    installed = {"version": "1.0", "packs": {}, "lastUpdated": ""}
    if installed_file.exists():
        try:
            installed = json.loads(installed_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    if pack_id in installed.get("packs", {}) and not force:
        return None, f"Pack '{pack_id}' ja instalado. Use --force para reinstalar."

    print(f"[XForge] Baixando {pack_id} v{pack.get('version', '?')}...")
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        try:
            tarball = fetch_pack(pack, td_path)
        except Exception as e:
            return None, f"Falha no download: {e}"

        print(f"[XForge] Verificando SHA256...")
        ok, msg = verify_pack(tarball, pack.get("sha256"))
        if not ok:
            tarball.unlink(missing_ok=True)
            return None, f"Verificacao falhou: {msg}"
        if not msg.startswith("skipped"):
            print(f"[XForge]   SHA256 OK")

        print(f"[XForge] Extraindo em .xforge/packs/{pack_id}/...")
        target = xforge_packs / pack_id
        if target.exists() and force:
            shutil.rmtree(target)
        try:
            manifest, files = extract_pack(tarball, target)
        except Exception as e:
            return None, f"Falha ao extrair: {e}"

    manifest["installedAt"] = datetime.now().isoformat()
    manifest["sourceUrl"] = pack.get("downloadUrl")
    installed.setdefault("packs", {})[pack_id] = manifest
    installed["lastUpdated"] = datetime.now().isoformat()
    installed_file.parent.mkdir(parents=True, exist_ok=True)
    installed_file.write_text(json.dumps(installed, indent=2, ensure_ascii=False), encoding="utf-8")

    return manifest, None



def update_registry(registry_url=None, registry_path=None):
    """Refresh registry.json from remote URL. Falls back to bundled registry on error.

    Returns (new_registry, error_msg).
    """
    url = registry_url or "https://raw.githubusercontent.com/renatotiburcio/xforge-packs/main/registry.json"
    local_path = registry_path or REGISTRY_LOCAL
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
        new_reg = json.loads(data.decode("utf-8"))
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(json.dumps(new_reg, indent=2, ensure_ascii=False), encoding="utf-8")
        return new_reg, None
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
        return load_registry(local_path), f"Falha ao atualizar de {url}: {e}"


def upgrade_pack(pack_id, project_root, force=False):
    """Upgrade an installed pack to latest version (force reinstall)."""
    xforge_packs = project_root / ".xforge" / "packs"
    installed_file = xforge_packs / "installed.json"
    if not installed_file.exists():
        return None, "Nenhum pack instalado. Use 'xforge pack install ID' primeiro."
    try:
        installed = json.loads(installed_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return None, f"installed.json invalido: {e}"
    if pack_id not in installed.get("packs", {}):
        return None, f"Pack {pack_id} nao esta instalado."
    return install_pack(pack_id, project_root, force=True)
