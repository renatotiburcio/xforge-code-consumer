---
id: lgpd-cookies-rastreamento
type: compliance
title: LGPD Cookies e Rastreamento: Conformidade em Websites e Apps
domain: compliance
trustScore: 85
source: LGPD Art. 7-9 + ANPD Orientacoes 02/2022
tags: [lgpd, cookies, rastreamento]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# LGPD Cookies e Rastreamento

## Classificacao de Cookies

| Tipo | Consentimento | LGPD |
|------|---------------|------|
| Essenciais | NAO | Art. 7 II |
| Funcionais | SIM | Art. 7 I |
| Analiticos | SIM | Art. 7 I |
| Publicidade | SIM | Art. 7 I + opt-in |

## Banner de Consentimento (requisitos)

1. Opt-in (NAO opt-out)
2. Granularidade por categoria
3. Revogacao facilitada
4. Linguagem clara
5. Registro de consentimento (timestamp, IP, opcoes)

## Banco de Dados (XForge Schema)

```sql
CREATE TABLE lgpd_consent (
    id UNIQUEIDENTIFIER PRIMARY KEY,
    user_id UNIQUEIDENTIFIER NOT NULL,
    consent_version VARCHAR(20) NOT NULL,
    categories_json NVARCHAR(MAX) NOT NULL,
    granted_at DATETIME2 NOT NULL,
    revoked_at DATETIME2 NULL,
    ip_address VARCHAR(45) NULL,
    user_agent NVARCHAR(500) NULL
);
```

## Google Analytics - Cuidados

- Anonimizar IP
- Desabilitar sinais demograficos
- Desabilitar Google Signals
- Modo de consentimento v2

## Facebook Pixel - Alternativa

- Conversions API (server-side) recomendado
- Se usar Pixel, consentimento previo para publicidade

## Referencias

- LGPD Lei 13.709/2018 Arts. 7-9
- ANPD Orientacoes 02/2022
