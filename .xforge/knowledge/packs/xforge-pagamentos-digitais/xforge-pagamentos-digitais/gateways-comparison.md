---
id: knowledge-pagamentos-gateways
type: knowledge
title: Comparativo de Gateways de Pagamento
domain: financeiro
trustScore: 78
source: documentacao oficial dos gateways
tags: [gateway, stripe, pagarme, mercado-pago, asaas, pagseguro, comparativo]
status: curated
priority: high
coverage: comprehensive
lastReviewed: 2026-06-13
---

# Comparativo de Gateways de Pagamento

## Mercado Brasileiro 2026

| Gateway | PIX | Cartao | Boleto | Assinatura | Split | Destaque |
|---------|-----|--------|--------|------------|-------|----------|
| Stripe | sim | sim | sim | sim | sim | DX, global |
| Pagar.me | sim | sim | sim | sim | sim | Brasa, bom split |
| Mercado Pago | sim | sim | sim | sim | sim | Integracao ML |
| Asaas | sim | sim | sim | sim | sim | Foco em recorrencia |
| PagSeguro | sim | sim | sim | sim | sim | Tradicional, PagBank |
| Iugu | sim | sim | sim | sim | sim | Brasa, foco B2B |
| Cielo | sim | sim | sim | nao | sim | Adquirente tradicional |
| Stone | sim | sim | sim | nao | sim | Maquininhas + API |

## Criterios de Escolha

### Custo
- Stripe: 4.99% + R$ 0.39 cartao, 0.99% PIX
- Pagar.me: ~4.99% cartao, ~1.99% PIX, ~R$ 3.50 boleto
- Mercado Pago: varia, ~5.0% cartao
- Asaas: 2.49% PIX, ~4.49% cartao (precos populares)

### DX (Developer Experience)
Stripe > Pagar.me > Mercado Pago > Asaas > Iugu

### Webhooks
Todos oferecem webhooks para payment.created, payment.paid, payment.refunded, subscription.created, subscription.canceled, charge.failed, chargeback.created.

### Split de Pagamento
Stripe Connect, Pagar.me Marketplaces, Asaas Cofrinhos permitem dividir pagamento entre seller, marketplace e plataforma.

## Recomendacao por Caso
- E-commerce simples: Mercado Pago ou PagSeguro
- Marketplace: Pagar.me ou Stripe Connect
- Assinatura / SaaS: Asaas ou Iugu
- Internacional: Stripe (multi-currency nativo)
- ERP completo: Pagar.me + Asaas (split + recorrencia)
