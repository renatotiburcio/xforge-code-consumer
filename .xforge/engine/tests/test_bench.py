"""Tests for bench.py benchmark script."""
import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(r"D:\\dev\\XForge-Development-New")
SCRIPT = ROOT / ".xforge" / "engine" / "bench.py"


def test_bench_runs():
    """bench.py should run without errors and produce output."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--iterations", "3", "--skip-heavy"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, r.stderr
    assert "XForge Engine Benchmark" in r.stdout
    assert "Iterations per op" in r.stdout
    assert "Slowest" in r.stdout


def test_bench_json_output():
    """bench.py --json should output valid JSON with performance metrics."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--iterations", "3", "--skip-heavy", "--json"],
        capture_output=True, text=True, timeout=60,
    )
    data = json.loads(r.stdout)
    # Verify all expected ops are measured
    assert "xforge_doctor" in data
    assert "xforge_knowledge_search" in data
    assert "xforge_workflow_list" in data
    assert "xforge_pack_list" in data
    # Verify metrics are present
    for op, m in data.items():
        assert "median_ms" in m, op
        assert "p95_ms" in m, op
        assert "iterations" in m, op
        assert m["median_ms"] >= 0