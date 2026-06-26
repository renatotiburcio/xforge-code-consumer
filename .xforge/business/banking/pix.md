---
title: "PIX \u2014 SPI, DICT, QR Codes e Webhooks"
id: knowledge-pix
type: knowledgesummary: "Arquitetura PIX: SPI (liquidacao), DICT (chaves), QR dinamico/estatico, webhooks"
keywords: ["pix", "spi", "dict", "qr-code", "webhook", "pagamento-instantaneo"]
trustScore: 85
lastValidated: 2026-06-13
---

# PIX \u2014 Arquitetura e Implementacao

## Camadas

```
[Cliente] -> [APP/ERP] -> [PSP] -> [SPI] <- [DICT]
```

## Componentes

| Componente | Funcao | Latencia |
|------------|--------|----------|
| **SPI** | Liquidacao bruta em tempo real | < 10s |
| **DICT** | Diretorio de chaves PIX | < 5s |
| **QR Code** | Payload estatico ou dinamico | n/a |
| **Webhook** | Notificacao de status | < 30s |

## Tipos de chave PIX

- CPF/CNPJ
- Email (validado)
- Celular (validado via SMS)
- Chave aleatoria (UUID)

## QR Codes

### Estatico
- Sem valor fixo, usuario digita no app
- 1 uso por pagamento

### Dinamico
- Com valor pre-fixado
- Tem `txid` (identificador unico)
- Reutilizavel ate expirar
- Suporta MCC (Merchant Category Code)

## Implementacao ERP (Python)

```python
def criar_cobranca_pix(valor: Decimal, txid: str) -> Cobranca:
type: knowledge
    return pix_api.post("/v2/cob", {
        "calendario": {"expiracao": 3600},
        "valor": {"original": str(valor)},
        "chave": "sua-chave@empresa.com.br",
        "infoAdicionais": [{"nome": "pedido", "valor": txid}]
    })

@router.post("/webhooks/pix")
def pix_webhook(payload: dict):
    txid = payload["pix"][0]["txid"]
    status = payload["pix"][0]["status"]  # CONCLUIDA ou REMOVIDA
    if status == "CONCLUIDA":
        pedido_service.marcar_pago(txid=txid)
```

## Webhooks

- Validar assinatura (HMAC-SHA256)
- Responder HTTP 200 rapido (processar async)
- Idempotencia via `txid`
- Retry com backoff exponencial

## Limites

- 24/7/365 sem horario
- Padrao: R$ 5.000/transacao (PF)
- Noturno (20h-6h): limite menor

## LGPD

- Chave PIX e dado pessoal
- Logs: criptografia at rest
- Retencao: 5 anos (BCB)