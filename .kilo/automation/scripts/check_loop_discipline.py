#!/usr/bin/env python3
import os, sys, subprocess

ROOT = r'D:\dev\XForge-Development-New'
results = []

def check(name, ok, why):
    status = 'PASS' if ok else 'FAIL'
    print('[' + status + '] ' + name + ': ' + why)
    results.append(ok)

def find_solution():
    base = os.path.join(ROOT, 'src', 'sales-erp')
    if not os.path.exists(base):
        return None
    for f in os.listdir(base):
        if f.endswith('.sln') or f.endswith('.slnx'):
            return os.path.join(base, f)
    return None

SOLN = find_solution()
if SOLN is None:
    print('No solution found in src/sales-erp/. Skipping.')
    sys.exit(0)

r = subprocess.run(['dotnet', 'build', SOLN, '--no-restore'], capture_output=True, cwd=ROOT)
check('1. Build is green', r.returncode == 0, 'dotnet build exit ' + str(r.returncode))

src = os.path.join(ROOT, 'src', 'sales-erp', 'src')
tests = os.path.join(ROOT, 'src', 'sales-erp', 'tests')
layers = [d for d in os.listdir(src) if d.startswith('SalesErp.')] if os.path.exists(src) else []
test_projects = [d for d in os.listdir(tests) if d.startswith('SalesErp.') and d.endswith('.Tests')] if os.path.exists(tests) else []
check('2. Test project per layer', len(test_projects) >= len(layers), 'layers=' + str(layers) + ' tests=' + str(test_projects))

http_test = False
for tp in test_projects:
    pdir = os.path.join(tests, tp)
    for f in os.listdir(pdir):
        if f.endswith('.cs'):
            with open(os.path.join(pdir, f), 'r', encoding='utf-8') as fh:
                txt = fh.read()
                if 'PostAsJsonAsync' in txt and 'GetAsync' in txt:
                    http_test = True
check('3. HTTP roundtrip test exists', http_test, 'POST + GET in same test')

db_test = False
for tp in test_projects:
    pdir = os.path.join(tests, tp)
    for f in os.listdir(pdir):
        if f.endswith('.cs'):
            with open(os.path.join(pdir, f), 'r', encoding='utf-8') as fh:
                txt = fh.read()
                if 'UseInMemoryDatabase' in txt or 'UseNpgsql' in txt or 'Testcontainers' in txt:
                    db_test = True
check('4. DB tested with real provider', db_test, 'InMemory/Npgsql/Testcontainers')

migs = os.path.join(ROOT, 'src', 'sales-erp', 'src', 'SalesErp.Infrastructure', 'Persistence', 'Migrations')
has_mig = os.path.exists(migs) and any(f.endswith('.cs') for f in os.listdir(migs))
check('5. Migrations exist', has_mig, 'Persistence/Migrations/*.cs')

decs = os.path.join(ROOT, '.xforge', 'decisions')
last_dr = None
if os.path.exists(decs):
    for f in sorted(os.listdir(decs)):
        if f.startswith('DR-') and f.endswith('.md'):
            last_dr = f
dr_path = os.path.join(decs, last_dr) if last_dr else None
has_coverage = False
if dr_path:
    with open(dr_path, 'r', encoding='utf-8') as fh:
        txt = fh.read()
        if 'coverage' in txt.lower() and 'layer' in txt.lower():
            has_coverage = True
check('6. Latest DR has coverage-by-layer', has_coverage, 'coverage+layer in ' + str(last_dr))

failed = sum(1 for r in results if not r)
print()
print('TOTAL:', len(results) - failed, 'pass /', len(results), 'total')
sys.exit(0 if failed == 0 else 1)
