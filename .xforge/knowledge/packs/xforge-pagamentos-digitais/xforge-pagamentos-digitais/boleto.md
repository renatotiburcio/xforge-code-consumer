---
id: knowledge-pagamentos-boleto
type: knowledge
title: Boleto Bancario - Sistema de Cobranca
domain: financeiro
trustScore: 85
source: febraban / bancos
tags: [boleto, febraban, cobranca, cnab, banco]
status: curated
priority: medium
coverage: comprehensive
lastReviewed: 2026-06-13
---

# Boleto Bancario - Sistema de Cobranca Brasileiro

## Codigo de Barras (44 digitos)
Estrutura padrao FEBRABAN:
- Banco(3) - codigo do banco (001 BB, 237 Bradesco, 341 Itau)
- Moeda(1) - 9 = Real
- Fator Vencimento(4) - dias desde 03/07/2000
- Valor(10) - valor em centavos (8 inteiros + 2 decimais)
- Livre(25) - nosso numero + digitos verificadores

## Pagamento
- Casa loterica - qualquer valor
- Bancos - Internet Banking, agencia, ATM
- Apps de banco - leitura do codigo de barras via camera
- D+1 a D+3 para liquidacao (varia por banco)

## CNAB 240/400
Layouts FEBRABAN para remessa (envio de boletos ao banco) e retorno (recebimento de pagamentos processados). CNAB 240 e o padrao atual.

## Boleto Registrado vs Nao Registrado
- Registrado (a partir de 2017): obrigatorio, controle via CIP
- Nao registrado: descontinuado para novas cobrancas

## Taxas
- Emissao: R$ 0.50 a R$ 5.00 por boleto
- Liquidacao: 1 a 3 dias uteis
