# Tests for recognition + self-learning tools (v3.12.0 per DR-0102)
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import json
import tempfile
from pathlib import Path
from tools import recognition

def test_recognition_detect_greenfield():
    with tempfile.TemporaryDirectory() as tmp:
        r = recognition.tool_recognition_detect({"path": tmp})
        assert r.get("ok"), r
        assert r.get("scenario") == "greenfield"
        assert r.get("is_greenfield") is True
        assert r.get("stack") == []

def test_recognition_detect_brownfield_dotnet():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "test.csproj").write_text("dotnetproj")
        r = recognition.tool_recognition_detect({"path": tmp})
        assert r.get("scenario") == "brownfield"
        assert ".NET" in r.get("stack", [])

def test_recognition_detect_brownfield_python():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "requirements.txt").write_text("flask")
        r = recognition.tool_recognition_detect({"path": tmp})
        assert r.get("scenario") == "brownfield"
        assert "Python" in r.get("stack", [])

def test_recognition_detect_no_path_uses_root():
    r = recognition.tool_recognition_detect({})
    assert r.get("ok")
    assert "path" in r
    assert "scenario" in r

def test_error_graph_add_new():
    pattern = "test_pattern_v3120_" + str(os.getpid())
    r = recognition.tool_error_graph_add({"pattern": pattern, "solution": "fix"})
    assert r.get("ok"), r
    assert r.get("action") == "added"
    assert r.get("totalErrors", 0) >= 1

def test_error_graph_add_increment():
    pattern = "test_pattern_increment_" + str(os.getpid())
    r1 = recognition.tool_error_graph_add({"pattern": pattern})
    r2 = recognition.tool_error_graph_add({"pattern": pattern})
    r3 = recognition.tool_error_graph_add({"pattern": pattern})
    assert r1.get("action") == "added"
    assert r2.get("action") == "incremented"
    assert r3.get("action") == "incremented"

def test_error_graph_add_missing_pattern():
    r = recognition.tool_error_graph_add({})
    assert not r.get("ok", True)
    assert "pattern" in r.get("error", "")

def test_error_graph_promote():
    pattern = "promote_test_" + str(os.getpid())
    for _ in range(3):
        recognition.tool_error_graph_add({"pattern": pattern})
    r = recognition.tool_error_graph_promote({"threshold": 3})
    assert r.get("ok"), r
    assert isinstance(r.get("promoted"), list)
    assert r.get("totalRules", 0) >= 1

def test_error_graph_promote_no_promotions():
    r = recognition.tool_error_graph_promote({"threshold": 999})
    assert r.get("ok")
    assert r.get("promoted") == []

def test_recognition_in_engine():
    import xforge_engine as xe
    assert "xforge_recognition_detect" in xe.TOOLS
    assert "xforge_error_graph_add" in xe.TOOLS
    assert "xforge_error_graph_promote" in xe.TOOLS
    assert xe.TOOLS["xforge_recognition_detect"] == recognition.tool_recognition_detect

# === v3.13.0 tests for deferred tools (DR-0103) ===

def test_init_smart_greenfield():
    with tempfile.TemporaryDirectory() as tmp:
        r = recognition.tool_recognition_init_smart({"path": tmp})
        assert r.get("ok"), r
        assert r.get("scenario") == "greenfield"
        assert r.get("action") == "bootstrap"
        assert (Path(tmp) / ".xforge").exists()
        assert (Path(tmp) / ".kilo").exists()

def test_init_smart_brownfield():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "package.json").write_text("{}")
        r = recognition.tool_recognition_init_smart({"path": tmp})
        assert r.get("scenario") == "brownfield"
        assert r.get("action") == "recognition"
        assert "Node.js" in r.get("stack", [])
        assert "dnaUpdated" in r

def test_learn_basic():
    r = recognition.tool_recognition_learn({"statement": "test learning"})
    assert r.get("ok"), r
    entry = r.get("entry", {})
    assert entry.get("statement") == "test learning"
    assert entry.get("kind") == "decision"  # default

def test_learn_missing_statement():
    r = recognition.tool_recognition_learn({})
    assert not r.get("ok", True)
    assert "statement" in r.get("error", "")

def test_learn_with_custom_fields():
    r = recognition.tool_recognition_learn({"kind": "preference", "statement": "no MediatR oficial", "source": "user-correction", "confidence": "0.95"})
    assert r.get("ok")
    entry = r.get("entry", {})
    assert entry.get("kind") == "preference"
    assert entry.get("source") == "user-correction"
    assert entry.get("confidence") == 0.95

def test_self_heal_no_rules():
    # Clear rules first
    graph = recognition._load_error_graph()
    graph["preventionRules"] = []
    recognition._save_error_graph(graph)
    r = recognition.tool_self_heal_apply({})
    assert r.get("ok")
    assert r.get("action") == "noop"
    assert r.get("applied") == 0

def test_self_heal_with_rules():
    # Add a rule first via add+promote
    pat = "selfheal_test_" + str(os.getpid())
    for _ in range(3):
        recognition.tool_error_graph_add({"pattern": pat})
    recognition.tool_error_graph_promote({"threshold": 3})
    r = recognition.tool_self_heal_apply({})
    assert r.get("ok")
    assert r.get("applied", 0) >= 1
    assert isinstance(r.get("rules"), list)

def test_recognition_in_engine_v313():
    import xforge_engine as xe
    assert "xforge_recognition_init_smart" in xe.TOOLS
    assert "xforge_recognition_learn" in xe.TOOLS
    assert "xforge_self_heal_apply" in xe.TOOLS
# === v3.16.0 SRP refactor (DR-0106) ===

def test_init_greenfield_creates_dirs():
    with tempfile.TemporaryDirectory() as tmp:
        r = recognition.tool_init_greenfield({"path": tmp})
        assert r.get("ok"), r
        assert r.get("scenario") == "greenfield"
        assert r.get("action") == "bootstrap"
        assert (Path(tmp) / ".xforge").exists()
        assert (Path(tmp) / ".kilo").exists()

def test_init_greenfield_no_dna_when_exists():
    with tempfile.TemporaryDirectory() as tmp:
        dna = Path(tmp) / ".xforge" / "project-dna" / "PROJECT-DNA.md"
        dna.parent.mkdir(parents=True, exist_ok=True)
        dna.write_text("existing", encoding="utf-8")
        r = recognition.tool_init_greenfield({"path": tmp})
        assert r.get("ok")
        assert r.get("created") == []  # DNA existed, no new file
        assert dna.read_text() == "existing"  # not overwritten

def test_init_brownfield_detects_stack():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "go.mod").write_text("module test")
        r = recognition.tool_init_brownfield({"path": tmp})
        assert r.get("ok"), r
        assert r.get("scenario") == "brownfield"
        assert r.get("action") == "recognition"
        assert "Go" in r.get("stack", [])
        assert "dnaUpdated" in r

def test_init_brownfield_empty_dir():
    with tempfile.TemporaryDirectory() as tmp:
        r = recognition.tool_init_brownfield({"path": tmp})
        # Empty dir = no stack detected, but still updates DNA
        assert r.get("ok")
        assert r.get("stack") == []  # no manifests

def test_smart_switch_dispatches_to_greenfield():
    with tempfile.TemporaryDirectory() as tmp:
        r = recognition.tool_recognition_init_smart({"path": tmp})
        assert r.get("scenario") == "greenfield"
        assert r.get("action") == "bootstrap"

def test_smart_switch_dispatches_to_brownfield():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "pyproject.toml").write_text("[project]")
        r = recognition.tool_recognition_init_smart({"path": tmp})
        assert r.get("scenario") == "brownfield"
        assert r.get("action") == "recognition"
        assert "Python" in r.get("stack", [])

def test_srp_tools_in_engine_v316():
    import xforge_engine as xe
    assert "xforge_init_greenfield" in xe.TOOLS
    assert "xforge_init_brownfield" in xe.TOOLS
    # Wrapper still works
    assert "xforge_recognition_init_smart" in xe.TOOLS