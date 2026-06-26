---
id: knowledge-pagamentos-cartao
type: knowledge
title: Processamento de Cartao de Credito e Debito
domain: financeiro
trustScore: 88
source: banderias / adquirentes
tags: [cartao, credito, debito, adquirente, bandeira, pci-dss]
status: curated
priority: high
coverage: comprehensive
lastReviewed: 2026-06-13
---

# Processamento de Cartao de Credito e Debito

## Participantes do Fluxo
1. Portador - dono do cartao
2. Estabelecimento (merchant) - quem vende
3. Adquirente - conecta merchant a bandeira (Cielo, Rede, Stone, Getnet, etc)
4. Bandeira - Visa, Mastercard, Elo, Hipercard, American Express
5. Emissor (issuer) - banco que emitiu o cartao (Itau, Bradesco, Nubank)

## Modalidades
- Credito a vista: 1 parcela, MD = 30 dias
- Credito parcelado: 2-18x, juros cobrados do portador
- Debito: liquidacao em D+1 ou D+2
- Voucher / Refeicao: VR, VA (Sodexo, Alelo, Ticket)

## Taxas Tipicas (Brasil, 2024-2026)
- Credito a vista: 1.5% a 3.0%
- Credito parcelado: 2.5% a 5.0% + juros
- Debito: 0.8% a 1.8%
- Voucher: ate 5%

## PCI-DSS Compliance
- Qualquer merchant que processa cartao precisa conformidade
- Niveis: 1 (>6M tx/ano) ate 4 (<20k tx/ano)
- Tokenizacao recomendada para nao armazenar PAN
- Criptografia ponto-a-ponto (P2PE) reduz escopo de auditoria

## Antifraude
- 3DS 2.0 (Visa Secure, Mastercard Identity Check) - obrigatorio desde 2024
- Blacklist de BINs / CPFs / dispositivos
- Analise comportamental via ML
