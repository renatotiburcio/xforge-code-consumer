"""Tests for security-audit.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\\dev\\XForge-Development-New")
SCRIPT = ROOT / ".kilo" / "automation" / "scripts" / "security-audit.py"


def test_security_audit_runs_clean():
    """security-audit.py should run successfully on the codebase."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=120,
    )
    # Exit 0 = clean, 1 = findings
    assert r.returncode in (0, 1)
    assert "XForge Security Audit" in r.stdout
    assert "Files scanned:" in r.stdout


def test_security_audit_json_output():
    """security-audit.py --json should output parseable JSON."""
    import json
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, timeout=120,
    )
    data = json.loads(r.stdout)
    assert "filesScanned" in data
    assert "findingsTotal" in data
    assert "bySeverity" in data
    assert "findings" in data
    assert isinstance(data["findings"], list)
    # No critical findings should exist
    assert data["bySeverity"].get("critical", 0) == 0
    assert data["bySeverity"].get("high", 0) == 0

    assert r.returncode in (0, 1)