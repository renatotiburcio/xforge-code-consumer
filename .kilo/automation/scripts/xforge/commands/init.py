"""
cmd_init - Bootstrap .kilo + .xforge em projeto.

Suporta modo --interactive (wizard).
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import argparse
import shutil
import json
from datetime import datetime
from pathlib import Path

from recognize import recognize
from pack import search_packs, install_pack

from .common import find_xforge_source


def _write_kilo_jsonc(project_root, name=None):
    """Emite kilo.jsonc compativel com Kilo Code CLI 1.0 schema."""
    import json
    target = project_root / "kilo.jsonc"
    if target.exists():
        return False
    description = "XForge project initialized via xforge CLI v3.3.0"
    if name:
        description = f"Project {name} - initialized via xforge CLI v3.3.0 (Kilo Code CLI 1.0 schema)"
    payload = {
        "$schema": "https://app.kilo.ai/config.json",
        "model": "anthropic/claude-sonnet-4-20250514",
        "provider": {
            "openrouter": {"options": {"apiKey": "{env:OPENROUTER_API_KEY}"}},
            "anthropic": {"options": {"apiKey": "{env:ANTHROPIC_API_KEY}"}},
            "ollama": {
                "options": {"baseURL": "http://localhost:11434/v1"},
                "models": {
                    "qwen2.5:7b": {},
                    "qwen2.5:14b": {},
                    "qwen2.5:72b": {}
                }
            }
        },
        "permission": {
            "*": "ask",
            "bash": "allow",
            "edit": {"*": "allow", ".xforge/decisions/**": "deny", ".kilo/rules/**": "deny"},
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "webfetch": "allow",
            "task": "allow"
        },
        "instructions": ["AGENTS.md", ".kilo/rules/*.md"],
        "agent": {
            "code": {"description": "Modo padrao de desenvolvimento"},
            "plan": {"description": "Planejamento e arquitetura"},
            "ask": {"description": "Perguntas rapidas"},
            "debug": {"description": "Debug e troubleshooting"},
            "review": {"description": "Code review"},
            "explore": {"description": "Exploracao de codigo"},
            "general": {"description": "Tarefas gerais"}
        },
        "skills": {"paths": [".kilo/skills"]},
        "mcp": {
            "xforge": {
                "type": "local",
                "command": ["node", ".xforge/mcp/server.js"],
                "enabled": True
            }
        },
        "experimental": {"openTelemetry": False}
    }
    if name:
        payload["name"] = name
        payload["description"] = description
        payload["createdAt"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return True


def _write_index_html(project_root):
    """Emite docs/index.html (landing minimo, link para SUMMARY.md)."""
    target = project_root / "docs" / "index.html"
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    html = (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>XForge Enterprise Development OS</title></head>'
        '<body><main><h1>XForge Enterprise Development OS</h1>'
        '<p>See <a href="SUMMARY.md">docs/SUMMARY.md</a> for the full manual.</p>'
        '<p>Kilo Code CLI 1.0 compatible. Schema: https://app.kilo.ai/config.json</p>'
        '</main></body></html>'
    )
    target.write_text(html, encoding="utf-8")
    return True


def cmd_init(args):
    """Bootstrap .kilo + .xforge em projeto. Suporta modo --interactive."""
    if getattr(args, "interactive", False):
        return cmd_init_interactive(args)

    project_root = Path.cwd()
    kilo_source, xforge_source = find_xforge_source()

    print(f"[XForge] Inicializando em: {project_root}")

    target_kilo = project_root / ".kilo"
    target_xforge = project_root / ".xforge"

    if target_kilo.exists() and not args.force:
        print("[XForge] ERRO: .kilo/ ja existe. Use --force para sobrescrever.")
        return 1

    if target_xforge.exists() and not args.force:
        print("[XForge] ERRO: .xforge/ ja existe. Use --force para sobrescrever.")
        return 1

    print(f"[XForge] Copiando .kilo/ de {kilo_source}...")
    if target_kilo.exists():
        shutil.rmtree(target_kilo)
    shutil.copytree(kilo_source, target_kilo)

    print(f"[XForge] Copiando .xforge/ de {xforge_source}...")
    kilo_created = _write_kilo_jsonc(project_root, name=getattr(args, "name", None))
    index_created = _write_index_html(project_root)
    if kilo_created:
        print("[XForge] kilo.jsonc criado (Kilo Code CLI 1.0 schema)")
    if index_created:
        print("[XForge] docs/index.html criado (landing)")
    if target_xforge.exists():
        shutil.rmtree(target_xforge)
    shutil.copytree(xforge_source, target_xforge)

    # Limpar state runtime
    runtime_paths = [
        target_xforge / "engine" / "daemon.pid",
        target_xforge / "engine" / "daemon-state.json",
        target_xforge / "rag" / "manifest.json",
        target_xforge / "rag" / "chunks",
        target_xforge / "rag" / "indexes",
    ]
    for p in runtime_paths:
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    has_existing = any((project_root / f).exists() for f in ["package.json", "*.csproj", "pyproject.toml", "go.mod", "Cargo.toml"])
    if args.analyze or has_existing:
        print("[XForge] Projeto detectado. Rodando reconhecimento...")
        result = recognize(project_root)
        print(f"[XForge] Stack: {', '.join(result['stack'])}")
        print(f"[XForge] Gaps: {len(result['gaps'])}")
        print(f"[XForge] PROJECT-DNA: {result['dna_file']}")

    print()
    print("[XForge] Inicializacao completa!")
    print()
    print("Proximos passos:")
    print("  1. xforge doctor    # Validar setup")
    print("  2. xforge recognize # Re-analisar projeto")
    print("  3. xforge status    # Ver status de adocao")
    return 0


def _write_kilo_jsonc(project_root, name=None):
    """Emite kilo.jsonc compativel com Kilo Code CLI 1.0 schema."""
    import json
    target = project_root / "kilo.jsonc"
    if target.exists():
        return False
    description = "XForge project initialized via xforge CLI v3.3.0"
    if name:
        description = f"Project {name} - initialized via xforge CLI v3.3.0 (Kilo Code CLI 1.0 schema)"
    payload = {
        "$schema": "https://app.kilo.ai/config.json",
        "model": "anthropic/claude-sonnet-4-20250514",
        "provider": {
            "openrouter": {"options": {"apiKey": "{env:OPENROUTER_API_KEY}"}},
            "anthropic": {"options": {"apiKey": "{env:ANTHROPIC_API_KEY}"}},
            "ollama": {
                "options": {"baseURL": "http://localhost:11434/v1"},
                "models": {
                    "qwen2.5:7b": {},
                    "qwen2.5:14b": {},
                    "qwen2.5:72b": {}
                }
            }
        },
        "permission": {
            "*": "ask",
            "bash": "allow",
            "edit": {"*": "allow", ".xforge/decisions/**": "deny", ".kilo/rules/**": "deny"},
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "webfetch": "allow",
            "task": "allow"
        },
        "instructions": ["AGENTS.md", ".kilo/rules/*.md"],
        "agent": {
            "code": {"description": "Modo padrao de desenvolvimento"},
            "plan": {"description": "Planejamento e arquitetura"},
            "ask": {"description": "Perguntas rapidas"},
            "debug": {"description": "Debug e troubleshooting"},
            "review": {"description": "Code review"},
            "explore": {"description": "Exploracao de codigo"},
            "general": {"description": "Tarefas gerais"}
        },
        "skills": {"paths": [".kilo/skills"]},
        "mcp": {
            "xforge": {
                "type": "local",
                "command": ["node", ".xforge/mcp/server.js"],
                "enabled": True
            }
        },
        "experimental": {"openTelemetry": False}
    }
    if name:
        payload["name"] = name
        payload["description"] = description
        payload["createdAt"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return True


def _write_index_html(project_root):
    """Emite docs/index.html (landing minimo, link para SUMMARY.md)."""
    target = project_root / "docs" / "index.html"
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    html = (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>XForge Enterprise Development OS</title></head>'
        '<body><main><h1>XForge Enterprise Development OS</h1>'
        '<p>See <a href="SUMMARY.md">docs/SUMMARY.md</a> for the full manual.</p>'
        '<p>Kilo Code CLI 1.0 compatible. Schema: https://app.kilo.ai/config.json</p>'
        '</main></body></html>'
    )
    target.write_text(html, encoding="utf-8")
    return True
    print("  3. xforge status    # Ver status de adocao")
    print()
    print("Documentacao:")
    print("  - Manual: docs/SUMMARY.md")
    print("  - GCF: .kilo/rules/02-genius-council-framework.md")
    return 0


def cmd_init_interactive(args):
    """Interactive wizard for `xforge init --interactive`.

    Asks user (via input()):
      1. Project name (for kilo.jsonc metadata)
      2. Confirm .kilo/.xforge init
      3. Which packs to install (multi-select)
      4. Whether to run recognize after init
    """
    print("[XForge] ============================================")
    print("[XForge]  Interactive Init Wizard (v3.1)")
    print("[XForge] ============================================")
    print()

    project_root = Path.cwd()
    target_kilo = project_root / ".kilo"
    target_xforge = project_root / ".xforge"

    if target_kilo.exists() or target_xforge.exists():
        if not args.force:
            print("[XForge] ERRO: .kilo/ ou .xforge/ ja existe. Use --force para sobrescrever.")
            return 1

    # Step 1: project name
    default_name = project_root.resolve().name
    try:
        name = input(f"[XForge] Nome do projeto [{default_name}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        name = default_name
    if not name:
        name = default_name

    # Step 2: confirm init
    print()
    print(f"[XForge] Sera criado:")
    print(f"  - {target_kilo}/  (skills, agents, rules, scripts)")
    print(f"  - {target_xforge}/  (decisions, packs, rag, memory)")
    print()
    try:
        confirm = input("[XForge] Continuar? [Y/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        confirm = "y"
    if confirm and confirm != "y" and confirm != "yes":
        print("[XForge] Cancelado.")
        return 1

    # Step 3: packs
    print()
    print("[XForge] Packs disponiveis:")
    packs = search_packs(min_trust=60)
    for i, p in enumerate(packs, 1):
        print(f"  {i}. {p.get("id", "?")} (trust:{p.get("trustScore", "?")}) - {p.get("description", "")[:50]}")
    print(f"  0. (nenhum)")
    print()
    selected = []
    try:
        choice = input(f"[XForge] Instalar packs (ex: 1,3 ou all ou vazio) [0]: ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = ""
    if choice.lower() == 'all':
        selected = [p["id"] for p in packs]
    elif choice:
        try:
            indices = [int(x.strip()) for x in choice.split(",") if x.strip()]
            selected = [packs[i - 1]["id"] for i in indices if 0 < i <= len(packs)]
        except (ValueError, IndexError):
            print(f"[XForge] Input invalido, continuando sem packs.")
            selected = []

    # Step 4: recognize?
    print()
    try:
        recognize_choice = input("[XForge] Rodar `xforge recognize` apos init? [Y/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        recognize_choice = "y"
    do_recognize = not recognize_choice or recognize_choice in ("y", "yes")

    # Execute init
    print()
    print("[XForge] Inicializando...")
    args_copy = argparse.Namespace(**vars(args))
    args_copy.interactive = False
    args_copy.name = name
    result = cmd_init(args_copy)
    if result != 0:
        return result

    # Save name to kilo.jsonc (best-effort)
    kilo_jsonc = project_root / "kilo.jsonc"
    if not kilo_jsonc.exists():
        kilo_jsonc.write_text(
            "{\n"
            f'  "name": "{name}",\n'
            f'  "createdAt": "{datetime.now().isoformat()}",\n'
            f'  "xforgeVersion": "{__version__}"\n'
            "}\n",
            encoding="utf-8",
        )
        print(f"[XForge] Criado kilo.jsonc com nome={name!r}")

    # Install packs
    for pack_id in selected:
        print(f"[XForge] Instalando pack: {pack_id}")
        manifest, err = install_pack(pack_id, project_root, force=args.force)
        if err:
            print(f"[XForge] AVISO: {err}")
        else:
            print(f"[XForge] OK: {manifest.get("id")} v{manifest.get("version")}")

    # Recognize
    if do_recognize:
        print()
        print("[XForge] Rodando recognize...")
        recognize(project_root)

    print()
    print("[XForge] ============================================")
    print("[XForge]  Init completo!")
    print("[XForge] ============================================")
    print()
    print("Proximos passos:")
    print("  xforge doctor")
    print("  xforge status")
    return 0


