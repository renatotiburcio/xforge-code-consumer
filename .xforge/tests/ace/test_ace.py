"""Unit tests for ACE (Aprendizado Continuo Estruturado)."""
import unittest
import os
import json
import tempfile
import shutil

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

AGENTS_DIR = os.path.join(ROOT, ".kilo", "agents")
WORKFLOWS_DIR = os.path.join(ROOT, ".kilo", "commands", "workflows")
COMMANDS_DIR = os.path.join(ROOT, ".kilo", "commands")
KNOWLEDGE_DIR = os.path.join(ROOT, ".xforge", "knowledge")
LEARNING_DIR = os.path.join(ROOT, ".xforge", "learning")


def load_agent_frontmatter(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    end = content.index("---", 3)
    frontmatter = content[3:end].strip()
    result = {}
    for line in frontmatter.split(chr(10)):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def load_file_content(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


class TestFeedbackCapture(unittest.TestCase):
    """B-034: feedback-capture agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        self.assertTrue(os.path.exists(path), "feedback-capture.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertEqual(fm["name"], "feedback-capture")
        self.assertEqual(fm["mode"], "subagent")

    def test_agent_has_feedback_format(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        content = load_file_content(path)
        self.assertIn("FeedbackEntry", content, "FeedbackEntry format missing")
        self.assertIn("feedbackId", content, "feedbackId field missing")
        self.assertIn("result", content, "result field missing")
        self.assertIn("SUCCESS", content, "SUCCESS result missing")

    def test_agent_has_error_classification(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        content = load_file_content(path)
        self.assertIn("compilation", content, "compilation error type missing")
        self.assertIn("runtime", content, "runtime error type missing")
        self.assertIn("timeout", content, "timeout error type missing")

    def test_agent_references_executor(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        content = load_file_content(path)
        self.assertIn("executor-tarefas", content, "No reference to executor-tarefas")

    def test_agent_has_recurring_detection(self):
        path = os.path.join(AGENTS_DIR, "feedback-capture.md")
        content = load_file_content(path)
        self.assertIn("recurring", content, "Recurring detection not mentioned")
        self.assertIn("previousOccurrences", content, "previousOccurrences field missing")


class TestLessonExtractor(unittest.TestCase):
    """B-035: lesson-extractor agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "lesson-extractor.md")
        self.assertTrue(os.path.exists(path), "lesson-extractor.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "lesson-extractor.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertEqual(fm["name"], "lesson-extractor")
        self.assertEqual(fm["mode"], "subagent")

    def test_agent_has_trust_score_calculation(self):
        path = os.path.join(AGENTS_DIR, "lesson-extractor.md")
        content = load_file_content(path)
        self.assertIn("trust_score", content, "Trust score calculation missing")
        self.assertIn("frequencia", content, "Frequency factor missing")

    def test_agent_has_lesson_format(self):
        path = os.path.join(AGENTS_DIR, "lesson-extractor.md")
        content = load_file_content(path)
        self.assertIn("Lesson", content, "Lesson format missing")
        self.assertIn("lessonId", content, "lessonId field missing")
        self.assertIn("anti-pattern", content, "anti-pattern type missing")

    def test_agent_references_feedback_capture(self):
        path = os.path.join(AGENTS_DIR, "lesson-extractor.md")
        content = load_file_content(path)
        self.assertIn("feedback-capture", content, "No reference to feedback-capture")


class TestErrorsSolutionsGraph(unittest.TestCase):
    """B-036: errors-solutions-graph.json exists and is valid."""

    def test_graph_file_exists(self):
        path = os.path.join(KNOWLEDGE_DIR, "errors-solutions-graph.json")
        self.assertTrue(os.path.exists(path), "errors-solutions-graph.json not found")

    def test_graph_is_valid_json(self):
        path = os.path.join(KNOWLEDGE_DIR, "errors-solutions-graph.json")
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        self.assertIn("version", data)
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertIn("indexes", data)

    def test_graph_has_node_types(self):
        path = os.path.join(KNOWLEDGE_DIR, "errors-solutions-graph.json")
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        self.assertIn("errors", data["nodes"])
        self.assertIn("solutions", data["nodes"])
        self.assertIn("antiPatterns", data["nodes"])
        self.assertIn("goldenRules", data["nodes"])

    def test_feedback_log_exists(self):
        path = os.path.join(LEARNING_DIR, "feedback-log.jsonl")
        self.assertTrue(os.path.exists(path), "feedback-log.jsonl not found")

    def test_feedback_stats_exists(self):
        path = os.path.join(LEARNING_DIR, "feedback-stats.json")
        self.assertTrue(os.path.exists(path), "feedback-stats.json not found")

    def test_feedback_stats_is_valid(self):
        path = os.path.join(LEARNING_DIR, "feedback-stats.json")
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        self.assertIn("totalFeedbacks", data)
        self.assertIn("byResult", data)
        self.assertIn("byComplexity", data)


class TestLessonApplier(unittest.TestCase):
    """B-037: lesson-applier agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "lesson-applier.md")
        self.assertTrue(os.path.exists(path), "lesson-applier.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "lesson-applier.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertEqual(fm["name"], "lesson-applier")
        self.assertEqual(fm["mode"], "subagent")

    def test_agent_has_injection_format(self):
        path = os.path.join(AGENTS_DIR, "lesson-applier.md")
        content = load_file_content(path)
        self.assertIn("LICOES APLICADAS", content, "Injection format missing")
        self.assertIn("Trust", content, "Trust score in injection missing")

    def test_agent_has_relevance_algorithm(self):
        path = os.path.join(AGENTS_DIR, "lesson-applier.md")
        content = load_file_content(path)
        self.assertIn("relevancia", content, "Relevance algorithm missing")
        self.assertIn("trust_score", content, "Trust score in relevance missing")

    def test_agent_references_graph(self):
        path = os.path.join(AGENTS_DIR, "lesson-applier.md")
        content = load_file_content(path)
        self.assertIn("knowledge graph", content, "No reference to knowledge graph")


class TestAprenderCommand(unittest.TestCase):
    """B-038: /aprender command exists and is valid."""

    def test_command_file_exists(self):
        path = os.path.join(COMMANDS_DIR, "aprender.md")
        self.assertTrue(os.path.exists(path), "aprender.md not found")

    def test_command_has_examples(self):
        path = os.path.join(COMMANDS_DIR, "aprender.md")
        content = load_file_content(path)
        self.assertIn("Exemplos", content, "No examples section")
        self.assertIn("--erro", content, "--erro flag missing")
        self.assertIn("--solucao", content, "--solucao flag missing")

    def test_command_has_flags(self):
        path = os.path.join(COMMANDS_DIR, "aprender.md")
        content = load_file_content(path)
        self.assertIn("--anti-pattern", content, "--anti-pattern flag missing")
        self.assertIn("--regra-ouro", content, "--regra-ouro flag missing")
        self.assertIn("--listar", content, "--listar flag missing")


class TestCicloAprendizado(unittest.TestCase):
    """B-039: ciclo-aprendizado workflow exists and is valid."""

    def test_workflow_file_exists(self):
        path = os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")
        self.assertTrue(os.path.exists(path), "ciclo-aprendizado.md not found")

    def test_workflow_references_all_agents(self):
        path = os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")
        content = load_file_content(path)
        self.assertIn("feedback-capture", content, "Missing feedback-capture reference")
        self.assertIn("lesson-extractor", content, "Missing lesson-extractor reference")
        self.assertIn("lesson-applier", content, "Missing lesson-applier reference")

    def test_workflow_has_trust_adjustment(self):
        path = os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")
        content = load_file_content(path)
        self.assertIn("Trust Scores", content, "Trust score adjustment section missing")
        self.assertIn("expira", content, "Expiration policy missing")

    def test_workflow_has_metrics(self):
        path = os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")
        content = load_file_content(path)
        self.assertIn("Metricas", content, "Metrics section missing")


class TestFeedbackCaptureFunctional(unittest.TestCase):
    """B-034: Functional test for feedback capture logic."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.feedback_log = os.path.join(self.test_dir, "feedback-log.jsonl")
        self.feedback_stats = os.path.join(self.test_dir, "feedback-stats.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_feedback_entry(self):
        entry = {
            "feedbackId": "FB-TEST-001",
            "timestamp": "2026-06-10T01:00:00Z",
            "taskId": "T-001",
            "result": "SUCCESS",
            "error": None,
            "tags": ["test"]
        }
        with open(self.feedback_log, "w", encoding="utf-8") as f:
            f.write(json.dumps(entry) + chr(10))
        self.assertTrue(os.path.exists(self.feedback_log))
        with open(self.feedback_log, "r", encoding="utf-8") as f:
            line = f.readline()
            parsed = json.loads(line)
        self.assertEqual(parsed["feedbackId"], "FB-TEST-001")

    def test_append_feedback_entries(self):
        for i in range(3):
            entry = {"feedbackId": f"FB-TEST-{i:03d}", "result": "SUCCESS"}
            with open(self.feedback_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + chr(10))
        with open(self.feedback_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 3)

    def test_feedback_stats_structure(self):
        stats = {
            "version": "1.0.0",
            "totalFeedbacks": 0,
            "byResult": {"SUCCESS": 0, "FAIL": 0, "PARTIAL": 0},
            "byComplexity": {"S": 0, "M": 0, "L": 0, "CRITICA": 0}
        }
        with open(self.feedback_stats, "w", encoding="utf-8") as f:
            json.dump(stats, f)
        with open(self.feedback_stats, "r", encoding="utf-8-sig") as f:
            loaded = json.load(f)
        self.assertEqual(loaded["totalFeedbacks"], 0)


class TestKnowledgeGraphFunctional(unittest.TestCase):
    """B-036: Functional test for knowledge graph operations."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.graph_path = os.path.join(self.test_dir, "test-graph.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_error_node(self):
        graph = {
            "version": "1.0.0",
            "nodes": {"errors": [], "solutions": [], "antiPatterns": [], "goldenRules": []},
            "edges": [],
            "indexes": {"byTaskType": {}, "byErrorType": {}, "byTag": {}}
        }
        error_node = {
            "id": "ERR-001",
            "type": "compilation",
            "message": "CS0246: tipo nao encontrado",
            "taskType": "criar",
            "frequency": 3
        }
        graph["nodes"]["errors"].append(error_node)
        with open(self.graph_path, "w", encoding="utf-8") as f:
            json.dump(graph, f)
        with open(self.graph_path, "r", encoding="utf-8-sig") as f:
            loaded = json.load(f)
        self.assertEqual(len(loaded["nodes"]["errors"]), 1)

    def test_trust_score_calculation(self):
        def calc_trust(sucessos, tentativas, frequencia):
            import math
            return (sucessos / tentativas) * math.log2(frequencia + 1) * 100
        score = calc_trust(8, 10, 4)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 200)


if __name__ == "__main__":
    unittest.main()
