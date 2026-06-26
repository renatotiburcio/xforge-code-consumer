"""
cmd_status - Status de adocao + metricas.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import json
from datetime import datetime
from pathlib import Path


def cmd_status(args):
    """Mostra status de adocao + metricas avancadas (v3.0-rc1)."""
    project_root = Path.cwd()

    print(f"[XForge] Status de adocao em: {project_root}")
    print()

    checks = {
        ".kilo/ existe": (project_root / ".kilo").exists(),
        ".xforge/ existe": (project_root / ".xforge").exists(),
        "PROJECT-DNA gerado": (project_root / ".xforge" / "project-dna" / "PROJECT-DNA.md").exists(),
        "kilo.jsonc existe": (project_root / ".kilo.jsonc").exists(),
        "AGENTS.md presente": (project_root / "AGENTS.md").exists(),
        "Git inicializado": (project_root / ".git").exists(),
        "RAG indexado": (project_root / ".xforge" / "rag" / "manifest.json").exists(),
    }

    adopted = sum(1 for v in checks.values() if v)
    total = len(checks)

    for check, ok in checks.items():
        icon = "[OK]" if ok else "[ ]"
        print(f"  {icon} {check}")

    print()
    pct = (adopted / total) * 100
    print(f"Adocao: {adopted}/{total} ({pct:.0f}%)")

    metrics = compute_adoption_metrics(project_root, checks)
    if metrics:
        print()
        print("Metricas avancadas:")
        for k, v in metrics.items():
            print(f"  - {k}: {v}")

    if pct < 100:
        print()
        print("Sugestoes:")
        if not checks["PROJECT-DNA gerado"]:
            print("  - Rode: xforge recognize")
        if not checks["RAG indexado"]:
            print("  - Rode: python .kilo/automation/scripts/rag/rag_local.py index")

    if args.log:
        log_adoption(project_root, adopted, total, metrics)
        print("[XForge] Adocao registrada em .xforge/.adoption.json")

    return 0

def compute_adoption_metrics(project_root, checks):
    """Compute extra adoption metrics."""
    metrics = {}
    rag_file = project_root / ".xforge" / "rag" / "manifest.json"
    if rag_file.exists():
        try:
            data = json.loads(rag_file.read_text(encoding="utf-8"))
            metrics["RAG docs"] = data.get("docs_indexed", 0)
            metrics["RAG chunks"] = data.get("chunks_total", 0)
        except (json.JSONDecodeError, OSError):
            pass
    packs_file = project_root / ".xforge" / "packs" / "installed.json"
    if packs_file.exists():
        try:
            data = json.loads(packs_file.read_text(encoding="utf-8"))
            metrics["Packs instalados"] = len(data.get("packs", {}))
        except (json.JSONDecodeError, OSError):
            pass
    decisions_dir = project_root / ".xforge" / "decisions"
    if decisions_dir.exists():
        drs = list(decisions_dir.glob("DR-*.md"))
        metrics["Decision Records"] = len(drs)
    backups_dir = project_root / ".xforge-backups"
    if backups_dir.exists():
        backups = list(backups_dir.glob("*.tar.gz"))
        metrics["Backups"] = len(backups)
    templates_dir = project_root / ".xforge" / "project-dna"
    if templates_dir.exists():
        dna = templates_dir / "PROJECT-DNA.md"
        if dna.exists():
            content = dna.read_text(encoding="utf-8")
            metrics["Stack detectado"] = "sim" if "Stack Detectado" in content or "Stack detectado" in content else "nao"
    return metrics

def log_adoption(project_root, adopted, total, metrics):
    """Log adoption snapshot to .xforge/.adoption.json (anonymous, local-only)."""
    log_file = project_root / ".xforge" / ".adoption.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    history = {"snapshots": []}
    if log_file.exists():
        try:
            history = json.loads(log_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    history["snapshots"].append({
        "timestamp": datetime.now().isoformat(),
        "adopted": adopted,
        "total": total,
        "percent": round((adopted / total) * 100, 1),
        "metrics": metrics,
    })
    history["lastUpdated"] = datetime.now().isoformat()
    log_file.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

