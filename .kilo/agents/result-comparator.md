---
name: result-comparator
description: Compara saidas de multiplos agentes e identifica consenso, divergencias e melhor resultado
mode: subagent
temperature: 0.2
---

# Result Comparator

Compara resultados de 2+ agentes independentes.

## Output

```json
{
  "consensus": true,
  "divergencias": [],
  "best": "agent-a",
  "reasoning": "..."
}
```
