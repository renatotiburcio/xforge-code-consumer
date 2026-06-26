# Open Finance Brasil - Fase 4

Visao geral do Open Finance Brasil e integracao com ecossistema.

## Fases

| Fase | Entregue | Foco |
|------|----------|------|
| 1 | 2021 | Dados cadastrais publicos |
| 2 | 2022 | Dados transacionais (contas) |
| 3 | 2023 | Iniciacao de pagamento (PIX, boleto) |
| 4 | 2024+ | Investimentos, credito, seguros, cambio |

## Papeis

- **Detentor** (Receptor): instituicao que detem os dados
- **Iniciador** (Transmissor): instituicao que inicia operacao
- **Usuario**: pessoa fisica ou juridica

## Fluxo de consentimento

1. Usuario acessa **iniciador** (ex: agregador)
2. Iniciador redireciona para **detentor** (banco do usuario)
3. Usuario autentica e autoriza compartilhamento
4. Detentor emite **consent** com TTL (ate 12 meses)
5. Iniciador troca codigo por **access_token**
6. Iniciador consome APIs com token

## Endpoints principais

| Recurso | Endpoint |
|---------|----------|
| Consent | `POST /consents/v1/consents` |
| Token | `POST /auth/v1/token` (grant_type=authorization_code) |
| Accounts | `GET /accounts/v1/accounts` |
| Transactions | `GET /accounts/v1/accounts/{id}/transactions` |
| Payment init | `POST /payments/v1/pix/payments` |
| Investments | `GET /investments/v1/investments` |

## mTLS

Todos os endpoints Open Finance exigem:
- Certificado mTLS emitido por ICP-Brasil
- Servidor homologacao: `mtls.br-openfinance.com.br`
- Cliente: certificado da instituicao registrada

## Webhooks

- Webhook de **payment** notifica status do pagamento iniciado
- Assinatura em header `x-signature` (HMAC-SHA256)

## LGPD

- Consentimento explicito por finalidade
- Retencao minima (ate 12 meses para dados transacionais)
- Direito de revogacao a qualquer momento via `DELETE /consents/{id}`

## Tags

open-finance, br, oauth, mTLS, integracao, lgpd, consent
