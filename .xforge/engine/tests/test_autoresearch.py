"""Tests for AutoResearch loop runtime."""
from pathlib import Path

def test_autoresearch_runs_and_records(call_tool):
    r = call_tool("xforge_autoresearch_run", {"iterations": 2})
    assert r["ok"] is True
    assert r["iterations"] == 2
    assert 0 <= r["currentXfs"] <= 1
    assert len(r["results"]) == 3
    assert r["results"][0]["status"] == "baseline"
    assert any("immutable-scoring" in p for p in r["protectedPaths"])


def test_autoresearch_results_file_exists(call_tool):
    call_tool("xforge_autoresearch_run", {"iterations": 1})
    results = Path(r"D:\dev\XForge-Development-New\.xforge\autoresearch\results.tsv")
    assert results.exists()
    content = results.read_text(encoding="utf-8")
    assert "step\texperiment\txfs" in content


def test_autoresearch_caps_iterations(call_tool):
    r = call_tool("xforge_autoresearch_run", {"iterations": 1000})
    assert r["ok"] is True
    assert r["iterations"] <= 20


def test_autoresearch_mutate_runs_and_copies_sandbox(call_tool):
    """Real mutate loop: copies knowledge to sandbox, runs E*.py, measures, decides."""
    r = call_tool("xforge_autoresearch_run_mutate", {"iterations": 3})
    assert r["ok"] is True, r
    assert r["iterations"] == 3
    assert r["experimentsAvailable"] >= 3
    assert "sandbox" in r["sandboxPath"]
    assert 0 <= r["currentXfs"] <= 1
    # baseline + 3 iterations = 4 results
    assert len(r["results"]) == 4
    assert r["results"][0]["status"] == "baseline"
    statuses = [res["status"] for res in r["results"][1:]]
    assert all(s in ("keep", "discard") for s in statuses)


def test_autoresearch_mutate_sandbox_dir_created(call_tool):
    """Sandbox must exist after running the mutate loop."""
    sandbox = Path(r"D:\dev\XForge-Development-New\.xforge\autoresearch\sandbox\knowledge")
    call_tool("xforge_autoresearch_run_mutate", {"iterations": 1})
    assert sandbox.exists()
    md_files = list(sandbox.rglob("*.md"))
    assert len(md_files) > 0


def test_autoresearch_mutate_caps_iterations(call_tool):
    r = call_tool("xforge_autoresearch_run_mutate", {"iterations": 9999})
    assert r["ok"] is True
    assert r["iterations"] <= 20
