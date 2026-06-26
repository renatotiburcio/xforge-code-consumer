---
id: erp-producao
type: knowledge
tags: [erp, producao, pcp, mrp, mps, bom, roteiro, op, oee, qualidade]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Produção Industrial
- **Principais responsabilidades**: Planejar produção via MPS (Plano Mestre) e MRP (cálculo de necessidades de materiais).; Gerenciar BOM (Bill of Materials): estrutura hierárquica de...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, producao, pcp, mrp, mps, bom, roteiro, op, oee, qualidade
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-producao` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Produção Industrial

## Propósito

Documentar o módulo de Planejamento e Controle da Produção (PCP), cobrindo tipos de produção, MRP/MRP II, BOM (Lista de Materiais), roteiro de fabricação, ordens de produção, apontamento, controle de qualidade, custo de produção e integração com estoque.

## Responsabilidades

- Planejar produção via MPS (Plano Mestre) e MRP (cálculo de necessidades de materiais).
- Gerenciar BOM (Bill of Materials): estrutura hierárquica de componentes, subconjuntos e matérias-primas.
- Definir roteiros de fabricação: sequência de operações, centros de trabalho, tempos de setup e execução.
- Criar e controlar Ordens de Produção (OP): status (criada, liberada, em andamento, parcial, finalizada, encerrada, cancelada).
- Realizar apontamento de produção: quantidades produzidas, refugo, tempo real por operação.
- Controlar qualidade: inspeção de entrada, em processo e final; não conformidades (NC); CEP (Controle Estatístico de Processo).
- Calcular custo de produção: matéria-prima + mão de obra direta + custos indiretos (CIF) rateados.
- Apurar OEE (Overall Equipment Effectiveness): Disponibilidade × Performance × Qualidade (meta: >85%).
- Integrar com compras (necessidades de MP), estoque (consumo/entrada), vendas (MTO/ATO) e financeiro (custos).

## Dependências

- **estoque.md** — Consumo de matéria-prima, entrada de produto acabado, WIP.
- **fluxo-compras.md** — Geração de pedidos de compra a partir do MRP.
- **fluxo-vendas.md** — Pedidos MTO/ATO que disparam produção.

## Restrições

- MRP requer MPS atualizado, BOM correto, estoques acurados e lead times realistas.
- Custo padrão exige revisão periódica e ajuste ao custo efetivo.
- Rateio de CIF: métodos por hora-máquina, hora-homem, custo de MP ou ABC.
- OEE benchmark: >85% world class, 75-84% bom, 65-74% aceitável, <50% crítico.
- Tipos de produção: contínua, intermitente/lote, discreta/unitária, por projeto.
- Modos: MTS (Make-to-Stock), MTO (Make-to-Order), ATO (Assemble-to-Order), ETO (Engineer-to-Order).

## Relacionados

- [estoque.md](estoque.md) — Gestão de estoque e movimentações.
- [fluxo-compras.md](fluxo-compras.md) — Compras e recebimento de materiais.
- [fluxo-vendas.md](fluxo-vendas.md) — Vendas e pedidos de produção.

