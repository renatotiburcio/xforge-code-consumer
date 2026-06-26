# Handoff Readiness Rules

## Bloqueios (NAO pode handoff)
- Clarity score < 80
- Qualquer TODO/placeholder
- C4 L1 ausente
- OpenAPI sem exemplos
- Sem plano de rollback
- Sem estrategia de testes

## Checklist Obrigatorio
- [ ] 11 arquivos gerados
- [ ] Clarity score >= 80
- [ ] Zero ambiguidades (pergunta como? respondida)
- [ ] 100% RFs com exemplo
- [ ] Diagrama C4 L1 renderizado
- [ ] OpenAPI valida (lint OK)
- [ ] Wireframes com todos os estados
- [ ] Plano de rollback explicito
- [ ] Estrategia de testes definida
- [ ] Aprovacao humana registrada

## Formato de Aprovacao

```markdown
## Handoff Approval
- Documento: sdd-{feature}.md
- Clarity score: 92/100
- Aprovador: {nome}
- Data: 2026-06-14
- Comentarios: OK, pode implementar
```

## Regra
Sem aprovacao humana, NAO handoff.
