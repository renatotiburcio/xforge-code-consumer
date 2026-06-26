---
id: fin-contas-receber
type: dominio
tags: [financeiro, contas-a-receber, clientes, recebimento, cobranca]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Gerenciar direitos de recebimento de clientes por vendas de mercadorias e prestação de serviços.
- **Principais responsabilidades**: Cadastro de clientes (CNPJ/CPF, IE/IM, endereço cobrança/entrega, limite crédito); Lançamento de títulos (valor, vencimento, NF-e vinculada, parcel...
- **Seções principais**: Purpose, Responsibilities, Formas de Recebimento, Cobrança
- **Tags**: financeiro, contas-a-receber, clientes, recebimento, cobranca
- **Tipo**: dominio | **Versão**: 2.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fin-contas-receber` |
| Tipo | dominio |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 10 |


# Contas a Receber

## Purpose
Gerenciar direitos de recebimento de clientes por vendas de mercadorias e prestação de serviços.

## Responsibilities
- Cadastro de clientes (CNPJ/CPF, IE/IM, endereço cobrança/entrega, limite crédito)
- Lançamento de títulos (valor, vencimento, NF-e vinculada, parcelamento)
- Cobrança (automática e manual)
- Conciliação de recebimentos
- Controle de inadimplência e PDD
- Contabilização automática

## Formas de Recebimento
| Forma | Liquidação |
|-------|------------|
| PIX | Imediato (QR Code estático/dinâmico) |
| Boleto | D+1 a D+3 |
| Cartão crédito | D+30 (ou conforme contrato) |
| Cartão débito | D+1 |
| Dinheiro | Imediato |
| Cheque | D+1 a D+3 |

## Cobrança
### Automática
- E-mail: boleto, lembretes (5 dias antes, no vencimento, 5 dias após)
- SMS: alertas de vencimento e atraso
- WhatsApp: comunicação direta

### Manual
- Telefone: contato direto
- Visita: inadimplência prolongada
- Notificação formal: carta, notificação extrajudicial
- Negociação: parcelamento, desconto para quitação

## Juros e Multa por Atraso
- Multa: 2% sobre valor do título
- Juros: 1% ao mês (pro rata die)
- Registro: receita financeira
- Base legal: Código Civil, art. 397 e 406

## Negativação / Protesto
- Negativação: SPC/Serasa (mínimo 30 dias de atraso)
- Protesto: cartório de protesto (custos de cartório)
- Efeito: restrição de crédito ao devedor

## Provisão para Devedores Duvidosos (PDD)
| Faixa atraso | Percentual sugerido |
|--------------|-------------------|
| 31-60 dias | 10% |
| 61-90 dias | 25% |
| 91-120 dias | 50% |
| 121-180 dias | 75% |
| +180 dias | 100% |

- Registro: despesa operacional (conta redutora de clientes)
- Estorno se houver recebimento posterior
- Base legal: Lei 6.404/76, art. 183; CPC 48

## Contabilização
```
Na venda:
  DÉBITO: Contas a Receber
  CRÉDITO: Receita Bruta

No recebimento:
  DÉBITO: Banco
  CRÉDITO: Contas a Receber

PDD:
  DÉBITO: Despesas - PDD
  CRÉDITO: Provisão para DD
```

## Dependencies
- `dominios/contabil/plano-de-contas.md`
- `dominios/contabil/avaliacao-estoque.md`
- `dominios/fiscal/nfe.md`

## Related Documents
- `dominios/financeiro/contas-a-pagar.md`
- `dominios/financeiro/pagamentos-digitais.md`
- `dominios/financeiro/fluxo-de-caixa.md`
- `dominios/erp/crm.md`

