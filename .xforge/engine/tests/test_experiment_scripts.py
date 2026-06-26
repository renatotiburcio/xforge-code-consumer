"""Tests for AutoResearch experiment scripts (E001-E012).

Verifies that all experiment scripts:
  - Exist in .xforge/autoresearch/experiments/
  - Are syntactically valid Python (compile)
  - Handle SANDBOX env var (required)
  - Exit cleanly on an empty sandbox with a structured result line
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(r"D:\dev\XForge-Development-New")
EXPERIMENTS_DIR = ROOT / ".xforge" / "autoresearch" / "experiments"
TEST_TMP = ROOT / ".xforge" / "autoresearch" / ".test-tmp"

EXPECTED_SCRIPTS = [
    "E001-strip-trailing-whitespace.py",
    "E002-normalize-line-endings.py",
    "E003-add-fence-language.py",
    "E004-dedupe-knowledge.py",
    "E005-trim-blank-lines.py",
    "E006-add-source-file-frontmatter.py",
    "E007-sort-tasks-by-id.py",
    "E008-remove-empty-dirs.py",
    "E009-detect-saturation.py",
    "E010-knowledge-growth.py",
    "E011-stub-proliferation.py",
    "E012-final-growth.py",
]


@pytest.fixture
def empty_sandbox():
    """Create a clean, project-local tmp directory for sandbox smoke tests.

    Avoids PermissionError on Windows when pytest's default tmp_path tries
    to use C:\\Users\\<user>\\AppData\\Local\\Temp\\pytest-of-<user>.
    """
    TEST_TMP.mkdir(parents=True, exist_ok=True)
    d = tempfile.mkdtemp(prefix="exp-", dir=str(TEST_TMP))
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_all_expected_scripts_present():
    for name in EXPECTED_SCRIPTS:
        p = EXPERIMENTS_DIR / name
        assert p.exists(), f"missing experiment: {name}"
        assert p.is_file(), f"not a file: {name}"


@pytest.mark.parametrize("script", EXPECTED_SCRIPTS)
def test_script_is_valid_python(script):
    p = EXPERIMENTS_DIR / script
    code = p.read_text(encoding="utf-8")
    try:
        compile(code, str(p), "exec")
    except SyntaxError as e:
        pytest.fail(f"{script} has syntax error: {e}")


@pytest.mark.parametrize("script", EXPECTED_SCRIPTS)
def test_script_uses_sandbox_env_var(script):
    p = EXPERIMENTS_DIR / script
    code = p.read_text(encoding="utf-8")
    assert "os.environ" in code, f"{script} does not read os.environ"
    assert "SANDBOX" in code, f"{script} does not reference SANDBOX env var"


@pytest.mark.parametrize("script", EXPECTED_SCRIPTS)
def test_script_runs_clean_with_empty_sandbox(script, empty_sandbox):
    """Smoke test: run each experiment against an empty tmp sandbox.
    It should exit 0 and print a result line, even with no files to mutate.
    """
    env = os.environ.copy()
    env["SANDBOX"] = str(empty_sandbox)
    p = EXPERIMENTS_DIR / script
    result = subprocess.run(
        [sys.executable, str(p)],
        capture_output=True, text=True, env=env, timeout=30,
    )
    assert result.returncode == 0, (
        f"{script} failed (exit={result.returncode}): {result.stderr}"
    )
    out = result.stdout.strip()
    assert out, f"{script} produced no stdout"
    assert "=" in out, f"{script} stdout has no metric: {out!r}"


def test_experiment_count_matches_expected():
    actual = sorted(p.name for p in EXPERIMENTS_DIR.glob("E*.py"))
    expected = sorted(EXPECTED_SCRIPTS)
    assert actual == expected, (
        f"experiments drift: extra={set(actual)-set(expected)} "
        f"missing={set(expected)-set(actual)}"
    )


def test_experiments_have_no_bom():
    """Regression: BOM in .py files breaks Python's compile() on stdin/file source."""
    for name in EXPECTED_SCRIPTS:
        p = EXPERIMENTS_DIR / name
        first_bytes = p.read_bytes()[:3]
        assert first_bytes != b"\xef\xbb\xbf", (
            f"{name} has UTF-8 BOM (breaks compile())"
        )