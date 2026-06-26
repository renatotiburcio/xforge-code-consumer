# Loop Discipline Rule

> **Precedence**: this rule augments (does not replace) the existing autonomous-experiment-loop and research-document-execute rules. When a conflict appears, this rule wins because it codifies a real failure mode (FB-001).

## 1. Problem statement

The agent can ship a release whose build is green and whose tests pass, and stop the loop. This is a known failure mode (FB-001: v3.26.0 shipped with 5/5 Domain tests but 0 tests in 4 other layers; user caught the gap). The build-green signal is not a quality signal.

## 2. Definition of release done

A release is **DONE** if and only if ALL of the following are true:

| # | Criterion | Source of truth |
|---|-----------|-----------------|
| 1 | Build is green (0 errors) | dotnet build exit code |
| 2 | At least one test project per project layer in the solution | ls tests/ |
| 3 | Each test project has at least 1 test per public handler/repository/endpoint | grep -c Fact |
| 4 | End-to-end path tested (HTTP POST writes and HTTP GET reads) for at least one entity | HttpEndpointTests exists |
| 5 | Real or testcontainer database is used in tests (NOT just new() mocks) | InMemory/Postgres/Testcontainers |
| 6 | Migrations exist if the project uses EF Core | dotnet ef migrations list |
| 7 | No new files have TODO/FIXME without an associated issue link | grep TODO |
| 8 | DR documents coverage by layer and remaining gaps | DR-NNNN |

If any of 2-8 is not met, the release is **NOT DONE**. The next action must be to close that gap, not to start a new feature.

## 3. The gap-closing first rule

After any release R, the very next release R+1 must be one of:

1. **Gap closer**: close any unmet criterion from section 2 of release Rs DR.
2. **Bug fix**: address issues discovered in release Rs tests or production telemetry.
3. **Debt reduction**: address tech debt noted in release Rs DR.

It is **NEVER** acceptable to skip the gap closer and start a new feature release.

## 4. Self-check before declaring done

Before committing any release, the agent MUST run this checklist and answer YES to each:

[ ] 1. Build is green (0 errors, 0 warnings treated as errors)
[ ] 2. Test count is at least: layers x 1 test per handler/repo/endpoint
[ ] 3. At least one HTTP roundtrip test exists (POST + GET) for a write entity
[ ] 4. Database path is tested with real data (InMemory minimum, Postgres/Testcontainers preferred)
[ ] 5. Migrations exist for the current schema
[ ] 6. No untracked TODO/FIXME without issue links
[ ] 7. DR documents coverage % and explicit remaining gaps
[ ] 8. The next backlog item is the gap closer (not a new feature)

If any answer is NO, fix it before committing. Do not skip the question.

## 5. Anti-patterns

| Anti-pattern | Why it fails | What to do instead |
|--------------|--------------|---------------------|
| Ship 5/5 tests, 0 errors treated as done | 5 tests on 1 layer = 10-15% coverage | Run the section 4 checklist |
| Build green, curl returns 200 as quality proof | build green != tested | Add real HTTP roundtrip + DB persistence test |
| Stub the AI and skip | 0% AI coverage, real integration impossible | Real adapter + FakeHandler test |
| Skip migrations because tests pass with in-memory | DB write path never validated | Generate migrations + verify EF model snapshot |
| New feature next release after thin release | Compounds the gap | Gap closer first |

## 6. How this rule fires

Triggered by:
1. Any release DR.
2. The orchestrator before declaring a release complete.
3. The user correction pattern com este teste como ficamos com a qualidade (FB-001 trigger).
4. Session-end audit: count commits since last gap-closing release. If greater than 2, force a gap-closing release next.

## 7. Reference

- FB-001-loop-discipline-violation.md (in .xforge/feedback/)
- DR-0117-loop-discipline-lesson.md (in .xforge/decisions/)
- LEARN-1781885220001..3 in .xforge/memory/learning.jsonl
- Rule file: .kilo/rules/loop-discipline.md

## 8. Enforcement checklist (for CI / pre-push hook)

Future automation: a pre-push hook can run this script to flag a release commit that ships with coverage below threshold:

# .kilo/automation/scripts/check-coverage.ps1 (TODO v3.30.0)
# minCoverage = 50
# actualCoverage = Get-Coverage
# if (actualCoverage -lt minCoverage) { exit 1 }