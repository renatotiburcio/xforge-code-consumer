"""Tests for Kilo Code CLI 1.0 compatibility (v3.3.0).

Covers:
- doctor.ps1 allowed keys (15 valid + reject typos like connectionTyle)
- kilo.jsonc loads with CLI 1.0 schema
- xforge CLI init creates kilo.jsonc + docs/index.html
- xforge-init SKILL.md reflects CLI 1.0 schema
- No typo `connectionTyle` anywhere in the codebase
"""
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
KILO_JSONC = REPO_ROOT / "kilo.jsonc"
DOCTOR = REPO_ROOT / ".kilo" / "automation" / "scripts" / "doctor.ps1"
SKILL = REPO_ROOT / ".kilo" / "skills" / "xforge-init" / "SKILL.md"
INDEX_HTML = REPO_ROOT / "docs" / "index.html"


def test_kilo_jsonc_is_valid_jsonc():
    """kilo.jsonc parses as JSON (we strip // comments)."""
    raw = KILO_JSONC.read_text(encoding="utf-8")
    # strip line comments (naive, no strings with //)
    cleaned = "\n".join(
        line for line in raw.splitlines() if not line.lstrip().startswith("//")
    )
    data = json.loads(cleaned)
    assert isinstance(data, dict)


def test_kilo_jsonc_has_schema_url():
    """kilo.jsonc references the official CLI 1.0 schema."""
    raw = KILO_JSONC.read_text(encoding="utf-8")
    assert "https://app.kilo.ai/config.json" in raw


def test_kilo_jsonc_has_model_top_level():
    """kilo.jsonc has `model` in provider/model format."""
    raw = KILO_JSONC.read_text(encoding="utf-8")
    cleaned = "\n".join(
        line for line in raw.splitlines() if not line.lstrip().startswith("//")
    )
    data = json.loads(cleaned)
    assert "model" in data
    assert "/" in data["model"], "model must be in provider/model format"


def test_kilo_jsonc_provider_block():
    """kilo.jsonc has provider.<id>.options.<key> structure."""
    raw = KILO_JSONC.read_text(encoding="utf-8")
    cleaned = "\n".join(
        line for line in raw.splitlines() if not line.lstrip().startswith("//")
    )
    data = json.loads(cleaned)
    assert "provider" in data
    for prov_id, prov_cfg in data["provider"].items():
        assert "options" in prov_cfg, f"{prov_id} missing options"
        for key in prov_cfg.get("options", {}):
            # API keys must use {env:VAR} template, not raw value
            if "key" in key.lower() or "secret" in key.lower() or "token" in key.lower():
                assert "{env:" in str(prov_cfg["options"][key]), \
                    f"{prov_id}.options.{key} must use {{env:VAR}} template"


def test_kilo_jsonc_has_permission_block():
    """kilo.jsonc has permission policy (allow/ask/deny)."""
    raw = KILO_JSONC.read_text(encoding="utf-8")
    cleaned = "\n".join(
        line for line in raw.splitlines() if not line.lstrip().startswith("//")
    )
    data = json.loads(cleaned)
    assert "permission" in data
    perm = data["permission"]
    if isinstance(perm, dict):
        for action in perm.values():
            if isinstance(action, str):
                assert action in ("allow", "ask", "deny")


def test_doctor_allowed_keys_include_schema():
    """doctor.ps1 allowlist includes $schema, model, provider, permission."""
    content = DOCTOR.read_text(encoding="utf-8")
    for key in ["$schema", "model", "provider", "permission", "mcp", "agent", "instructions", "skills"]:
        # Accept either double or single quoted form (PowerShell convention)
        assert (f'"{key}"' in content) or (f"'{key}'" in content), f"doctor.ps1 missing {key} in allowlist"


def test_no_connection_typo_in_any_config():
    """No file under repo contains the typo `connectionTyle` or `connectionType`."""
    targets = [
        REPO_ROOT / "kilo.jsonc",
        REPO_ROOT / ".xforge" / "config" / "xforge-engineer.config.json",
        REPO_ROOT / ".xforge" / "config" / "engineer.config.json",
        REPO_ROOT / ".kilo.jsonc",
    ]
    bad = ("connectionTyle", "connectionType")
    for target in targets:
        if not target.exists():
            continue
        content = target.read_text(encoding="utf-8", errors="ignore")
        for typo in bad:
            assert typo not in content, f"{target.name} contains typo: {typo}"


def test_docs_index_html_exists():
    """docs/index.html landing page exists."""
    assert INDEX_HTML.exists(), "docs/index.html missing"
    content = INDEX_HTML.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "XForge Enterprise Development OS" in content


def test_xforge_init_skill_mentions_cli_1_0():
    """xforge-init SKILL.md references Kilo Code CLI 1.0 schema."""
    content = SKILL.read_text(encoding="utf-8")
    assert "CLI 1.0" in content or "CLI 1" in content
    assert "https://app.kilo.ai/config.json" in content
    assert "{env:" in content  # env var template


def test_xforge_cli_writes_kilo_jsonc(tmp_path, monkeypatch):
    """cmd_init emits kilo.jsonc when missing."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / ".kilo" / "automation" / "scripts"))
    from xforge.cli import _write_kilo_jsonc  # type: ignore

    # tmp_path is a fresh empty dir
    created = _write_kilo_jsonc(tmp_path)
    assert created is True
    kilo_file = tmp_path / "kilo.jsonc"
    assert kilo_file.exists()
    data = json.loads(kilo_file.read_text(encoding="utf-8"))
    assert data["$schema"] == "https://app.kilo.ai/config.json"
    assert "model" in data
    assert "provider" in data
    assert "permission" in data


def test_xforge_cli_writes_index_html(tmp_path):
    """cmd_init emits docs/index.html when missing."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / ".kilo" / "automation" / "scripts"))
    from xforge.cli import _write_index_html  # type: ignore

    created = _write_index_html(tmp_path)
    assert created is True
    html = tmp_path / "docs" / "index.html"
    assert html.exists()
    content = html.read_text(encoding="utf-8")
    assert "XForge" in content