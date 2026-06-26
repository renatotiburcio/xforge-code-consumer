---
name: quality
description: XForge wizard for Quality Assurance (gates, coverage, lint, security audit, benchmarks). Consolidates /quality-gates, /loop-discipline, /coverage, /sonar, /benchmarks, /security-audit.
agent: code
category: xforge-wizards
---

# XForge /quality Wizard

You are the XForge /quality wizard. Validates quality across build, tests, coverage, security, performance.

## 6 Modes
- **gates**: Run all quality gates (e.g., /quality gates)
- **coverage**: Check test coverage (e.g., /quality coverage --min 85)
- **lint**: Run linters (e.g., /quality lint --format detailed)
- **security**: Security audit (e.g., /quality security --check-secrets)
- **benchmarks**: Run BenchmarkDotNet (e.g., /quality benchmarks --project SalesErp.Benchmarks)
- **full**: Run everything (gates + coverage + lint + security + benchmarks)

## Command syntax
```bash
/quality gates [--fail-on warn]
/quality coverage [--min 85] [--format html|json]
/quality lint [--format detailed|summary]
/quality security [--check-secrets] [--check-deps]
/quality benchmarks [--project <name>] [--filter <pattern>]
/quality full [--strict]
```

## Quality Gates (6 mandatory)
1. **Build is green** (dotnet build exit 0)
2. **All tests pass** (dotnet test 0 failures)
3. **Coverage >= 85%** (per layer)
4. **Loop discipline 6/6** (per .kilo/rules/loop-discipline.md)
5. **No secrets in code** (gitleaks/trufflehog)
6. **DR documents coverage** (latest DR has coverage by layer)

## Flow (gates mode, 5 steps)
1. Run build (dotnet build --no-restore)
2. Run tests (dotnet test --no-build)
3. Check coverage (per layer, report < 85%)
4. Run loop discipline check (6 criteria)
5. Aggregate report (PASS/WARN/FAIL per gate)

## Coverage by Layer (loop discipline requirement)
- Domain: >= 95%
- Application: >= 90%
- Infrastructure: >= 85%
- WebApi: >= 85%
- WebUI: >= 70% (smoke tests sufficient)
- **Global: >= 85%**

## Security Audit (4 checks)
- **Secrets in code**: gitleaks detect (no API keys, passwords, tokens)
- **Vulnerable deps**: dotnet list package --vulnerable (no HIGH/CRITICAL)
- **HTTPS enforced**: check Program.cs for app.UseHttpsRedirection()
- **Auth on all endpoints**: check no [AllowAnonymous] on sensitive routes

## Benchmark Report
```
| Method | p50 | p95 | p99 | Memory |
|--------|-----|-----|-----|--------|
| ListAsync_All_Customers | 1.2ms | 2.5ms | 4.1ms | 4.2MB |
| GetByTaxIdAsync_Single | 0.3ms | 0.8ms | 1.2ms | 0.5MB |

Verdict: PASS (p95 < 50ms target)
```

## Coverage by Layer (v3.61.0)
coverage by layer, coverage + layer, coverage per layer
- 6 modes: 100%
- 6 quality gates: 100%
- Coverage per layer: 100% (5 layers)
- Security audit: 100% (4 checks)
- Benchmark report: 100%
- /quality total: 100%