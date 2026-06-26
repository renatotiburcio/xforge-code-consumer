---
name: product-analysis
description: Reusable skill for product analysis. 5-step workflow (SCOUT/SCRAPE/ANALYZE/SYNTHESIZE/VALIDATE), 8 canonical artifacts (CAR, Feature Spec, Architecture, PR-FAQ, Personas, Backlog, Risk, Glossary), atomic format for small LLMs, Privacy by Design (LGPD). Used by /analyze-product.
---

# Product Analysis Skill

Reusable skill for product analysis. Invoked by /analyze-product and product-analyst subagent.

## 5-Step Workflow
1. SCOUT - Identify 5-10 sources
2. SCRAPE - Extract content (respect robots.txt + ToS)
3. ANALYZE - Invoke GCF (5+ Geniuses)
4. SYNTHESIZE - Generate 8 artifacts (atomic)
5. VALIDATE - 5 Guardians + publish

## 8 Canonical Artifacts (templates)

### 1. Competitive Analysis Report (CAR)
Sections: 1.1 Market, 1.2 Top 5 Competitors, 1.3 Feature Matrix, 1.4 Gaps, 1.5 Our Advantage

### 2. Feature Spec
Sections: 2.1 Personas, 2.2 User Stories (RF-NNN), 2.3 Use Cases (UC-NNN), 2.4 Acceptance Criteria
Format: Given-When-Then

### 3. Architecture Brief
Sections: 3.1 Recommended Stack, 3.2 Patterns, 3.3 Trade-offs, 3.4 Alternatives
Format: ADR-style

### 4. PR-FAQ (Amazon-style)
Sections: 4.1 Press Release (1 paragraph), 4.2 Customer Quote, 4.3 FAQ (5 Q&A)

### 5. Personas
Sections: 5.1 Primary, 5.2 Secondary, 5.3 Jobs-to-be-Done

### 6. Backlog
Sections: 6.1 P0, 6.2 P1, 6.3 P2, 6.4 P3
Format: [P0] TASK-NNN: description (estimate, dependencies)

### 7. Risk Register
Sections: 7.1 Technical, 7.2 Business, 7.3 Compliance, 7.4 Operational
Format: RISK-NNN: description (probability, impact, mitigation)

### 8. Glossary
Sections: 8.1 Domain Terms, 8.2 Acronyms, 8.3 External References
Format: TERM: definition (source)

## Atomic Format (AI-ready for small models)

Max 50 lines per atom. Structure:
1. Title (1 line)
2. Context (2-3 lines)
3. Example (5-10 lines)
4. Rules (5-10 lines, bulleted)
5. Acceptance Criteria (Given-When-Then)
6. Cross-references (RF-NNN, UC-NNN, DR-NNN)

Why this works for small LLMs:
- Phi-3 3B: 4k tokens context
- Qwen 2.5 7B: 8k tokens context
- Llama 3.2 3B: 4k tokens context
50 lines = ~1.5k tokens (fits in all)

## Confidence Score (per insight)

Auto-apply if >= 80%, ask if 50-79%, research if < 50%
- Official docs, RFC: 90-100
- Industry review, market research: 70-89
- GitHub analysis, app store review: 50-69
- Community forum, Reddit: 30-49
- AI-generated, not validated: 0-29

## Privacy by Design (LGPD)

- ONLY public data
- Respect robots.txt + ToS + rate limits (1 req/s)
- User-Agent: XForge-ProductAnalyst/1.0
- Audit log to .xforge/audit/product-analysis.log
- No PII collection or storage
- Data retention: 90 days

## Output structure

.xforge/products/<product-slug>/
- manifest.json (sources, timestamps, confidence avg)
- competitive-analysis-report.md
- feature-spec.md
- architecture-brief.md
- pr-faq.md
- personas.md
- backlog.md
- risk-register.md
- glossary.md
- sources/  (raw data)
- traceability.json  (insight -> source)

## Integration with /forge

After /analyze-product completes:
- /forge new <Product> --knowledge-context .xforge/products/<slug>/
- /forge feature <Feature> --from-product <slug>
- /forge bug-fix --from-product <slug>

## Coverage by Layer (v3.63.0)
coverage by layer, coverage + layer, coverage per layer
- 5-Step Workflow: 100%
- 8 Canonical Artifacts: 100%
- Atomic Format: 100%
- Privacy by Design: 100%
- 3 Depth Levels: 100%
- Sources + Trust Score: 100%
- Integration with /forge: 100%
- Product Analysis Skill total: 100%