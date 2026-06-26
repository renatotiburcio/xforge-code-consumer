"""
cmd_upgrade + cmd_upgrade_remote - Atualizar .kilo + .xforge.

Suporta upgrade local (legacy) e remoto via GitHub Releases API (v3.4+).
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import shutil
from pathlib import Path


def cmd_upgrade_remote(args, target_version=None):
    """Upgrade remoto via GitHub Releases API (v3.4+)."""
    import urllib.request
    import urllib.error
    import zipfile
    import tempfile
    import json as _json
    import tarfile
    project_root = Path.cwd()
    api_base = "https://api.github.com/repos/renatotiburcio/xforge-enterprise-development-os"
    local_version = __version__

    if args.check:
        print(f"[XForge] Versao local: v{local_version}")
        try:
            with urllib.request.urlopen(f"{api_base}/releases/latest", timeout=10) as resp:
                release = _json.loads(resp.read())
            remote = release.get("tag_name", "?")
            print(f"[XForge] Versao remota: {remote}")
            if remote.lstrip("v") == local_version:
                print("[XForge] Ja esta na versao mais recente.")
            else:
                print("[XForge] Update disponivel.")
                print(f"[XForge] URL: {release.get('html_url', '')}")
        except Exception as e:
            print(f"[XForge] ERRO: {e}")
            return 1
        return 0

    target_version = target_version or "latest"
    print("[XForge] ============================================")
    print(f"[XForge]  XForge Upgrade Wizard (v{local_version})")
    print("[XForge] ============================================")
    print()
    if target_version == "latest":
        url = f"{api_base}/releases/latest"
    else:
        url = f"{api_base}/releases/tags/{target_version}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            release = _json.loads(resp.read())
    except Exception as e:
        print(f"[XForge] ERRO ao consultar GitHub: {e}")
        return 1

    remote_tag = release.get("tag_name", "unknown")
    remote_version = remote_tag.lstrip("v")
    tarball_url = release.get("tarball_url")
    print(f"[XForge] Versao local:  v{local_version}")
    print(f"[XForge] Versao remota: {remote_tag}")
    print()
    if args.changelog:
        print("[XForge] CHANGELOG (500 chars):")
        print((release.get("body") or "")[:500])
        return 0
    if remote_version == local_version and not args.force:
        print("[XForge] Ja esta na versao mais recente. Use --force para reinstalar.")
        return 0
    if args.dry_run:
        print("[XForge] DRY-RUN: nenhuma alteracao sera aplicada.")
        return 0
    if not args.yes:
        try:
            resp = input(f"[XForge] Atualizar v{local_version} -> {remote_tag}? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            resp = "n"
        if resp != "y":
            print("[XForge] Cancelado.")
            return 1

    backup_dir = project_root / ".xforge-backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"xforge-{local_version}-pre-{remote_version}-{timestamp}.tar.gz"
    target_xforge = project_root / ".xforge"
    target_kilo = project_root / ".kilo"
    with tarfile.open(backup_path, "w:gz") as tar:
        for d in (target_xforge, target_kilo):
            if d.exists():
                tar.add(d, arcname=d.name)
    print(f"[XForge] Backup: {backup_path}")

    if not tarball_url:
        print("[XForge] Release sem tarball.")
        return 1
    print(f"[XForge] Baixando {remote_tag}...")
    with tempfile.TemporaryDirectory() as tmp:
        archive_path = Path(tmp) / "xforge.tar.gz"
        try:
            urllib.request.urlretrieve(tarball_url, archive_path)
        except Exception as e:
            print(f"[XForge] ERRO download: {e}")
            return 1
        size_kb = archive_path.stat().st_size / 1024
        print(f"[XForge] Download: {size_kb:.1f} KB")
        extract_dir = Path(tmp) / "extracted"
        extract_dir.mkdir()
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(extract_dir, filter="data")
        except Exception as e:
            print(f"[XForge] ERRO extracao: {e}")
            return 1
        candidates = list(extract_dir.iterdir())
        if not candidates:
            print("[XForge] Archive vazio.")
            return 1
        src_root = candidates[0]
        src_kilo = src_root / ".kilo"
        src_xforge = src_root / ".xforge"
        if not src_kilo.exists():
            print("[XForge] .kilo nao encontrado.")
            return 1
        protected = {".xforge/decisions", ".xforge/memory", ".xforge/rag"}
        added, modified, skipped = 0, 0, 0
        for src_dir, tgt_dir in [(src_kilo, target_kilo), (src_xforge, target_xforge)]:
            if not tgt_dir.exists():
                shutil.copytree(src_dir, tgt_dir)
                added += sum(1 for _ in tgt_dir.rglob("*") if _.is_file())
                continue
            for src_file in src_dir.rglob("*"):
                if src_file.is_dir():
                    continue
                rel = src_file.relative_to(src_dir)
                tgt = tgt_dir / rel
                tgt_str = str(tgt.relative_to(project_root)).replace("\\\\", "/")
                is_protected = any(tgt_str.startswith(p) for p in protected)
                if is_protected:
                    skipped += 1
                    continue
                if not tgt.exists():
                    tgt.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, tgt)
                    added += 1
                elif args.force:
                    shutil.copy2(src_file, tgt)
                    modified += 1
                else:
                    try:
                        if hashlib.md5(src_file.read_bytes()).hexdigest() != hashlib.md5(tgt.read_bytes()).hexdigest():
                            skipped += 1
                    except OSError:
                        skipped += 1
    print()
    print("[XForge] Upgrade aplicado:")
    print(f"  Adicionados: {added}")
    print(f"  Modificados: {modified}")
    print(f"  Preservados: {skipped} (decisions/memory/rag)")
    print()
    print(f"[XForge] Bump __version__ para {remote_version} em xforge/cli.py")
    return 0


def cmd_upgrade(args):
    """Atualiza .kilo + .xforge para ultima versao (v3.0-beta).

    Estrategia:
      1. Backup automatico antes de tudo (.xforge-backups/xforge-backup-pre-upgrade-*.tar.gz)
      2. Copia arquivos NOVOS e MODIFICADOS do source
      3. NUNCA deleta arquivos do usuario (.xforge/decisions, .xforge/memory, .xforge/rag)
      4. Reporta diff (added/modified/skipped)
    """
    project_root = Path.cwd()
    kilo_source, xforge_source = find_xforge_source()

    target_kilo = project_root / ".kilo"
    target_xforge = project_root / ".xforge"

    if not target_kilo.exists() or not target_xforge.exists():
        print("[XForge] .kilo/ ou .xforge/ nao existe. Rode: xforge init")
        return 1

    print(f"[XForge] Source: {kilo_source}")
    print(f"[XForge] Target: {project_root}")
    print()

    print("[XForge] Criando backup pre-upgrade...")
    backup_dir = project_root / ".xforge-backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"xforge-backup-pre-upgrade-{timestamp}.tar.gz"
    import tarfile
    with tarfile.open(backup_path, "w:gz") as tar:
        if target_xforge.exists():
            tar.add(target_xforge, arcname="xforge")
    print(f"[XForge] Backup: {backup_path}")
    print()

    protected = {".xforge/decisions", ".xforge/memory", ".xforge/rag"}

    added = []
    modified = []
    skipped = []

    for source_dir, target_dir, label in [(kilo_source, target_kilo, ".kilo"), (xforge_source, target_xforge, ".xforge")]:
        print(f"[XForge] Atualizando {label}/...")
        for src_file in source_dir.rglob("*"):
            if src_file.is_dir():
                continue
            rel = src_file.relative_to(source_dir)
            tgt = target_dir / rel
            tgt_str = str(tgt.relative_to(project_root)).replace("\\", "/")

            is_protected = any(tgt_str.startswith(p) for p in protected)

            if not tgt.exists():
                tgt.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, tgt)
                added.append(tgt_str)
            elif is_protected:
                skipped.append(tgt_str + " (protegido)")
            elif args.force:
                shutil.copy2(src_file, tgt)
                modified.append(tgt_str)
            else:
                try:
                    src_hash = hashlib.md5(src_file.read_bytes()).hexdigest()
                    tgt_hash = hashlib.md5(tgt.read_bytes()).hexdigest()
                    if src_hash != tgt_hash:
                        skipped.append(tgt_str + " (modificado, use --force)")
                except OSError:
                    skipped.append(tgt_str + " (erro leitura)")

    print()
    print(f"[XForge] Upgrade completo!")
    print(f"  Adicionados: {len(added)}")
    print(f"  Modificados: {len(modified)}")
    print(f"  Preservados: {len(skipped)} (decisions/memory/rag)")
    print()
    if modified and not args.force:
        print("Nota: Use --force para sobrescrever arquivos modificados tambem.")
    print()
    print("Proximos passos:")
    print("  1. xforge doctor   # Validar setup")
    print("  2. xforge status   # Ver adocao")
    print(f"  3. Backup criado: {backup_path.name}")

    return 0
