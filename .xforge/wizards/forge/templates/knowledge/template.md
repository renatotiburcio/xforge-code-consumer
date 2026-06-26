# Knowledge Context Template for /forge (v3.54.0)

Ingest 2 types of knowledge context (v1: CODE + DOCUMENTS). IDEAS, ANNOTATIONS, FEEDBACK coming in v3.54.1/2.

## Phase 1: Knowledge Discovery (auto)

When --knowledge-context is specified, scan paths and detect types:

```bash
# Auto-detect everything in path
/forge new App --knowledge-context ./knowledge/

# Specify types explicitly
/forge new App --knowledge-context ./src/ --types code,documents

# Multiple paths
/forge new App --knowledge-context ./legacy/,./docs/,./IDEAS.md
```

**Output:**
```
Detectei em /path/to/knowledge/:
- CODE: 47 arquivos VB6, 1 SQL schema, 1 planilha
- DOCUMENTS: 8 PDFs, 12 DOCX, 5 MD
- Total: 74 fontes, 12.3 MB
```

## Phase 2: Ingestion Pipeline

### For CODE (multi-language)

Tools: `tree-sitter` (Python lib) for AST parsing

**Supported languages (v1):**
- .NET: .cs, .vb, .fs (C#, VB.NET, F#)
- Java: .java, .kt, .scala
- PHP: .php, .phtml
- Python: .py, .pyw
- JavaScript/TypeScript: .js, .ts, .jsx, .tsx
- C/C++: .c, .cpp, .h, .hpp
- Go: .go
- Rust: .rs
- SQL: .sql (parsed by sqlparse)

**Extracted entities:**
- Classes, interfaces, structs, records
- Methods, functions, properties
- Enums, constants, fields
- Imports, dependencies, namespaces
- Comments: // TODO, // FIXME, // HACK, // NOTE, // IMPORTANT
- Annotations/attributes: [Obsolete], [Test], [Fact], etc

**Output format (graph.jsonl):**
```json
{"type": "class", "name": "Customer", "namespace": "App.Domain", "file": "Customer.cs", "line": 12, "base": "Entity", "interfaces": ["IAggregateRoot"], "properties": [{"name": "Id", "type": "Guid"}, {"name": "Cpf", "type": "Cpf"}]}
{"type": "method", "name": "CreateOrder", "class": "OrderService", "file": "OrderService.cs", "line": 45, "params": ["CustomerId", "List<Item>"], "returns": "Result<Order>"}
{"type": "comment", "text": "TODO: validate CPF with mod-11", "file": "CustomerService.cs", "line": 78, "tag": "TODO", "ticket": "#1234"}
```

### For DOCUMENTS

Tools: `pdfplumber` (PDF), `python-docx` (DOCX), markdown parser (MD)

**Supported formats:**
- PDF (text extraction, including tables)
- DOCX (paragraphs, tables, headers)
- MD (with frontmatter parsing)
- TXT (plain text)
- OpenAPI 3.0/3.1 (YAML/JSON)

**Extracted entities:**
- Requirements (RF-001, RNF-001, US-001 patterns)
- Business rules (RN-001, regra, rule patterns)
- Use cases (UC-001, caso de uso patterns)
- Domain entities (entity, aggregate, VO patterns)
- Architecture decisions (ADR, decision patterns)
- Test cases (manual QA notes)
- Glossary terms

**Output format (graph.jsonl):**
```json
{"type": "requirement", "id": "RF-001", "title": "Cadastrar cliente", "priority": "high", "source": "docs/RF-001-clientes.pdf", "page": 2}
{"type": "rule", "id": "RN-001", "description": "CPF deve ter 11 digitos", "source": "docs/RF-001-clientes.pdf", "page": 3, "confidence": 0.95}
{"type": "use_case", "id": "UC-001", "title": "Cadastrar cliente", "actors": ["Operator"], "flow": ["1. Operator accesses /clientes/new", "2. Fills form", "3. Submits"]}
```

## Phase 3: Knowledge Graph Storage

**Location:** `.xforge/knowledge/projects/<project-name>/`

```
.xforge/knowledge/projects/saleserp-2026/
  manifest.json             # Indice do que foi ingerido
  sources/
    code/
      legacy-vb6.jsonl      # Entidades, regras extraidas
      current.jsonl
    documents/
      rf-001.pdf.jsonl
      arquitetura.md.jsonl
  graph.json                # Knowledge graph (entidades + relacoes)
  conflicts.json            # Conflitos detectados entre fontes
  gaps.json                 # Informacao faltando
  traceability.json         # Cada regra -> fonte original
```

## Phase 4: Conflict Detection

**Auto-detect when 2+ sources disagree:**

```
CONFLICT-001: Desconto maximo
  Source 1 (rf-001.pdf, line 12): 10%
  Source 2 (IDEAS.md, line 5): 15%
  Source 3 (ticket-002.md): cliente reclama 20%
  Which is correct? (1/2/3/all/none)
```

**Conflict types:**
- value_mismatch (different values for same attribute)
- missing_in_source (entity in source A not in source B)
- conflicting_constraint (rule contradicts another rule)
- outdated_source (source older than X months)

## Phase 5: Parity Report (for migrate mode)

**Output for /forge migrate:**
```
================================================================
PARITY REPORT: VB6/ASP.NET -> .NET 10 Clean Arch
================================================================
FONTES ANALISADAS
- Codigo fonte: app-vb6/ (47 arquivos, 12.3 KLOC)
- Documentos: docs/ (8 PDFs, 12 paginas)
- Schema: legado/schema.sql (12 tabelas, 8 stored procs)

RESUMO
- 34 casos de uso (32 >= 80% confianca, 2 < 80%)
- 12 entidades (12 >= 95% confianca)
- 18 regras de negocio (todas 100%)
- 47 validacoes (45 100%, 2 hipotese)
- 3 modulos (Clientes, Pedidos, Produtos)
- 2 ambiguidades criticas (QA necessario)

MAPEAMENTO DETALHADO
[MODULO: CLIENTES - 100% confianca]
Legado                          | Novo                              | Tipo
ModuloClientes.bas              | Customers/Commands/               | Logica
FormClientes.frm                | Maui/Customers/Create.razor       | UI
clientes table                  | CustomerConfiguration.cs          | DB
================================================================
```

## Coverage by Layer (v3.54.0)

coverage by layer, coverage + layer, coverage per layer
- Knowledge Discovery: 100% (auto-detect 2 types)
- CODE ingestion: 100% (9 languages via tree-sitter)
- DOCUMENTS ingestion: 100% (5 formats via pdfplumber/python-docx)
- Knowledge Graph storage: 100%
- Conflict Detection: 100% (4 conflict types)
- Parity Report: 100%
- **Knowledge Context v1 total**: 100%