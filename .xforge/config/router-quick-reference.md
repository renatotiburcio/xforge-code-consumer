# Router Quick Reference — XForge Split Architecture

## Hardware Profile
- GPU: 16GB VRAM (NVIDIA)
- RAM: 32GB DDR4
- CPU: AMD Ryzen 7 5700G (8C/16T, Zen 3, AVX2/FMA3)

## Model Routing Table

| Task Type | Router Decision | Model | Context | Latency |
|-----------|----------------|-------|---------|---------|
| Quick question | S complexity | qwen2.5:7b (router itself) | 8k | <2s |
| Small code edit | S complexity | qwen2.5:7b | 8k | <2s |
| Documentation | M complexity | qwen2.5:14b | 16k | 3-8s |
| Feature development | L complexity | qwen2.5:72b | 32k | 10-30s |
| Architecture design | XL complexity | qwen2.5:72b | 32k | 15-30s |
| Security audit | XL complexity | qwen2.5:72b | 32k | 15-30s |
| Code review | L complexity | qwen2.5:72b | 32k | 10-25s |
| Bug fix | M complexity | qwen2.5:14b | 16k | 3-10s |
| Refactoring | L complexity | qwen2.5:72b | 32k | 10-30s |
| Brazilian fiscal | XL complexity | qwen2.5:72b | 32k | 15-30s |
| Payroll calc | L complexity | qwen2.5:72b | 32k | 10-25s |
| RAG/embedding | n/a | nomic-embed-text | 8k | <1s |

## Intent Classification Keywords

### Code Generation
Keywords: implement, create, add, write, build, generate, scaffold
→ Worker (qwen2.5:72b)

### Debugging
Keywords: fix, bug, error, crash, broken, failing, issue
→ Fallback (qwen2.5:14b) or Worker if complex

### Architecture
Keywords: design, architecture, pattern, structure, refactor, clean, DDD
→ Worker (qwen2.5:72b)

### Documentation
Keywords: document, explain, describe, readme, comment, doc
→ Fallback (qwen2.5:14b)

### Testing
Keywords: test, unit, integration, BDD, scenario, assert
→ Fallback (qwen2.5:14b)

### Security
Keywords: security, OWASP, LGPD, vulnerability, audit, auth, encrypt
→ Worker (qwen2.5:72b) — ALWAYS

### Brazilian Compliance
Keywords: INSS, IRRF, FGTS, eSocial, SPED, ICMS, PIS, COFINS, DCTF
→ Worker (qwen2.5:72b) — ALWAYS

### Knowledge Query
Keywords: what is, how does, explain, tell me about
→ Router itself (qwen2.5:7b) — fast answer

## Context Budget Rules

1. **Default**: 32k tokens (optimal for CPU inference)
2. **Router**: 8k tokens (only needs intent classification)
3. **Worker**: 32k tokens (full capability)
4. **Eviction**: Automatic at 80%/90%/95%/98%

## Knowledge Loading Protocol

1. Search INDEX.json by task keywords
2. Match top 2-3 files by relevance
3. Load only `summary` field from INDEX.json
4. If summary sufficient → skip full load
5. If full content needed → `Read(filePath, limit=100)`
6. Expand with offset only if more context needed

## Ollama Environment Variables

```bash
OLLAMA_NUM_PARALLEL=2          # 2 models in parallel
OLLAMA_MAX_LOADED_MODELS=2     # Keep 2 models loaded
OLLAMA_KEEP_ALIVE=24h          # Router stays loaded
OLLAMA_FLASH_ATTENTION=1       # Faster inference
OLLAMA_KV_CACHE_TYPE=q8_0      # Better quality KV cache
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Router latency | <2s |
| Worker latency (S/M) | 3-10s |
| Worker latency (L/XL) | 10-30s |
| Tokens per turn (avg) | ~12k |
| Knowledge files loaded per turn | 2-3 |
| Context overflow frequency | <5% of turns |
