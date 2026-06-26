---
name: marketplace-integration-expert
description: Expert em integracao com marketplaces: Mercado Livre, Amazon, Shopee, Magalu, API, pedidos, estoque e precos.
metadata:
  version: "1.0.0"
  xforge-category: "domain-expert"
---

# marketplace-integration-expert

## Objetivo

Integrar ERP com marketplaces para sincronização de pedidos, estoque e preços.

## Marketplaces Suportados

| Marketplace | API | Autenticação | Frete |
|-------------|-----|-------------|-------|
| Mercado Livre | REST | OAuth 2.0 | Coleta própria |
| Amazon | SP-API | OAuth + LWA | FBA/MFN |
| Shopee | REST | OAuth 2.0 | Próprio |
| Magalu | REST | OAuth 2.0 | MagaluLog |
| Americanas | REST | API Key | Loggi |
| Via Varejo | REST | OAuth | Próprio |
| MadeiraMadeira | REST | OAuth | Próprio |

## Fluxo de Integração

```
Marketplace → Webhook/Polling → Integração → ERP
                                                ↓
ERP → Atualização estoque/preço → API → Marketplace
```

### Sincronização de Pedidos
1. Receber notificação de novo pedido
2. Buscar detalhes via API
3. Criar pedido no ERP
4. Reservar estoque
5. Gerar NF-e
6. Atualizar status no marketplace
7. Enviar código de rastreio

### Sincronização de Estoque
1. Estoque ERP mudou
2. Calcular estoque disponível (físico - reservado - marketplace)
3. Atualizar em todos os marketplaces
4. Rate limit: 1 atualização por minuto por SKU

### Sincronização de Preços
1. Preço base definido no ERP
2. Aplicar regras: markup marketplace, promoções, comissões
3. Enviar para marketplace
4. Verificar se não viola política de preço mínimo

## API Mercado Livre

```http
GET /items/{item_id}
Authorization: Bearer {access_token}

Response:
{
  "id": "MLB123456",
  "title": "Produto",
  "price": 99.90,
  "available_quantity": 50,
  "status": "active"
}
```

## API Amazon SP-API

```http
POST /orders/v0/orders/{orderId}/shipmentconfirmation
{
  "packageDetail": {
    "packageReferenceId": "1",
    "carrierCode": "correios",
    "trackingNumber": "QA123456789BR"
  }
}
```

## Procedimento

1. Cadastrar credenciais de API
2. Configurar webhooks
3. Mapear categorias marketplace ↔ categorias ERP
4. Sincronizar produtos (estoque + preço)
5. Processar pedidos automatizados
6. Monitorar erros e reenvios

## Regras

- Estoque sempre negativo = proteção
- Preço marketplace ≥ preço mínimo definido
- NF-e obrigatória para todas as vendas
- Tracking atualizado em até 24h
- Log de todas as sincronizações
