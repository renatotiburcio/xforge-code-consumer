---
id: knowledge-compliance-audit-trail
type: knowledge
title: Trilha de Auditoria LGPD (Audit Trail)
category: compliance
domain: compliance
trustScore: 85
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [lgpd, audit, compliance, log, immutable]
---

# Trilha de Auditoria LGPD (Audit Trail)

## Contexto

A LGPD (Lei Geral de Protecao de Dados) exige que operacoes com dados pessoais
sejam registradas para fins de prestacao de contas (Art. 37) e demonstracao
de eficacia das medidas de seguranca (Art. 46).

## O que registrar

Para cada operacao com dado pessoal:

- **Quando**: timestamp UTC (ISO 8601, com millisegundos)
- **Quem**: identificador do operador (user ID, IP, session)
- **O que**: tipo de operacao (read, write, delete, export, anonymize)
- **Onde**: tabela + campo + chave do registro
- **Base legal**: consentimento, contrato, obrigacao legal, etc.
- **Retencao**: prazo de retencao conforme politica

## Implementacao no XForge

Camada transversal com 3 niveis:

1. **Application level**: log estruturado Serilog + correlation ID
2. **Database level**: trigger PostgreSQL que grava em `audit_log` immutable
3. **Storage level**: append-only WORM (Write Once Read Many) com hash chain

## Schema minimo

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_id VARCHAR(64) NOT NULL,
    actor_ip INET,
    operation VARCHAR(32) NOT NULL,
    table_name VARCHAR(64) NOT NULL,
    record_id VARCHAR(64) NOT NULL,
    field_name VARCHAR(64),
    old_value_hash VARCHAR(64),
    new_value_hash VARCHAR(64),
    legal_basis VARCHAR(32) NOT NULL,
    correlation_id UUID NOT NULL,
    prev_hash VARCHAR(64),
    row_hash VARCHAR(64) NOT NULL
);
CREATE INDEX idx_audit_actor ON audit_log(actor_id, occurred_at DESC);
CREATE INDEX idx_audit_record ON audit_log(table_name, record_id, occurred_at DESC);
```

## Hash Chain (imutabilidade)

Cada registro inclui `prev_hash` (hash do registro anterior) e `row_hash`
(hash do registro atual incluindo `prev_hash`). Qualquer alteracao invalida
a cadeia. Verificacao periodica via job noturno.

## Retencao

| Tipo de dado | Retencao | Justificativa |
|--------------|----------|---------------|
| Operacoes de marketing | 5 anos | Art. 27 CDC |
| Dados de funcionarios | 30 anos | CLT + previdenciario |
| Operacoes financeiras | 10 anos | SPED + legislacao fiscal |
| Logs de acesso | 6 meses | Art. 50 LGPD |

## Referencias

- LGPD Art. 37, 46, 50
- ISO 27001 A.12.4 (Logging and monitoring)
- COBIT 2019 DSS05.06

