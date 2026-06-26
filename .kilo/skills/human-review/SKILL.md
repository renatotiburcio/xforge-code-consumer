---
name: human-review
description: Use when a task requires human approval before proceeding, when confidence is low, or when changes affect production systems.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# human-review

## Objetivo

Garantir revisão humana em pontos críticos do fluxo.

## Quando Exigir Review Humano

| Critério | Ação |
|----------|------|
| Alteração de RBAC | Sempre |
| Alteração de governance | Sempre |
| Dados LGPD expostos | Sempre |
| Migration de banco | Sempre |
| Release para produção | Sempre |
| Score de confiança < 50 | Sempre |
| Custo estimado > $5 | Avisar |
| Breaking change em API | Sempre |
| Arquitetura nova | Sempre |

## Procedimento

1. Identificar se a tarefa requer review
2. Se sim → pausar execução
3. Formatar contexto para o revisor
4. Usar `question` tool para obter aprovação
5. Registrar decisão (aprovado/rejeitado + motivo)
6. Continuar ou reverter conforme decisão

## Template de Pedido de Review

```
⏸️ REVISÃO HUMANA NECESSÁRIA

**Tarefa**: [descrição]
**Risco**: [baixo/médio/alto/crítico]
**Impacto**: [o que muda]
**Alternativas**: [opções consideradas]

Aprovar esta ação? [Sim/Não]
```

## Nunca Fazer

- Pular review em dados sensíveis
- Assumir aprovação silenciosa
- Modificar após rejeição sem nova aprovação
