"""Unit tests for LDV (Loop de Decomposicao com Validacao)."""
import unittest
import os
import json
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

AGENTS_DIR = os.path.join(ROOT, ".kilo", "agents")
WORKFLOWS_DIR = os.path.join(ROOT, ".kilo", "commands", "workflows")
COMMANDS_DIR = os.path.join(ROOT, ".kilo", "commands")
CHECKLISTS_DIR = os.path.join(ROOT, ".kilo", "checklists")


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


class TestDeepRequestAnalyzer(unittest.TestCase):
    """B-026: deep-request-analyzer agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "deep-request-analyzer.md")
        self.assertTrue(os.path.exists(path), "deep-request-analyzer.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "deep-request-analyzer.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertIn("name", fm)
        self.assertEqual(fm["name"], "deep-request-analyzer")
        self.assertIn("mode", fm)
        self.assertEqual(fm["mode"], "primary")

    def test_agent_has_analysis_result_format(self):
        path = os.path.join(AGENTS_DIR, "deep-request-analyzer.md")
        content = load_file_content(path)
        self.assertIn("AnalysisResult", content, "AnalysisResult format not documented")
        self.assertIn("requestId", content, "requestId field missing")
        self.assertIn("intent", content, "intent field missing")
        self.assertIn("complexity", content, "complexity field missing")
        self.assertIn("acceptanceCriteria", content, "acceptanceCriteria field missing")
        self.assertIn("requiresHumanReview", content, "requiresHumanReview field missing")

    def test_agent_has_complexity_rules(self):
        path = os.path.join(AGENTS_DIR, "deep-request-analyzer.md")
        content = load_file_content(path)
        self.assertIn("CRITICA", content, "CRITICA complexity level missing")

    def test_agent_has_intent_rules(self):
        path = os.path.join(AGENTS_DIR, "deep-request-analyzer.md")
        content = load_file_content(path)
        self.assertIn("criar", content, "criar intent missing")
        self.assertIn("migrar", content, "migrar intent missing")
        self.assertIn("corrigir", content, "corrigir intent missing")


class TestTaskDecomposer(unittest.TestCase):
    """B-027: task-decomposer agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "task-decomposer.md")
        self.assertTrue(os.path.exists(path), "task-decomposer.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "task-decomposer.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertEqual(fm["name"], "task-decomposer")
        self.assertEqual(fm["mode"], "subagent")

    def test_agent_has_dag_validation(self):
        path = os.path.join(AGENTS_DIR, "task-decomposer.md")
        content = load_file_content(path)
        self.assertIn("DAG", content, "DAG not mentioned")
        self.assertIn("ciclos", content, "Cycle detection not mentioned")
        self.assertIn("topologica", content, "Topological sort not mentioned")

    def test_agent_has_decomposition_result_format(self):
        path = os.path.join(AGENTS_DIR, "task-decomposer.md")
        content = load_file_content(path)
        self.assertIn("DecompositionResult", content, "DecompositionResult format missing")
        self.assertIn("executionOrder", content, "executionOrder missing")

    def test_agent_references_analyzer(self):
        path = os.path.join(AGENTS_DIR, "task-decomposer.md")
        content = load_file_content(path)
        self.assertIn("deep-request-analyzer", content, "No reference to deep-request-analyzer")


class TestExecutorTarefas(unittest.TestCase):
    """B-031: executor-tarefas agent exists and is valid."""

    def test_agent_file_exists(self):
        path = os.path.join(AGENTS_DIR, "executor-tarefas.md")
        self.assertTrue(os.path.exists(path), "executor-tarefas.md not found")

    def test_agent_has_valid_frontmatter(self):
        path = os.path.join(AGENTS_DIR, "executor-tarefas.md")
        fm = load_agent_frontmatter(path)
        self.assertIsNotNone(fm, "Invalid frontmatter")
        self.assertEqual(fm["name"], "executor-tarefas")
        self.assertEqual(fm["mode"], "subagent")

    def test_agent_has_retry_policy(self):
        path = os.path.join(AGENTS_DIR, "executor-tarefas.md")
        content = load_file_content(path)
        self.assertIn("maxRetries", content, "maxRetries not mentioned")
        self.assertIn("retry", content, "retry policy missing")

    def test_agent_has_execution_result_format(self):
        path = os.path.join(AGENTS_DIR, "executor-tarefas.md")
        content = load_file_content(path)
        self.assertIn("TaskExecutionResult", content, "TaskExecutionResult format missing")
        self.assertIn("completed", content, "completed status missing")
        self.assertIn("failed", content, "failed status missing")


class TestLDVWorkflow(unittest.TestCase):
    """B-029: loop-decomposicao-validacao workflow exists and is valid."""

    def test_workflow_file_exists(self):
        path = os.path.join(WORKFLOWS_DIR, "loop-decomposicao-validacao.md")
        self.assertTrue(os.path.exists(path), "loop-decomposicao-validacao.md not found")

    def test_workflow_references_all_agents(self):
        path = os.path.join(WORKFLOWS_DIR, "loop-decomposicao-validacao.md")
        content = load_file_content(path)
        self.assertIn("deep-request-analyzer", content, "Missing deep-reference")
        self.assertIn("task-decomposer", content, "Missing task-decomposer reference")
        self.assertIn("executor-tarefas", content, "Missing executor-tarefas reference")

    def test_workflow_has_consolidation_step(self):
        path = os.path.join(WORKFLOWS_DIR, "loop-decomposicao-validacao.md")
        content = load_file_content(path)
        self.assertIn("consolidacao", content, "Consolidation step missing")

    def test_workflow_has_error_handling(self):
        path = os.path.join(WORKFLOWS_DIR, "loop-decomposicao-validacao.md")
        content = load_file_content(path)
        self.assertIn("Erro", content, "Error handling section missing")
        self.assertIn("escalacao", content, "Escalation not mentioned")


class TestDecomporCommand(unittest.TestCase):
    """B-030: /decompor command exists and is valid."""

    def test_command_file_exists(self):
        path = os.path.join(COMMANDS_DIR, "decompor.md")
        self.assertTrue(os.path.exists(path), "decompor.md not found")

    def test_command_has_examples(self):
        path = os.path.join(COMMANDS_DIR, "decompor.md")
        content = load_file_content(path)
        self.assertIn("Exemplos", content, "No examples section")
        self.assertIn("--analise", content, "--analise flag missing")
        self.assertIn("--dag", content, "--dag flag missing")


class TestLDVChecklist(unittest.TestCase):
    """B-032: LDV validation checklist exists and is valid."""

    def test_checklist_file_exists(self):
        path = os.path.join(CHECKLISTS_DIR, "ldv-validation-checklist.md")
        self.assertTrue(os.path.exists(path), "ldv-validation-checklist.md not found")

    def test_checklist_has_all_phases(self):
        path = os.path.join(CHECKLISTS_DIR, "ldv-validation-checklist.md")
        content = load_file_content(path)
        self.assertIn("Fase 1", content, "Phase 1 missing")
        self.assertIn("Fase 2", content, "Phase 2 missing")
        self.assertIn("Fase 3", content, "Phase 3 missing")
        self.assertIn("Fase 4", content, "Phase 4 missing")
        self.assertIn("Fase 5", content, "Phase 5 missing")
        self.assertIn("Fase 6", content, "Phase 6 (final gate) missing")

    def test_checklist_has_metrics(self):
        path = os.path.join(CHECKLISTS_DIR, "ldv-validation-checklist.md")
        content = load_file_content(path)
        self.assertIn("Metricas", content, "Metrics section missing")
        self.assertIn("Taxa de sucesso", content, "Success rate metric missing")


if __name__ == "__main__":
    unittest.main()
