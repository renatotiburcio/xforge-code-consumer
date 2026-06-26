---
name: strategic-roadmap
description: Use when creating, updating, or analyzing project roadmaps, milestones, or strategic planning.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# strategic-roadmap

## Objetivo

Criar e manter roadmap estratégico do projeto.

## Estrutura do Roadmap

### Horizontes

| Horizonte | Prazo | Foco |
|-----------|-------|------|
| **Curto** | 1-4 semanas | Features atuais, bugs críticos |
| **Médio** | 1-3 meses | Novas capacidades, refactor |
| **Longo** | 3-12 meses | Arquitetura, escala, novos mercados |

### Formato

```markdown
## Roadmap Q1 2024

### Curto Prazo (Sprint 1-4)
- [ ] Feature X (prioridade: alta)
- [ ] Bug Y fix (prioridade: crítica)

### Médio Prazo (Mês 2-3)
- [ ] Refactor módulo Z
- [ ] Migração de banco

### Longo Prazo (Q2-Q4)
- [ ] Microserviços (se necessário)
- [ ] Multi-tenancy
```

## Procedimento

1. Coletar demandas (product, tech, security)
2. Priorizar por impacto x esforço
3. Estimar timeline
4. Alocar recursos
5. Definir milestones
6. Revisar semanalmente

## Regras

- Roadmax 10 itens por horizonte
- Sempre incluir tech debt
- Sempre incluir security improvements
- Revisar a cada 2 semanas
