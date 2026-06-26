---
id: erp-estoque
type: knowledge
tags: [erp, estoque, custos, inventario, movimentacoes, peps, ueps, cm]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Gestão de Estoque e Custos
- **Principais responsabilidades**: Controlar saldos de estoque por produto, filial, depósito e localização.; Registrar movimentações: entrada (compra, produção, devolução), saída (ve...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, estoque, custos, inventario, movimentacoes, peps, ueps, cm
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-estoque` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Gestão de Estoque e Custos

## Propósito

Documentar a gestão de estoque do ERP, incluindo tipos de estoque, movimentações, métodos de custeio (PEPS, UEPS, Custo Médio, Custo Padrão), controle de inventário, cálculo de preço de venda e integração com compras e vendas.

## Responsabilidades

- Controlar saldos de estoque por produto, filial, depósito e localização.
- Registrar movimentações: entrada (compra, produção, devolução), saída (venda, consumo, perda), transferência e ajuste.
- Calcular custo de aquisição: preço + frete + seguro + impostos não recuperáveis − descontos.
- Aplicar métodos de custeio: PEPS (FIFO), Custo Médio Ponderado (CMP), Custo Padrão. UEPS é proibido no Brasil.
- Gerenciar inventário: rotativo (contínuo por amostra), cíclico (por classe ABC) e anual (100% dos itens).
- Calcular indicadores: giro de estoque, cobertura em dias, ponto de pedido, estoque mínimo/máximo.
- Apurar preço de venda via markup, margem de contribuição ou full cost.
- Controlar curva ABC (Pareto): Classe A (20% itens, 80% valor), B (30%, 15%), C (50%, 5%).

## Dependências

- **fluxo-compras.md** — Entrada de mercadorias, 3-way match, custo de aquisição.
- **fluxo-vendas.md** — Baixa de estoque na venda, reserva de mercadorias.
- **producao.md** — Consumo de matéria-prima, entrada de produto acabado, WIP.
- **pdv-frente-caixa.md** — Baixa automática no PDV, estoque negativo.

## Restrições

- UEPS (LIFO) é vedado pela Lei 12.973/2014 para apuração de IRPJ/CSLL.
- Mudança de método de custeio requer autorização prévia da RFB e aplicação prospectiva.
- Inventário anual é obrigatório para fins contábeis e fiscais (art. 246, RFB).
- Crédito de ICMS/PIS/COFINS depende do regime tributário (Real vs. Presumido).
- Custo de aquisição deve seguir CPC 16: vProd + vFrete + vSeg + vOutro + IPI + ICMS_ST − vDesc − créditos.

## Relacionados

- [fluxo-compras.md](fluxo-compras.md) — Recebimento e entrada de mercadorias.
- [fluxo-vendas.md](fluxo-vendas.md) — Vendas e reserva de estoque.
- [producao.md](producao.md) — Ordens de produção e consumo de insumos.
- [pdv-frente-caixa.md](pdv-frente-caixa.md) — PDV e baixa de estoque.

