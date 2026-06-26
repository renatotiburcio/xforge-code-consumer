"""
cmd_restore - Restore .xforge state de backup.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
from pathlib import Path


def cmd_restore(args):
    """Restore .xforge state de backup."""
    project_root = Path.cwd()
    backup_dir = project_root / ".xforge-backups"

    if not backup_dir.exists():
        print("[XForge] .xforge-backups/ nao existe.")
        return 1

    backups = sorted(backup_dir.glob("xforge-backup-*.tar.gz"), reverse=True)
    if not backups:
        print("[XForge] Nenhum backup encontrado.")
        return 1

    print("[XForge] Backups disponiveis:")
    for i, b in enumerate(backups[:10], 1):
        print(f"  {i}. {b.name}")

    if args.backup_index is None:
        try:
            choice = input(f"Escolha (1-{min(10, len(backups))}): ").strip()
            idx = int(choice) - 1
        except (ValueError, EOFError):
            print("[XForge] Escolha invalida.")
            return 1
    else:
        idx = args.backup_index - 1

    if idx < 0 or idx >= len(backups):
        print("[XForge] Indice invalido.")
        return 1

    backup_path = backups[idx]
    print(f"[XForge] Restaurando de: {backup_path}")

    import tarfile
    xforge_dir = project_root / ".xforge"
    if xforge_dir.exists():
        shutil.rmtree(xforge_dir)


    with tarfile.open(backup_path, "r:gz") as tar:
        try:
            tar.extractall(project_root, filter="data")
        except TypeError:
            tar.extractall(project_root)

    print("[XForge] Restore completo.")
    return 0


