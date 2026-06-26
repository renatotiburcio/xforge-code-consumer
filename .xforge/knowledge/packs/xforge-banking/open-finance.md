---
title: "Open Finance Brasil \u2014 Visao Geral"
id: knowledge-open-finance
type: knowledge
summary: "Ecosistema Open Finance BR: participantes, escopos, APIs, seguranca e fases"
keywords: ["open-finance", "open-banking", "pix", "initiation", "apis-brasileiras"]
trustScore: 82
lastValidated: 2026-06-13
---

# Open Finance Brasil

## O que e

Open Finance Brasil e o ecossistema de compartilhamento padronizado de dados e servicos financeiros entre instituicoes reguladas pelo Banco Central do Brasil, em vigor desde 2021.

## Participantes

| Tipo | Exemplos | Papel |
|------|----------|-------|
| Transmissor | bancos, fintechs, cooperativas | expoe dados do usuario via APIs |
| Receptor | ERPs, gestoras, fintechs | consome dados com consentimento |
| Iniciador de transacao | fintechs de pagamento | inicia PIX, boleto, transferencia |
| Detentor de dados | bancos, corretoras | fonte de verdade para contas |

## Escopos (4 oficiais)

1. **Dados cadastrais**: nome, CPF/CNPJ, endereco, contas
2. **Dados transacionais**: historico, saldos
3. **Iniciacao de pagamento**: PIX, TED, boleto
4. **Investimentos**: renda fixa, variavel, fundos

## Fases

- **Fase 1** (ago/2021): PF cadastral e transacional
- **Fase 2** (ago/2022): PJ + inicio de pagamento
- **Fase 3** (fev/2023): investimentos + seguros
- **Fase 4** (mar/2024): expansoes operacionais

## Fluxo de consentimento

1. **Aprovacao**: usuario autentica no transmissor
2. **Autorizacao**: redirecionamento via OAuth 2.0 + PKCE
3. **Token**: access_token curta duracao + refresh_token
4. **Uso**: ERPs chamam APIs com scopes
5. **Revogacao**: usuario pode revogar a qualquer momento

## Seguranca obrigatoria

- mTLS (ICP-Brasil) entre receptor e transmissor
- OAuth 2.0 com PKCE
- JWS (assinatura digital) em todas requests
- LGPD compliance
- Logs de auditoria por 5 anos

## Integracao ERP

1. Cadastro no diretorio de participantes do BCB
2. Certificado ICP-Brasil A1 ou A3
3. Cliente OAuth 2.0 com PKCE
4. Endpoints:
   - `/accounts` (lista contas)
   - `/transactions` (extrato)
   - `/payments/initiate` (iniciacao)
5. Webhook para status de pagamento

## Cuidados

- NUNCA armazenar access_token sem criptografia
- Renovar refresh_token antes de expirar
- Circuit breaker para APIs externas
- Rate limits: 300 req/5min por transmissor