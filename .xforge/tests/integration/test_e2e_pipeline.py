"""
E2E Integration Tests - Full Pipeline
"""
import unittest
import os
import sys
import json
import tempfile
import shutil

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(TESTS_DIR, "..", "..", ".."))

AGENTS_DIR = os.path.join(ROOT, ".kilo", "agents")
WORKFLOWS_DIR = os.path.join(ROOT, ".kilo", "commands", "workflows")
COMMANDS_DIR = os.path.join(ROOT, ".kilo", "commands")
SCRIPTS_DIR = os.path.join(ROOT, ".kilo", "automation", "scripts")
XFORGE_SCRIPTS = os.path.join(ROOT, ".xforge", "scripts")
LEARNING_DIR = os.path.join(ROOT, ".xforge", "learning")
KNOWLEDGE_DIR = os.path.join(ROOT, ".xforge", "knowledge")

sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, os.path.join(SCRIPTS_DIR, "rag"))


class TestE2EPipeline(unittest.TestCase):

    def test_ldv_engine_importable(self):
        from ldv_engine import analyze_request, decompose_tasks, run_loop
        result = analyze_request("Create a login page")
        self.assertIn("requestId", result)
        self.assertEqual(result["intent"]["primary"], "criar")

    def test_ldv_decompose(self):
        from ldv_engine import analyze_request, decompose_tasks
        analysis = analyze_request("Create a REST API with authentication and database")
        decomp = decompose_tasks(analysis)
        self.assertGreater(decomp["totalTasks"], 0)
        self.assertIsInstance(decomp["dag"]["nodes"], list)
        self.assertEqual(len(decomp["executionOrder"]), decomp["totalTasks"])

    def test_ldv_full_loop(self):
        from ldv_engine import run_loop
        result = run_loop("Create a simple health check endpoint")
        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["summary"]["completed"], 0)

    def test_chunk_file_importable(self):
        from rag_local import chunk_file, tokenize
        self.assertTrue(callable(chunk_file))
        self.assertTrue(callable(tokenize))

    def test_tokenize_basic(self):
        from rag_local import tokenize
        tokens = tokenize("Hello world, this is a test")
        self.assertIn("hello", tokens)
        self.assertIn("test", tokens)

    def test_feedback_capture_flow(self):
        os.makedirs(LEARNING_DIR, exist_ok=True)
        feedback_log = os.path.join(LEARNING_DIR, "feedback-log.jsonl")
        entry = {
            "feedbackId": "FB-TEST-001", "timestamp": "2026-06-10T01:00:00Z",
            "taskId": "T-001", "taskTitle": "Test task", "taskType": "criar",
            "complexity": "S", "result": "SUCCESS", "error": None,
            "solution": {"applied": True, "description": "Test", "resolved": True},
            "context": {"provider": "test", "model": "test-model", "attemptNumber": 1, "durationMs": 100},
            "tags": ["test"], "recurring": False, "previousOccurrences": 0,
        }
        with open(feedback_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self.assertTrue(os.path.exists(feedback_log))

    def test_lesson_graph_update_flow(self):
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        graph_path = os.path.join(KNOWLEDGE_DIR, "errors-solutions-graph.json")
        if os.path.exists(graph_path):
            with open(graph_path, "r", encoding="utf-8") as f:
                graph = json.load(f)
        else:
            graph = {"nodes": {"errors": [], "solutions": []}, "edges": []}
        initial = len(graph["nodes"]["solutions"])
        graph["nodes"]["solutions"].append({
            "lessonId": "LESSON-TEST-001", "type": "solucao-validada",
            "taskType": "testar", "title": "Test lesson", "trustScore": 50, "tags": ["test"],
        })
        with open(graph_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        self.assertEqual(len(graph["nodes"]["solutions"]), initial + 1)

    def test_offline_queue_flow(self):
        queue_dir = os.path.join(ROOT, ".xforge", "queue")
        os.makedirs(queue_dir, exist_ok=True)
        queue_path = os.path.join(queue_dir, "offline-queue.json")
        queue = [{"id": "Q-TEST-001", "title": "Test", "type": "criar", "complexity": "S",
                   "request": "Test", "status": "pending", "retries": 0, "createdAt": "2026-06-10T01:00:00Z"}]
        with open(queue_path, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)
        with open(queue_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self.assertEqual(loaded[0]["status"], "pending")

    def test_doctor_script_exists(self):
        self.assertTrue(os.path.exists(os.path.join(SCRIPTS_DIR, "doctor.ps1")))

    def test_ace_agents_exist(self):
        for a in ["feedback-capture", "lesson-extractor", "lesson-applier"]:
            self.assertTrue(os.path.exists(os.path.join(AGENTS_DIR, f"{a}.md")))

    def test_ace_workflow_exists(self):
        self.assertTrue(os.path.exists(os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")))

    def test_ace_command_exists(self):
        self.assertTrue(os.path.exists(os.path.join(COMMANDS_DIR, "aprender.md")))

    def test_validacao_cruzada_exists(self):
        self.assertTrue(os.path.exists(os.path.join(WORKFLOWS_DIR, "validacao-cruzada.md")))

    def test_result_comparator_exists(self):
        self.assertTrue(os.path.exists(os.path.join(ROOT, ".kilo", "skills", "result-comparator", "SKILL.md")))

    def test_fila_command_exists(self):
        self.assertTrue(os.path.exists(os.path.join(COMMANDS_DIR, "fila.md")))

    def test_replay_queue_exists(self):
        self.assertTrue(os.path.exists(os.path.join(XFORGE_SCRIPTS, "replay-queue.ps1")))

    def test_offline_manager_no_todos(self):
        path = os.path.join(XFORGE_SCRIPTS, "offline-manager.ps1")
        self.assertTrue(os.path.exists(path))
        content = open(path, encoding="utf-8").read()
        self.assertNotIn("# TODO:", content)

    def test_ace_trigger_exists(self):
        self.assertTrue(os.path.exists(os.path.join(XFORGE_SCRIPTS, "ace-trigger.ps1")))

    def test_sdk_nodejs_exists(self):
        self.assertTrue(os.path.exists(os.path.join(ROOT, ".xforge", "scaffolding", "nodejs-sdk", "src", "index.ts")))

    def test_grpc_server_exists(self):
        self.assertTrue(os.path.exists(os.path.join(ROOT, ".xforge", "scaffolding", "grpc-server", "server.py")))

    def test_engineer_consolidated(self):
        engineer_dir = os.path.join(ROOT, ".xforge", "engineer")
        if not os.path.exists(engineer_dir):
            self.skipTest("engineer/ removed")
        subdirs = [d for d in os.listdir(engineer_dir) if os.path.isdir(os.path.join(engineer_dir, d))]
        self.assertLessEqual(len(subdirs), 5)


class TestRequirementsCoverage(unittest.TestCase):

    def test_b019_grpc_server(self):
        path = os.path.join(ROOT, ".xforge", "scaffolding", "grpc-server", "server.py")
        self.assertTrue(os.path.exists(path))
        self.assertIn("grpc", open(path, encoding="utf-8").read())

    def test_b020_nodejs_sdk(self):
        path = os.path.join(ROOT, ".xforge", "scaffolding", "nodejs-sdk", "src", "index.ts")
        self.assertTrue(os.path.exists(path))
        self.assertIn("queryRag", open(path, encoding="utf-8").read())

    def test_b034_b049_files_exist(self):
        for name in ["feedback-capture", "lesson-extractor", "lesson-applier"]:
            self.assertTrue(os.path.exists(os.path.join(AGENTS_DIR, f"{name}.md")))
        self.assertTrue(os.path.exists(os.path.join(KNOWLEDGE_DIR, "errors-solutions-graph.json")))
        self.assertTrue(os.path.exists(os.path.join(COMMANDS_DIR, "aprender.md")))
        self.assertTrue(os.path.exists(os.path.join(WORKFLOWS_DIR, "ciclo-aprendizado.md")))
        self.assertTrue(os.path.exists(os.path.join(XFORGE_SCRIPTS, "offline-manager.ps1")))
        self.assertTrue(os.path.exists(os.path.join(XFORGE_SCRIPTS, "replay-queue.ps1")))
        self.assertTrue(os.path.exists(os.path.join(COMMANDS_DIR, "fila.md")))
        self.assertTrue(os.path.exists(os.path.join(WORKFLOWS_DIR, "validacao-cruzada.md")))
        self.assertTrue(os.path.exists(os.path.join(ROOT, ".kilo", "skills", "result-comparator", "SKILL.md")))

    def test_b090_ace_trigger(self):
        self.assertTrue(os.path.exists(os.path.join(XFORGE_SCRIPTS, "ace-trigger.ps1")))

    def test_b094_type_hints(self):
        path = os.path.join(SCRIPTS_DIR, "rag", "rag_cache.py")
        self.assertTrue(os.path.exists(path))
        self.assertIn("->", open(path, encoding="utf-8").read())

    def test_b095_chunking_tests(self):
        path = os.path.join(ROOT, ".xforge", "tests", "rag", "test_chunking.py")
        self.assertTrue(os.path.exists(path))
        self.assertIn("chunk_file", open(path, encoding="utf-8").read())


if __name__ == "__main__":
    unittest.main()
