# Bug-Fix Mode Template for /forge (v3.55.0)

Fix a specific bug. Uses ANNOTATIONS (TODO/FIXME) + FEEDBACK (bug tracker) to find root cause.

## Command syntax
```bash
/forge bug-fix 'NullReferenceException in GetByIdAsync' --file CustomerService.cs
/forge bug-fix 'Login fails after password reset' --evidence tickets/T-1234
/forge bug-fix --recurring --id BUG-001
```

## Flow (7 steps)
1. Parse bug description (or use --id from bug tracker)
2. Search ANNOTATIONS (// FIXME, // HACK for this file/feature)
3. Search FEEDBACK (tickets, reviews, logs mentioning this bug)
4. Cross-reference (correlate annotations + feedback)
5. Root cause analysis (invoke GCF with relevant Geniuses)
6. Generate fix (minimal change + test for regression + commit)
7. Verify (build + test + close related tickets)

## Questions (8 max)
1. Bug description? (or --id from tracker)
2. Affected file/feature? (auto-detect)
3. Repro steps? (if from tickets)
4. Severity? (P0/P1/P2/P3)
5. Is this a regression? (yes/no)
6. Hotfix or proper fix? (hotfix = minimal, proper = full)
7. Tests affected? (auto-detect)
8. Update CHANGELOG? (yes/no)

## Generated artifacts
- Fix: minimal code change in the affected file
- Regression test: Application.Tests/.../RegressionTest.cs
- Annotation update: change // FIXME to // FIXED with link to commit
- Changelog entry (if --changelog yes)
- Commit: fix(scope): <description>

## Auto-detection from BUG-NNN
When --id is specified, auto-fill:
- Description (from bug tracker)
- Affected area (from extracted_keywords)
- Evidence (from all sources mentioning it)
- Priority (from bug tracker)
- Suggested fix (from related ANNOTATIONS or stack traces)

## Coverage by Layer (v3.55.0)
coverage by layer, coverage + layer, coverage per layer
- Bug detection: 100% (from ANNOTATIONS + FEEDBACK)
- Root cause analysis: 100% (GCF + 5 Geniuses)
- Fix generation: 100% (minimal + regression test)
- Bug-fix mode total: 100%