---
id: auditoria-interna-anual
type: fluxo
title: Auditoria Interna Anual: Checklist de Compliance para ERP
domain: compliance
trustScore: 85
source: XForge + SOX/ISO 27001/27002
tags: [auditoria, compliance, sox]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# Auditoria Interna Anual

## Escopo

| Area | Periodicidade |
|------|---------------|
| Acesso | Trimestral |
| Mudancas | Mensal |
| Transacoes | Mensal |
| Integracoes | Trimestral |
| Dados | Mensal |
| Seguranca | Mensal |
| Compliance | Anual |

## Controle de Acesso

- Lista usuarios ativos (sem orfaos)
- Perfil RBAC adequado
- Sem admin sem justificativa
- Contas servico com senha forte + rotacao 90 dias
- MFA privilegio elevado
- Logs login 1 ano
- Alertas login suspeito
- Desligados removidos 24h
- Senha 12+ chars, 90 dias expiracao
- Revisao trimestral privilegios

## Segregacao de Funcoes (SoD)

| Perfil A | Perfil B | Conflito? |
|----------|----------|-----------|
| Criar Fornecedor | Aprovar Pagamento | SIM |
| Emitir NFe | Cancelar NFe | SIM |
| Lancar Folha | Aprovar Folha | SIM |
| Cadastrar Cliente | Aprovar Credito | SIM |

## Auditoria Transacoes

```sql
-- Lancamentos manuais fora do horario
SELECT usuario_id, COUNT(*), MIN(data), MAX(data)
FROM lancamento_contabil
WHERE tipo = 'manual' AND DATEPART(HOUR, data) NOT BETWEEN 8 AND 18
GROUP BY usuario_id HAVING COUNT(*) > 5;

-- Estornos acima de R$ 10.000
SELECT * FROM estorno WHERE valor > 10000
ORDER BY data DESC;
```

## Integridade Dados

- Backup full diario + incremental 6h
- RPO: < 6 horas
- RTO: < 4 horas
- Teste de restore trimestral
- Checksum SHA-256 criticos
- Replicacao geografica (DR site)
- Retencao 5 anos (fiscal) / 20 anos (trabalhista)
- Pseudonimizacao backup (LGPD)

## OWASP Top 10

- Injection: ORM/parametros
- Broken Authentication: MFA + lockout
- Sensitive Data: TLS 1.3 + AES-256
- XXE: desabilitar DTD
- Broken Access Control: RBAC
- Security Misconfiguration: hardening
- XSS: sanitizacao + CSP
- Insecure Deserialization: validar schema
- Vulnerable Components: SCA
- Insufficient Logging: centralizar

## LGPD Checklist

- Inventario dados pessoais
- Base legal documentada
- RIPD alto risco
- Consentimento opt-in
- 10 direitos implementados + testados
- DPO designado
- Plano resposta incidentes testado
- Retencao aplicada
- Treinamento anual
- Contratos operadores (Art. 39)

## Maturidade (CMM)

| Nivel | Score | Caracteristica |
|-------|-------|----------------|
| 1 | 0-20 | Ad-hoc |
| 2 | 21-40 | Documentado nao testado |
| 3 | 41-60 | Testado + monitored |
| 4 | 61-80 | Metricas + SLAs |
| 5 | 81-100 | Melhoria continua |

## Referencias

- ISO 27001:2022
- SOX Section 404
- LGPD Lei 13.709/2018
- COBIT 2019
- ITIL 4
