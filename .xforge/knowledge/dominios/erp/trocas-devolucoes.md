---
id: erp-trocas-devolucoes
type: knowledge
tags: [erp, trocas, devolucoes, estorno, nfe-devolucao, cdc, comissoes, estoque]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Trocas e Devoluções
- **Principais responsabilidades**: Processar devoluções de venda: total, parcial, por arrependimento (CDC art. 49 — 7 dias), por vício (CDC art. 18/26 — 30/90 dias).; Processar troca...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, trocas, devolucoes, estorno, nfe-devolucao, cdc, comissoes, estoque
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-trocas-devolucoes` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Trocas e Devoluções

## Propósito

Documentar o módulo de trocas e devoluções do ERP, cobrindo tipos de devolução (total, parcial, arrependimento), processo completo, documentos fiscais de devolução, estorno de estoque, impacto financeiro e estorno de comissões.

## Responsabilidades

- Processar devoluções de venda: total, parcial, por arrependimento (CDC art. 49 — 7 dias), por vício (CDC art. 18/26 — 30/90 dias).
- Processar trocas: simples (mesmo valor), com diferença de valor (cliente paga ou recebe crédito), por crédito.
- Emitir NF-e de devolução referenciando a NF-e original (chave de acesso obrigatória).
- Aplicar CFOPs de devolução: 5.201/6.201 (produção própria), 5.202/6.202 (mercadoria de terceiros).
- Realizar estorno de estoque: entrada do produto devolvido pelo custo original (PEPS, UEPS ou Médio).
- Estornar comissões proporcionalmente: (valor devolvido / valor original) × comissão paga.
- Gerar estorno financeiro: crédito ao cliente, abatimento de títulos ou nova duplicata (troca com diferença).
- Controlar devolução ao fornecedor: NF-e de devolução de compra (CFOP 1.201/2.201), estorno de crédito fiscal.
- Apurar relatórios: devoluções por produto, cliente, vendedor, motivo e custo total.

## Dependências

- **fluxo-vendas.md** — NF-e original, pedido de venda, comissões.
- **faturamento.md** — Emissão de NF-e de devolução, CFOPs, transmissão SEFAZ.
- **estoque.md** — Estorno de estoque, métodos de custeio, inspeção.

## Restrições

- Devolução de venda sempre vinculada à NF-e original (chave de acesso).
- Valor devolvido não pode exceder o valor original.
- CDC: política da empresa pode ser mais favorável, nunca mais restritiva.
- Estorno de crédito fiscal (ICMS, IPI, PIS, COFINS) no período de escrituração da NF-e de devolução.
- Inspeção obrigatória do produto devolvido: classificar como novo, usado, com defeito ou inutilizável.
- CFOP de devolução de compra: 1.201/2.201 (industrialização), 1.202/2.202 (comercialização).

## Relacionados

- [fluxo-vendas.md](fluxo-vendas.md) — Vendas, pedidos e comissões.
- [faturamento.md](faturamento.md) — Documentos fiscais e devolução.
- [estoque.md](estoque.md) — Controle de estoque e custos.

