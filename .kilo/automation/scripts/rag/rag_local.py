import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Semantic search support (optional)
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


ROOT = Path.cwd()
RAG_ROOT = ROOT / ".xforge" / "rag"
CONFIG_PATH = RAG_ROOT / "config.json"
MANIFEST_PATH = RAG_ROOT / "manifest.json"
CHUNKS_PATH = RAG_ROOT / "chunks" / "chunks.jsonl"
LEXICAL_PATH = RAG_ROOT / "indexes" / "lexical.json"
REPORT_PATH = RAG_ROOT / "reports" / "index-report.md"
SECRET_REPORT_PATH = RAG_ROOT / "reports" / "secret-scan-report.md"

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonc", ".yml", ".yaml", ".ps1", ".py",
    ".cs", ".csproj", ".sln", ".html", ".css", ".js", ".ts", ".csv", ""
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\s;]{8,}"),
    re.compile(r"(?i)(?<![A-Za-z])token(?![A-Za-z])\s*[:=]\s*['\"]?[^'\"\s;]{12,}"),
    re.compile(r"(?i)Password\s*=\s*[^;\s]{4,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)ghp_[0-9A-Za-z]{36,}"),
    re.compile(r"(?i)gho_[0-9A-Za-z]{36,}"),
    re.compile(r"(?i)ghu_[0-9A-Za-z]{36,}"),
    re.compile(r"(?i)ghs_[0-9A-Za-z]{36,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
    re.compile(r"(?i)(Server|Host)\s*=.*[Pp]assword\s*="),
    re.compile(r"(?i)Authorization:\s*Basic\s+[A-Za-z0-9+/=]+"),
    re.compile(r"(?i)Authorization:\s*Bearer\s+[A-Za-z0-9._-]+"),
    re.compile(r"(?i)sk-[A-Za-z0-9]{20,}"),
]

SOURCE_TYPES = [
    (".kilo/commands/", "commands", "high"),
    (".kilo/skills/", "skills", "high"),
    (".kilo/agents/", "agents", "high"),
    (".kilo/rules/", "rules", "high"),
    (".xforge/memory/", "memory", "high"),
    (".xforge/project-dna/", "project-dna", "high"),
    (".xforge/decisions/", "decisions", "high"),
    (".xforge/knowledge/", "knowledge", "medium"),
    (".xforge/engineer/official-knowledge-seeds/", "official", "high"),
    (".xforge/engineer/knowledge-packs/", "knowledge", "medium"),
    (".xforge/engineer/", "engineer-docs", "medium"),
]


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "chunk": {"maxLines": 40, "overlapLines": 5},
        "sources": [".xforge", ".kilo", "AGENTS.md", "README.md", ".xforge/docs/INSTALL.md"],
        "excludePatterns": [],
    }


def tokenize(text):
    return [t.lower() for t in re.findall(r"[\wÀ-ÿ#.+/-]{2,}", text)]


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def cosine_similarity(vec1, vec2):
    if not HAS_NUMPY:
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def should_exclude(path: Path, patterns):
    text = path.as_posix()
    return any(pattern and pattern in text for pattern in patterns)


def source_type_for(rel):
    for prefix, source_type, trust in SOURCE_TYPES:
        if rel.startswith(prefix):
            return source_type, trust
    if rel in {"AGENTS.md", "README.md", ".xforge/docs/INSTALL.md"}:
        return "root-docs", "high"
    return "unknown", "low"


def trust_weight(trust):
    return {"high": 1.25, "medium": 1.0, "low": 0.75}.get(trust, 1.0)


def source_weight(source_type):
    return {
        "commands": 1.25,
        "rules": 1.2,
        "agents": 1.15,
        "skills": 1.1,
        "project-dna": 1.25,
        "memory": 1.2,
        "official": 1.2,
        "knowledge": 1.0,
        "engineer-docs": 0.95,
        "unknown": 0.75,
    }.get(source_type, 1.0)


def has_secret(text):
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def iter_source_files(config):
    patterns = config.get("excludePatterns", [])
    for source in config.get("sources", []):
        path = ROOT / source
        if not path.exists():
            continue
        candidates = [path] if path.is_file() else path.rglob("*")
        for item in candidates:
            if not item.is_file():
                continue
            if should_exclude(item, patterns):
                continue
            if item.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            yield item


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def chunk_file(path: Path, max_lines: int, overlap: int):
    text = read_text(path)
    lines = text.splitlines()
    if not lines:
        return []
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel = path.name
    source_type, trust = source_type_for(rel)
    chunks = []
    step = max(1, max_lines - overlap)
    for start in range(0, len(lines), step):
        end = min(len(lines), start + max_lines)
        chunk_text = "\n".join(lines[start:end]).strip()
        if len(chunk_text) < 20:
            continue
        if has_secret(chunk_text):
            continue
        chunk_id = sha256_text(f"{rel}:{start + 1}:{end}:{chunk_text}")[:24]
        chunks.append({
            "id": f"chunk_{chunk_id}",
            "path": rel,
            "sourceType": source_type,
            "trust": trust,
            "startLine": start + 1,
            "endLine": end,
            "text": chunk_text,
            "sha256": sha256_text(chunk_text),
            "tokensApprox": len(tokenize(chunk_text)),
        })
    return chunks


def build_index(chunks):
    doc_freq = defaultdict(int)
    chunk_terms = {}
    for chunk in chunks:
        terms = Counter(tokenize(chunk["text"]))
        chunk_terms[chunk["id"]] = terms
        for term in terms:
            doc_freq[term] += 1

    total = len(chunks)
    index = {
        "version": "1.1.0",
        "chunkCount": total,
        "terms": {},
        "chunks": {
            chunk["id"]: {
                "path": chunk["path"],
                "sourceType": chunk["sourceType"],
                "trust": chunk["trust"],
                "startLine": chunk["startLine"],
                "endLine": chunk["endLine"],
                "tokensApprox": chunk["tokensApprox"],
            }
            for chunk in chunks
        },
    }

    for chunk_id, terms in chunk_terms.items():
        meta = index["chunks"][chunk_id]
        norm = 1 / math.sqrt(max(meta["tokensApprox"], 1))
        boost = trust_weight(meta["trust"]) * source_weight(meta["sourceType"])
        for term, tf in terms.items():
            idf = math.log((1 + total) / (1 + doc_freq[term])) + 1
            score = tf * idf * norm * boost
            index["terms"].setdefault(term, []).append([chunk_id, round(score, 8)])

    return index


def collect_documents(config):
    docs = {}
    for path in iter_source_files(config):
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = path.name
        docs[rel] = {
            "path": rel,
            "sha256": sha256_file(path),
            "updatedAt": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        }
    return docs


def index_command():
    config = load_config()
    max_lines = int(config.get("chunk", {}).get("maxLines", 40))
    overlap = int(config.get("chunk", {}).get("overlapLines", 5))
    chunks = []
    documents = collect_documents(config)
    for rel in documents:
        chunks.extend(chunk_file(ROOT / rel, max_lines, overlap))

    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEXICAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CHUNKS_PATH.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    LEXICAL_PATH.write_text(json.dumps(build_index(chunks), ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = {
        "version": "1.1.0",
        "lastIndexedAt": now_utc(),
        "documentCount": len(documents),
        "chunkCount": len(chunks),
        "documents": documents,
        "indexPath": ".xforge/rag/indexes/lexical.json",
        "chunksPath": ".xforge/rag/chunks/chunks.jsonl",
        "reportPath": ".xforge/rag/reports/index-report.md",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    by_type = Counter(chunk["sourceType"] for chunk in chunks)
    report = ["# RAG Index Report", "", f"Indexed at: {manifest['lastIndexedAt']}",
              f"Documents: {manifest['documentCount']}", f"Chunks: {manifest['chunkCount']}", "", "## Chunks By Source Type"]
    report.extend(f"- {k}: {v}" for k, v in sorted(by_type.items()))
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "documents"}, ensure_ascii=False, indent=2))


def load_chunks():
    chunks = {}
    if not CHUNKS_PATH.exists():
        return chunks
    for line in CHUNKS_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            chunk = json.loads(line)
            chunks[chunk["id"]] = chunk
    return chunks


def semantic_search(query, chunks, top_n=5):
    if not HAS_NUMPY:
        return []
    query_tokens = tokenize(query)
    if not query_tokens:
        return []
    all_tokens = list(set(query_tokens))
    for chunk in chunks.values():
        all_tokens.extend(t for t in tokenize(chunk["text"]) if t not in all_tokens)
    qvec = [query_tokens.count(t) for t in all_tokens]
    results = []
    for cid, chunk in chunks.items():
        ctokens = tokenize(chunk["text"])
        cvec = [ctokens.count(t) for t in all_tokens]
        sim = cosine_similarity(qvec, cvec)
        if sim > 0:
            results.append((cid, sim))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


def query_command(query, top, source_type=None, semantic=False):
    if not LEXICAL_PATH.exists() or not CHUNKS_PATH.exists():
        raise SystemExit("RAG index not found. Run index-local.ps1 first.")
    index = json.loads(LEXICAL_PATH.read_text(encoding="utf-8"))
    chunks = load_chunks()
    lexical_scores = defaultdict(float)
    for term in tokenize(query):
        for chunk_id, score in index.get("terms", {}).get(term, []):
            lexical_scores[chunk_id] += score

    semantic_scores = {}
    if semantic:
        sem_results = semantic_search(query, chunks, top)
        for cid, s in sem_results:
            semantic_scores[cid] = s

    def combined(chunk_id):
        lex = lexical_scores.get(chunk_id, 0.0)
        sem = semantic_scores.get(chunk_id, 0.0)
        if semantic:
            return 0.6 * lex + 0.4 * sem
        return lex

    all_ids = set(lexical_scores.keys()) | set(semantic_scores.keys())
    results = []
    for chunk_id in sorted(all_ids, key=lambda cid: combined(cid), reverse=True):
        chunk = chunks.get(chunk_id)
        if not chunk:
            continue
        if source_type and chunk.get("sourceType") != source_type:
            continue
        excerpt = re.sub(r"\s+", " ", chunk["text"]).strip()[:500]
        lex_score = round(lexical_scores.get(chunk_id, 0.0), 6)
        sem_score = round(semantic_scores.get(chunk_id, 0.0), 6)
        result = {
            "chunkId": chunk_id,
            "score": round(combined(chunk_id), 6),
            "lexicalScore": lex_score,
            "semanticScore": sem_score,
            "trust": chunk.get("trust", "unknown"),
            "sourceType": chunk.get("sourceType", "unknown"),
            "path": chunk["path"],
            "startLine": chunk["startLine"],
            "endLine": chunk["endLine"],
            "excerpt": excerpt,
        }
        results.append(result)
        if len(results) >= top:
            break
    mode = "local-hybrid" if semantic else "local-lexical"
    print(json.dumps({"query": query, "sourceType": source_type, "mode": mode, "results": results}, ensure_ascii=False, indent=2))


def status_command():
    config = load_config()
    current = collect_documents(config)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    indexed = manifest.get("documents", {})
    changed = [p for p, d in current.items() if indexed.get(p, {}).get("sha256") != d["sha256"]]
    removed = [p for p in indexed if p not in current]
    added = [p for p in current if p not in indexed]
    stale = bool(changed or removed or added or not manifest)
    output = {
        "stale": stale,
        "lastIndexedAt": manifest.get("lastIndexedAt"),
        "currentDocumentCount": len(current),
        "indexedDocumentCount": len(indexed),
        "added": added[:50],
        "changed": changed[:50],
        "removed": removed[:50],
        "addedCount": len(added),
        "changedCount": len(changed),
        "removedCount": len(removed),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if stale else 0


def secret_scan_command():
    config = load_config()
    findings = []
    for path in iter_source_files(config):
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = path.name
        text = read_text(path)
        for i, line in enumerate(text.splitlines(), 1):
            if has_secret(line):
                findings.append({"path": rel, "line": i, "kind": "potential-secret"})
    SECRET_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# RAG Secret Scan Report", "", f"Findings: {len(findings)}"]
    for f in findings[:200]:
        lines.append(f"- {f['path']}:{f['line']} {f['kind']}")
    SECRET_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"findings": findings, "findingCount": len(findings), "reportPath": ".xforge/rag/reports/secret-scan-report.md"}, ensure_ascii=False, indent=2))
    return 1 if findings else 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("index")
    sub.add_parser("status")
    sub.add_parser("secret-scan")
    q = sub.add_parser("query")
    q.add_argument("--query", required=True)
    q.add_argument("--top", type=int, default=5)
    q.add_argument("--source-type", default=None)
    q.add_argument("--semantic", action="store_true", default=False)
    args = parser.parse_args()
    if args.command == "index":
        index_command()
    elif args.command == "query":
        query_command(args.query, args.top, args.source_type, args.semantic)
    elif args.command == "status":
        raise SystemExit(status_command())
    elif args.command == "secret-scan":
        raise SystemExit(secret_scan_command())


if __name__ == "__main__":
    main()
