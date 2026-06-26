#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# run_all_tests.py - Executa todas as test suites do template.
import subprocess, sys, os
from pathlib import Path
TESTS = [
    '.kilo/mcp/compliance-intelligence/tests/test_classify_domain.py',
    '.kilo/mcp/compliance-intelligence/tests/test_extract_rules.py',
    '.kilo/mcp/compliance-intelligence/tests/test_knowledge_ops.py',
    '.kilo/mcp/market-intelligence/tests/test_market_tools.py',
    '.kilo/mcp/product-engineering/tests/test_product_tools.py',
    '.kilo/mcp/product-engineering/tests/test_integration.py',
]
passed, failed = 0, 0
for t in TESTS:
    if not os.path.exists(t):
        print('MISSING:', t)
        failed += 1
        continue
    r = subprocess.run([sys.executable, t], capture_output=True, text=True)
    status = 'PASS' if r.returncode == 0 else 'FAIL'
    print(status, ':', t)
    if r.returncode != 0:
        failed += 1
        print('  stderr:', r.stderr[:200])
    else:
        passed += 1
print()
print('SUMMARY:', passed, '/', passed + failed, 'passed')
sys.exit(0 if failed == 0 else 1)
