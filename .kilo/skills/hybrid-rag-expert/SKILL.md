---
name: hybrid-rag-expert
description: Executes local RAG retrieval and plans hybrid lexical, vector, structural and graph retrieval.
metadata:
  version: "51.0.0"
  xforge-category: "knowledge-first"
---

# hybrid-rag-expert

## Trigger

Use when the task needs project knowledge retrieval, context search, document lookup, memory lookup or knowledge gap analysis.

## Current Implementation

Local lexical RAG is implemented through:

```powershell
.\.kilo\automation\scripts\rag\index-local.ps1
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "..."
```

## Procedure

1. Check whether `.xforge/rag/indexes/lexical.json` exists.
2. If missing or stale, run `index-local.ps1`.
3. Run `query-local.ps1` with the user question.
4. Use returned file paths and line numbers as citations.
5. Separate retrieved facts from inference.
6. Report gaps when retrieval is weak.

## Future Hybrid Layers

- lexical ranking;
- vector embeddings;
- structural search;
- knowledge graph;
- runtime/incidents.

## Output

- retrieved context;
- sources;
- confidence/trust;
- gaps;
- recommended next action.

