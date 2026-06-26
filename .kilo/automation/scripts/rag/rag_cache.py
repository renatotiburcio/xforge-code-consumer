"""
RAG Incremental Cache - Diff-based reindexing.
Tracks file hashes to avoid reindexing unchanged documents.
Manifest stored at .xforge/rag/manifest.json
"""
import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


def get_project_root() -> Path:
    """Find project root by walking up from script location."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "kilo.jsonc").exists() or (current / ".kilo").is_dir():
            return current
        current = current.parent
    return Path.cwd()


def load_manifest(manifest_path: Path) -> Dict[str, Any]:
    """Load existing manifest or create empty one."""
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0.0", "files": {}, "lastFullIndex": None}


def save_manifest(manifest_path: Path, manifest: Dict[str, Any]) -> None:
    """Save manifest to disk."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def file_hash(filepath: Path) -> Optional[str]:
    """Calculate SHA-256 hash of file contents."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, IOError):
        return None


def detect_changes(root: Path, config: Dict[str, Any], manifest: Dict[str, Any]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Compare current files against manifest to detect changes.
    Returns: (added, modified, deleted, unchanged)
    """
    sources = config.get("sources", [])
    exclude = config.get("excludePatterns", [])

    current_files: Dict[str, str] = {}

    for source in sources:
        source_path = root / source
        if source_path.is_file():
            rel = str(source_path.relative_to(root))
            if not any(exc in rel for exc in exclude):
                h = file_hash(source_path)
                if h:
                    current_files[rel] = h
        elif source_path.is_dir():
            for fp in source_path.rglob("*"):
                if fp.is_file():
                    rel = str(fp.relative_to(root))
                    rel = rel.replace(os.sep, "/")
                    if not any(exc in rel for exc in exclude):
                        h = file_hash(fp)
                        if h:
                            current_files[rel] = h

    previous_files = manifest.get("files", {})

    added: List[str] = []
    modified: List[str] = []
    deleted: List[str] = []
    unchanged: List[str] = []

    for rel, h in current_files.items():
        if rel not in previous_files:
            added.append(rel)
        elif previous_files[rel] != h:
            modified.append(rel)
        else:
            unchanged.append(rel)

    for rel in previous_files:
        if rel not in current_files:
            deleted.append(rel)

    return added, modified, deleted, unchanged


def incremental_index(root: Path, config_path: Optional[Path] = None) -> int:
    """
    Perform incremental RAG indexing.
    Only reindex files that are new or modified since last index.
    Returns the number of changes detected.
    """
    root = Path(root)

    # Load RAG config
    if config_path is None:
        config_path = root / ".xforge" / "rag" / "config.json"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Load manifest
    manifest_path = root / ".xforge" / "rag" / "manifest.json"
    manifest = load_manifest(manifest_path)

    # Detect changes
    added, modified, deleted, unchanged = detect_changes(root, config, manifest)

    total_changes = len(added) + len(modified) + len(deleted)

    print(f"RAG Incremental Cache Report")
    print(f"============================")
    print(f"Added:     {len(added)}")
    print(f"Modified:  {len(modified)}")
    print(f"Deleted:   {len(deleted)}")
    print(f"Unchanged: {len(unchanged)}")
    print(f"Total:     {len(added) + len(modified) + len(deleted) + len(unchanged)}")
    print()

    if total_changes == 0:
        print("No changes detected. RAG index is up to date.")
        return 0

    print(f"Changes detected: {total_changes} files need reindexing.")

    # Update manifest with current file hashes
    new_manifest_files: Dict[str, str] = {}

    sources = config.get("sources", [])
    exclude = config.get("excludePatterns", [])

    for source in sources:
        source_path = root / source
        if source_path.is_file():
            rel = str(source_path.relative_to(root)).replace(os.sep, "/")
            if not any(exc in rel for exc in exclude):
                h = file_hash(source_path)
                if h:
                    new_manifest_files[rel] = h
        elif source_path.is_dir():
            for fp in source_path.rglob("*"):
                if fp.is_file():
                    rel = str(fp.relative_to(root)).replace(os.sep, "/")
                    if not any(exc in rel for exc in exclude):
                        h = file_hash(fp)
                        if h:
                            new_manifest_files[rel] = h

    manifest["files"] = new_manifest_files
    manifest["lastFullIndex"] = datetime.now().isoformat()

    # Save updated manifest
    save_manifest(manifest_path, manifest)
    print(f"Manifest updated: {manifest_path}")

    return total_changes


if __name__ == "__main__":
    root = get_project_root()
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            manifest_path = root / ".xforge" / "rag" / "manifest.json"
            if manifest_path.exists():
                manifest = load_manifest(manifest_path)
                print(f"Last index: {manifest.get('lastFullIndex', 'never')}")
                print(f"Tracked files: {len(manifest.get('files', {}))}")
            else:
                print("No manifest found. Run incremental index first.")
        elif sys.argv[1] == "diff":
            config_path = root / ".xforge" / "rag" / "config.json"
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            manifest_path = root / ".xforge" / "rag" / "manifest.json"
            manifest = load_manifest(manifest_path)
            added, modified, deleted, unchanged = detect_changes(root, config, manifest)
            print(f"Added: {len(added)}, Modified: {len(modified)}, Deleted: {len(deleted)}, Unchanged: {len(unchanged)}")
        else:
            print(f"Usage: python rag_cache.py [status|diff]")
    else:
        changes = incremental_index(root)
        sys.exit(0 if changes >= 0 else 1)
