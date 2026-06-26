"""
cmd_backup - Backup .xforge state.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
from datetime import datetime
from pathlib import Path


def cmd_backup(args):
    """Backup .xforge state."""
    project_root = Path.cwd()
    xforge_dir = project_root / ".xforge"

    if not xforge_dir.exists():
        print("[XForge] .xforge/ nao existe. Nada para backup.")
        return 1

    backup_dir = project_root / ".xforge-backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"xforge-backup-{timestamp}.tar.gz"

    print(f"[XForge] Criando backup em: {backup_path}")
    import tarfile
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(xforge_dir, arcname="xforge")

    print(f"[XForge] Backup criado: {backup_path}")
    return 0

