# Fullstack Analysis Rules

## Proposito
Padronizar a analise e documentacao de sistemas fullstack para que qualquer agente implemente sem ambiguidade.

## 12 Mandamentos

1. Sempre criar 00-brief.md antes de qualquer doc
2. Sempre numerar RF, RNF, RN, US com IDs estaveis
3. Sempre incluir exemplo concreto por secao
4. Sempre usar C4 (L1, L2, L3) para arquitetura
5. Sempre OpenAPI 3.1 com exemplos por endpoint
6. Sempre wireframe textual + fluxo Mermaid para UI
7. Sempre diagrama de sequencia para fluxos criticos
8. Sempre threat model basico (STRIDE) para features com dados
9. Sempre plano de rollback explicito
10. Sempre estrategia de testes (unit, integration, e2e, contract)
11. Nunca entregar doc com TODO no output final
12. Nunca usar termos vagos (rapido, grande) sem metrica

## Estrutura Obrigatoria

```
.xforge/analysis/{feature}/
  00-brief.md
  01-requirements.md
  02-architecture.md
  03-data-model.md
  04-api-contract.yaml
  05-ui-flows.md
  06-sdd.md
  07-diagrams/
  08-gap-report.md
  09-code-map.md
  10-handoff-checklist.md
```

## Quality Gate

Apos criar, validar:
- [ ] 11 arquivos presentes
- [ ] Clarity score >= 80
- [ ] Zero TODO em output
- [ ] 100% dos RFs com exemplo
- [ ] Diagrama C4 L1 renderizado
