---
id: knowledge-pagamentos-pix
type: knowledge
title: PIX - Sistema de Pagamentos Instantaneos
domain: financeiro
trustScore: 92
source: bacen.gov.br / ispb-rules
tags: [pix, pagamentos, bacen, qr-code, spi]
status: curated
priority: high
coverage: comprehensive
lastReviewed: 2026-06-13
---

# PIX - Sistema de Pagamentos Instantaneos Brasileiros

PIX e o sistema de pagamentos instantaneos criado pelo Banco Central do Brasil (BACEN), operacional desde 16/11/2020. Permite transferencias 24/7/365 com liquidacao em ate 10 segundos.

## Chaves PIX (4 tipos)
1. CPF/CNPJ - pessoa fisica ou juridica
2. Email - qualquer email valido
3. Telefone - formato E.164 (+55XX...)
4. Chave aleatoria - UUID v4 gerada pelo PSP

## Fluxo Tecnico
- SPI (Sistema de Pagamentos Instantaneos) - infraestrutura BACEN
- PSP (Provedor de Servico de Pagamento) - intermediario (bancos, fintechs)
- DICT (Diretorio de Identificadores de Contas Transacionais) - registro de chaves

## APIs e Integracao
- API PIX BACEN (versao atual 1.0) - para participantes diretos
- Open Finance + PIX - iniciado em 2024, permite iniciar PIX via OF
- QR Code dinamico vs estatico: estatico (valor fixo, multiplo) vs dinamico (valor/vencimento especificos, uso unico)

## Custos
- PF: gratuito em todos os PSPs
- PJ: varia de R$ 0 a R$ 0,50 por transacao (decisao do PSP)
- TED/DOC substituido por PIX em 90%+ dos casos

## Cuidados
- MFA obrigatorio para alteracao de chaves
- Bloqueio cautelar disponivel em caso de fraude
- MED (Mecanismo Especial de Devolucao) para fraudes
