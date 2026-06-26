"""
Shared helpers for xforge CLI commands.

Fornece utilities usadas por multiplos commands:
- find_xforge_source: localiza origem .kilo/.xforge

Versao: v3.9.0 CLI Modularization per DR-0082
"""
from pathlib import Path


def find_xforge_source():
    "Encontra a origem do .kilo + .xforge."
    cli_path = Path(__file__).resolve()
    # commands/_common.py -> commands/ -> xforge/ -> scripts/ -> .kilo/automation/
    kilo_root = cli_path.parents[3]
    xforge_source = kilo_root.parent / ".xforge"
    return kilo_root, xforge_source


# XFORGE_PKG_DIR: moved from cli.py to break circular import
XFORGE_PKG_DIR = Path(__file__).resolve().parent.parent
