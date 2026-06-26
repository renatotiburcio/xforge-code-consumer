---
id: nfe-basics
type: knowledge
tags: [nfe, fiscal, br]
owner: fiscal-team
version: "1.0"
updated: "2026-06-13"
---
# NF-e - Modelo 55

## Schema XML
- infNFe > ide (identificacao)
- infNFe > emit (emitente)
- infNFe > dest (destinatario)
- infNFe > det[] (itens)
- infNFe > total (ICMS, IPI)
- infNFe > transp (transporte)
- infNFe > cobr (cobranca)
- infNFe > pag (pagamento)

## Validacoes comuns
- 204: Duplicidade de NF-e
- 539: Duplicidade de chave
- 611: CNPJ/CPF do destinatario invalido
- 703: Data de entrada/saida posterior a atual