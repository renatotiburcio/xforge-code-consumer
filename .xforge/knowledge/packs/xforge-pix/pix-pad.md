# PIX Pad (API Padrao do Banco Central)

Guia de integracao com a API padrao PIX do Banco Central do Brasil.

## Endpoints principais (BCB)

| Endpoint | Metodo | Descricao |
|----------|--------|-----------|
| `/pix/v1/cob` | POST | Criar cobranca imediata |
| `/pix/v1/cob/{txid}` | GET | Consultar cobranca |
| `/pix/v1/cob/{txid}` | PATCH | Atualizar cobranca |
| `/pix/v1/pix` | POST | Enviar PIX |
| `/pix/v1/pix/{e2eid}` | GET | Consultar PIX enviado |
| `/pix/v1/webhook/{chave}` | PUT | Configurar webhook |

## Autenticacao

- mTLS (certificado A1 emitido por ICP-Brasil)
- OAuth 2.0 com client_credentials
- Scopos: `cob.read`, `cob.write`, `pix.read`, `pix.write`, `webhook.read`, `webhook.write`

## Exemplo: criar cobranca

```http
POST /pix/v1/cob HTTP/1.1
Host: api-pix.bcb.gov.br
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "calendario": {"expiracao": 3600},
  "devedor": {"cpf": "12345678901", "nome": "Joao da Silva"},
  "valor": {"original": "100.50"},
  "chave": "minha-chave@exemplo.com",
  "infoAdicionais": [{"nome": "pedido", "valor": "12345"}]
}
```

Resposta:

```json
{
  "txid": "abc123...",
  "status": "ATIVA",
  "valor": "100.50",
  "pixCopiaECola": "00020126580014br.gov.bcb.pix..."
}
```

## Homologacao

Ambiente sandbox: `api-pix-h.bcb.gov.br`
- Chaves de teste: geradas no portal developer
- mTLS com certificado sandbox (auto-assinado)

## Erros canonicos

| HTTP | codigo | descricao |
|------|--------|-----------|
| 400 | COBRANCA_INVALIDA | Campos obrigatorios faltando |
| 401 | NAO_AUTORIZADO | Token expirado ou invalido |
| 403 | ACESSO_NEGADO | Scope insuficiente |
| 404 | COBRANCA_NAO_ENCONTRADA | txid inexistente |
| 422 | VALOR_INVALIDO | Valor negativo ou zero |
| 503 | SERVICO_INDISPONIVEL | BCB em manutencao |

## Tags

pix, bcb, mTLS, oauth, integracao, br
