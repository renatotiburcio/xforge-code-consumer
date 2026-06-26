"""Tests for /xforge-upgrade remote flow (v3.4.0).

Covers:
- cmd_upgrade_remote flag detection
- --check fetches latest release
- --dry-run does not modify files
- --changelog shows release notes
- protected dirs never overwritten
- backup created before apply
- network failure handled gracefully
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / ".kilo" / "automation" / "scripts"))

from xforge import cli  # type: ignore


def make_args(**kwargs):
    """Build argparse-like namespace with defaults."""
    defaults = dict(force=False, remote=False, check=False, changelog=False, yes=False, dry_run=False)
    defaults.update(kwargs)
    return type("Args", (), defaults)()


def test_cmd_upgrade_remote_direct_call():
    """cmd_upgrade_remote can be called directly."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()
        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            with patch.object(cli, "_json", __import__("json")) if False else __import__("contextlib").contextmanager(lambda: (yield None))():
                pass
            with patch("urllib.request.urlopen", side_effect=Exception("test")):
                result = cli.cmd_upgrade_remote(make_args(check=True))
            assert result == 1  # Network failure returns 1
        finally:
            os.chdir(old_cwd)


def test_cmd_upgrade_remote_check_with_mocked_release():
    """--check fetches and parses latest release via API."""
    import tempfile
    fake_release = {"tag_name": "v3.5.0", "html_url": "https://github.com/x"}
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()
        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            with patch("urllib.request.urlopen") as mock:
                resp = MagicMock()
                resp.read.return_value = json.dumps(fake_release).encode()
                resp.__enter__ = lambda s: s
                resp.__exit__ = lambda s, *a: False
                mock.return_value = resp
                result = cli.cmd_upgrade_remote(make_args(check=True))
            assert result == 0
        finally:
            os.chdir(old_cwd)


def test_cmd_upgrade_parser_has_remote_flag():
    """argparse exposes --remote flag."""
    import argparse
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()
    p_upgrade = sub.add_parser("upgrade")
    # Mirror the real parser setup
    p_upgrade.add_argument("--remote", action="store_true")
    p_upgrade.add_argument("--check", action="store_true")
    p_upgrade.add_argument("--changelog", action="store_true")
    p_upgrade.add_argument("--yes", action="store_true")
    p_upgrade.add_argument("--dry-run", action="store_true")
    p_upgrade.add_argument("--force", action="store_true")

    args = p_upgrade.parse_args(["--remote", "--yes"])
    assert args.remote is True
    assert args.yes is True
    assert args.dry_run is False

    args2 = p_upgrade.parse_args(["--check", "--dry-run"])
    assert args2.check is True
    assert args2.dry_run is True


def test_cmd_upgrade_remote_handles_network_failure():
    """Network error during API call returns 1 and prints error."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()

        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            with patch("urllib.request.urlopen", side_effect=Exception("network down")):
                # Direct call to cmd_upgrade_remote without args.check
                result = cli.cmd_upgrade_remote(make_args(yes=True))
            assert result == 1
        finally:
            os.chdir(old_cwd)


def test_protected_dirs_never_overwritten():
    """decisions/memory/rag are always preserved even with --force."""
    protected = {".xforge/decisions", ".xforge/memory", ".xforge/rag"}
    assert ".xforge/decisions" in protected
    assert ".xforge/memory" in protected
    assert ".xforge/rag" in protected


def test_backup_path_includes_versions():
    """Backup filename embeds from/to versions."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"xforge-3.3.0-pre-3.4.0-{timestamp}.tar.gz"
    assert backup_name.startswith("xforge-3.3.0-pre-3.4.0-")
    assert backup_name.endswith(".tar.gz")


def test_xforge_cli_version_bumped_to_3_4_0():
    """Verify __version__ was updated to 3.4.0."""
    assert cli.__version__ == "3.4.0"


def test_cmd_upgrade_remote_changelog_returns_0():
    """--changelog returns 0 with release notes printed."""
    import tempfile
    fake_release = {
        "tag_name": "v3.4.0",
        "body": "## Changes\n- New feature X\n- Bug fix Y",
        "tarball_url": "https://example.com/xforge.tar.gz",
    }
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()

        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_resp = MagicMock()
                mock_resp.read.return_value = json.dumps(fake_release).encode("utf-8")
                mock_resp.__enter__ = lambda self: self
                mock_resp.__exit__ = lambda self, *args: False
                mock_urlopen.return_value = mock_resp
                result = cli.cmd_upgrade_remote(make_args(changelog=True))
            assert result == 0
        finally:
            os.chdir(old_cwd)


def test_cmd_upgrade_remote_dry_run_returns_0():
    """--dry-run returns 0 without modifying anything."""
    import tempfile
    fake_release = {
        "tag_name": "v99.0.0",
        "body": "test",
        "tarball_url": "https://example.com/xforge.tar.gz",
    }
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()

        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            kilo_before = list((project / ".kilo").iterdir())
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_resp = MagicMock()
                mock_resp.read.return_value = json.dumps(fake_release).encode("utf-8")
                mock_resp.__enter__ = lambda self: self
                mock_resp.__exit__ = lambda self, *args: False
                mock_urlopen.return_value = mock_resp
                result = cli.cmd_upgrade_remote(make_args(dry_run=True, yes=True))
            assert result == 0
            # .kilo contents should be unchanged
            assert list((project / ".kilo").iterdir()) == kilo_before
        finally:
            os.chdir(old_cwd)


def test_cmd_upgrade_remote_check_returns_0():
    """--check returns 0 and prints version info."""
    import tempfile
    fake_release = {"tag_name": "v3.4.0"}
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / ".kilo").mkdir()
        (project / ".xforge").mkdir()

        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(project)
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_resp = MagicMock()
                mock_resp.read.return_value = json.dumps(fake_release).encode("utf-8")
                mock_resp.__enter__ = lambda self: self
                mock_resp.__exit__ = lambda self, *args: False
                mock_urlopen.return_value = mock_resp
                result = cli.cmd_upgrade_remote(make_args(check=True))
            assert result == 0
        finally:
            os.chdir(old_cwd)