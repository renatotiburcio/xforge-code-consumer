"""Tests for pack.py module."""
import io
import json
import sys
import tarfile
import tempfile
import shutil
from pathlib import Path

import pack

XFORGE_PKG = Path(__file__).resolve().parent.parent
PACK_PKG = XFORGE_PKG / "pack_registry"


def test_load_registry_default():
    reg = pack.load_registry()
    assert reg["version"] == "1.0"
    assert len(reg["packs"]) >= 5


def test_load_registry_custom_path(tmp_path):
    p = tmp_path / "reg.json"
    p.write_text(json.dumps({"version": "9.9", "packs": []}), encoding="utf-8")
    reg = pack.load_registry(p)
    assert reg["version"] == "9.9"


def test_load_registry_missing_file(tmp_path):
    reg = pack.load_registry(tmp_path / "missing.json")
    assert reg == {"version": "1.0", "packs": []}


def test_search_packs_no_filter():
    results = pack.search_packs(min_trust=0)
    assert len(results) >= 5


def test_search_packs_query():
    results = pack.search_packs(query="fiscal")
    ids = [p["id"] for p in results]
    assert "xforge-fiscal" in ids


def test_search_packs_min_trust():
    results = pack.search_packs(min_trust=95)
    for p in results:
        assert p["trustScore"] >= 95


def test_search_packs_tag():
    results = pack.search_packs(tag="pix")
    assert all("pix" in p["tags"] for p in results)


def test_search_packs_no_results():
    results = pack.search_packs(query="zzz_nonexistent_zzz")
    assert results == []


def test_resolve_pack_found():
    p = pack.resolve_pack("xforge-fiscal")
    assert p is not None
    assert p["id"] == "xforge-fiscal"


def test_resolve_pack_not_found():
    p = pack.resolve_pack("nonexistent")
    assert p is None


def test_compute_sha256(tmp_path):
    p = tmp_path / "test.txt"
    p.write_bytes(b"hello world")
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert pack.compute_sha256(p) == expected


def test_verify_pack_placeholder():
    """Placeholder hashes are skipped (test mode)."""
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as f:
        f.write(b"hello")
        path = Path(f.name)
    try:
        ok, msg = pack.verify_pack(path, "placeholder-foo")
        assert ok is True
        assert "skipped" in msg
    finally:
        path.unlink()


def test_verify_pack_hash_match(tmp_path):
    p = tmp_path / "x.tar.gz"
    p.write_bytes(b"hello world")
    expected = pack.compute_sha256(p)
    ok, msg = pack.verify_pack(p, expected)
    assert ok is True
    assert msg == "ok"


def test_verify_pack_hash_mismatch(tmp_path):
    p = tmp_path / "x.tar.gz"
    p.write_bytes(b"hello")
    ok, msg = pack.verify_pack(p, "0" * 64)
    assert ok is False
    assert "mismatch" in msg


def test_extract_pack(tmp_path):
    """Create a minimal tar.gz and extract."""
    import io as _io
    tarball = tmp_path / "pack.tar.gz"
    pack_id = "test-pack"
    with tarfile.open(tarball, "w:gz") as tar:
        ti1 = tarfile.TarInfo(name=f"{pack_id}/manifest.json")
        c1 = json.dumps({"id": pack_id, "version": "1.0", "name": "Test"}).encode("utf-8")
        ti1.size = len(c1)
        tar.addfile(ti1, _io.BytesIO(c1))
        ti2 = tarfile.TarInfo(name=f"{pack_id}/data.txt")
        c2 = b"hello"
        ti2.size = len(c2)
        tar.addfile(ti2, _io.BytesIO(c2))

    target = tmp_path / "extracted"
    manifest, files = pack.extract_pack(tarball, target)
    assert manifest["id"] == pack_id
    assert "data.txt" in files
    assert (target / "data.txt").read_text(encoding="utf-8") == "hello"


def test_extract_pack_missing_manifest(tmp_path):
    """Pack without manifest.json should raise."""
    tarball = tmp_path / "bad.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        ti = tarfile.TarInfo(name="x/data.txt")
        data = b"data"
        ti.size = len(data)
        tar.addfile(ti, io.BytesIO(data))
    target = tmp_path / "out"
    try:
        pack.extract_pack(tarball, target)
        assert False, "should have raised"
    except ValueError as e:
        assert "manifest" in str(e).lower()


def test_install_pack_end_to_end(tmp_path):
    """Full install: download from local file:// URL, verify, extract, register."""
    project = tmp_path / "project"
    project.mkdir()
    (project / ".xforge" / "packs").mkdir(parents=True)

    custom_reg = tmp_path / "registry.json"
    reg_data = {
        "version": "1.0",
        "packs": [
            {
                "id": "xforge-test",
                "name": "Test Pack",
                "version": "1.0.0",
                "description": "Test",
                "trustScore": 90,
                "tags": ["test"],
                "size_kb": 1,
                "downloadUrl": "file://xforge/registry/packs/xforge-test.tar.gz",
                "sha256": "placeholder-skip-test",
                "official": True,
            }
        ],
    }
    custom_reg.write_text(json.dumps(reg_data), encoding="utf-8")

    import tarfile as _tarfile
    import io as _io
    pack_dir = PACK_PKG / "packs"
    pack_dir.mkdir(parents=True, exist_ok=True)
    with _tarfile.open(pack_dir / "xforge-test.tar.gz", "w:gz") as tar:
        ti = _tarfile.TarInfo(name="xforge-test/manifest.json")
        c1 = json.dumps({"id": "xforge-test", "version": "1.0.0", "name": "Test"}).encode("utf-8")
        ti.size = len(c1)
        tar.addfile(ti, _io.BytesIO(c1))
        ti2 = _tarfile.TarInfo(name="xforge-test/data.md")
        c2 = b"# Test data"
        ti2.size = len(c2)
        tar.addfile(ti2, _io.BytesIO(c2))

    try:
        manifest, err = pack.install_pack("xforge-test", project, registry_path=custom_reg)
        assert err is None, f"install failed: {err}"
        assert manifest["id"] == "xforge-test"
        assert (project / ".xforge" / "packs" / "xforge-test" / "data.md").exists()
        installed = json.loads((project / ".xforge" / "packs" / "installed.json").read_text(encoding="utf-8"))
        assert "xforge-test" in installed["packs"]
    finally:
        fake_test = pack_dir / "xforge-test.tar.gz"
        if fake_test.exists():
            fake_test.unlink()


def test_install_pack_low_trust_blocked(tmp_path):
    custom_reg = tmp_path / "registry.json"
    reg_data = {
        "version": "1.0",
        "packs": [
            {
                "id": "xforge-low-trust",
                "name": "Low Trust",
                "version": "1.0.0",
                "trustScore": 30,
                "description": "Low trust",
                "tags": [],
                "downloadUrl": "file://xforge/registry/packs/xforge-test.tar.gz",
                "sha256": "placeholder",
            }
        ],
    }
    custom_reg.write_text(json.dumps(reg_data), encoding="utf-8")
    project = tmp_path / "project"
    project.mkdir()
    (project / ".xforge" / "packs").mkdir(parents=True)
    manifest, err = pack.install_pack("xforge-low-trust", project, registry_path=custom_reg)
    assert manifest is None
    assert "Trust" in err or "trust" in err


def test_install_pack_force_overrides_trust(tmp_path):
    custom_reg = tmp_path / "registry.json"
    reg_data = {
        "version": "1.0",
        "packs": [
            {
                "id": "xforge-low",
                "name": "Low Trust",
                "version": "1.0.0",
                "trustScore": 30,
                "downloadUrl": "file://xforge/registry/packs/xforge-low.tar.gz",
                "sha256": "placeholder-test-skip",
            }
        ],
    }
    custom_reg.write_text(json.dumps(reg_data), encoding="utf-8")

    import tarfile
    pack_dir = PACK_PKG / "packs"
    pack_dir.mkdir(parents=True, exist_ok=True)
    fake_tarball = pack_dir / "xforge-low.tar.gz"
    with tarfile.open(fake_tarball, "w:gz") as tar:
        ti = tarfile.TarInfo(name="xforge-low/manifest.json")
        content = json.dumps({"id": "xforge-low", "version": "1.0.0"}).encode("utf-8")
        ti.size = len(content)
        tar.addfile(ti, io.BytesIO(content))

    project = tmp_path / "project"
    project.mkdir()
    (project / ".xforge" / "packs").mkdir(parents=True)
    try:
        manifest, err = pack.install_pack("xforge-low", project, registry_path=custom_reg, force=True)
        assert err is None, f"force install failed: {err}"
        assert manifest["id"] == "xforge-low"
    finally:
        if fake_tarball.exists():
            fake_tarball.unlink()



def test_extract_validates_zip_slip(tmp_path):
    """Pack with .. in path should raise UnsafePackError."""
    import io as _io
    tarball = tmp_path / "evil.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        ti = tarfile.TarInfo(name="evil/../../etc/passwd")
        c = b"pwned"
        ti.size = len(c)
        tar.addfile(ti, _io.BytesIO(c))
    try:
        pack.extract_pack(tarball, tmp_path / "out")
        assert False, "should have raised UnsafePackError"
    except pack.UnsafePackError as e:
        assert "traversal" in str(e).lower() or "absolute" in str(e).lower()


def test_extract_validates_absolute_path(tmp_path):
    """Pack with /etc/passwd should raise."""
    import io as _io
    tarball = tmp_path / "abs.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        ti = tarfile.TarInfo(name="evil//etc/passwd")
        c = b"pwned"
        ti.size = len(c)
        tar.addfile(ti, _io.BytesIO(c))
    try:
        pack.extract_pack(tarball, tmp_path / "out")
        assert False, "should have raised"
    except pack.UnsafePackError as e:
        assert "absolute" in str(e).lower() or "path" in str(e).lower()


def test_validate_member_path_safe(tmp_path):
    """Safe path returns the relative path."""
    rel = pack._validate_member_path("pack-id/data.txt", tmp_path)
    assert rel == "data.txt"


def test_validate_member_path_nested(tmp_path):
    rel = pack._validate_member_path("pack-id/sub/dir/data.txt", tmp_path)
    assert rel == "sub/dir/data.txt"


def test_update_registry_fallback(tmp_path):
    """If URL fails, returns bundled registry."""
    custom_reg = tmp_path / "reg.json"
    custom_reg.write_text(json.dumps({"version": "fallback", "packs": [{"id": "test"}]}), encoding="utf-8")
    new_reg, err = pack.update_registry(
        registry_url="http://invalid.invalid.example/registry.json",
        registry_path=custom_reg,
    )
    assert err is not None
    assert "fallback" in [p.get("id") for p in new_reg["packs"]] or new_reg.get("version") == "fallback"


def test_upgrade_pack_not_installed(tmp_path):
    project = tmp_path / "p"
    project.mkdir()
    (project / ".xforge" / "packs").mkdir(parents=True)
    (project / ".xforge" / "packs" / "installed.json").write_text('{"packs":{}}', encoding="utf-8")
    manifest, err = pack.upgrade_pack("nope", project)
    assert manifest is None
    assert "nao esta instalado" in err
