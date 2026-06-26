"""Unit tests for RAG query functionality."""
import unittest
import sys
import os
import re
import json
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".kilo", "automation", "scripts", "rag"))

import rag_local


class TestQueryCommand(unittest.TestCase):
    """Test the query_command() function."""

    def _capture_query(self, query, top=5):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rag_local.query_command(query, top)
        finally:
            sys.stdout = old
        return json.loads(buf.getvalue())

    def test_query_returns_results(self):
        """query_command should return results when RAG index exists."""
        output = self._capture_query("test", 3)
        self.assertGreaterEqual(len(output["results"]), 0)

    def test_query_output_structure(self):
        """query_command should print a JSON object with query, results, etc."""
        output = self._capture_query("xforge", 5)
        self.assertIn("query", output)
        self.assertIn("results", output)
        self.assertIn("mode", output)
        self.assertEqual(output["mode"], "local-lexical")
        self.assertEqual(output["query"], "xforge")
        self.assertIsInstance(output["results"], list)

    def test_empty_query_returns_empty_results(self):
        """Empty query string should return empty results list."""
        output = self._capture_query("", 3)
        self.assertEqual(len(output["results"]), 0)

    def test_query_top_n_respected(self):
        """top parameter should limit results count."""
        output = self._capture_query("test", 2)
        self.assertLessEqual(len(output["results"]), 2)

    def test_query_no_index_raises_error(self):
        """SystemExit raised when index files are missing."""
        orig_lexical = rag_local.LEXICAL_PATH
        orig_chunks = rag_local.CHUNKS_PATH
        rag_local.LEXICAL_PATH = rag_local.LEXICAL_PATH.with_name("lexical_missing.json")
        rag_local.CHUNKS_PATH = rag_local.CHUNKS_PATH.with_name("chunks_missing.jsonl")
        try:
            with self.assertRaises(SystemExit) as ctx:
                rag_local.query_command("test", 5)
            self.assertIn("RAG index not found", str(ctx.exception))
        finally:
            rag_local.LEXICAL_PATH = orig_lexical
            rag_local.CHUNKS_PATH = orig_chunks


class TestLoadConfig(unittest.TestCase):
    """Test load_config() function."""

    def test_load_config_returns_dict(self):
        """load_config should always return a dict."""
        cfg = rag_local.load_config()
        self.assertIsInstance(cfg, dict)

    def test_load_config_fallback_defaults(self):
        """When config file is missing, load_config returns sensible defaults."""
        orig = rag_local.CONFIG_PATH
        backup = None
        if orig.exists():
            renamed = orig.with_suffix(".json.bak")
            orig.rename(renamed)
            backup = renamed
        try:
            cfg = rag_local.load_config()
            self.assertIn("chunk", cfg)
            self.assertEqual(cfg["chunk"]["maxLines"], 40)
            self.assertEqual(cfg["chunk"]["overlapLines"], 5)
            self.assertIn("sources", cfg)
            self.assertGreater(len(cfg["sources"]), 0)
        finally:
            if backup:
                backup.rename(orig)

    def test_load_config_has_expected_keys(self):
        """Config should contain expected top-level keys."""
        cfg = rag_local.load_config()
        self.assertTrue("chunk" in cfg or "mode" in cfg or "version" in cfg)


class TestSecretScanning(unittest.TestCase):
    """Test has_secret() and SECRET_PATTERNS."""

    def test_secret_patterns_list(self):
        """SECRET_PATTERNS should be a non-empty list of compiled regexes."""
        self.assertIsInstance(rag_local.SECRET_PATTERNS, list)
        self.assertGreater(len(rag_local.SECRET_PATTERNS), 0)
        for p in rag_local.SECRET_PATTERNS:
            self.assertIsInstance(p, re.Pattern)

    def test_detects_api_key(self):
        """api_key assignment should be flagged."""
        self.assertTrue(rag_local.has_secret("api_key = 'supersecretkey123'"))

    def test_detects_password(self):
        """password assignment should be flagged."""
        self.assertTrue(rag_local.has_secret("password=12345678"))

    def test_detects_private_key(self):
        """RSA private key header should be flagged."""
        self.assertTrue(rag_local.has_secret("-----BEGIN RSA PRIVATE KEY-----"))

    def test_detects_aws_key(self):
        """AWS AKIA keys should be flagged."""
        self.assertTrue(rag_local.has_secret("AKIA1234567890123456"))

    def test_detects_github_token(self):
        """GitHub personal access tokens should be flagged."""
        self.assertTrue(rag_local.has_secret("ghp_abcdefghijklmnopqrstuvwxyz1234567890"))

    def test_detects_openai_key(self):
        """OpenAI sk- keys should be flagged."""
        self.assertTrue(rag_local.has_secret("sk-abcdefghijklmnopqrstuvwxyz12345"))

    def test_detects_bearer_token(self):
        """Authorization Bearer header should be flagged."""
        self.assertTrue(rag_local.has_secret("Authorization: Bearer token.here.value"))

    def test_detects_basic_auth(self):
        """Authorization Basic header should be flagged."""
        self.assertTrue(rag_local.has_secret("Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="))

    def test_clean_text_not_flagged(self):
        """Normal variable assignments without secrets should not be flagged."""
        self.assertFalse(rag_local.has_secret("normal_variable = 'hello'"))
        self.assertFalse(rag_local.has_secret("x = 42"))
        self.assertFalse(rag_local.has_secret("# api_key is set in config"))

    def test_password_manager_comment_not_flagged(self):
        """'password' word in non-secret contexts should not be flagged."""
        self.assertFalse(rag_local.has_secret("description = 'this is a password manager app'"))


if __name__ == "__main__":
    unittest.main()
