---
id: knowledge-compliance-consent-management
type: knowledge
title: Gestao de Consentimento LGPD
category: compliance
domain: compliance
trustScore: 85
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [lgpd, consent, compliance, privacy]
---

# Gestao de Consentimento LGPD

## Base legal

O consentimento (Art. 8 LGPD) e uma das 10 bases legais para tratamento de
dados pessoais. Deve ser:

- **Livre**: sem coercao
- **Informado**: titular sabe o que esta autorizando
- **Inequivoco**: acao positiva explicita (nao pode ser pre-selecionado)

## Granularidade

Para cada finalidade de uso, obter consentimento SEPARADO:

```
[ ] Receber newsletter semanal
[ ] Receber ofertas personalizadas baseadas em compras
[ ] Compartilhar dados com parceiros para fins de marketing
[ ] Pesquisa de satisfacao pos-venda
```

**Nunca** consentimento unico para multiplas finalidades.

## Registro

Para cada consentimento obtido:

- timestamp + IP + user agent
- texto EXATO apresentado ao titular
- versao do termo
- canal (web, app, papel, telefone)
- identificador do operador que coletou

## Retirada

O titular pode retirar consentimento a qualquer hora (Art. 8 par. 5).
A retirada deve ser tao facil quanto a concessao (Art. 8 par. 6).

```sql
CREATE TABLE consent_record (
    id BIGSERIAL PRIMARY KEY,
    data_subject_id VARCHAR(64) NOT NULL,
    purpose VARCHAR(64) NOT NULL,
    granted BOOLEAN NOT NULL,
    granted_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    text_version VARCHAR(32) NOT NULL,
    channel VARCHAR(16) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    operator_id VARCHAR(64)
);
```

## Menores

Para tratamento de dados de menores de 18 anos, consentimento deve ser
dado por pelo menos um dos pais ou responsavel legal (Art. 14).

## Relacao com outras bases

Consentimento NAO e necessario quando:

- Cumprimento de obrigacao legal (ex: SPED)
- Execucao de contrato (ex: compra)
- Exercicio regular de direitos (ex: processo)
- Interesse legitimo (avaliado caso a caso)

## Referencias

- LGPD Art. 7, 8, 14, 18
- GDPR Art. 6, 7, 8 (referencia)
- Marco Civil da Internet Art. 7

