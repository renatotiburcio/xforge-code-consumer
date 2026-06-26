---
id: contabil-lancamentos-automatizados
type: domain
tags: [contabil, lancamentos, automatizados, vendas, compras, folha, financeiro, erp]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Lançamentos Automatizados
- **Principais responsabilidades**: Todo lançamento automático deve gerar histórico com referência ao documento origem; Centro de custo é herdado do cadastro do item/funcionário/conta...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, lancamentos, automatizados, vendas, compras, folha, financeiro, erp
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-lancamentos-automatizados` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# Lançamentos Automatizados

## Propósito

Mapear os lançamentos contábeis gerados automaticamente pelo ERP a partir dos eventos operacionais dos módulos de vendas, compras, folha de pagamento, financeiro e ajustes de estoque.

## Responsabilidades

**Vendas (NF-e emitida):**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Receita | Contas a Receber | Receita Bruta |
| ICMS | Contas a Receber | ICMS a Recolher |
| PIS | Contas a Receber | PIS a Recolher |
| COFINS | Contas a Receber | COFINS a Recolher |
| CMV | CMV | Estoque |

**Compras (NF-e recebida):**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Estoque | Estoque | Fornecedores |
| ICMS crédito | ICMS a Recuperar | Fornecedores |
| PIS crédito | PIS a Recuperar | Fornecedores |
| COFINS crédito | COFINS a Recuperar | Fornecedores |
| Despesa | Despesa (conta) | Fornecedores |

**Folha de Pagamento:**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Salário | Despesas com Pessoal | Banco / Salários a Pagar |
| INSS patronal | Despesas - INSS | INSS a Recolher |
| FGTS | Despesas - FGTS | FGTS a Recolher |
| INSS retido | Salários a Pagar | INSS a Recolher |
| IRRF retido | Salários a Pagar | IRRF a Recolher |
| 13º (provisão) | Despesas - 13º | Provisão 13º |
| Férias (provisão) | Despesas - Férias | Provisão Férias |

**Financeiro (Recebimento / Pagamento):**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Recebimento | Banco | Contas a Receber |
| Pagamento | Fornecedores | Banco |
| Juros mora | Despesas Financeiras | Contas a Receber |
| Desconto concedido | Descontos Concedidos | Contas a Receber |
| Juros passivos | Juros Passivos | Fornecedores |
| Desconto obtido | Fornecedores | Descontos Obtidos |

**Transferência Bancária:**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Transferência | Banco Destino | Banco Origem |

**Ajuste de Estoque:**

| Evento | Débito | Crédito |
|--------|--------|---------|
| Entrada (inventário) | Estoque | Ajuste de Estoque |
| Saída (perda, quebra) | Perdas de Estoque | Estoque |

**Regras Gerais:**
- Todo lançamento automático deve gerar histórico com referência ao documento origem
- Centro de custo é herdado do cadastro do item/funcionário/conta
- Lançamentos automáticos passam por validação antes do fechamento do período
- Estorno de lançamento automático exige estorno manual com justificativa

## Dependências

- **escrituracao-contabil.md** — estrutura e método das partidas dobradas
- **plano-de-contas.md** — contas utilizadas nos lançamentos
- **centro-de-custo.md** — distribuição por centro de custo
- **avaliacao-estoque.md** — métodos de avaliação para CMV e ajustes

## Restrições

- Lançamentos automáticos não substituem a revisão contábil
- Fechamento de período bloqueia novos lançamentos automáticos sem autorização
- Integração com fiscal: impostos apurados devem conferir com SPED Fiscal
- Log de auditoria obrigatório para todo lançamento gerado automaticamente

## Documentos Relacionados

- ERP — Módulo Faturamento (vendas)
- ERP — Módulo Compras
- ERP — Módulo Folha de Pagamento
- ERP — Módulo Financeiro
- ERP — Módulo Fiscal (apuração de impostos)
