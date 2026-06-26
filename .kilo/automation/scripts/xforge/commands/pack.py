"""
cmd_pack - Marketplace pack management.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import json
from pathlib import Path

from pack import install_pack, search_packs, load_registry, resolve_pack, MIN_TRUST_SCORE, update_registry, upgrade_pack


def cmd_pack(args):
    """Marketplace pack management: list, search, info, install, remove."""
    pass
    xforge_dir = Path.cwd() / ".xforge"
    installed_file = xforge_dir / "packs" / "installed.json"

    if args.pack_cmd == "list":
        if not installed_file.exists():
            print("[XForge] Nenhum pack instalado (rode xforge init primeiro).")
            return 0
        try:
            data = json.loads(installed_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("[XForge] installed.json invalido.")
            return 1

        packs = data.get("packs", {})
        if not packs:
            print("[XForge] Nenhum pack instalado.")
            return 0

        print(f"[XForge] {len(packs)} packs instalados:")
        for pid, p in packs.items():
            ts = p.get("trustScore", "?")
            ver = p.get("version", "?")
            print(f"  - {pid:<25} v{ver} trust:{ts}")
        return 0

    if args.pack_cmd == "info":
        if not installed_file.exists():
            print(f"[XForge] Pack {args.pack_id} nao instalado.")
            return 1
        data = json.loads(installed_file.read_text(encoding="utf-8"))
        p = data.get("packs", {}).get(args.pack_id)
        if not p:
            print(f"[XForge] Pack {args.pack_id} nao instalado.")
            return 1
        print(json.dumps(p, indent=2, ensure_ascii=False))
        return 0

    if args.pack_cmd == "remove":
        if not installed_file.exists():
            print(f"[XForge] Nada para remover.")
            return 1
        data = json.loads(installed_file.read_text(encoding="utf-8"))
        if args.pack_id not in data.get("packs", {}):
            print(f"[XForge] Pack {args.pack_id} nao instalado.")
            return 1

        pack = data["packs"][args.pack_id]
        removed_paths = []
        for f in pack.get("files", []):
            path = xforge_dir / f
            if path.exists():
                removed_paths.append(path)
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
        for rp in sorted(removed_paths, key=lambda p: -len(p.parts)):
            parent = rp.parent
            while parent != xforge_dir and parent.exists():
                try:
                    parent.rmdir()
                    parent = parent.parent
                except OSError:
                    break
        pack_target = xforge_dir / "packs" / args.pack_id
        if pack_target.exists():
            shutil.rmtree(pack_target)
        del data["packs"][args.pack_id]
        data["lastUpdated"] = datetime.now().isoformat()
        installed_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[XForge] Pack {args.pack_id} removido.")
        return 0

    if args.pack_cmd == "search":
        results = search_packs(query=args.pack_id, min_trust=0)
        if not results:
            print("[XForge] Nenhum pack encontrado.")
            return 0
        print(f"[XForge] {len(results)} packs encontrados:")
        for p in results:
            tags = ",".join(p.get("tags", [])[:3])
            pid = p.get("id", "?")
            ver = p.get("version", "?")
            trust = p.get("trustScore", "?")
            desc = p.get("description", "")
            print(f"  - {pid:<28} v{ver} trust:{trust} ({tags})")
            print(f"      {desc}")
        return 0

    if args.pack_cmd == "install":
        if not args.pack_id:
            print("[XForge] Uso: xforge pack install PACK_ID [--force]")
            print("[XForge] Para listar: xforge pack search")
            return 1
        manifest, err = install_pack(args.pack_id, Path.cwd(), force=args.force)
        if err:
            print(f"[XForge] ERRO: {err}")
            return 1
        print(f"[XForge] Pack instalado: {manifest.get('id')} v{manifest.get('version')}")
        print(f"[XForge] Arquivos: {len(manifest.get('files', []))}")
        return 0

    if args.pack_cmd == "update":
        url = args.source or "https://raw.githubusercontent.com/renatotiburcio/xforge-packs/main/registry.json"
        print(f"[XForge] Atualizando registry de: {url}")
        new_reg, err = update_registry(registry_url=url)
        if err:
            print(f"[XForge] AVISO: {err}")
            print("[XForge] Usando registry bundled (pode estar desatualizado).")
        else:
            n_packs = len(new_reg.get("packs", []))
            print(f"[XForge] Registry atualizado: {n_packs} packs disponiveis.")
        return 0

    if args.pack_cmd == "upgrade":
        if not args.pack_id:
            print("[XForge] Uso: xforge pack upgrade PACK_ID [--force]")
            return 1
        manifest, err = upgrade_pack(args.pack_id, Path.cwd(), force=args.force)
        if err:
            print(f"[XForge] ERRO: {err}")
            return 1
        print(f"[XForge] Pack atualizado: {manifest.get('id')} v{manifest.get('version')}")
        return 0

    return 1




