---
id: erp-agronegocio
type: knowledge
tags: [erp, agronegocio, lcdpr, itr, irpf, safra, rebanho, produtor-rural]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Agronegócio — LCDPR e ITR
- **Principais responsabilidades**: Controlar LCDPR para produtor rural com receita bruta anual > R$ 4.800.000,00 (obrigatório) ou ≤ R$ 4.800.000,00 (optante).; Gerenciar estrutura do...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, agronegocio, lcdpr, itr, irpf, safra, rebanho, produtor-rural
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-agronegocio` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Agronegócio — LCDPR e ITR

## Propósito

Documentar os requisitos fiscais e contábeis específicos do agronegócio no ERP, com foco no LCDPR (Livro Caixa Digital do Produtor Rural) e ITR (Imposto Territorial Rural), incluindo obrigatoriedade, estrutura, apuração de resultado e integração com IRPF.

## Responsabilidades

- Controlar LCDPR para produtor rural com receita bruta anual > R$ 4.800.000,00 (obrigatório) ou ≤ R$ 4.800.000,00 (optante).
- Gerenciar estrutura do LCDPR: identificação do produtor, estabelecimentos, imóveis rurais, contas bancárias, plano de contas, centros de custo.
- Registrar movimentações: receitas (venda de produtos, subsídios, financeiras), despesas (insumos, mão de obra, depreciação, energia, frete), investimentos, financiamentos.
- Controlar safras e rebanho: movimentação de estoque, apuração de resultado por safra.
- Apurar resultado: Receitas − Despesas = Resultado Bruto; Resultado Bruto − IRPJ − CSLL = Resultado Líquido.
- Integrar resultado do LCDPR com IRPF (ficha "Atividade Rural" da Declaração de Ajuste Anual).
- Calcular ITR: base de cálculo = Valor da Terra Nua (VTN) − Deduções (APP, reserva legal, interesse ecológico).
- Aplicar alíquotas do ITR conforme área do imóvel e grau de utilização (0,03% a 3,50%).
- Gerar DITR (Declaração do ITR) com prazo na última quinzena de setembro.
- Controlar imóveis rurais: cadastro de áreas (total, utilizável, preservação), cálculo do grau de utilização.

## Dependências

- **estoque.md** — Controle de estoque de produtos agrícolas, movimentações de safra.
- **faturamento.md** — Emissão de NF-e de produtos agropecuários.

## Restrições

- LCDPR: regime de caixa obrigatório para receita ≤ R$ 4.800.000; regime de competência obrigatório para receita > R$ 4.800.000.
- Prazo de entrega do LCDPR: último dia útil de maio do exercício seguinte.
- Multa por atraso no LCDPR: R$ 500/mês (mínimo); omissão/incorreção: 2% do valor da operação.
- ITR: imunes pequenas glebas (até 30 ha) exploradas por proprietário sem outro imóvel, terras indígenas, assentamentos de reforma agrária.
- Multa por atraso na DITR: 1% ao mês (mínimo R$ 50,00).
- Grau de utilização = (Área Utilizável − Área Não Utilizada) / Área Total × 100.

## Relacionados

- [estoque.md](estoque.md) — Controle de estoque e custos.
- [faturamento.md](faturamento.md) — Emissão de documentos fiscais.

