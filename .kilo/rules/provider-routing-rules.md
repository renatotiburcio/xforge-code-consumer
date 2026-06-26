# provider-routing-rules

## Context-Based Provider Selection

### Local (128k tokens — Ollama)
- Default: ollama/llama3 (local, no token cost, 128k context)
- Fallback: ollama/local-model (any pulled model)
- Use for: simple edits, small file creation, quick fixes, most daily tasks
- Offline: always available, no API key needed

### Standard Cloud (128k-200k tokens)
- Default: openrouter/anthropic/claude-sonnet-4-20250514
- Fallback: openai/gpt-4o
- Use for: feature development, refactoring, multi-file changes, moderate complexity

### Premium Cloud (200k+ tokens)
- Default: anthropic/claude-opus-4
- Fallback: openai/gpt-4o
- Use for: architecture decisions, complex migrations, security audits, critical code

### Ultra (Max quality)
- Default: anthropic/claude-opus-4
- Fallback: openai/o1
- Use for: LGPD, fiscal, legal, multi-agent orchestration, zero-tolerance tasks

### Offline Mode
- When cloud providers unavailable: ollama/llama3 (128k context)
- Check ollama status: powershell .xforge/scripts/offline-manager.ps1 status
- Enable offline: powershell .xforge/scripts/offline-manager.ps1 enable

## Cost Optimization
- Always try local (ollama/llama3 128k) first for simple and medium tasks
- Use economy tier for tasks that do not need reasoning
- Reserve premium/cloud for complex architecture and security
- Log provider choice and estimated cost for each task
