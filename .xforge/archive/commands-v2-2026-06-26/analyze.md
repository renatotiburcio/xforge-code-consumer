---
name: analyze
description: Analise completa de codigo, arquitetura, produto ou concorrencia
category: xforge-core
---

# /analyze

Analise qualquer aspecto do projeto.

## Sintaxe

```
/analyze codigo
/analyze arquitetura
/analyze produto
/analyze concorrencia
/analyze legacy
```

## Sub-comandos

| Sub-comando | Descricao | Substitui |
|-------------|-----------|-----------|
| codigo | Analise de codigo, qualidade, gaps | analyze-project, development-recognize-project |
| arquitetura | Analise arquitetural, DDD, modulos | analyze-legacy-apps |
| produto | Analise de produto, ROI, priorizacao | analyze-product |
| concorrencia | Analise competitiva | analyze-competitor-*, analyze-competitor-hybrid |
| legacy | Analise de sistemas legados | analyze-legacy-apps |
| impact | Analise de impacto de mudancas | analyze-impact |
