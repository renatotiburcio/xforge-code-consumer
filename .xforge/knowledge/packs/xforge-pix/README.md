# Pack xforge-pix

Integracao PIX + Open Finance no contexto XForge.

## Conteudo

| Arquivo | Topico |
|---------|--------|
| `README.md` | Visao geral |
| `pix-pad.md` | PIX Pad (API padrao do BC) |
| `open-finance.md` | Open Finance Fase 4 |
| `webhook-handling.md` | Webhooks PIX + idempotencia |

## Stack

- HTTP client via IHttpClientFactory
- mTLS para conexao com PSP
- Webhook signature validation
- Idempotency-Key em todos POSTs

## Tags

pix, open-finance, pagamento, integracao, webhook, mTLS
