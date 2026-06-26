"""Shared fixtures for xforge tests."""
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid
from pathlib import Path

import pytest


XFORGE_PKG_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = XFORGE_PKG_DIR.parent
KILO_SOURCE = SCRIPTS_DIR.parent.parent.parent
XFORGE_SOURCE = KILO_SOURCE.parent / ".xforge"

sys.path.insert(0, str(XFORGE_PKG_DIR))


@pytest.fixture
def tmp_project():
    """Create a unique empty project directory in C:\\TEMP."""
    base = Path(tempfile.gettempdir()) / f"xforge_test_{uuid.uuid4().hex[:8]}"
    project = base / "test-project"
    project.mkdir(parents=True)
    yield project
    if base.exists():
        shutil.rmtree(base, ignore_errors=True)


@pytest.fixture
def tmp_path(tmp_path):
    """Override tmp_path to use C:\\TEMP (pytest temp dir is locked on Windows)."""
    base = Path(tempfile.gettempdir()) / f"xforge_pyt_{uuid.uuid4().hex[:8]}"
    base.mkdir()
    yield base
    if base.exists():
        shutil.rmtree(base, ignore_errors=True)


@pytest.fixture
def fake_xforge_source():
    """Create a fake .kilo + .xforge source tree to simulate the install repo."""
    base = Path(tempfile.gettempdir()) / f"xforge_source_{uuid.uuid4().hex[:8]}"
    kilo_src = base / "xforge-enterprise-development-os"
    kilo_src.mkdir(parents=True)
    kilo_dir = kilo_src / ".kilo"
    (kilo_dir / "automation" / "scripts").mkdir(parents=True)
    (kilo_dir / "rules").mkdir()
    (kilo_dir / "fake-kilo.txt").write_text("kilo-source", encoding="utf-8")
    (kilo_dir / "rules" / "test.md").write_text("# test rule", encoding="utf-8")

    xforge_src = kilo_src / ".xforge"
    (xforge_src / "decisions").mkdir(parents=True)
    (xforge_src / "memory").mkdir()
    (xforge_src / "fake-xforge.txt").write_text("xforge-source", encoding="utf-8")

    yield kilo_src, kilo_dir, xforge_src
    if base.exists():
        shutil.rmtree(base, ignore_errors=True)


@pytest.fixture
def mock_xforge_source(monkeypatch, fake_xforge_source):
    """Monkey-patch find_xforge_source() in cli.py to return the fake source."""
    kilo_src, kilo_dir, xforge_src = fake_xforge_source

    def fake_find():
        return kilo_dir, xforge_src

    monkeypatch.setattr("cli.find_xforge_source", fake_find)
    return kilo_src, kilo_dir, xforge_src


@pytest.fixture
def dotnet_project(tmp_project):
    (tmp_project / "MyApp.csproj").write_text(
        "<Project Sdk=\"Microsoft.NET.Sdk\"></Project>", encoding="utf-8"
    )
    (tmp_project / "Domain").mkdir()
    (tmp_project / "Repository").mkdir()
    (tmp_project / "tests").mkdir()
    return tmp_project


@pytest.fixture
def python_project(tmp_project):
    (tmp_project / "pyproject.toml").write_text(
        "[project]\nname = \"test\"\nversion = \"0.1.0\"\n", encoding="utf-8"
    )
    return tmp_project


@pytest.fixture
def node_project(tmp_project):
    (tmp_project / "package.json").write_text(
        '{"name": "test-app", "version": "0.1.0", "dependencies": {"react": "^18.0.0"}}',
        encoding="utf-8",
    )
    return tmp_project
