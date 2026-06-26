"""Unit tests for RAG chunking logic."""
import unittest
import os
import json
import tempfile
import shutil

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(TESTS_DIR, "..", "..", ".."))
sys_path = os.path.join(ROOT, ".kilo", "automation", "scripts", "rag")

import sys
sys.path.insert(0, sys_path)

from rag_local import chunk_file, tokenize


class TestChunkFile(unittest.TestCase):
    """B-095: Test chunk_file() from rag_local.py with real files."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_file(self, name, content):
        path = os.path.join(self.test_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_chunk_file_basic(self):
        from pathlib import Path
        content = "\n".join([f"Line {i}: This is test content for chunking." for i in range(50)])
        path = self._create_file("test_basic.txt", content)
        chunks = chunk_file(Path(path), max_lines=20, overlap=5)
        self.assertGreater(len(chunks), 0)
        self.assertTrue(all("id" in c for c in chunks))
        self.assertTrue(all("text" in c for c in chunks))
        self.assertTrue(all("path" in c for c in chunks))

    def test_chunk_file_small_file(self):
        from pathlib import Path
        path = self._create_file("small.txt", "Just one line")
        chunks = chunk_file(Path(path), max_lines=20, overlap=5)
        self.assertLessEqual(len(chunks), 1)

    def test_chunk_file_overlap(self):
        from pathlib import Path
        lines = [f"Line {i}" for i in range(100)]
        content = "\n".join(lines)
        path = self._create_file("overlap_test.txt", content)
        chunks = chunk_file(Path(path), max_lines=30, overlap=10)
        self.assertGreater(len(chunks), 1)
        for i in range(len(chunks) - 1):
            self.assertLess(chunks[i]["startLine"], chunks[i + 1]["startLine"])

    def test_chunk_file_empty(self):
        from pathlib import Path
        path = self._create_file("empty.txt", "")
        chunks = chunk_file(Path(path), max_lines=20, overlap=5)
        self.assertEqual(len(chunks), 0)

    def test_chunk_file_with_overlap_zero(self):
        from pathlib import Path
        lines = [f"Line {i}" for i in range(40)]
        content = "\n".join(lines)
        path = self._create_file("no_overlap.txt", content)
        chunks = chunk_file(Path(path), max_lines=20, overlap=0)
        self.assertGreater(len(chunks), 0)

    def test_tokenize_basic(self):
        tokens = tokenize("Hello world, this is a test")
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("test", tokens)

    def test_tokenize_unicode(self):
        tokens = tokenize("Sistema de gestao empresarial com API REST")
        self.assertGreater(len(tokens), 0)
        self.assertTrue(any("gestao" in t or "sistema" in t for t in tokens))

    def test_chunk_file_preserves_content(self):
        from pathlib import Path
        lines = [f"Important line {i}" for i in range(60)]
        content = "\n".join(lines)
        path = self._create_file("preserve.txt", content)
        chunks = chunk_file(Path(path), max_lines=30, overlap=5)
        for chunk in chunks:
            self.assertGreater(len(chunk["text"]), 20)
            self.assertIn("preserve.txt", chunk["path"])


class TestChunkFileEdgeCases(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_file(self, name, content):
        path = os.path.join(self.test_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_single_long_line(self):
        from pathlib import Path
        content = "word " * 500
        path = self._create_file("long_line.txt", content)
        chunks = chunk_file(Path(path), max_lines=10, overlap=2)
        self.assertGreater(len(chunks), 0)

    def test_file_with_blank_lines(self):
        from pathlib import Path
        lines = []
        for i in range(30):
            if i % 3 == 0:
                lines.append("")
            else:
                lines.append(f"Content line {i}")
        content = "\n".join(lines)
        path = self._create_file("blanks.txt", content)
        chunks = chunk_file(Path(path), max_lines=10, overlap=2)
        self.assertGreater(len(chunks), 0)


if __name__ == "__main__":
    unittest.main()
