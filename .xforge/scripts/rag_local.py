#!/usr/bin/env python3
"""
rag_local.py - RAG lexical indexer for XForge (DR-0181, v50.0.1+)

Rebuilds:
- .xforge/rag/manifest.json (sha256 + updatedAt per document)
- .xforge/rag/chunks/chunks.jsonl (40-line chunks with overlap)
- .xforge/rag/indexes/lexical.json (inverted index: term -> [chunkIds])
- .xforge/rag/reports/index-report.md (human-readable report)

Usage:
    python .xforge/scripts/rag_local.py reindex
    python .xforge/scripts/rag_local.py status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Stopwords for inverted index
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was",
    "were", "will", "with", "this", "these", "those", "but", "or", "not",
    "be", "been", "being", "have", "had", "having", "do", "does", "did",
    "can", "could", "should", "would", "may", "might", "must", "shall",
}


def detect_source_type(path: str) -> str:
    """Categorize file path into a source type."""
    if path.startswith(".kilo/skills"):
        return "skill"
    if path.startswith(".kilo/agents"):
        return "agent"
    if path.startswith(".kilo/commands"):
        return "command"
    if path.startswith(".kilo/rules"):
        return "rule"
    if path.startswith(".xforge/knowledge"):
        return "knowledge"
    if path.startswith(".xforge/decisions"):
        return "decision"
    if path.endswith("AGENTS.md") or path.endswith("README.md"):
        return "doc"
    return "other"


def file_sha256(path: Path) -> str:
    """Compute SHA256 hex digest."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def chunk_text(text: str, max_lines: int, overlap: int) -> list[tuple[int, int, str]]:
    """Split text into overlapping line chunks.

    Returns list of (start_line, end_line, chunk_text).
    Lines are 1-indexed.
    """
    lines = text.splitlines(keepends=True)
    chunks: list[tuple[int, int, str]] = []
    if not lines:
        return chunks

    step = max(1, max_lines - overlap)
    for i in range(0, len(lines), step):
        end = min(i + max_lines, len(lines))
        chunk = "".join(lines[i:end])
        chunks.append((i + 1, end, chunk))  # 1-indexed
        if end == len(lines):
            break
    return chunks


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-word, filter stopwords and short tokens."""
    tokens = re.findall(r"[a-z]{3,}|[\d]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def walk_source(source: str, project_root: Path, excludes: list[str]) -> list[Path]:
    """Enumerate all files under a source path (relative or absolute)."""
    src = Path(source)
    if not src.is_absolute():
        src = project_root / src

    if not src.exists():
        return []

    files: list[Path] = []
    if src.is_file():
        files.append(src)
    else:
        for path in src.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(project_root).as_posix()
            if any(ex in rel for ex in excludes):
                continue
            files.append(path)
    return files


def build_index(chunks: list[dict]) -> dict:
    """Build inverted index: term -> [{chunkId, path, line}]."""
    terms: dict[str, list[dict]] = {}
    for chunk in chunks:
        for token in set(tokenize(chunk.get("text", ""))):
            terms.setdefault(token, []).append({
                "chunkId": chunk["id"],
                "path": chunk["path"],
                "line": chunk["startLine"],
            })
    # Sort each term's postings for deterministic output
    for term in terms:
        terms[term].sort(key=lambda p: (p["path"], p["line"]))
    return {"version": "1.1.0", "chunkCount": len(chunks), "terms": terms}


def reindex(project_root: Path) -> dict:
    """Full reindex from config.json sources."""
    config_path = project_root / ".xforge/rag/config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config: {config_path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    sources = config.get("sources", [])
    excludes = config.get("excludePatterns", [])
    max_lines = config.get("chunk", {}).get("maxLines", 40)
    overlap = config.get("chunk", {}).get("overlapLines", 5)

    print(f"[reindex] Sources: {len(sources)}")
    print(f"[reindex] Excludes: {len(excludes)} patterns")
    print(f"[reindex] Chunk config: {max_lines} lines, overlap {overlap}")

    # 1. Walk all files
    all_files: list[Path] = []
    for src in sources:
        files = walk_source(src, project_root, excludes)
        print(f"[reindex]   {src}: {len(files)} files")
        all_files.extend(files)

    # 2. Compute manifest + chunks
    manifest_docs: dict[str, dict] = {}
    chunks: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()

    for fpath in sorted(set(all_files)):
        try:
            rel = fpath.relative_to(project_root).as_posix()
        except ValueError:
            rel = fpath.as_posix()

        try:
            sha = file_sha256(fpath)
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            print(f"[reindex]   skip {rel}: {e}")
            continue

        manifest_docs[rel] = {
            "path": rel,
            "sha256": sha,
            "updatedAt": now,
        }

        for start, end, chunk_text_content in chunk_text(text, max_lines, overlap):
            cid = "chunk_" + hashlib.md5(
                f"{rel}:{start}:{end}".encode("utf-8")
            ).hexdigest()
            chunks.append({
                "id": cid,
                "path": rel,
                "sourceType": detect_source_type(rel),
                "trust": "medium",
                "startLine": start,
                "endLine": end,
                "text": chunk_text_content,
            })

    # 3. Write manifest.json
    manifest = {
        "version": "1.1.0",
        "lastIndexedAt": now,
        "documentCount": len(manifest_docs),
        "chunkCount": len(chunks),
        "documents": manifest_docs,
        "indexPath": ".xforge/rag/indexes/lexical.json",
        "chunksPath": ".xforge/rag/chunks/chunks.jsonl",
        "reportPath": ".xforge/rag/reports/index-report.md",
    }
    (project_root / ".xforge/rag/manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # 4. Write chunks.jsonl
    chunks_path = project_root / ".xforge/rag/chunks/chunks.jsonl"
    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    with open(chunks_path, "w", encoding="utf-8", newline="\n") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # 5. Build + write lexical index
    index = build_index(chunks)
    idx_path = project_root / ".xforge/rag/indexes/lexical.json"
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(
        json.dumps(index, ensure_ascii=False),
        encoding="utf-8",
    )

    # 6. Write report
    report_path = project_root / ".xforge/rag/reports/index-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = f"""# RAG Index Report

- lastIndexedAt: {now}
- documents: {len(manifest_docs)}
- chunks: {len(chunks)}
- terms (unique): {len(index['terms'])}
- sourceTypes: {', '.join(sorted({c['sourceType'] for c in chunks}))}

## Source Distribution

| SourceType | Chunks |
|---|---:|
"""
    counts: dict[str, int] = {}
    for c in chunks:
        counts[c["sourceType"]] = counts.get(c["sourceType"], 0) + 1
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        report += f"| {k} | {v} |\n"

    report += "\n## Top 20 Terms\n\n"
    top = sorted(index["terms"].items(), key=lambda x: -len(x[1]))[:20]
    for term, postings in top:
        report += f"- `{term}` ({len(postings)})\n"

    report_path.write_text(report, encoding="utf-8")

    return {
        "documents": len(manifest_docs),
        "chunks": len(chunks),
        "terms": len(index["terms"]),
    }


def status(project_root: Path) -> dict:
    """Show current index status."""
    manifest_path = project_root / ".xforge/rag/manifest.json"
    if not manifest_path.exists():
        return {"stale": True, "reason": "no manifest"}

    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    last = m.get("lastIndexedAt")
    docs = m.get("documents", {})

    # Compare sha256 against filesystem
    stale = 0
    for rel, info in docs.items():
        fpath = project_root / rel
        if not fpath.exists():
            continue
        try:
            current_sha = file_sha256(fpath)
        except OSError:
            continue
        if current_sha != info.get("sha256"):
            stale += 1

    return {
        "lastIndexedAt": last,
        "documentCount": m.get("documentCount", len(docs)),
        "stale": stale > 0,
        "staleCount": stale,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="XForge RAG local indexer")
    parser.add_argument("command", choices=["reindex", "status"], help="command")
    args = parser.parse_args()

    project_root = Path.cwd()
    if not (project_root / ".xforge/rag/config.json").exists():
        print("ERROR: .xforge/rag/config.json not found. Run from project root.", file=sys.stderr)
        return 1

    if args.command == "reindex":
        result = reindex(project_root)
        print()
        print(f"[reindex] DONE: {result['documents']} docs, {result['chunks']} chunks, {result['terms']} terms")
        return 0
    elif args.command == "status":
        s = status(project_root)
        print(json.dumps(s, indent=2, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    sys.exit(main())