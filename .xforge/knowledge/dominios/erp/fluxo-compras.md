---
id: erp-fluxo-compras
type: knowledge
tags: [erp, compras, procure-to-pay, cotacao, pedido-compra, recebimento, 3-way-match]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Fluxo de Compras
- **Principais responsabilidades**: Processar requisições de compra por departamento com aprovação por alçada de valor.; Gerar cotações (RFQ) enviadas a múltiplos fornecedores com cri...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, compras, procure-to-pay, cotacao, pedido-compra, recebimento, 3-way-match
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-fluxo-compras` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Fluxo de Compras

## Propósito

Documentar o ciclo completo de compras (Procure-to-Pay), desde a identificação de necessidade interna até o pagamento ao fornecedor, passando por requisição, cotação, pedido, recebimento e faturamento de entrada.

## Responsabilidades

- Processar requisições de compra por departamento com aprovação por alçada de valor.
- Gerar cotações (RFQ) enviadas a múltiplos fornecedores com critérios ponderados (preço, prazo, qualidade, garantia, frete).
- Criar pedidos de compra (PO) com itens, condições de pagamento, prazo de entrega e tipo de frete.
- Realizar recebimento com conferência quantitativa e qualitativa (pedido × NF-e × recebimento = 3-way match).
- Classificar NF-e de entrada com CFOP, CST de ICMS/IPI/PIS/COFINS conforme regime tributário.
- Gerar títulos de contas a pagar automaticamente a partir da NF-e de entrada.
- Controlar devolução de compra com NF-e de devolução (CFOP 1.201/2.201), estorno de estoque e crédito fiscal.
- Apurar KPIs: lead time por fornecedor, % rejeição, economia em cotações, giro de estoque.

## Dependências

- **estoque.md** — Entrada de mercadorias, custo de aquisição, inventário.
- **faturamento.md** — Classificação fiscal de NF-e de entrada, créditos de impostos.
- **producao.md** — Geração de necessidades de compra via MRP.

## Restrições

- Pagamento só é liberado após 3-way match (pedido × recebimento × NF-e) com tolerância configurável.
- Crédito de ICMS/IPI/PIS/COFINS depende do regime tributário (Lucro Real = não cumulativo).
- CFOP de entrada: 1xxx (mesmo estado), 2xxx (interestadual), 3xxx (exterior).
- CST de ICMS: 00 (tributado), 60 (ST), 40 (isenta), etc.
- Retenções na fonte (IRRF, INSS, CSLL, PIS, COFINS, ISS) aplicam-se a serviços, não a mercadorias.
- Tolerância de recebimento: ±5% para produtos a granel, 0% para itens contáveis.

## Relacionados

- [estoque.md](estoque.md) — Gestão de estoque e custos.
- [faturamento.md](faturamento.md) — Documentos fiscais de entrada.
- [producao.md](producao.md) — MRP e necessidades de materiais.

