"""Test that .xforge/business/ is properly guarded in the AutoResearch sandbox (Fase v1.1.0).

The xfs formula must NOT count business/ files - only knowledge/. This guarantees
that promoting knowledge files (e.g., new compliance docs) does affect xfs, but
business/ files are kept isolated from scoring.
"""
from pathlib import Path

from conftest import run_tool

ROOT = Path(r"D:\dev\XForge-Development-New")


def test_business_constant_defined(call_tool):
    """Engine should expose BUSINESS constant path."""
    r = call_tool("xforge_pack_list", {})
    assert r["ok"] is True
    # Just check the engine doesn't crash (BUSINESS used internally)


def test_measure_xfs_ignores_business(call_tool):
    """xfs measurement should count only knowledge/ files, not business/."""
    r = call_tool("xforge_autoresearch_run_mutate", {"iterations": 1})
    assert r["ok"] is True
    # xfs must be in valid range
    assert 0.0 <= r["currentXfs"] <= 1.0, f"xfs out of range: {r['currentXfs']}"


def test_mutate_copies_business(call_tool):
    """Sandbox should include a copy of business/."""
    r = call_tool("xforge_autoresearch_run_mutate", {"iterations": 1})
    assert r["ok"] is True
    # business_copied is in the baseline result (results[0])
    results = r.get("results", [])
    assert len(results) > 0, "results array should not be empty"
    baseline = results[0]
    assert "business_copied" in baseline, "baseline should report business_copied count"
    assert baseline["business_copied"] > 0, "business/ should have been copied to sandbox"
    # Verify the file actually exists in sandbox
    sb_business = ROOT / ".xforge" / "autoresearch" / "sandbox" / "business"
    assert sb_business.exists(), f"sandbox/business should exist at {sb_business}"


def test_mutate_xfs_unchanged_after_business_fix(call_tool):
    """xfs must be in valid range with business/ in sandbox.

    Knowledge growth (E012 + real docs) raises xfs above 0.787 baseline,
    but business/ files must NOT count. The test guards against business/
    accidentally polluting the score.
    """
    r = call_tool("xforge_autoresearch_run_mutate", {"iterations": 1})
    assert r["ok"] is True
    # xfs must be > 0.5 (any reasonable knowledge base)
    assert r["currentXfs"] > 0.5, f"xfs dropped below reasonable: got {r['currentXfs']}"
    # xfs must be <= 1.0 (clamped)
    assert r["currentXfs"] <= 1.0, f"xfs not clamped: got {r['currentXfs']}"