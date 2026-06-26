---
name: trust-score
description: Use when assigning or validating confidence, source reliability, knowledge trust, decay score, or promotion readiness.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# trust-score

## Objetivo

Calcular e gerenciar o nível de confiança de conhecimento, fontes e decisões.

## Faixas de Score

| Score | Nível | Significado | Ação |
|-------|-------|-------------|------|
| 90-100 | **Verified** | Confirmado por múltiplas fontes | Promover automaticamente |
| 70-89 | **Trusted** | Fonte confiável, poucos registros | Usar com registro |
| 50-69 | **Provisional** | Precisa de mais validação | Marcar como incerto |
| 30-49 | **Unverified** | Não confirmado | Usar com cautela |
| 0-29 | **Deprecated** | Obsoleto ou contraditório | Não usar, revisitar |

## Fórmula

```
trust_score = (source_reliability * 0.3) + (recency * 0.2) + (corroboration * 0.3) + (domain_criticality * 0.2)
```

- **source_reliability** (0-100): Documentação oficial=100, Blog=60, AI-generated=40
- **recency** (0-100): Atualizado nos últimos 30 dias=100, >1 ano=20
- **corroboration** (0-100): 3+ fontes independentes=100, 1 fonte=30
- **domain_criticality** (0-100): Fiscal/Legal=100, Security=80, Feature=50

## Decay

- Score diminui 5 pontos por mês sem uso
- Score diminui 10 pontos quando contradito por nova informação
- Score é resetado quando fonte original é atualizada

## Procedimento

1. Identificar a afirmação/conhecimento
2. Avaliar fonte, data, corroboracão, criticidade
3. Calcular score
4. Se score < 50 → marcar para revisão
5. Se score > 80 → candidato a promoção
6. Registrar no knowledge graph
