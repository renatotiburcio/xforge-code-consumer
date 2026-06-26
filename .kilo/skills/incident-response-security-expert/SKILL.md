---
name: incident-response-security-expert
description: Expert em resposta a incidentes de segurança: triagem, contenção, erradicação, recuperação e lições aprendidas.
metadata:
  version: "37.0.0"
  xforge-category: "continuous-security"
---

# incident-response-security-expert

## Objetivo

Responder a incidentes de segurança de forma estruturada e reproduzível.

## Fases de Resposta

### 1. Triagem (0-15 min)
- Classificar: data breach / DoS / unauthorized access / malware
- Severidade: P1 (crítico) a P4 (baixo)
- Identificar sistemas afetados
- Notificar equipe de segurança

### 2. Contenção (15-60 min)
- Isolar sistemas comprometidos
- Revogar credenciais suspectas
- Bloquear IPs/usuarios maliciosos
- Preservar evidências (logs, snapshots)

### 3. Erradicação (1-24h)
- Identificar root cause
- Remover malware/backdoor
- Corrigir vulnerabilidade
- Atualizar patches

### 4. Recuperação (24-72h)
- Restaurar de backup limpo
- Verificar integridade
- Monitorar comportamento
- Validar normalidade

### 5. Lições Aprendidas
- Post-mortem em 48h
- Documentar timeline
- Identificar gaps de processo
- Atualizar playbooks

## Procedimento

1. Receber alerta de incidente
2. Classificar e escalonar
3. Executar fase correspondente
4. Documentar cada ação com timestamp
5. Reportar status a cada 30min (P1) ou 2h (P2)
6. Criar post-mortem após resolução

## Saída

```json
{
  "incident": "INC-2024-001",
  "severity": "P2",
  "type": "unauthorized-access",
  "timeline": [],
  "rootCause": "...",
  "resolution": "...",
  "lessonsLearned": []
}
```
