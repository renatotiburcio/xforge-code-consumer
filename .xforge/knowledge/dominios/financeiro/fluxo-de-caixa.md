---
id: fin-fluxo-caixa
type: dominio
tags: [financeiro, fluxo-caixa, dfc, projecao, tesouraria]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Controlar entradas e saídas financeiras, projetar saldos futuros e garantir liquidez operacional.
- **Principais responsabilidades**: Controle diário de entradas e saídas; Projeção de caixa (diária, semanal, mensal); Análise por centro de custo e conta bancária
- **Seções principais**: Purpose, Responsibilities, Caixa Diário, Caixa Projetado
- **Tags**: financeiro, fluxo-caixa, dfc, projecao, tesouraria
- **Tipo**: dominio | **Versão**: 2.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fin-fluxo-caixa` |
| Tipo | dominio |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 10 |


# Fluxo de Caixa

## Purpose
Controlar entradas e saídas financeiras, projetar saldos futuros e garantir liquidez operacional.

## Responsibilities
- Controle diário de entradas e saídas
- Projeção de caixa (diária, semanal, mensal)
- Análise por centro de custo e conta bancária
- Alertas de saldo negativo
- Integração com contas a pagar e receber

## Caixa Diário
- Entradas: vendas à vista, recebimentos, resgates de aplicações
- Saídas: pagamentos, despesas operacionais, transferências
- Saldo do dia: Entradas – Saídas
- Saldo acumulado: Saldo anterior + Saldo do dia

## Caixa Projetado
```
Saldo projetado = Saldo atual + Recebimentos futuros – Pagamentos futuros
```
- Horizonte: diário, semanal, mensal
- Alertas automáticos de saldo negativo
- Base: títulos de contas a pagar e receber com vencimento futuro

## DFC — Demonstração dos Fluxos de Caixa
Método direto (preferencial pelo CPC 03):
```
(+/-) Atividades Operacionais
  Recebimentos de clientes
  Pagamentos a fornecedores
  Pagamento de salários
  Pagamento de impostos
(+/-) Atividades de Investimento
  Aquisição de ativo imobilizado
  Venda de ativos
(+/-) Atividades de Financiamento
  Empréstimos obtidos
  Amortização de empréstimos
  Pagamento de dividendos
(=) Variação Líquida de Caixa
```

## Fluxo por Centro de Custo
- Receitas e despesas alocadas por área
- Resultado por centro: Receitas – Despesas
- Análise de performance: centros lucrativos vs. deficitários

## Fluxo por Conta Bancária
- Saldo individualizado por conta
- Transferências entre contas
- Conciliação: saldo contábil vs. saldo bancário

## Indicadores de Liquidez
| Indicador | Fórmula | Referência |
|-----------|---------|------------|
| Liquidez Corrente | Ativo Circulante / Passivo Circulante | > 1,0 |
| Liquidez Seca | (AC – Estoques) / PC | > 0,5 |
| Liquidez Imediata | Disponibilidades / PC | > 0,2 |

## Dependencies
- `dominios/financeiro/contas-a-pagar.md`
- `dominios/financeiro/contas-a-receber.md`
- `dominios/financeiro/conciliacao-bancaria.md`
- `dominios/contabil/demonstracoes-contabeis.md`

## Related Documents
- `dominios/contabil/centro-de-custo.md`
- `dominios/financeiro/pagamentos-digitais.md`

