---
id: erp-pdv-frente-caixa
type: knowledge
tags: [erp, pdv, frente-caixa, vendas, fiscal, nfc-e, sat, pagamentos]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre PDV / Frente de Caixa
- **Principais responsabilidades**: Registrar vendas no ponto de caixa com cálculo de totais, descontos e troco.; Processar múltiplas formas de pagamento: dinheiro, cartão (TEF), PIX,...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, pdv, frente-caixa, vendas, fiscal, nfc-e, sat, pagamentos
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-pdv-frente-caixa` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# PDV / Frente de Caixa

## Propósito

Documentar o módulo de Ponto de Venda (PDV) / Frente de Caixa do ERP, cobrindo conceitos, tipos por segmento, hardware, arquitetura, fluxo de venda, integração fiscal (NFC-e/SAT), formas de pagamento e fechamento de caixa.

## Responsabilidades

- Registrar vendas no ponto de caixa com cálculo de totais, descontos e troco.
- Processar múltiplas formas de pagamento: dinheiro, cartão (TEF), PIX, VR/VA, cheque, fiado.
- Emitir documentos fiscais eletrônicos (NFC-e, SAT/CF-e) com integração à SEFAZ.
- Controlar abertura, movimentação, sangria, reforço e fechamento de caixa.
- Gerenciar controle de mesas/comandas para bares e restaurantes.
- Realizar baixa automática de estoque no momento do pagamento.
- Controlar inventário rotativo e transferências entre filiais.

## Dependências

- **estoque.md** — Baixa automática, controle de estoque negativo, inventário.
- **faturamento.md** — Emissão de NFC-e/SAT, contingência, cancelamento de documentos fiscais.
- **fluxo-vendas.md** — Conversão de orçamento em pedido, comissionamento.
- **trocas-devolucoes.md** — Cancelamento de cupom, estorno de venda.

## Restrições

- Caixa deve estar fechado do dia anterior para permitir abertura.
- Fundo de caixa (troco inicial) é obrigatório na abertura.
- Cancelamento de NFC-e: prazo definido pelo estado (geralmente 30 min a 24h).
- Cancelamento de SAT: até o primeiro minuto do próximo dia.
- Estoque negativo requer senha de supervisor (configurável).
- Contingência NFC-e: transmissão em até 7 dias; SAT: até 24 horas.

## Relacionados

- [estoque.md](estoque.md) — Controle de estoque e movimentações.
- [faturamento.md](faturamento.md) — Emissão de documentos fiscais.
- [fluxo-vendas.md](fluxo-vendas.md) — Pipeline de vendas e comissões.
- [trocas-devolucoes.md](trocas-devolucoes.md) — Trocas, devoluções e estornos.

