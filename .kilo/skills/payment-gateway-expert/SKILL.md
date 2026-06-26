---
name: payment-gateway-expert
description: Expert em gateways de pagamento: Stripe, Pagar.me, Mercado Pago, PagSeguro, Asaas, Pix, cartao e boleto.
metadata:
  version: "1.0.0"
  xforge-category: "domain-expert"
---

# payment-gateway-expert

## Objetivo

Integrar e gerenciar gateways de pagamento para e-commerce e SaaS.

## Gateways Suportados

| Gateway | Cartão | Boleto | Pix | Assinatura |
|---------|:------:|:------:|:---:|:----------:|
| Stripe | ✅ | ✅ | ✅ | ✅ |
| Pagar.me | ✅ | ✅ | ✅ | ✅ |
| Mercado Pago | ✅ | ✅ | ✅ | ✅ |
| PagSeguro | ✅ | ✅ | ✅ | ✅ |
| Asaas | ✅ | ✅ | ✅ | ✅ |
| Stone | ✅ | ✅ | ✅ | ❌ |
| Cielo | ✅ | ✅ | ✅ | ❌ |

## Fluxo de Pagamento

```
Cliente → Checkout → Gateway → Bandeira → Adquirente → Banco Emissor
                                    ↓
                            Autorização → Captura → Liquidacao
                                    ↓
                            Recusa → Retry/Outro método
```

### Checkout
1. Cliente seleciona método de pagamento
2. Dados validados (Luhn, BIN, CVC)
3. Tokenização do cartão (nunca salvar dados brutos)
4. Envio para autorização

### Autorização
- Verificação de fundos
- Análise de risco (AVS, CVV, velocity)
- Resposta: aprovado/recusado/pendente

### Captura
- Autorização → Captura (confirmação)
- Captura pode ser imediata ou adiada
- Split de valores (marketplace)

### Liquidação
- Gateway repassa ao lojista
- Taxa: ~2% cartão crédito, ~1% débito
- Prazo: D+1 (débito) a D+30 (crédito parcelado)

## Integrações

### Stripe
```javascript
const paymentIntent = await stripe.paymentIntents.create({
  amount: 9990, // R$ 99,90 em centavos
  currency: 'brl',
  payment_method_types: ['card', 'boleto', 'pix'],
});
```

### Pagar.me
```javascript
const transaction = await pagarme.transaction.create({
  amount: 9990,
  payment_method: 'credit_card',
  card: { number: '4111111111111111', ... },
});
```

### Asaas
```javascript
const payment = await asaas.payments.create({
  billingType: 'PIX',
  value: 99.90,
  dueDate: '2024-01-30',
  description: 'Pedido #1234',
});
```

## Procedimento

1. Configurar credenciais do gateway
2. Implementar tokenização
3. Criar fluxo de checkout
4. Processar webhooks de status
5. Conciliar pagamentos com pedidos
6. Gerenciar estornos e chargebacks

## Regras

- NUNCA salvar dados de cartão no ERP
- Sempre usar tokenização
- Webhooks processados idempotentemente
- Log completo de transações
- Reconciliação diária obrigatória
