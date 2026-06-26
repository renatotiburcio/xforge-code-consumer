"""Regression tests for pytest invocation in xforge_engine._run_pytest_cached.

Bug history:
- v1.1.2: subprocess used cwd=project_root, missing pytest.ini/conftest.py
- v1.1.2: regex `(\d+) passed` matched FIRST occurrence (progress noise)
- Fix: cwd=engine_dir + parse last line only + no:cacheprovider
"""
import re
import subprocess
import sys


def _parse_pytest_summary(stdout: str):
    """Same logic as engine._run_pytest_cached (replicated for testability)."""
    last_line = stdout.strip().split(chr(10))[-1] if stdout.strip() else ""
    m = re.search(r"(\d+) passed", last_line)
    m_failed = re.search(r"(\d+) failed", last_line)
    passed = int(m.group(1)) if m else 0
    failed = int(m_failed.group(1)) if m_failed else 0
    return passed, failed


def test_parse_quiet_format_146_passed():
    """Quiet mode: 146 passed, 1 skipped (no = signs)."""
    out = "146 passed, 1 skipped in 49.39s"
    p, f = _parse_pytest_summary(out)
    assert p == 146
    assert f == 0


def test_parse_verbose_format_with_equals():
    """Verbose mode: ============= 145 passed, 2 skipped =============="""
    out = "============= 145 passed, 2 skipped in 45s ============="
    p, f = _parse_pytest_summary(out)
    assert p == 145
    assert f == 0


def test_parse_with_failures():
    """Mixed: 10 passed, 3 failed."""
    out = "=========== 10 passed, 3 failed, 2 skipped in 12s ==========="
    p, f = _parse_pytest_summary(out)
    assert p == 10
    assert f == 3


def test_parse_empty_output_returns_zero():
    out = ""
    p, f = _parse_pytest_summary(out)
    assert p == 0
    assert f == 0


def test_ignore_progress_noise_passed_word():
    """Progress lines like "tests/test_x.py::test_y PASSED [ 50%]" should NOT match.
    The PASSED is uppercase without a digit prefix."""
    out = """tests/test_x.py::test_y PASSED [ 50%]
tests/test_z.py::test_w PASSED [100%]
145 passed, 1 skipped in 45s"""
    p, f = _parse_pytest_summary(out)
    # Last line is the summary, not progress
    assert p == 145
    assert f == 0


def test_pytest_collect_only_finds_140_plus_tests():
    """Use --co (collect only) to verify test discovery works from engine dir.
    Running the full suite here would take 50+s and hit the test timeout.
    """
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "--co", "-q", "-p", "no:cacheprovider"],
        capture_output=True, text=True, timeout=30,
        cwd=r"D:\dev\XForge-Development-New\.xforge\engine",
    )
    assert r.returncode in (0, 5), f"collection failed: {r.returncode}: {r.stdout[-500:]}"
    m = re.search(r"(\d+) tests? collected", r.stdout)
    assert m is not None, f"no test count found in: {r.stdout[:500]}"
    count = int(m.group(1))
    assert count >= 140, f"expected >=140 tests collected, got {count}"