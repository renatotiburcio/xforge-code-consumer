---
id: ordem-compra-fornecedor
type: fluxo
title: Ordem de Compra: Fluxo Completo do Aprovado ao Recebido
domain: comercial
trustScore: 88
source: XForge ERP + pratica de mercado
tags: [ordem-compra, compras, aprovacao]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# Ordem de Compra: Fluxo Completo

## Visao Geral

A Ordem de Compra (OC) formaliza a compra de mercadorias ou servicos.

## Etapas

1. Solicitacao de Compra (SC)
2. Cotacao (3+ fornecedores)
3. Aprovacao (multi-nivel)
4. Ordem de Compra (OC) emitida
5. Recebimento (2 etapas: fisica + fiscal)
6. Atualizacao estoque
7. Lancamento CP
8. SPED EFD

## Aprovacao por Valor

| Valor | Aprovador | SLA |
|-------|-----------|-----|
| < R$ 1.000 | Comprador | Automatica |
| R$ 1.000-10.000 | Gerente | 24h |
| R$ 10.000-50.000 | Diretor | 48h |
| > R$ 50.000 | CEO+CFO | 72h |

## Conferencia (2 Etapas)

**Fisica**: contar volumes, conferir produtos vs OC, verificar avarias
**Fiscal**: confrontar NFe com OC (valores, CFOP, NCM), conferir impostos, verificar certidoes

## KPIs

| KPI | Meta |
|-----|------|
| Lead time medio | < 7 dias |
| % entregas no prazo | > 85% |
| Taxa devolucao | < 3% |
| % OC automatica | > 50% |

## Excecoes

- Fornecedor atrasado: Reabrir cotacao
- Produto avariado: Devolucao + nota credito
- Divergencia fiscal: Bloquear + contatar contador
- Erro quantidade: Recebimento parcial

## Referencias

- XForge ERP
- Pratica de mercado BR
