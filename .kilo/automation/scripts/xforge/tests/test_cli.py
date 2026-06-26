"""Tests for xforge.cli commands."""
import argparse
import io
import sys
import json
import tarfile
from pathlib import Path

import cli
import recognize


def make_args(**kwargs):
    """Create a simple Namespace with defaults."""
    defaults = {"template": None, "analyze": False, "force": False, "backup_index": None, "name": None, "stack": "generic", "pack_cmd": None, "pack_id": None, "source": None, "log": False, "interactive": False, "council_cmd": None, "topic": None, "genius_id": None, "domain": None}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_version_constant():
    assert cli.__version__ == "3.4.0"


def test_find_xforge_source_returns_paths():
    kilo, xforge = cli.find_xforge_source()
    assert "kilo" in kilo.name.lower() or kilo.name == ".kilo"
    assert "xforge" in xforge.name.lower()


def test_init_copies_kilo_and_xforge(tmp_project, mock_xforge_source):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args())
        assert result == 0
        assert (tmp_project / ".kilo").exists()
        assert (tmp_project / ".xforge").exists()
        assert (tmp_project / ".kilo" / "fake-kilo.txt").read_text(encoding="utf-8") == "kilo-source"
        assert (tmp_project / ".xforge" / "fake-xforge.txt").read_text(encoding="utf-8") == "xforge-source"
    finally:
        os.chdir(old_cwd)


def test_init_fails_if_kilo_exists(tmp_project, mock_xforge_source):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".xforge").mkdir()
        result = cli.cmd_init(make_args())
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_init_force_overwrites(tmp_project, mock_xforge_source):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".kilo" / "old.txt").write_text("old", encoding="utf-8")
        (tmp_project / ".xforge").mkdir()
        result = cli.cmd_init(make_args(force=True))
        assert result == 0
        assert not (tmp_project / ".kilo" / "old.txt").exists()
    finally:
        os.chdir(old_cwd)


def test_init_analyze_flag_runs_recognize(tmp_project, mock_xforge_source, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_recognize(root):
        captured["called"] = True
        captured["root"] = root
        return {"stack": ["dotnet"], "manifests": [], "conventions": {}, "gaps": [], "dna_file": str(root / "PROJECT-DNA.md")}

    monkeypatch.setattr("cli.recognize", fake_recognize)
    try:
        os.chdir(tmp_project)
        (tmp_project / "test.csproj").write_text("<Project/>", encoding="utf-8")
        result = cli.cmd_init(make_args(analyze=True))
        assert result == 0
        assert captured.get("called") is True
    finally:
        os.chdir(old_cwd)


def test_status_shows_adoption(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_status(make_args())
        assert result == 0
        output = "\n".join(captured.get("output", []))
        assert "Status de adocao" in output
        assert "0/7" in output
    finally:
        os.chdir(old_cwd)


def test_status_full_adoption(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    (tmp_project / ".kilo").mkdir()
    (tmp_project / ".xforge").mkdir()
    (tmp_project / ".xforge" / "project-dna").mkdir()
    (tmp_project / ".xforge" / "project-dna" / "PROJECT-DNA.md").write_text("# DNA", encoding="utf-8")
    (tmp_project / ".kilo.jsonc").write_text("{}", encoding="utf-8")
    (tmp_project / "AGENTS.md").write_text("# AGENTS", encoding="utf-8")
    (tmp_project / ".git").mkdir()
    (tmp_project / ".xforge" / "rag").mkdir()
    (tmp_project / ".xforge" / "rag" / "manifest.json").write_text("{}", encoding="utf-8")

    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        cli.cmd_status(make_args())
        output = "\n".join(captured.get("output", []))
        assert "7/7" in output
    finally:
        os.chdir(old_cwd)


def test_backup_creates_archive(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    (tmp_project / ".xforge").mkdir()
    (tmp_project / ".xforge" / "state.txt").write_text("state", encoding="utf-8")

    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_backup(make_args())
        assert result == 0
        backups = list((tmp_project / ".xforge-backups").glob("xforge-backup-*.tar.gz"))
        assert len(backups) == 1
        with tarfile.open(backups[0], "r:gz") as tar:
            names = tar.getnames()
            assert any("xforge/state.txt" in n for n in names)
    finally:
        os.chdir(old_cwd)


def test_backup_fails_without_xforge(tmp_project):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_backup(make_args())
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_restore_fails_without_backups(tmp_project):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_restore(make_args(backup_index=1))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_restore_picks_correct_backup(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    (tmp_project / ".xforge-backups").mkdir()
    backup1 = tmp_project / ".xforge-backups" / "xforge-backup-20200101-hhmmss.tar.gz"
    backup2 = tmp_project / ".xforge-backups" / "xforge-backup-20260101-hhmmss.tar.gz"

    with tarfile.open(backup1, "w:gz") as tar:
        tar.add(tmp_project / ".xforge-backups", arcname="placeholder1")
    with tarfile.open(backup2, "w:gz") as tar:
        ti = tarfile.TarInfo(name="xforge/data.txt")
        data = b"backup2-content"
        ti.size = len(data)
        tar.addfile(ti, io.BytesIO(data))

    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_restore(make_args(backup_index=1))
        assert result == 0
        assert (tmp_project / "xforge" / "data.txt").exists()
        assert (tmp_project / "xforge" / "data.txt").read_bytes() == b"backup2-content"
    finally:
        os.chdir(old_cwd)


def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["xforge"])
    result = cli.main()
    assert result == 1
    out = capsys.readouterr().out
    assert "usage" in out.lower() or "XForge CLI" in out


def test_main_version(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["xforge", "--version"])
    with __import__("pytest").raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "3.4.0" in out


def test_main_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["xforge", "--help"])
    with __import__("pytest").raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "init" in out
    assert "recognize" in out
    assert "status" in out
    assert "doctor" in out
    assert "upgrade" in out
    assert "new" in out
    assert "backup" in out
    assert "restore" in out


def test_upgrade_adds_new_files(tmp_project, mock_xforge_source):
    import os
    kilo_src, kilo_dir, xforge_src = mock_xforge_source
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".xforge").mkdir()

        (xforge_src / "new-file.txt").write_text("new-content", encoding="utf-8")

        result = cli.cmd_upgrade(make_args())
        assert result == 0
        assert (tmp_project / ".xforge" / "new-file.txt").exists()
        assert (tmp_project / ".xforge" / "new-file.txt").read_text(encoding="utf-8") == "new-content"
    finally:
        os.chdir(old_cwd)


def test_upgrade_preserves_decisions(tmp_project, mock_xforge_source):
    import os
    kilo_src, kilo_dir, xforge_src = mock_xforge_source
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "decisions").mkdir()
        user_decision = tmp_project / ".xforge" / "decisions" / "DR-USER-test.md"
        user_decision.write_text("# USER DECISION - DO NOT OVERWRITE", encoding="utf-8")

        (xforge_src / "decisions" / "DR-NEW-test.md").write_text("# new", encoding="utf-8")

        result = cli.cmd_upgrade(make_args())
        assert result == 0
        assert user_decision.read_text(encoding="utf-8") == "# USER DECISION - DO NOT OVERWRITE"
        assert (tmp_project / ".xforge" / "decisions" / "DR-NEW-test.md").exists()
    finally:
        os.chdir(old_cwd)


def test_upgrade_creates_backup(tmp_project, mock_xforge_source):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "state.txt").write_text("state", encoding="utf-8")
        cli.cmd_upgrade(make_args())
        backups = list((tmp_project / ".xforge-backups").glob("xforge-backup-pre-upgrade-*.tar.gz"))
        assert len(backups) == 1
    finally:
        os.chdir(old_cwd)


def test_upgrade_fails_without_init(tmp_project):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_upgrade(make_args())
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_upgrade_force_overwrites(tmp_project, mock_xforge_source):
    import os
    kilo_src, kilo_dir, xforge_src = mock_xforge_source
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".kilo").mkdir()
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "test.txt").write_text("OLD", encoding="utf-8")
        (xforge_src / "test.txt").write_text("NEW", encoding="utf-8")

        result = cli.cmd_upgrade(make_args())
        assert result == 0
        assert (tmp_project / ".xforge" / "test.txt").read_text(encoding="utf-8") == "OLD"

        result = cli.cmd_upgrade(make_args(force=True))
        assert result == 0
        assert (tmp_project / ".xforge" / "test.txt").read_text(encoding="utf-8") == "NEW"
    finally:
        os.chdir(old_cwd)
def test_new_list_shows_templates(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        captured = {}
        def fake_print(*args, **kwargs):
            captured.setdefault("output", []).append(" ".join(str(a) for a in args))
        monkeypatch.setattr("builtins.print", fake_print)
        result = cli.cmd_new(make_args(stack="list"))
        assert result == 0
        output = "\n".join(captured.get("output", []))
        assert "Templates disponiveis" in output
        assert "dotnet-webapi" in output
        assert "python-fastapi" in output
        assert "react-vite" in output
    finally:
        os.chdir(old_cwd)


def test_new_creates_project_from_template(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_new(make_args(stack="generic", name="myproj"))
        assert result == 0
        assert (tmp_project / "myproj").exists()
        assert (tmp_project / "myproj" / "README.md").exists()
        assert (tmp_project / "myproj" / ".gitignore").exists()
    finally:
        os.chdir(old_cwd)


def test_new_fails_for_unknown_template(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_new(make_args(stack="nope-template", name="bad"))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_new_default_name(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_new(make_args(stack="generic"))
        assert result == 0
        assert (tmp_project / "my-generic").exists()
    finally:
        os.chdir(old_cwd)


def test_new_force_overwrites(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        (tmp_project / "myproj").mkdir()
        (tmp_project / "myproj" / "old.txt").write_text("OLD", encoding="utf-8")
        result = cli.cmd_new(make_args(stack="generic", name="myproj"))
        assert result == 1
        result = cli.cmd_new(make_args(stack="generic", name="myproj", force=True))
        assert result == 0
        assert not (tmp_project / "myproj" / "old.txt").exists()
    finally:
        os.chdir(old_cwd)
def test_pack_list_empty(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "packs").mkdir()
        result = cli.cmd_pack(make_args(pack_cmd="list", pack_id=None))
        assert result == 0
    finally:
        os.chdir(old_cwd)


def test_pack_list_shows_installed(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "packs").mkdir()
        installed = {"version": "1.0", "packs": {"xforge-fiscal": {"name": "Fiscal", "version": "1.0", "trustScore": 95, "files": []}}, "lastUpdated": "2026-06-17"}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")
        result = cli.cmd_pack(make_args(pack_cmd="list", pack_id=None))
        assert result == 0
        output = "\n".join(captured.get("output", []))
        assert "xforge-fiscal" in output
    finally:
        os.chdir(old_cwd)


def test_pack_info(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "packs").mkdir()
        installed = {"version": "1.0", "packs": {"xforge-fiscal": {"name": "Fiscal", "version": "2.0", "trustScore": 95}}, "lastUpdated": ""}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")
        result = cli.cmd_pack(make_args(pack_cmd="info", pack_id="xforge-fiscal"))
        assert result == 0
    finally:
        os.chdir(old_cwd)


def test_pack_remove(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "packs").mkdir()
        (tmp_project / ".xforge" / "packs" / "fiscal-data.txt").write_text("data", encoding="utf-8")
        installed = {"version": "1.0", "packs": {"xforge-fiscal": {"name": "Fiscal", "version": "1.0", "trustScore": 95, "files": ["packs/fiscal-data.txt"]}}, "lastUpdated": ""}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")

        result = cli.cmd_pack(make_args(pack_cmd="remove", pack_id="xforge-fiscal"))
        assert result == 0
        assert not (tmp_project / ".xforge" / "packs" / "fiscal-data.txt").exists()
        new_data = json.loads((tmp_project / ".xforge" / "packs" / "installed.json").read_text(encoding="utf-8"))
        assert "xforge-fiscal" not in new_data["packs"]
    finally:
        os.chdir(old_cwd)


def test_pack_remove_nonexistent(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge").mkdir()
        (tmp_project / ".xforge" / "packs").mkdir()
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text('{"packs":{}}', encoding="utf-8")
        result = cli.cmd_pack(make_args(pack_cmd="remove", pack_id="nope"))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_pack_search_finds_all(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_pack(make_args(pack_cmd="search", pack_id=None))
        assert result == 0
        output = "\n".join(captured.get("output", []))
        assert "packs encontrados" in output
        assert "xforge-fiscal" in output
    finally:
        os.chdir(old_cwd)


def test_pack_search_with_query(tmp_project, monkeypatch):
    import os
    old_cwd = os.getcwd()
    captured = {}
    def fake_print(*args, **kwargs):
        captured.setdefault("output", []).append(" ".join(str(a) for a in args))
    monkeypatch.setattr("builtins.print", fake_print)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_pack(make_args(pack_cmd="search", pack_id="pix"))
        assert result == 0
        output = "\n".join(captured.get("output", []))
        assert "xforge-pix" in output
        assert "xforge-fiscal" not in output
    finally:
        os.chdir(old_cwd)


def test_pack_install_real_pack(tmp_project, monkeypatch):
    """End-to-end: install xforge-fiscal from local registry."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
        result = cli.cmd_pack(make_args(pack_cmd="install", pack_id="xforge-fiscal"))
        assert result == 0
        pack_dir = tmp_project / ".xforge" / "packs" / "xforge-fiscal"
        assert pack_dir.exists()
        assert (pack_dir / "knowledge").exists()
        installed = json.loads((tmp_project / ".xforge" / "packs" / "installed.json").read_text(encoding="utf-8"))
        assert "xforge-fiscal" in installed["packs"]
    finally:
        os.chdir(old_cwd)


def test_pack_install_already_installed(tmp_project):
    """If pack already installed, return error unless --force."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        installed = {"packs": {"xforge-fiscal": {"id": "xforge-fiscal", "version": "1.0.0"}}, "lastUpdated": ""}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")
        result = cli.cmd_pack(make_args(pack_cmd="install", pack_id="xforge-fiscal"))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_pack_install_nonexistent(tmp_project):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        result = cli.cmd_pack(make_args(pack_cmd="install", pack_id="xforge-nonexistent"))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_pack_update_falls_back_to_bundled(tmp_project, monkeypatch):
    """When network fails, use bundled registry."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_pack(make_args(pack_cmd="update", pack_id=None))
        assert result == 0
    finally:
        os.chdir(old_cwd)


def test_pack_update_with_custom_source(tmp_project, monkeypatch):
    """--source URL is passed to update_registry."""
    import os
    from pack import update_registry
    captured = {}
    def fake_update(registry_url=None, registry_path=None):
        captured["url"] = registry_url
        return ({"packs": []}, None)
    monkeypatch.setattr("cli.update_registry", fake_update)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_pack(make_args(pack_cmd="update", pack_id=None, source="https://example.com/reg.json"))
        assert result == 0
        assert captured["url"] == "https://example.com/reg.json"
    finally:
        os.chdir(old_cwd)


def test_pack_upgrade_nonexistent(tmp_project):
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text('{"packs":{}}', encoding="utf-8")
        result = cli.cmd_pack(make_args(pack_cmd="upgrade", pack_id="nope"))
        assert result == 1
    finally:
        os.chdir(old_cwd)


def test_pack_upgrade_existing(tmp_project, monkeypatch):
    """upgrade delegates to install_pack with force=True (reinstall)."""
    import os
    import pack as pack_module
    old_cwd = os.getcwd()
    captured = {}
    def fake_install(pack_id, project_root, force=False):
        captured["pack_id"] = pack_id
        captured["force"] = force
        return ({"id": pack_id, "version": "1.0", "files": []}, None)
    monkeypatch.setattr(pack_module, "install_pack", fake_install)
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        installed = {"packs": {"xforge-fiscal": {"id": "xforge-fiscal", "version": "1.0.0"}}, "lastUpdated": ""}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")
        monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
        result = cli.cmd_pack(make_args(pack_cmd="upgrade", pack_id="xforge-fiscal"))
        assert result == 0
        assert captured["pack_id"] == "xforge-fiscal"
        assert captured["force"] is True
    finally:
        os.chdir(old_cwd)


def test_pack_remove_clears_xforge_packs(tmp_project, monkeypatch):
    """remove deletes pack files AND cleans up xforge_packs dir if empty."""
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        (tmp_project / ".xforge" / "packs").mkdir(parents=True)
        (tmp_project / ".xforge" / "packs" / "xforge-fiscal").mkdir()
        (tmp_project / ".xforge" / "packs" / "xforge-fiscal" / "data.txt").write_text("x", encoding="utf-8")
        installed = {"packs": {"xforge-fiscal": {"id": "xforge-fiscal", "files": ["packs/xforge-fiscal/data.txt"]}}, "lastUpdated": ""}
        (tmp_project / ".xforge" / "packs" / "installed.json").write_text(json.dumps(installed), encoding="utf-8")
        monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
        result = cli.cmd_pack(make_args(pack_cmd="remove", pack_id="xforge-fiscal"))
        assert result == 0
        assert not (tmp_project / ".xforge" / "packs" / "xforge-fiscal").exists()
    finally:
        os.chdir(old_cwd)



def test_init_interactive_creates_kilo_and_xforge(tmp_project, monkeypatch, mock_xforge_source):
    """Interactive wizard asks name, inits, creates kilo.jsonc."""
    import os
    old_cwd = os.getcwd()
    inputs = iter([
        "my-test-app",  # name
        "Y",  # confirm init
        "0",  # no packs
        "n",  # skip recognize
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args(interactive=True))
        assert result == 0
        assert (tmp_project / ".kilo").exists()
        assert (tmp_project / ".xforge").exists()
        assert (tmp_project / "kilo.jsonc").exists()
        content = (tmp_project / "kilo.jsonc").read_text(encoding="utf-8")
        assert "my-test-app" in content
    finally:
        os.chdir(old_cwd)


def test_init_interactive_cancel(tmp_project, monkeypatch):
    """User cancels at confirmation step."""
    import os
    inputs = iter(["test-name", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    captured = {}
    monkeypatch.setattr("builtins.print", lambda *a, **kw: captured.setdefault("output", []).append(" ".join(str(x) for x in a)))
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args(interactive=True))
        assert result == 1
        output_text = "\n".join(captured.get("output", []))
        assert "Cancelado" in output_text
        assert not (tmp_project / ".kilo").exists()
    finally:
        os.chdir(old_cwd)


def test_init_interactive_eof_uses_defaults(tmp_project, monkeypatch, mock_xforge_source):
    """If stdin closes (EOFError), wizard uses defaults."""
    import os
    def fake_input(_):
        raise EOFError()
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args(interactive=True))
        assert result == 0
        assert (tmp_project / ".kilo").exists()
        assert (tmp_project / "kilo.jsonc").exists()
    finally:
        os.chdir(old_cwd)


def test_init_interactive_invalid_pack_choice_continues(tmp_project, monkeypatch, mock_xforge_source):
    """Invalid pack choice (e.g., '99') should not crash wizard."""
    import os
    inputs = iter(["app", "Y", "99,abc", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args(interactive=True))
        assert result == 0
    finally:
        os.chdir(old_cwd)


def test_init_interactive_all_packs(tmp_project, monkeypatch, mock_xforge_source):
    """`all` installs all packs."""
    import os
    inputs = iter(["app", "Y", "all", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_project)
        result = cli.cmd_init(make_args(interactive=True))
        assert result == 0
    finally:
        os.chdir(old_cwd)
