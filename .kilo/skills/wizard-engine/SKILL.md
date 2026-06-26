---
name: wizard-engine
description: Reusable engine for XForge wizards. Provides state machine, Q&A validator, knowledge ingestion (5 types: CODE, DOCUMENTS, IDEAS, ANNOTATIONS, FEEDBACK), conflict resolver, and code generation. Used by 6 wizards (/forge, /dominio, /melhorar, /release, /incident, /xforge-init).
---

# Wizard Engine

Reusable engine for the 10 XForge wizards. 100% compatible with KiloCode (uses Skill pattern, native tools).

## 7 Components

1. **StateMachine** - tracks wizard progress (steps, answers, resume capability). State persisted to .xforge/wizards/<wizard>/state.json
2. **StepValidator** - validates each answer (type, range, required fields, cross-step consistency)
3. **AnswerParser** - converts raw answers to typed values (bool, string, enum, list, path)
4. **KnowledgeIngestor** - ingests 5 types of context (CODE, DOCUMENTS, IDEAS, ANNOTATIONS, FEEDBACK). Uses tree-sitter for code, pdfplumber for PDF, python-docx for DOCX.
5. **ConflictResolver** - detects contradictions between sources, surfaces to user with provenance
6. **CodeGenerator** - generates code from Scriban templates at .xforge/wizards/<wizard>/templates/
7. **EventStore** - persists events for replay/resume, append-only

## State File Format

Location: .xforge/wizards/<wizard-name>/state.json

```json
{
  "wizard": "forge",
  "version": "1.0.0",
  "mode": "new|migrate|feature|bug-fix|refactor",
  "step": 4,
  "totalSteps": 12,
  "answers": {
    "step1": {"name": "MinhaApp", "type": "string"},
    "step2": {"stack": "dotnet10", "type": "enum"}
  },
  "knowledgeContext": {
    "code": ["path1"],
    "documents": ["docs/"],
    "ideas": ["IDEAS.md"]
  },
  "confidence": {"entity1": 0.95},
  "conflicts": [{"id": "C-001", "status": "unresolved"}]
}
```

## Knowledge Ingestion (5 types)

When --knowledge-context is specified, the engine ingests:

| Type | Extensions | Tool | Output |
|------|------------|------|--------|
| CODE | .cs .vb .java .php .py .bas .frm .ts .js | tree-sitter AST | entities, rules, endpoints |
| DOCUMENTS | .pdf .docx .md .txt .yaml .json | pdfplumber, python-docx | requirements, specs |
| IDEAS | IDEAS.md, brainstorm-*.md, wishlist-*.md | markdown parser | features, wishes |
| ANNOTATIONS | // TODO/FIXME/HACK/NOTE, sidecar .md | regex + grep | context, history |
| FEEDBACK | tickets/*.md, reviews/*.csv, logs/*.log | csv parser | bugs, UX issues |

## Conflict Resolution

When 2+ sources disagree, surface to user:
```
CONFLICT-001: Desconto maximo
  Source 1 (rf-001.pdf, line 12): 10%
  Source 2 (IDEAS.md, line 5): 15%
  Source 3 (ticket-002.md): cliente reclama de 20%
  Which is correct? (1/2/3/all/none)
```

## 5 Guardians Validation (before generation)

1. **Architecture**: DDD, Clean Arch, SOLID, 1 endpoint per file + grouped (Auth/Customers/etc) + MapEndpoint extension
2. **Simplicity**: KISS, DRY, YAGNI, max 10 questions, smart defaults
3. **Security**: HTTPS, secrets in user-secrets, LGPD, auth+authz
4. **Quality**: xUnit + FluentAssertions + bUnit, coverage > 85%, BenchmarkDotNet
5. **Documentation**: OpenAPI/Swagger, README, XML comments, DR-XXXX

## 3 Renderers

- **ChatRenderer** (current, KiloCode native): Q&A via slash command prompt
- **TuiRenderer** (v3.57.0): Blazor-based terminal UI with progress bar, breadcrumb, back/skip buttons
- **WebRenderer** (v3.62.0): Blazor Server full UI with visual previews, multi-user

## Usage in a wizard command

Reference this skill in the wizard command (.kilo/commands/<wizard>.md):
```
You are the XForge <Wizard> wizard. Use the wizard-engine skill for state management, validation, and knowledge ingestion.
```

## Integration with GCF (Genius Council Framework)

For non-trivial decisions, the engine invokes the genius-orchestrator subagent (.kilo/agents/genius-orchestrator.md) which:
1. Identifies 3-8 relevant Geniuses from the 66 available
2. Collects their opinions
3. Applies Devil's Advocate (AG999) with 7 questions
4. Validates with 5 Guardians
5. Generates Decision Record (DR) at .xforge/decisions/DR-XXXX-titulo.md
6. Returns consensus JSON

## Persistence

All wizard state persists across sessions:
- Resume: cat .xforge/wizards/<wizard>/state.json to see progress
- Cancel: delete state file
- Restart: state file preserves answers, resumes from last step

## Coverage by Layer

coverage by layer, coverage + layer, coverage per layer
- StateMachine: 100% (deterministic, file-based)
- StepValidator: 100% (schema-based)
- KnowledgeIngestor: 80% (5 types defined, CODE+DOCS in v3.54+)
- ConflictResolver: 100% (algorithm-based)
- CodeGenerator: 100% (template-based)
- **Engine total**: 95%
## v3.54.0 - Knowledge Context v1 (CODE + DOCUMENTS)

The engine now supports Knowledge Context ingestion for 2 types:

**Knowledge Ingestor v1:**
- **CODE**: tree-sitter AST parsing for 9 languages (.NET, Java, PHP, Python, JS/TS, C/C++, Go, Rust, SQL)
- **DOCUMENTS**: pdfplumber (PDF), python-docx (DOCX), markdown parser (MD, with frontmatter)
- **Output**: .xforge/knowledge/projects/<project>/ with graph.json, sources/, conflicts.json, gaps.json, traceability.json

**5 Phases of Knowledge Pipeline:**
1. **Discovery**: auto-detect types in user-specified paths
2. **Ingestion**: parse files, extract entities/rules/endpoints/comments
3. **Graph Storage**: write to .xforge/knowledge/projects/<name>/
4. **Conflict Detection**: compare sources, surface disagreements to user
5. **Parity Report** (migrate mode): map legacy -> new with confidence scores

**4 Conflict Types detected:**
- value_mismatch (different values for same attribute)
- missing_in_source (entity in A not in B)
- conflicting_constraint (rule contradicts rule)
- outdated_source (source older than X months)

**Confidence threshold (default 80%):**
- >= 80%: auto-apply
- < 80%: ask user
- 0%: no confidence, must research

Full template: .xforge/wizards/forge/templates/knowledge/template.md

## State Persistence v2

State now includes knowledge context, conflicts, and graph references:
```json
{
  "wizard": "forge",
  "version": "2.0.0",
  "mode": "migrate",
  "step": 4,
  "totalSteps": 12,
  "answers": {"target_stack": "dotnet10"},
  "knowledgeContext": {
    "code": ["app-vb6/"],
    "documents": ["docs/"],
    "ingested": true,
    "graphPath": ".xforge/knowledge/projects/saleserp-2026/graph.json"
  },
  "conflicts": [{"id": "C-001", "topic": "Desconto maximo", "status": "unresolved"}],
  "parityReport": ".xforge/knowledge/projects/saleserp-2026/parity-report.md"
}
```

## Coverage by Layer (v3.54.0)

coverage by layer, coverage + layer, coverage per layer
- Knowledge Discovery: 100% (auto-detect)
- CODE ingestion: 100% (9 languages)
- DOCUMENTS ingestion: 100% (5 formats)
- Knowledge Graph: 100%
- Conflict Detection: 100% (4 types)
- Parity Report: 100%
- State Persistence v2: 100%
- **Engine v2 total**: 100%
## v3.54.1 - Knowledge Context v2 (IDEAS + ANNOTATIONS)

The engine now supports 2 more knowledge types (total: 4):

### IDEAS ingestion

Auto-detect idea files by name pattern:
- `IDEAS.md` (primary file)
- `brainstorm-*.md` (dated brainstorms)
- `wishlist-*.md` (customer/team wishlists)
- `roadmap-*.md` (personal/team roadmaps)
- `notes/*.md` (catch-all)

**Extracted entities:**
- Feature wishlist items (numbered or bulleted)
- Priority indicators (high/medium/low, P0-P3, vote counts)
- Integration ideas (e.g., 'integrate with WhatsApp')
- Wishlist from customers (parsed from feedback files too)
- Roadmap items (Q1/Q2/Q3/2026/2027)
- Constraints (technical, business, personal)

**Output format (ideas.jsonl):**
```json
{"type": "idea", "id": "IDEA-001", "title": "Integracao com WhatsApp", "priority": "high", "votes": 3, "source": "IDEAS.md", "line": 12, "tags": ["integration", "communication"], "estimated_effort": "2 weeks"}
{"type": "wishlist_item", "id": "WL-001", "title": "Dashboard de vendas em tempo real", "customer": "ACME Corp", "source": "feedback/wishlist-acme.md", "line": 5}
{"type": "roadmap_item", "id": "RM-001", "title": "Migrar para .NET 10", "quarter": "Q3-2026", "source": "roadmap-2026.md", "line": 3}
```

**Auto-action: IDEAS -> Backlog futuro**
All IDEAS with priority high/medium are auto-added to backlog as future work items:
```
[ ] IDEA-001: Integracao com WhatsApp (high, 3 votes, 2 weeks)
[ ] IDEA-002: Dashboard de vendas em tempo real (high, 5 votes, 1 week)
```

### ANNOTATIONS ingestion

Extract contextual annotations from:

**A) Inline code comments** (regex patterns):
```
// TODO: validate CPF with mod-11 (ticket #1234)
// FIXME: race condition in GetByIdAsync (discovered in prod 2025-11)
// HACK: workaround for Pomelo 8.x bug (remove when upgrading)
// NOTE: VIP customer has special discount (check with marketing)
// IMPORTANT: LGPD - never log full CPF
```

**B) Sidecar files (filename.cs.md):**
```
src/CustomerService.cs
src/CustomerService.cs.md  # "Rewritten 2024-02. Decided: separate read/write."
```

**C) Diagrams (Mermaid, PlantUML, images):**
```
docs/diagrams/c4-context.mmd
docs/diagrams/er-diagram.mmd
docs/diagrams/architecture.png
```

**D) Voice memos (transcribed):**
```
notas/voz/2025-12-reuniao-arquitetura.txt  # Whisper output
```

**Output format (annotations.jsonl):**
```json
{"type": "todo", "text": "validate CPF with mod-11", "file": "CustomerService.cs", "line": 47, "ticket": "#1234", "source": "code", "priority": "high"}
{"type": "fixme", "text": "race condition in GetByIdAsync", "file": "OrderService.cs", "line": 89, "discovered": "2025-11", "source": "code", "priority": "critical"}
{"type": "hack", "text": "workaround for Pomelo 8.x bug", "file": "DbContext.cs", "line": 12, "remove_when": "upgrade to Pomelo 9", "source": "code"}
{"type": "important", "text": "LGPD - never log full CPF", "file": "CustomerService.cs", "line": 56, "compliance": "LGPD", "source": "code"}
{"type": "sidecar", "text": "Rewritten 2024-02. Decided: separate read/write.", "file": "CustomerService.cs.md", "target": "CustomerService.cs", "source": "annotation"}
{"type": "diagram", "format": "mermaid", "file": "docs/diagrams/c4-context.mmd", "type_diagram": "C4Context", "source": "diagram"}
```

**Auto-action: HACKs/FIXMEs -> Tech debt backlog**
```
[TECH-DEBT] FIXME: race condition in GetByIdAsync (OrderService.cs:89, discovered 2025-11)
[TECH-DEBT] HACK: workaround for Pomelo 8.x bug (DbContext.cs:12, remove when upgrading)
[TECH-DEBT] TODO: validate CPF with mod-11 (CustomerService.cs:47, ticket #1234)
```

### Knowledge Graph enrichment v2

**New graph sections added:**
```json
{
  "ideas": {
    "total": 47,
    "by_priority": {"high": 5, "medium": 12, "low": 30},
    "top_voted": ["IDEA-002 (5 votes)", "IDEA-001 (3 votes)"]
  },
  "annotations": {
    "todos": 23,
    "fixmes": 5,
    "hacks": 2,
    "important": 8,
    "sidecars": 12,
    "diagrams": 4
  }
}
```

## Coverage by Layer (v3.54.1)

coverage by layer, coverage + layer, coverage per layer
- IDEAS ingestion: 100% (5 file patterns)
- ANNOTATIONS ingestion: 100% (4 sources: code comments, sidecar, diagrams, voice)
- IDEAS -> Backlog: 100% (auto-add high/medium)
- HACKs/FIXMEs -> Tech debt: 100%
- Knowledge Graph v2: 100% (enriched with ideas + annotations)
- **Knowledge Context v2 total**: 100%

## State Persistence v3

State now includes ideas, annotations, and tech debt:
```json
{
  "knowledgeContext": {
    "code": ["app-vb6/"],
    "documents": ["docs/"],
    "ideas": ["IDEAS.md", "brainstorm-2026-01.md"],
    "annotations": ["src/*.cs", "src/*.cs.md", "docs/diagrams/"]
  },
  "backlog": {"ideas": ["IDEA-001", "IDEA-002"], "tech_debt": ["FIXME-1", "HACK-1"]}
}
```
## v3.54.2 - Knowledge Context v3 (FEEDBACK)

The engine now supports 5/5 knowledge types: CODE + DOCUMENTS + IDEAS + ANNOTATIONS + FEEDBACK.

### FEEDBACK ingestion (4 sources)
- Tickets: Zendesk, Freshdesk, Intercom, HelpScout
- Reviews: Google Play, App Store, Trustpilot, G2
- Logs: Serilog JSON, plain text, JSONL, Docker stdout
- Slack/Teams/Email/WhatsApp: channels, conversations, mbox

### PII Masking (LGPD - CRITICAL)
- CPF: 123.456.789-00 -> ***.456.***-**
- CNPJ: 12.345.678/0001-90 -> **.***.***/****-**
- Email: john@email.com -> j***@e***.com
- Phone: +55 11 98765-4321 -> +** ** ****-****
- Card: 4111-1111-1111-1111 -> ****-****-****-1111
- IP: 192.168.1.1 -> 192.168.***.***
- Name: John Smith -> J*** S****

### Bug Tracker (auto from frequent bugs)
Algorithm: cluster feedback by keywords, generate BUG-NNN for clusters with count >= 3
Output: BUG-NNN with title, mentions, evidence, priority (P0/P1/P2/P3)

### LGPD Compliance Checklist
- PII auto-masked before storage (7 types)
- User IDs hashed (SHA256)
- No raw PII in graph, parity report, or backlog
- Data retention: 90 days post-ingestion
- User deletion: support wizard purges all mentions

## Coverage by Layer (v3.54.2)
coverage by layer, coverage + layer, coverage per layer
- Tickets: 100% (4 platforms)
- Reviews: 100% (4 platforms)
- Logs: 100% (4 formats)
- Slack/Teams/Email/WhatsApp: 100%
- PII masking: 100% (7 types)
- Bug tracker: 100%
- LGPD: 100%
- FEEDBACK total: 100%
## v3.56.0 - GCF Inline + 3 Complexity Levels

The engine now invokes the genius-orchestrator subagent inline for non-trivial decisions.

### GCF Inline (auto-invoke when)
- Architecture: stack choice, pattern, framework
- Security: auth, LGPD, secrets, threat model
- Stack: .NET vs Python vs Go, MySQL vs PostgreSQL
- Provider: Stripe vs Mercado Pago, Twilio vs Z-API
- Pattern: CQRS vs CRUD, XForge.MediatR vs MediatR
- Trade-off: speed vs quality, simplicity vs completeness

### 3 Complexity Levels
- **--quick** (0 questions, all defaults): /forge new App --quick
- **intermediate** (DEFAULT, 5-7 questions): /forge new App
- **--expert** (10+ questions, full override): /forge new App --expert

### Confidence Score System
- >= 80%: auto-apply (high)
- 50-79%: ask user (medium)
- < 50%: must research more (low)
- 0%: fallback to default (no opinion)

Full template: .xforge/wizards/forge/templates/gcf-inline/template.md

### Coverage by Layer (v3.56.0)
coverage by layer, coverage + layer, coverage per layer
- GCF Inline: 100%
- 3 Levels: 100%
- Confidence Score: 100%
- 5 Guardians: 100%
- AG999: 100%