"""
cmd_doctor - Validar setup.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
import subprocess
from pathlib import Path


def cmd_doctor(args):
    """Valida setup."""
    import subprocess

    kilo_dir = Path.cwd() / ".kilo"
    doctor_script = None

    for path in [
        kilo_dir / "automation" / "scripts" / "doctor.ps1",
        kilo_dir / "automation" / "scripts" / "doctor.py",
    ]:
        if path.exists():
            doctor_script = path
            break

    if not doctor_script:
        print("[XForge] Doctor nao encontrado em .kilo/automation/scripts/")
        return 1

    print(f"[XForge] Rodando doctor: {doctor_script.name}")
    if doctor_script.suffix == ".ps1":
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(doctor_script)],
            capture_output=True, text=True
        )
    else:
        result = subprocess.run(["python", str(doctor_script)], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


