---
name: policy-engine
description: Use when a task must enforce enterprise policies, module policies, fiscal policies, customer policies, security constraints, or approval gates.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# policy-engine

## Objetivo

Validar que nenhuma ação viola políticas enterprise antes de executar.

## Tipos de Política

| Tipo | Escopo | Exemplo |
|------|--------|---------|
| **Enterprise** | Todo o sistema | Não usar preview packages |
| **Módulo** | Por módulo/feature | Padrões de naming |
| **Fiscal/Legal** | Dados sensíveis | LGPD, SPED, NFe |
| **Cliente** | Por tenant | Configurações custom |
| **Segurança** | Global | RBAC, auth, encryption |

## Procedimento

1. Identificar políticas aplicáveis à tarefa
2. Ler políticas relevantes em .kilo/rules/
3. Validar cada ação contra as políticas
4. Se violação → bloquear e reportar
5. Se OK → registrar aprovação no audit trail
6. Para políticas fiscais/legais → exigir validação humana

## Bloqueios Automáticos

- Pacote preview/alpha/beta → BLOQUEADO
- Dados LGPD sem criptografia → BLOQUEADO
- Modificação de governance sem aprovação → BLOQUEADO
- Release com testes falhando → BLOQUEADO
- Hardcoded secrets → BLOQUEADO

## Saída

```json
{
  "policiesChecked": ["enterprise", "security", "fiscal"],
  "violations": [],
  "approved": true,
  "approver": "system|human",
  "timestamp": "ISO-8601"
}
```
