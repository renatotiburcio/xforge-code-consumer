---
id: producao-ordem
type: fluxo
tags: [producao, pcp, mrp, op, qualidade, custo, wip, refugo]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Fluxo de Produção por Ordem (OP)
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Métricas (KPIs)
- **Tags**: producao, pcp, mrp, op, qualidade, custo, wip, refugo
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `producao-ordem` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# Fluxo de Produção por Ordem (OP)

## Propósito
Documentar o fluxo completo de produção industrial: planejamento, emissão de OP, requisição de materiais, apontamento, controle de qualidade e apuração de custo, incluindo WIP e refugo.

## Etapas

1. **Planejamento (MPS/MRP)**: Plano Mestre define "o que" e "quando" produzir. MRP calcula necessidades líquidas a partir do BOM, estoques, lead times e políticas de lote. Gera ordens planejadas de compra e fabricação. CRP valida capacidade dos centros de trabalho.
2. **Emissão da OP**: Ordem gerada pelo MRP ou manualmente. Contém: produto, quantidade, datas planejadas, roteiro de fabricação, BOM explodida. Status: Criada → Liberada (após validação e separação de materiais).
3. **Requisição de Materiais**: Baixa automática de matérias-primas do estoque (empenho → consumo) conforme BOM. WIP movimentado entre operações do roteiro. Estoques geridos: matéria-prima, WIP, produto acabado, consumíveis e sucata.
4. **Apontamento de Produção**: Registro por operação — quantidade produzida, quantidade refugo, tempo real, operador. Dados coletados via terminal no chão de fábrica ou dispositivo móvel.
5. **Controle de Qualidade**: Inspeção de entrada (matérias-primas), em processo (CEP — controle estatístico) e final (produto acabado). Não conformidades geram ficha NC com disposição: retrabalho, sucata, uso como está ou retorno ao fornecedor.
6. **Entrada em Estoque**: Após aprovação final, produtos entram no estoque de PA. Refugados vão para quarentena ou sucata.
7. **Apuração de Custo**: Custo = Matéria-Prima + Mão de Obra Direta + Custos Indiretos (CIF). Rateio por hora-máquina, hora-homem ou ABC. Custo unitário = custo total / quantidade produzida. Análise de variação: real vs. planejado.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Estoque máteria-prima suficiente? | Não | MRP gera requisição automática ao compras |
| Capacidade CT disponível? | Não | Reprogramar, horas extras ou terceirizar |
| Inspeção final aprovada? | Não | NC → retrabalho/sucata |
| Custo real dentro da tolerância? | Não (+/- 3%) | Análise de variação, ação corretiva |

## Métricas (KPIs)

- **OEE** (Overall Equipment Effectiveness): Disponibilidade × Performance × Qualidade (meta >85%)
- **Taxa de Refugo**: qtd refugo / total (<2%)
- **Lead Time de Fabricação**: data fim - data início
- **Cumprimento de Prazo**: OPs no prazo / total (>95%)
- **Custo Real vs Planejado**: variação (<±3%)

## Integrações

- **Compras**: MRP gera requisição automática → pedido → recebimento → inspeção de entrada
- **Estoque**: movimentações de MP, WIP, PA, sucata; inventário rotativo e anual
- **Fiscal**: NF-e entrada (MP), NF-e saída (PA), créditos ICMS/IPI, SPED Fiscal
- **Financeiro**: custo de produção, rateio CIF, contabilização de perdas
- **Vendas**: MTS (estoque) vs MTO/ATO (sob encomenda), OTIF

## Documentos Relacionados

- [Fluxo de Vendas](venda-completa.md)
- [Fluxo de Compras](compra-completa.md)
- [PDV/Frente de Caixa](pdv-venda.md)

