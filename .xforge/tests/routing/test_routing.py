"""Unit tests for Smart Routing (B-041 a B-044)."""
import unittest
import os
import json

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
AGENTS_DIR = os.path.join(ROOT, ".kilo", "agents")
RULES_DIR = os.path.join(ROOT, ".kilo", "rules")
KILO_JSONC = os.path.join(ROOT, "kilo.jsonc")

def load_jsonc(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    cleaned = chr(10).join(
        line for line in content.split(chr(10))
        if not line.strip().startswith("//")
    )
    return json.loads(cleaned)

def read_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def get_frontmatter(path):
    content = read_file(path)
    if not content.startswith("---"):
        return {}
    end = content.index("---", 3)
    fm = {}
    for line in content[3:end].strip().split(chr(10)):
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


class TestComplexityClassifier(unittest.TestCase):
    def test_agent_exists(self):
        self.assertTrue(os.path.exists(os.path.join(AGENTS_DIR, "complexity-classifier.md")))

    def test_agent_frontmatter(self):
        fm = get_frontmatter(os.path.join(AGENTS_DIR, "complexity-classifier.md"))
        self.assertEqual(fm.get("name"), "complexity-classifier")
        self.assertEqual(fm.get("mode"), "subagent")

    def test_agent_has_factors(self):
        content = read_file(os.path.join(AGENTS_DIR, "complexity-classifier.md"))
        self.assertIn("fileScope", content)
        self.assertIn("riskLevel", content)
        self.assertIn("reversibility", content)

    def test_agent_has_tier_mapping(self):
        content = read_file(os.path.join(AGENTS_DIR, "complexity-classifier.md"))
        self.assertIn("economy", content)
        self.assertIn("ultra", content)


class TestSmartRoutingRules(unittest.TestCase):
    def test_rules_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(RULES_DIR, "00-xforge-rule-index.md")))

    def test_routing_tiers_in_jsonc(self):
        data = load_jsonc(KILO_JSONC)
        tiers = data["routing"]["complexityRouting"]["tiers"]
        for tier_name in ["economy", "standard", "premium", "ultra"]:
            self.assertIn(tier_name, tiers, f"{tier_name} tier missing")

    def test_special_rules_in_jsonc(self):
        data = load_jsonc(KILO_JSONC)
        sr = data["routing"]["complexityRouting"]["specialRules"]
        self.assertIn("security", sr)
        self.assertIn("lgpd", sr)

    def test_failover_in_tiers(self):
        data = load_jsonc(KILO_JSONC)
        tiers = data["routing"]["complexityRouting"]["tiers"]
        for name, tier in tiers.items():
            self.assertIn("fallback", tier, f"{name} missing fallback")


class TestKiloJsoncRouting(unittest.TestCase):
    def test_jsonc_valid(self):
        data = load_jsonc(KILO_JSONC)
        self.assertIn("routing", data)

    def test_complexity_routing_exists(self):
        data = load_jsonc(KILO_JSONC)
        self.assertIn("complexityRouting", data["routing"])

    def test_tiers_exist(self):
        data = load_jsonc(KILO_JSONC)
        tiers = data["routing"]["complexityRouting"]["tiers"]
        for tier in ["economy", "standard", "premium", "ultra"]:
            self.assertIn(tier, tiers)

    def test_tier_fields(self):
        data = load_jsonc(KILO_JSONC)
        tiers = data["routing"]["complexityRouting"]["tiers"]
        for name, tier in tiers.items():
            self.assertIn("provider", tier, f"{name} missing provider")
            self.assertIn("model", tier, f"{name} missing model")
            self.assertIn("fallback", tier, f"{name} missing fallback")

    def test_special_rules(self):
        data = load_jsonc(KILO_JSONC)
        sr = data["routing"]["complexityRouting"]["specialRules"]
        self.assertIn("security", sr)
        self.assertIn("lgpd", sr)

    def test_economy_config(self):
        data = load_jsonc(KILO_JSONC)
        eco = data["routing"]["complexityRouting"]["tiers"]["economy"]
        self.assertEqual(eco["complexity"], "S")
        self.assertEqual(eco["priority"], "cost")

    def test_ultra_config(self):
        data = load_jsonc(KILO_JSONC)
        ultra = data["routing"]["complexityRouting"]["tiers"]["ultra"]
        self.assertEqual(ultra["complexity"], "CRITICA")
        self.assertLessEqual(ultra["temperature"], 0.1)


class TestClassificationLogic(unittest.TestCase):
    def _classify(self, score):
        if score <= 4: return "S"
        elif score <= 9: return "M"
        elif score <= 15: return "L"
        return "CRITICA"

    def test_simple(self):
        self.assertEqual(self._classify(1), "S")

    def test_moderate(self):
        self.assertEqual(self._classify(7), "M")

    def test_complex(self):
        self.assertEqual(self._classify(12), "L")

    def test_critical(self):
        self.assertEqual(self._classify(19), "CRITICA")


if __name__ == "__main__":
    unittest.main()
