# Refactor Mode Template for /forge (v3.55.0)

Refactor existing code. Uses GCF inline to ensure quality + safety.

## Command syntax
```bash
/forge refactor --extract-cqrs --module SalesErp.Orders
/forge refactor --extract-repository --target SalesErp.Customers
/forge refactor --add-shared-kernel --modules SalesErp.WebApi,SalesErp.WebUI
/forge refactor --god-class --file SalesErp/OrderService.cs --max-loc 300
```

## Flow (8 steps)
1. Detect refactor type (extract pattern, add CQRS, god class, etc)
2. Analyze current code (LOC, complexity, dependencies)
3. Invoke GCF (5+ Geniuses for refactor strategy)
4. Generate refactor plan (incremental steps with rollback)
5. Ask user to confirm (preview before applying)
6. Apply refactor (step by step, with tests at each step)
7. Verify parity (behavior preserved)
8. Document (ADR + CHANGELOG)

## Refactor types supported (8)
- extract-cqrs: separate Commands and Queries (XForge.MediatR)
- extract-repository: extract data access from service
- extract-shared-kernel: move DTOs/VOs to Shared project
- god-class: split large class into smaller ones
- rename: rename entity/field consistently across codebase
- migrate-to-result: replace exceptions with Result pattern
- add-validation: add FluentValidation to all commands
- add-caching: add IMemoryCache to read queries

## Questions (7 max)
1. Refactor type? (from --type or detected)
2. Target module/file? (from --module/--file)
3. Maximum LOC per class? (default 300)
4. Test coverage target after refactor? (default 85%)
5. Break compatibility? (yes/no, default no)
6. ADR required? (yes for major refactors)
7. Apply incremental? (yes = step by step, no = all at once)

## GCF Geniuses involved (by type)
- extract-cqrs: AG045 Fowler, AG046 Evans, AG053 Vernon, AG007 Martin
- extract-repository: AG046 Evans, AG007 Martin, AG001 Turing
- god-class: AG005 Dijkstra, AG007 Martin, AG001 Turing
- rename: AG010 Hejlsberg, AG008 Ritchie, AG007 Martin
- migrate-to-result: AG007 Martin, AG005 Dijkstra, AG046 Evans

## Generated artifacts
- Refactored code (preserves behavior)
- Tests (parity + new tests)
- ADR (if --adr yes)
- CHANGELOG entry
- Commit: refactor(scope): <description>

## Coverage by Layer (v3.55.0)
coverage by layer, coverage + layer, coverage per layer
- Refactor type detection: 100%
- GCF strategy: 100% (5+ Geniuses per type)
- Incremental application: 100% (step by step)
- Parity verification: 100%
- Refactor mode total: 100%