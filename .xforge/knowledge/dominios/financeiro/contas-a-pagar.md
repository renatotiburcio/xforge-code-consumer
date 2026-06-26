---
id: fin-contas-pagar
type: dominio
tags: [financeiro, contas-a-pagar, fornecedores, pagamento]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Gerenciar obrigações financeiras da empresa com fornecedores, prestadores de serviço e demais credores.
- **Principais responsabilidades**: Cadastro de fornecedores (CNPJ, IE, endereço, dados bancários, condições comerciais); Lançamento de títulos (valor, vencimento, forma de pagamento,...
- **Seções principais**: Purpose, Responsibilities, Tipos de Despesas, Formas de Pagamento
- **Tags**: financeiro, contas-a-pagar, fornecedores, pagamento
- **Tipo**: dominio | **Versão**: 2.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fin-contas-pagar` |
| Tipo | dominio |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 11 |


# Contas a Pagar

## Purpose
Gerenciar obrigações financeiras da empresa com fornecedores, prestadores de serviço e demais credores.

## Responsibilities
- Cadastro de fornecedores (CNPJ, IE, endereço, dados bancários, condições comerciais)
- Lançamento de títulos (valor, vencimento, forma de pagamento, centro de custo)
- Agendamento e aprovação de pagamentos
- Conciliação de pagamentos realizados
- Contabilização automática

## Tipos de Despesas
| Categoria | Exemplos |
|-----------|----------|
| Fixas | Aluguel, salários, energia, internet, seguros, SaaS |
| Variáveis | Matéria-prima, comissões, frete, embalagens |
| Compras | Mercadorias, materiais, equipamentos, manutenção |
| Folha | Salários, férias, 13º, FGTS, INSS, VT, VR |
| Impostos | ICMS, ISS, PIS, COFINS, IRPJ, CSLL, IPTU |

## Formas de Pagamento
| Forma | Liquidação |
|-------|------------|
| PIX | Imediato |
| TED | Mesmo dia (horário comercial) |
| Boleto | D+1 a D+3 |
| Cheque | D+1 a D+3 (compensação) |
| Cartão crédito | Conforme contrato (D+30 típico) |
| Débito automático | D+1 |

## Fluxo de Aprovação
1. Lançamento do título → 2. Verificação de 3-way match (pedido NF-e × recebimento) → 3. Aprovação por valor → 4. Agendamento → 5. Pagamento → 6. Conciliação → 7. Contabilização

## Desconto por Antecipação
```
Valor desconto = Valor nominal × Taxa × (Dias antecipados / 30)
```
Diferença registrada como receita financeira.

## Juros e Multa por Atraso
- Multa: 2% sobre valor do título
- Juros: 1% ao mês (pro rata die)
- Base legal: Código Civil, art. 406

## Conciliação
- Automática: por valor, data e beneficiário
- Manual: para casos sem correspondência
- Frequência recomendada: diária ou semanal

## Contabilização
```
Na emissão:
  DÉBITO: Despesa / Estoque
  CRÉDITO: Fornecedores

No pagamento:
  DÉBITO: Fornecedores
  CRÉDITO: Banco
```

## Dependencies
- `dominios/contabil/plano-de-contas.md`
- `dominios/contabil/lancamentos-automatizados.md`
- `dominios/fiscal/nfe.md` (para 3-way match)

## Related Documents
- `dominios/financeiro/contas-a-receber.md`
- `dominios/financeiro/conciliacao-bancaria.md`
- `dominios/financeiro/fluxo-de-caixa.md`

