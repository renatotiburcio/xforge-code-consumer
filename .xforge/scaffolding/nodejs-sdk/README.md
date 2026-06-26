# @xforge/sdk — Node.js SDK

## Install

```bash
npm install @xforge/sdk
```

## Usage

```typescript
import { XForgeClient } from '@xforge/sdk';

const client = new XForgeClient({
  projectRoot: '/path/to/project',
  provider: 'openrouter',
  model: 'anthropic/claude-sonnet-4-20250514'
});

// Run doctor
const result = await client.doctor();
console.log(`Errors: ${result.errors}, Warnings: ${result.warnings}`);

// Query RAG
const docs = await client.queryRag('architecture decisions', 5);

// List agents
const agents = await client.listAgents('primary');
```

## Status

Scaffolding — API defined, implementation pending.
