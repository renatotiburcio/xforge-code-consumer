"""
xforge CLI v3.9 - Thin Dispatcher

Versao 3.9.0: CLI Modularization per DR-0082.
Cada command e um modulo em commands/ package.

Comandos disponiveis:
  xforge init [--template T] [--analyze] [--force] [--interactive]
  xforge recognize
  xforge status [--log]
  xforge doctor
  xforge upgrade [--force] [--remote] [--check] [--changelog] [--yes] [--dry-run]
  xforge new STACK [--name N]
  xforge backup
  xforge restore [--index N]
  xforge pack CMD [PACK_ID] [--source S] [--force]
  xforge council CMD [TOPIC]
"""
import argparse
import sys
from pathlib import Path

from commands import init, recognize, status, doctor, upgrade, new, backup, restore, pack, council


__version__ = "3.9.0"
XFORGE_PKG_DIR = Path(__file__).resolve().parent


# Command registry - new command = 1 linha aqui + 1 modulo em commands/
COMMANDS = {
    "init": init.cmd_init,
    "recognize": recognize.cmd_recognize,
    "status": status.cmd_status,
    "doctor": doctor.cmd_doctor,
    "upgrade": upgrade.cmd_upgrade,
    "new": new.cmd_new,
    "backup": backup.cmd_backup,
    "restore": restore.cmd_restore,
    "pack": pack.cmd_pack,
    "council": council.cmd_council,
}


def build_parser():
    "Build argparse parser with all subcommands."
    parser = argparse.ArgumentParser(
        prog="xforge",
        description="XForge CLI v3.9 - Installable Toolkit, CLI Modularization",
    )
    parser.add_argument("--version", action="version", version="xforge " + __version__)

    sub = parser.add_subparsers(dest="cmd", help="Comandos disponiveis")

    # init
    p = sub.add_parser("init", help="Bootstrap .kilo + .xforge no projeto atual")
    p.add_argument("--template", help="Template de projeto")
    p.add_argument("--analyze", action="store_true", help="Rodar recognize apos init")
    p.add_argument("--force", action="store_true", help="Sobrescrever existentes")
    p.add_argument("--interactive", "-i", action="store_true", help="Modo wizard")

    # recognize
    sub.add_parser("recognize", help="Analisar projeto e gerar PROJECT-DNA")

    # status
    p = sub.add_parser("status", help="Mostrar status de adocao + metricas")
    p.add_argument("--log", action="store_true", help="Registrar snapshot em .xforge/.adoption.json")

    # doctor
    sub.add_parser("doctor", help="Validar setup")

    # upgrade
    p = sub.add_parser("upgrade", help="Atualizar .kilo + .xforge")
    p.add_argument("--force", action="store_true", help="Sobrescrever arquivos modificados")
    p.add_argument("--remote", action="store_true", help="v3.4+ Baixar upgrade do GitHub Releases API")
    p.add_argument("--check", action="store_true", help="v3.4+ Apenas verificar update")
    p.add_argument("--changelog", action="store_true", help="v3.4+ Mostrar changelog remoto")
    p.add_argument("--yes", action="store_true", help="v3.4+ Upgrade sem prompt")
    p.add_argument("--dry-run", action="store_true", help="v3.4+ Mostrar sem aplicar")

    # new
    p = sub.add_parser("new", help="Criar novo projeto com template")
    p.add_argument("stack", help="Stack")
    p.add_argument("--name", help="Nome do projeto")

    # backup
    sub.add_parser("backup", help="Backup de .xforge state")

    # pack
    p = sub.add_parser("pack", help="Marketplace packs")
    p.add_argument("pack_cmd", choices=["list","search","info","install","remove","update","upgrade"], help="Comando")
    p.add_argument("pack_id", nargs="?", help="Pack ID")
    p.add_argument("--source", help="Source URL/path para install")
    p.add_argument("--force", action="store_true", help="Forcar instalacao")

    # restore
    p = sub.add_parser("restore", help="Restore de backup")
    p.add_argument("--index", type=int, dest="backup_index")

    # council
    p = sub.add_parser("council", help="Council of Geniuses GCF subcommands")
    p.add_argument("council_cmd", choices=["list","review","guards","devils-advocate","da","ask"], help="Comando do Council")
    p.add_argument("topic", nargs="?", help="Topico / path / genius_id")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        return 1

    handler = COMMANDS.get(args.cmd)
    if handler is None:
        print(f"[XForge] Comando desconhecido: {args.cmd}")
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
