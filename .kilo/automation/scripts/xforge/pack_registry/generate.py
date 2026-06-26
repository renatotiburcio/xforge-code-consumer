"""Generate sample pack tarballs (bundled with xforge CLI v3.0-rc2)."""
import io
import json
import tarfile
from pathlib import Path

REG_DIR = Path(__file__).resolve().parent
PACKS_DIR = REG_DIR / "packs"
PACKS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_PACKS = {
    "xforge-fiscal-1.2.0": {
        "version": "1.2.0", "trustScore": 95,
        "files": {
            "manifest.json": {"id": "xforge-fiscal", "name": "Brazilian Fiscal Pack", "version": "1.2.0", "description": "NFe, NFCe, NFS-e, ICMS, PIS/COFINS, SPED"},
            "knowledge/icms.md": "# ICMS\n\nImposto sobre Circulacao de Mercadorias e Servicos.\n",
            "knowledge/pis-cofins.md": "# PIS/COFINS\n\nContribuicoes sociais sobre receita.\n",
            "rules/RN-001.md": "# RN-001: Aliquota ICMS padrao\n\nA aliquota padrao de ICMS e 18% mas pode variar por UF.\n",
        },
    },
    "xforge-hr-1.1.0": {
        "version": "1.1.0", "trustScore": 92,
        "files": {
            "manifest.json": {"id": "xforge-hr", "name": "HR/Payroll Pack", "version": "1.1.0"},
            "knowledge/clt.md": "# CLT\n\nConsolidacao das Leis do Trabalho.\n",
            "knowledge/esocial.md": "# eSocial\n\nSistema de escritura fiscal digital.\n",
        },
    },
    "xforge-accounting-1.0.5": {
        "version": "1.0.5", "trustScore": 90,
        "files": {
            "manifest.json": {"id": "xforge-accounting", "name": "Accounting Pack", "version": "1.0.5"},
            "knowledge/plano-contas.md": "# Plano de Contas\n\nEstrutura contabil brasileira.\n",
        },
    },
    "xforge-suas-1.0.0": {
        "version": "1.0.0", "trustScore": 85,
        "files": {
            "manifest.json": {"id": "xforge-suas", "name": "SUAS Pack", "version": "1.0.0"},
            "knowledge/loas.md": "# LOAS\n\nLei Organica da Assistencia Social.\n",
        },
    },
    "xforge-pix-0.9.0": {
        "version": "0.9.0", "trustScore": 88,
        "files": {
            "manifest.json": {"id": "xforge-pix", "name": "PIX Pack", "version": "0.9.0"},
            "knowledge/pix.md": "# PIX\n\nPagamento instantaneo brasileiro.\n",
        },
    },
    "xforge-frontend-kit-1.0.0": {
        "version": "1.0.0", "trustScore": 80,
        "files": {
            "manifest.json": {"id": "xforge-frontend-kit", "name": "Frontend UI Kit", "version": "1.0.0"},
            "components/Button.tsx": "export function Button({ children }: { children: React.ReactNode }) {\n  return <button className=\"px-4 py-2 bg-blue-600 text-white rounded\">{children}</button>;\n}\n",
        },
    },
    "xforge-testing-advanced-1.0.0": {
        "version": "1.0.0", "trustScore": 87,
        "files": {
            "manifest.json": {"id": "xforge-testing-advanced", "name": "Advanced Testing Pack", "version": "1.0.0"},
            "knowledge/mutation-testing.md": "# Mutation Testing\n\nVerifica qualidade dos testes via mutantes.\n",
        },
    },
}

for slug, pack in SAMPLE_PACKS.items():
    tar_path = PACKS_DIR / f"{slug}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        for relpath, content in pack["files"].items():
            content_bytes = json.dumps(content, indent=2, ensure_ascii=False).encode("utf-8") if isinstance(content, dict) else content.encode("utf-8")
            ti = tarfile.TarInfo(name=f"{slug.replace('.tar.gz', '')}/{relpath}")
            ti.size = len(content_bytes)
            tar.addfile(ti, io.BytesIO(content_bytes))
    print(f"Created: {tar_path.name} ({tar_path.stat().st_size}B)")

print(f"\n{len(SAMPLE_PACKS)} sample packs in {PACKS_DIR}")
