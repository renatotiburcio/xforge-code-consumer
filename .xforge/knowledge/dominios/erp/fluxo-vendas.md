---
id: erp-fluxo-vendas
type: knowledge
tags: [erp, vendas, pipeline, pedido, faturamento, comissoes, crm, nfe]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Fluxo de Vendas
- **Principais responsabilidades**: Gerenciar o pipeline: prospecção → orçamento → pedido → expedição → faturamento → recebimento.; Criar e controlar orçamentos com validade, alçadas ...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, vendas, pipeline, pedido, faturamento, comissoes, crm, nfe
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-fluxo-vendas` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Fluxo de Vendas

## Propósito

Documentar o pipeline completo de vendas no ERP, desde a prospecção até o recebimento financeiro, passando por orçamento, pedido, expedição, faturamento, transporte e cobrança.

## Responsabilidades

- Gerenciar o pipeline: prospecção → orçamento → pedido → expedição → faturamento → recebimento.
- Criar e controlar orçamentos com validade, alçadas de aprovação, revisões e conversão em pedido.
- Processar pedidos de venda com tipos: normal, entrega futura, consignação, e-commerce, bonificação, exportação.
- Controlar status do pedido: em aberto, aprovado, bloqueado, em separação, faturado, parcialmente faturado, encerrado, cancelado.
- Realizar expedição: romaneio de separação (picking), conferência, embalagem, romaneio de entrega.
- Gerar documentos fiscais: NF-e (modelo 55), NFC-e (modelo 65), CT-e, MDF-e.
- Calcular comissões por vendedor: por produto, cliente, faixa de valor, região, meta atingida.
- Gerar títulos de contas a receber a partir do faturamento (boleto, PIX, cartão, dinheiro).
- Controlar devoluções: NF-e de devolução (CFOP 5.201/6.201), estorno de estoque, comissão e financeiro.
- Apurar KPIs: ticket médio, taxa de conversão, vendas por dimensão, meta vs. realizado, CAC, LTV.

## Dependências

- **orcamentos.md** — Criação e aprovação de orçamentos, alçadas de desconto.
- **faturamento.md** — Emissão de NF-e/NFC-e, transmissão à SEFAZ, contingência.
- **estoque.md** — Reserva de estoque, baixa na expedição.
- **trocas-devolucoes.md** — Processo de devolução, estornos fiscais e financeiros.
- **crm.md** — Pipeline de vendas, histórico de interações, follow-up.

## Restrições

- Pedido só é creditamente liberado após aprovação de crédito do cliente.
- NF-e de devolução deve referenciar a NF-e original (chave de acesso).
- Cancelamento de NF-e: prazo por estado (24h maioria, até 72h alguns, 7 dias AM/AP/BA/CE/DF/ES/GO/MA/PA/PB/PE/PI/RN/RO/RR/SE/TO).
- Comissões podem ser calculadas no faturamento ou no recebimento (configurável).
- CFOP deve corresponder à natureza da operação e UF de origem/destino.

## Relacionados

- [orcamentos.md](orcamentos.md) — Orçamentos e propostas comerciais.
- [faturamento.md](faturamento.md) — Emissão de documentos fiscais.
- [estoque.md](estoque.md) — Controle de estoque e movimentações.
- [trocas-devolucoes.md](trocas-devolucoes.md) — Devoluções e estornos.
- [crm.md](crm.md) — Gestão de relacionamento com cliente.

