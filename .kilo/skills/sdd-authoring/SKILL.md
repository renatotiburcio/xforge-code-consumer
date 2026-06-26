---
name: sdd-authoring
version: 1.0.0
trust: 92
type: skill
domain: sdd
description: Template canonico de SDD (12 secoes) + checklist de qualidade
---

# Skill: SDD Authoring

## Template canonico (12 secoes)
1. Metadata
2. Context
3. Personas & Cenarios
4. Requisitos (RF/RNF/RN)
5. Arquitetura (C4)
6. Modelo de Dados
7. API Contract
8. UI/UX
9. Testes
10. Observabilidade
11. Seguranca & LGPD
12. Plano de Entrega

## Checklist de qualidade
- [ ] Cada RF tem criterio de aceite mensuravel
- [ ] Cada RNF tem metrica (p95, SLA, etc)
- [ ] C4 L1 + L2 + L3 presentes
- [ ] ER com cardinalidade
- [ ] OpenAPI 3.1 com exemplos
- [ ] Wireframes com estados (loading/empty/error)
- [ ] Fluxograma de UX
- [ ] Estrategia de testes (unit/integration/e2e)
- [ ] Logs, metricas, traces definidos
- [ ] Threat model basico
- [ ] Plano de rollback

## Regra
- Sem TODO no output final
- Toda secao tem exemplo concreto
- Toda decisao tem tradeoff
