---
name: support-playbook
description: Use when creating, updating, or following support playbooks for common issues and troubleshooting.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# support-playbook

## Objetivo

Documentar e seguir procedimentos de suporte para issues comuns.

## Estrutura do Playbook

```markdown
## Issue: [Nome]

### Sintomas
- [lista de sintomas observáveis]

### Causas Comuns
1. Causa A (mais provável)
2. Causa B
3. Causa C

### Diagnóstico
1. Passo para verificar causa A
2. Passo para verificar causa B

### Resolução
1. Se causa A → [ação]
2. Se causa B → [ação]

### Prevenção
- [como evitar que aconteça novamente]
```

## Playbooks Essenciais

| Issue | Prioridade |
|-------|:----------:|
| API return 500 | Alta |
| Database connection timeout | Crítica |
| Auth token expired | Média |
| Slow query performance | Alta |
| Memory leak | Crítica |

## Procedimento

1. Identificar issue recorrente
2. Documentar sintomas e causas
3. Criar passo-a-passo de resolução
4. Testar playbook com pessoa nova
5. Atualizar baseado em feedback
6. Versionar no .xforge/knowledge/

## Regras

- Playbooks devem ser testáveis
- Incluir screenshots quando útil
- Manter atualizado
- Versionar como código
