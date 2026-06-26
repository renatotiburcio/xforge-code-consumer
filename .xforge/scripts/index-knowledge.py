#!/usr/bin/env python3
"""
XForge Knowledge Indexer — Generate embeddings for all knowledge files.

Usage:
    python .xforge/scripts/index-knowledge.py [--reindex] [--stats]

Requirements:
    - Ollama running locally (optional, falls back to hash-based embeddings)
    - Python 3.11+
"""

import json
import os
import sys
import hashlib
import math
import re
import time
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_DIR = ROOT / ".xforge" / "knowledge"
INDEX_FILE = KNOWLEDGE_DIR / "INDEX.json"
EMBEDDINGS_FILE = KNOWLEDGE_DIR / "embeddings.json"

OLLAMA_ENDPOINT = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 768
TIMEOUT = 30


def log(msg: str, level: str = "INFO"):
    """Simple logging."""
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {level}: {msg}", file=sys.stderr)


def hash_embedding(text: str, dim: int = EMBEDDING_DIM) -> list[float]:
    """Generate a deterministic hash-based embedding (fallback)."""
    hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
    vector = []
    for i in range(dim):
        vector.append(math.sin(hash_val + i) * 0.5)
    # Normalize
    norm = math.sqrt(sum(v * v for v in vector))
    if norm == 0:
        return vector
    return [v / norm for v in vector]


def ollama_embedding(text: str) -> Optional[list[float]]:
    """Get embedding from Ollama API."""
    try:
        import urllib.request
        data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text[:2048]}).encode()
        req = urllib.request.Request(
            OLLAMA_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode())
            return result.get("embedding")
    except Exception:
        return None


def chunk_text(text: str, max_chars: int = 500) -> list[str]:
    """Split text into chunks for embedding."""
    sentences = re.split(r'[.!?\n]+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current) + len(sentence) > max_chars:
            if current:
                chunks.append(current)
            current = sentence
        else:
            current += " " + sentence if current else sentence
    if current:
        chunks.append(current)
    return chunks or [text[:max_chars]]


def load_index() -> dict:
    """Load knowledge INDEX.json."""
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {"entries": [], "totalEntries": 0}


def save_embeddings(embeddings: list[dict]):
    """Save embeddings to file."""
    EMBEDDINGS_FILE.write_text(json.dumps(embeddings, indent=2), encoding="utf-8")
    log(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_FILE}")


def load_embeddings() -> list[dict]:
    """Load existing embeddings."""
    if EMBEDDINGS_FILE.exists():
        return json.loads(EMBEDDINGS_FILE.read_text(encoding="utf-8"))
    return []


def check_ollama() -> bool:
    """Check if Ollama is available."""
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Index knowledge with embeddings")
    parser.add_argument("--reindex", action="store_true", help="Reindex all files")
    parser.add_argument("--stats", action="store_true", help="Show stats only")
    parser.add_argument("--max-entries", type=int, default=50, help="Max entries to index (default 50)")
    parser.add_argument("--use-hash", action="store_true", help="Use hash embeddings (fast, no Ollama)")
    args = parser.parse_args()

    log("Starting knowledge indexing...")

    # Check Ollama
    ollama_available = check_ollama() and not args.use_hash
    if ollama_available:
        log("Ollama detected — using real embeddings")
    else:
        log("Using hash-based embeddings (fast mode)")

    # Load index
    index = load_index()
    entries = index.get("entries", [])
    log(f"Found {len(entries)} knowledge entries")

    if args.stats:
        embeddings = load_embeddings()
        log(f"Existing embeddings: {len(embeddings)}")
        sources = set(e.get("source", "") for e in embeddings)
        log(f"Sources: {len(sources)}")
        return

    # Load existing embeddings
    existing = load_embeddings()
    existing_ids = {e["id"] for e in existing}

    embeddings = list(existing) if not args.reindex else []
    new_count = 0
    skip_count = 0
    error_count = 0

    for entry in entries:
        entry_id = entry.get("id", "")
        if not entry_id:
            continue

        if entry_id in existing_ids and not args.reindex:
            skip_count += 1
            continue

        # Limit entries
        if new_count >= args.max_entries:
            log(f"Reached max entries limit ({args.max_entries})")
            break

        # Get text content
        path = entry.get("path", "")
        title = entry.get("title", "")
        summary = entry.get("summary", "")

        # Try to read file
        text = ""
        file_path = ROOT / path
        if file_path.exists():
            try:
                text = file_path.read_text(encoding="utf-8")[:40048]
            except Exception:
                text = f"{title} {summary}"
        else:
            text = f"{title} {summary}"

        if not text.strip():
            skip_count += 1
            continue

        # Generate embedding
        try:
            if ollama_available:
                vector = ollama_embedding(text[:2048])
                if vector is None:
                    vector = hash_embedding(text)
            else:
                vector = hash_embedding(text)

            embeddings.append({
                "id": entry_id,
                "vector": vector,
                "metadata": {
                    "title": title,
                    "path": path,
                    "domain": entry.get("domain", ""),
                    "tags": entry.get("tags", []),
                    "timestamp": int(time.time())
                }
            })
            new_count += 1

            if new_count % 10 == 0:
                log(f"Indexed {new_count} entries...")

        except Exception as e:
            log(f"Error indexing {entry_id}: {e}", "ERROR")
            error_count += 1

    # Save
    save_embeddings(embeddings)

    log(f"Indexing complete:")
    log(f"  New: {new_count}")
    log(f"  Skipped: {skip_count}")
    log(f"  Errors: {error_count}")
    log(f"  Total: {len(embeddings)}")


if __name__ == "__main__":
    main()
