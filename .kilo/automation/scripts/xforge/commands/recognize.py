"""
cmd_recognize - Analisar projeto e gerar PROJECT-DNA.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
from pathlib import Path

from recognize import recognize


def cmd_recognize(args):
    """Reconhecer projeto e gerar/atualizar PROJECT-DNA."""
    project_root = Path.cwd()
    result = recognize(project_root)
    print()
    print(f"[XForge] Stack: {', '.join(result['stack'])}")
    print(f"[XForge] Convencoes detectadas: {len([v for v in result['conventions'].values() if v])}")
    print(f"[XForge] Gaps: {len(result['gaps'])}")
    print(f"[XForge] PROJECT-DNA: {result['dna_file']}")
    return 0

