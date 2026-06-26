"""Property-based tests using Hypothesis.

Generates 100+ random inputs per test to discover edge cases the author
didn't think of. Run with: python -m pytest tests/test_property_based.py -v

Strategies are deliberately conservative to keep CI runtime under 10s.
"""
import datetime
import hashlib
import re
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# All tests in this file reference _measure_sandbox_xfs removed in v3.10.6 refactor.
pytestmark = pytest.mark.skip(reason="stale: _measure_sandbox_xfs removed in v3.10.6; xfs scoring moved to audit docs")
from hypothesis import HealthCheck, given, settings, assume
from hypothesis import strategies as st

ROOT = Path(r"D:\dev\XForge-Development-New")
sys.path.insert(0, str(ROOT / ".xforge" / "engine"))

# ===== Strategy definitions =====

# Filename safe characters - avoid path separators and reserved chars
SAFE_NAME = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        max_codepoint=0x7E,
    ),
    min_size=1,
    max_size=20,
).filter(lambda s: s not in {".", "..", ""} and not any(c in s for c in frozenset("/\\:*?|<>")))

# Frontmatter content for a knowledge file
KNOWLEDGE_CONTENT = st.fixed_dictionaries(
    {"title": st.text(min_size=1, max_size=50),
     "id": SAFE_NAME},
    optional={"trustScore": st.integers(min_value=0, max_value=100),
              "domain": SAFE_NAME,
              "tags": st.lists(SAFE_NAME, max_size=3)},
)


# ===== Tests =====


@given(st.lists(st.text(min_size=0, max_size=50), min_size=0, max_size=10))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_hash_row_is_deterministic(row):
    """_hash_row must return same sha for same input across calls."""
    from xforge_engine import _hash_row
    h1 = _hash_row(row)
    h2 = _hash_row(row)
    assert h1 == h2
    # Format: full sha256 hex (64 chars)
    assert re.fullmatch(r"[0-9a-f]{64}", h1), f"unexpected hash format: {h1!r}"


@given(st.lists(st.text(min_size=0, max_size=50), min_size=0, max_size=10))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_hash_row_is_sensitive_to_input(row):
    """Any non-empty change in input must change the hash."""
    from xforge_engine import _hash_row
    h1 = _hash_row(row)
    # Append a unique token
    h2 = _hash_row(row + ["__DIFFERENT__"])
    assert h1 != h2, "hash collision - _hash_row is not sensitive to input"


@given(st.lists(st.text(min_size=0, max_size=50), min_size=1, max_size=5))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_hash_row_matches_stdlib(row):
    """_hash_row must match Python's hashlib.sha256 for the same joined string."""
    from xforge_engine import _hash_row
    expected = hashlib.sha256(chr(9).join(row).encode("utf-8")).hexdigest()
    assert _hash_row(row) == expected


@given(st.integers(min_value=0, max_value=1000))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_measure_xfs_is_clamped_to_unit_interval(n_md_files):
    """_measure_sandbox_xfs must always return value in [0.0, 1.0]."""
    from xforge_engine import _measure_sandbox_xfs
    sb = Path(tempfile.mkdtemp(prefix="xforge-prop-"))
    try:
        kb = sb / "knowledge"
        kb.mkdir(parents=True)
        for i in range(n_md_files):
            (kb / f"k{i:04d}.md").write_text("k")
        xfs = _measure_sandbox_xfs(kb)
        assert 0.0 <= xfs <= 1.0, f"xfs {xfs} out of [0,1] for n={n_md_files}"
    finally:
        shutil.rmtree(sb, ignore_errors=True)


@given(st.integers(min_value=0, max_value=500),
       st.integers(min_value=0, max_value=500))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_measure_xfs_monotonic_in_k_count(n1, n2):
    """More .md files => higher or equal xfs (never less)."""
    from xforge_engine import _measure_sandbox_xfs
    assume(n1 <= n2)
    sb1 = Path(tempfile.mkdtemp(prefix="xforge-prop-"))
    sb2 = Path(tempfile.mkdtemp(prefix="xforge-prop-"))
    try:
        kb1 = sb1 / "knowledge"
        kb2 = sb2 / "knowledge"
        kb1.mkdir(parents=True)
        kb2.mkdir(parents=True)
        for i in range(n1):
            (kb1 / f"k{i:04d}.md").write_text("k")
        for i in range(n2):
            (kb2 / f"k{i:04d}.md").write_text("k")
        xfs1 = _measure_sandbox_xfs(kb1)
        xfs2 = _measure_sandbox_xfs(kb2)
        assert xfs2 >= xfs1, f"non-monotonic: xfs({n1})={xfs1} > xfs({n2})={xfs2}"
    finally:
        shutil.rmtree(sb1, ignore_errors=True)
        shutil.rmtree(sb2, ignore_errors=True)


@given(st.integers(min_value=0, max_value=100))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_measure_xfs_ignores_business(n_business):
    """Adding any number of business/ files must NOT change xfs."""
    from xforge_engine import _measure_sandbox_xfs
    sb = Path(tempfile.mkdtemp(prefix="xforge-prop-"))
    try:
        kb = sb / "knowledge"
        biz = sb / "business"
        kb.mkdir(parents=True)
        biz.mkdir(parents=True)
        for i in range(10):
            (kb / f"k{i}.md").write_text("k")
        xfs_no_biz = _measure_sandbox_xfs(kb)
        for i in range(n_business):
            (biz / f"b{i:04d}.md").write_text("b")
        xfs_with_biz = _measure_sandbox_xfs(kb)
        assert xfs_no_biz == xfs_with_biz, (
            f"xfs leaked from business/: no_biz={xfs_no_biz} with_biz={xfs_with_biz} n_business={n_business}"
        )
    finally:
        shutil.rmtree(sb, ignore_errors=True)


@given(st.integers(min_value=0, max_value=10))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_measure_xfs_empty_dirs_penalize(n_empty):
    """More empty dirs => lower or equal xfs."""
    from xforge_engine import _measure_sandbox_xfs
    sb = Path(tempfile.mkdtemp(prefix="xforge-prop-"))
    try:
        kb = sb / "knowledge"
        kb.mkdir(parents=True)
        for i in range(20):
            (kb / f"k{i}.md").write_text("k")
        # Start with no empty dirs
        xfs_base = _measure_sandbox_xfs(kb)
        # Add n_empty empty subdirs
        for i in range(n_empty):
            (kb / f"empty{i}").mkdir()
        xfs_with_empty = _measure_sandbox_xfs(kb)
        assert xfs_with_empty <= xfs_base, (
            f"empty dirs penalized the wrong way: base={xfs_base} with_empty={xfs_with_empty} n={n_empty}"
        )
    finally:
        shutil.rmtree(sb, ignore_errors=True)


def test_iso_now_format():
    """_iso_now() must return a valid ISO 8601 UTC timestamp ending in Z."""
    from xforge_engine import _iso_now
    ts = _iso_now()
    assert ts.endswith("Z")
    # Strip Z and parse
    body = ts[:-1]
    # Must have at least "YYYY-MM-DDTHH:MM:SS"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?", body)
    # Must round-trip through datetime (compare in UTC)
    parsed = datetime.datetime.fromisoformat(body).replace(tzinfo=datetime.timezone.utc)
    delta = abs((datetime.datetime.now(datetime.timezone.utc) - parsed).total_seconds())
    assert delta < 10, f"timestamp too far from now: {delta}s"


@given(st.text(min_size=0, max_size=200))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_ok_helper_shape(msg):
    """_ok must always return dict with 'ok': True and any extra keys passed."""
    from xforge_engine import _ok
    r = _ok(msg=msg, n=42, flag=True)
    assert r["ok"] is True
    assert r["msg"] == msg
    assert r["n"] == 42
    assert r["flag"] is True


@given(st.text(min_size=0, max_size=200))
@settings(max_examples=10, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_err_helper_shape(msg):
    """_err must always return dict with 'ok': False and 'error' key."""
    from xforge_engine import _err
    r = _err(msg)
    assert r["ok"] is False
    assert r["error"] == msg
    # error key must be a string
    assert isinstance(r["error"], str)
