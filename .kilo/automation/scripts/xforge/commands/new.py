"""
cmd_new - Criar novo projeto com template.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import shutil
import json
from pathlib import Path

from .common import XFORGE_PKG_DIR


def cmd_new(args):
    """Cria novo projeto a partir de template."""
    tpl_dir = XFORGE_PKG_DIR / "templates"

    if not tpl_dir.exists():
        print("[XForge] Diretorio de templates nao encontrado.")
        return 1

    if args.stack in ("list", "--list", "-l"):
        catalog = tpl_dir / "CATALOG.json"
        if catalog.exists():
            import json
            data = json.loads(catalog.read_text(encoding="utf-8"))
            print("[XForge] Templates disponiveis (v3.0-beta):")
            for slug in data.get("templates", []):
                meta_file = tpl_dir / slug / "template.json"
                if meta_file.exists():
                    meta = json.loads(meta_file.read_text(encoding="utf-8"))
                    print(f"  - {slug:<20} {meta.get('description', '')}")
                else:
                    print(f"  - {slug}")
        else:
            for d in sorted(tpl_dir.iterdir()):
                if d.is_dir():
                    print(f"  - {d.name}")
        return 0

    project_name = args.name
    if not project_name:
        project_name = f"my-{args.stack}"
        print(f"[XForge] Nome nao informado, usando: {project_name}")

    template_path = tpl_dir / args.stack
    if not template_path.exists():
        print(f"[XForge] Template '{args.stack}' nao encontrado.")
        print(f"[XForge] Rode: xforge new list")
        return 1

    target = Path.cwd() / project_name
    if target.exists() and not args.force:
        print(f"[XForge] ERRO: {target} ja existe. Use --force.")
        return 1

    print(f"[XForge] Criando projeto '{project_name}' de template '{args.stack}'...")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(template_path, target)

    print(f"[XForge] Projeto criado em: {target}")
    print()

    import json
    meta_file = template_path / "template.json"
    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        skills = meta.get("skills", [])
        if skills:
            print("Skills recomendadas para este projeto:")
            for s in skills:
                print(f"  - {s}")
            print()
            print("Para ativar, adicione em .kilo/config.local.json ou use-as via GCF.")

    print()
    print("Proximos passos:")
    print(f"  cd {project_name}")
    print(f"  xforge init           # Bootstrap .kilo + .xforge")
    print(f"  xforge recognize      # Detectar stack")
    print(f"  xforge status         # Ver adocao")
    return 0



