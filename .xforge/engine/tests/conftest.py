"""Shared pytest fixtures for XForge engine tests."""
import os, sys, subprocess, json, tempfile
from pathlib import Path
import pytest

ENGINE = Path(__file__).parent.parent / "xforge_engine.py"
ROOT = Path(r"D:\dev\XForge-Development-New")


def run_tool(tool, args):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(args, f)
        tmp = f.name
    try:
        r = subprocess.run(["python", str(ENGINE), tool, "@" + tmp],
                           capture_output=True, text=True, timeout=60, cwd=str(ROOT))
        if r.returncode not in (0, 1):
            raise RuntimeError(f"engine exit {r.returncode}: {r.stderr}")
        return json.loads(r.stdout)
    finally:
        os.unlink(tmp)


@pytest.fixture
def call_tool():
    return run_tool