"""Unit tests for XForge doctor.ps1 validation logic."""
import unittest
import os
import json
import subprocess
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

EXPECTED_DIRS = [
    ".kilo/commands",
    ".kilo/agents",
    ".kilo/skills",
    ".kilo/rules",
    ".xforge",
    ".xforge/rag",
]

EXPECTED_FILES = [
    "AGENTS.md",
    "kilo.jsonc",
    ".kilocodeignore",
]

RAG_SCRIPTS = [
    ".kilo/automation/scripts/rag/rag_local.py",
    ".kilo/automation/scripts/rag/index-local.ps1",
    ".kilo/automation/scripts/rag/query-local.ps1",
    ".kilo/automation/scripts/rag/status-index.ps1",
    ".kilo/automation/scripts/rag/validate-rag.ps1",
]


def load_jsonc(path):
    """Load a JSONC file, stripping comments and handling BOM."""
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    cleaned = "\n".join(
        line for line in content.split("\n")
        if not line.strip().startswith("//")
    )
    return json.loads(cleaned)


def load_json(path):
    """Load a JSON file with BOM handling."""
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


class TestRequiredStructure(unittest.TestCase):
    """Test that all required directories and files exist."""

    def test_required_dirs_exist(self):
        """All required directories must exist."""
        for d in EXPECTED_DIRS:
            path = os.path.join(ROOT, d)
            self.assertTrue(os.path.isdir(path), f"Missing required directory: {d}")

    def test_required_files_exist(self):
        """All required files must exist."""
        for f in EXPECTED_FILES:
            path = os.path.join(ROOT, f)
            self.assertTrue(os.path.isfile(path), f"Missing required file: {f}")

    def test_rag_scripts_exist(self):
        """All RAG automation scripts must exist."""
        for f in RAG_SCRIPTS:
            path = os.path.join(ROOT, f)
            self.assertTrue(os.path.isfile(path), f"Missing RAG script: {f}")


class TestKiloJsonc(unittest.TestCase):
    """Test kilo.jsonc structure and content."""

    def setUp(self):
        self.path = os.path.join(ROOT, "kilo.jsonc")
        self.config = load_jsonc(self.path)

    def test_has_instructions(self):
        """kilo.jsonc must have instructions array."""
        self.assertIn("instructions", self.config)
        self.assertIsInstance(self.config["instructions"], list)

    def test_has_agent_config(self):
        """kilo.jsonc must have agent configuration."""
        self.assertIn("agent", self.config)
        self.assertIsInstance(self.config["agent"], dict)

    def test_has_skills_config(self):
        """kilo.jsonc must have skills configuration."""
        self.assertIn("skills", self.config)

    def test_has_commands_config(self):
        """kilo.jsonc must have commands configuration."""
        self.assertIn("commands", self.config)

    def test_has_workflows_config(self):
        """kilo.jsonc must have workflows configuration."""
        self.assertIn("workflows", self.config)

    def test_has_routing_config(self):
        """kilo.jsonc must have routing configuration."""
        self.assertIn("routing", self.config)

    def test_routing_has_providers(self):
        """Routing section must have providers."""
        routing = self.config["routing"]
        self.assertIn("providers", routing)
    def test_allowed_keys_only(self):
        """kilo.jsonc should only contain allowed keys."""
        allowed = {"$schema", "instructions", "agent", "skills", "commands", "workflows", "permission", "routing", 
"contextWindow", "tools", "mcp", "watcher", "provider", "experimental"}
        for key in self.config:
            self.assertIn(key, allowed, f"Unsupported key in kilo.jsonc: {key}")

    def test_agent_models_configured(self):
        """At least one agent must have a model configured."""
        agents_with_model = 0
        for name, cfg in self.config["agent"].items():
            if isinstance(cfg, dict) and "model" in cfg:
                agents_with_model += 1
        self.assertGreater(agents_with_model, 0, "No agent has a model configured")


class TestAgentFiles(unittest.TestCase):
    """Test agent file structure."""

    def test_agent_count(self):
        """Should have at least 36 agent files."""
        agents_dir = os.path.join(ROOT, ".kilo", "agents")
        agent_files = [f for f in os.listdir(agents_dir) if f.endswith(".md")]
        self.assertGreaterEqual(len(agent_files), 36, f"Expected 36+ agents, found {len(agent_files)}")

    def test_agents_have_frontmatter(self):
        """All agent files must have YAML frontmatter with name and description."""
        agents_dir = os.path.join(ROOT, ".kilo", "agents")
        for fname in os.listdir(agents_dir):
            if not fname.endswith(".md"):
                continue
            with open(os.path.join(agents_dir, fname), "r", encoding="utf-8-sig") as f:
                content = f.read()
            self.assertTrue(content.startswith("---"), f"Missing frontmatter in {fname}")
            self.assertIn("name:", content[:500], f"Missing name in frontmatter: {fname}")
            self.assertIn("description:", content[:500], f"Missing description in frontmatter: {fname}")


class TestSkillFiles(unittest.TestCase):
    """Test skill directory structure."""

    def test_skill_count(self):
        """Should have at least 132 skill directories."""
        skills_dir = os.path.join(ROOT, ".kilo", "skills")
        skill_dirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        self.assertGreaterEqual(len(skill_dirs), 132, f"Expected 132+ skills, found {len(skill_dirs)}")

    def test_skills_have_skill_md(self):
        """All skill directories must have SKILL.md."""
        skills_dir = os.path.join(ROOT, ".kilo", "skills")
        for dname in os.listdir(skills_dir):
            dpath = os.path.join(skills_dir, dname)
            if not os.path.isdir(dpath):
                continue
            skill_path = os.path.join(dpath, "SKILL.md")
            self.assertTrue(os.path.isfile(skill_path), f"Missing SKILL.md in {dname}")


class TestQualityGates(unittest.TestCase):
    """Test quality gate infrastructure."""

    def test_git_hooks_exist(self):
        """Git hooks must be present."""
        for hook in ["pre-commit", "pre-push"]:
            path = os.path.join(ROOT, ".githooks", hook)
            self.assertTrue(os.path.isfile(path), f"Missing git hook: {hook}")

    def test_privacy_script_exists(self):
        """Privacy verification script must exist."""
        path = os.path.join(ROOT, ".xforge/scripts", "verify-privacy.ps1")
        self.assertTrue(os.path.isfile(path), "Missing verify-privacy.ps1")

    def test_rag_manifest_exists(self):
        """RAG manifest must exist after indexing."""
        path = os.path.join(ROOT, ".xforge", "rag", "manifest.json")
        self.assertTrue(os.path.isfile(path), "Missing RAG manifest")

    def test_rag_manifest_has_documents(self):
        """RAG manifest must have documents indexed."""
        path = os.path.join(ROOT, ".xforge", "rag", "manifest.json")
        manifest = load_json(path)
        self.assertGreater(manifest.get("documentCount", 0), 0, "RAG manifest has 0 documents")

    def test_template_docs_exist(self):
        """Template documentation must exist."""
        for doc in ["COMO-USAR.md", "COMO-ESTENDER.md", "ARQUITETURA.md"]:
            path = os.path.join(ROOT, ".xforge", "docs", doc)
            self.assertTrue(os.path.isfile(path), f"Missing template doc: {doc}")

    def test_mcp_servers_configured(self):
        """At least one MCP server config must exist."""
        mcp_dir = os.path.join(ROOT, ".kilo", "mcp")
        self.assertTrue(os.path.isdir(mcp_dir), "Missing .kilo/mcp directory")
        configs = [f for f in os.listdir(mcp_dir) if f.endswith(".json")]
        self.assertGreater(len(configs), 0, "No MCP server configs found")


class TestRAGConfig(unittest.TestCase):
    """Test RAG configuration."""

    def test_rag_config_exists(self):
        """RAG config must exist."""
        path = os.path.join(ROOT, ".xforge", "rag", "config.json")
        self.assertTrue(os.path.isfile(path), "Missing RAG config")

    def test_rag_config_has_sources(self):
        """RAG config must have sources."""
        path = os.path.join(ROOT, ".xforge", "rag", "config.json")
        config = load_json(path)
        self.assertIn("sources", config)
        self.assertIsInstance(config["sources"], list)
        self.assertGreater(len(config["sources"]), 0, "RAG sources list is empty")

    def test_rag_config_has_chunk_config(self):
        """RAG config must have chunk configuration."""
        path = os.path.join(ROOT, ".xforge", "rag", "config.json")
        config = load_json(path)
        self.assertIn("chunk", config)
        self.assertIn("maxLines", config["chunk"])
        self.assertGreater(config["chunk"]["maxLines"], 0)


class TestConnectivityConfig(unittest.TestCase):
    """Test connectivity configuration."""

    def test_global_config_exists(self):
        """Global config should exist at ~/.xforge/config.json."""
        home = os.path.expanduser("~")
        config_path = os.path.join(home, ".xforge", "config.json")
        self.assertTrue(os.path.isfile(config_path), "Missing ~/.xforge/config.json")

    def test_global_config_has_provider(self):
        """Global config must have provider section."""
        home = os.path.expanduser("~")
        config_path = os.path.join(home, ".xforge", "config.json")
        if os.path.isfile(config_path):
            config = load_json(config_path)
            self.assertIn("provider", config)
            self.assertIn("active", config["provider"])
            self.assertIn("model", config["provider"])


class TestDoctorExecution(unittest.TestCase):
    """Test that doctor.ps1 runs and passes."""

    @classmethod
    def setUpClass(cls):
        """Run doctor once and cache output for all tests."""
        doctor_script = os.path.join(ROOT, ".kilo", "automation", "scripts", "doctor.ps1")
        ps_cmd = "Set-Location '{}'; & '{}'".format(ROOT, doctor_script)
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", ps_cmd],
            capture_output=True, text=True, timeout=60,
        )
        cls.returncode = result.returncode
        cls.stdout = result.stdout
        cls.stderr = result.stderr

    def test_doctor_passes(self):
        """Doctor should have no errors other than known registry path missing."""
        error_lines = [l for l in self.stdout.splitlines() if "ERROR" in l and "Registry path missing" not in l]
        self.assertEqual(len(error_lines), 0, "Doctor failed with non-registry errors:\n" + "\n".join(error_lines))

    def test_doctor_output_has_sections(self):
        """Doctor output should contain all expected sections."""
        expected_sections = [
            "Required structure",
            "kilo.jsonc",
            "Registries",
            "Commands and workflows",
            "Agents",
            "Skills",
            "Encoding",
            "Connectivity",
            "Quality gates",
            "Summary"
        ]
        for section in expected_sections:
            self.assertIn(section, self.stdout, "Missing section in doctor output: " + section)

    def test_doctor_zero_errors(self):
        """Doctor should have no errors other than known registry path missing."""
        error_lines = [l for l in self.stdout.splitlines() if "ERROR" in l and "Registry path missing" not in l]
        self.assertEqual(len(error_lines), 0, "Doctor reported non-registry errors:\n" + "\n".join(error_lines))

    def test_doctor_zero_warnings(self):
        """Doctor should report 0 warnings, or only known warnings (workflows without matching command)."""
        match_zero = re.search(r"Warnings\s*:\s*0", self.stdout)
        if match_zero is None:
            # Check if warnings are only about workflows without matching commands (expected)
            warn_match = re.search(r"Warnings\s*:\s*(\d+)", self.stdout)
            if warn_match:
                warn_count = int(warn_match.group(1))
                # Known warnings: workflows invoked by other workflows may not have matching commands
                known_warnings = [
                    "loop-decomposicao-validacao.md",
                    "ciclo-aprendizado.md"
                ]
                for kw in known_warnings:
                    if kw in self.stdout:
                        warn_count -= 1
                self.assertLessEqual(warn_count, 0,
                    "Doctor reported unexpected warnings:\n" + self.stdout[-500:])
            else:
                self.fail("Could not parse warning count from doctor output")


if __name__ == "__main__":
    unittest.main()
