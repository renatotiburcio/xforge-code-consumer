---
name: security
description: Auditoria completa de seguranca e compliance
category: xforge-core
---

# /security

Auditoria de seguranca e compliance.

## Sintaxe

```
/security full
/security api
/security dependencies
/security data-protection
/security lgpd
/security auth
/security audit
/security ci-cd
/security release
```

## Sub-comandos

| Sub-comando | Descricao | Substitui |
|-------------|-----------|-----------|
| full | Auditoria completa | security-audit |
| api | Verificacao de APIs | security-api-check |
| dependencies | Verificacao de dependencias | security-dependencies-check |
| data-protection | Protecao de dados | security-data-protection-check |
| lgpd | Compliance LGPD | security-lgpd-check |
| auth | Verificacao de autenticacao | security-auth-check, security-authorization-check |
| auditoria | Auditoria de logs | security-logs-audit-check |
| ci-cd | Verificacao CI/CD | security-ci-cd-check |
| release | Gate de release | security-release-gate |
| backup | Backup e restore | security-backup-restore-check |
| golden-rule | Regras douradas | security-golden-rule-check |
