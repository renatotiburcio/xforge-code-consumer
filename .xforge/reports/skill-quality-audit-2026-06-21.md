# Skill Quality Audit (v50.0.1, 2026-06-21)

## Summary

| Metric | Count |
|---|---:|
| Total skills | 171 |
| Missing SKILL.md | 0 |
| Missing description field | 0 |
| Skills with <50 lines | **54** (32%) |
| Skills with <30 lines | **7** |

## Top 20 Shortest Skills (debt reduction priority)

| Skill | Lines | Notes |
|---|---:|---|
| accounting-business-expert | 26 | stub-like |
| business-platform-architect | 26 | stub-like |
| commercial-business-expert | 26 | stub-like |
| competitive-intelligence-expert | 26 | stub-like |
| curated-operational-knowledge-expert | 29 | stub-like |
| endpoints-cqrs-dtos-architecture-expert | 29 | stub-like |
| blazor-tailwind | 34 | thin |
| automapper-standard | 35 | thin |
| devops-ci-cd-expert | 35 | thin |
| api-integration-expert | 36 | thin |
| automapper-mapping-expert | 36 | thin |
| business-analysis-expert | 36 | thin |
| database-efcore-expert | 36 | thin |
| architecture-enterprise-expert | 37 | thin |
| blazor-enterprise-expert | 40 | thin |
| brazil-software-market-intelligence-expert | 40 | thin |
| csharp-clean-code-expert | 40 | thin |
| dotnet-standards | 45 | thin |
| ecosystem-consolidation | 48 | thin |
| cost-management | 49 | thin |

## Observations

1. **Many skills are <50 lines** — likely just frontmatter + 1-2 paragraphs. Real content lives in the dedicated knowledge packs (fiscal, contabil, etc) instead.

2. **The 26-line stubs are mostly business expert skills** — these likely need real content (they were mass-created in v3.38+).

3. **All 171 skills have proper frontmatter** — no schema violations.

4. **No empty descriptions** — discoverability is fine.

## Recommendation

Three priority buckets for debt reduction:

1. **Quick wins (7 skills, <30 lines)**: Add 30-50 lines of practical guidance to each. ~1h total.
2. **Medium effort (47 skills, 30-49 lines)**: Audit each for whether the brief is sufficient or needs expansion. ~3h batch.
3. **Strategic review**: Identify the 10 most-used skills and invest in deeper content.

## Next Step

T045: B-026 (deep-request-analyzer) — high-leverage skill for the LDV. Multi-hour but high value.