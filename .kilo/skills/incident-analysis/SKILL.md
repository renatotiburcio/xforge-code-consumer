---
name: incident-analysis
description: Use when analyzing production incidents, errors, failures, degraded performance, or unexpected behavior.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# incident-analysis

## Objetivo

Diagnosticar e resolver incidentes de produção de forma estruturada.

## Classificação de Severidade

| Severidade | Descrição | SLA Resposta | SLA Resolução |
|:----------:|-----------|:------------:|:-------------:|
| P1 | Sistema indisponível | 15 min | 2 horas |
| P2 | Funcionalidade crítica degradada | 30 min | 4 horas |
| P3 | Funcionalidade parcial afetada | 2 horas | 24 horas |
| P4 | Issue menor, workaround disponível | 8 horas | 72 horas |

## Procedimento (5 Whys)

1. **Identificar**: O que aconteceu? Quando? Impacto?
2. **Reproduzir**: Condições que levaram ao incidente
3. **Root Cause**: Perguntar "por quê?" 5 vezes
4. **Corrigir**: Fix imediato (hotfix) se P1/P2
5. **Prevenir**: Ações para evitar recorrência
6. **Documentar**: Post-mortem em .xforge/operations/incidents/

## Template Post-Mortem

```markdown
## Incident: [título]
- **Data**: ISO-8601
- **Severidade**: P1-P4
- **Duração**: X minutos
- **Impacto**: [descrição]
- **Root Cause**: [causa raiz]
- **Correção**: [o que foi feito]
- **Prevenção**: [ações futuras]
- **Ações**: [task list com owner e deadline]
```

## Nunca Fazer

- Deletar logs de incidentes
- Culpar indivíduos
- Pular root cause analysis
- Aplicar fix sem testar
