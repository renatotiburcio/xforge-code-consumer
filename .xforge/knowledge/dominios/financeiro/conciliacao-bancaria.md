---
id: fin-conciliacao-bancaria
type: dominio
tags: [financeiro, conciliacao, banco, extrato, ofx, cnab]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Verificar e confirmar que os registros contábeis correspondem aos extratos bancários reais.
- **Principais responsabilidades**: Importação de extratos (OFX, CNAB 240, CSV); Conciliação automática e manual; Identificação e correção de divergências
- **Seções principais**: Purpose, Responsabilities, Importação de Extratos, Conciliação Automática
- **Tags**: financeiro, conciliacao, banco, extrato, ofx, cnab
- **Tipo**: dominio | **Versão**: 2.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fin-conciliacao-bancaria` |
| Tipo | dominio |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 9 |


# Conciliação Bancária

## Purpose
Verificar e confirmar que os registros contábeis correspondem aos extratos bancários reais.

## Responsabilities
- Importação de extratos (OFX, CNAB 240, CSV)
- Conciliação automática e manual
- Identificação e correção de divergências
- Relatórios de conciliação

## Importação de Extratos
| Formato | Uso |
|---------|-----|
| OFX | Padrão para importação de extratos |
| CNAB 240 | FEBRABAN para cobrança/pagamento |
| CSV | Exportação manual de bancos |
| API Open Finance | Integração direta via Open Finance |

## Conciliação Automática
- Critérios: valor (±R$ 0,01), data (±1 dia), histórico/descrição
- Correspondência exata: valor e data idênticos
- Correspondência parcial: valor ou data aproximados
- Marcação automática de transações conciliadas

## Conciliação Manual
- Busca por valor, data ou descrição
- Vinculação manual ao lançamento contábil
- Justificativa para divergências
- Aprovação por responsável

## Diferenças Comuns
| Tipo | Causa | Ação |
|------|-------|------|
| Valor diferente | Juros, taxas, descontos não registrados | Ajuste contábil |
| Data diferente | Compensação bancária, feriados | Ajuste de período |
| Não identificado | Recebimento/pagamento sem registro | Complementar registro |
| Duplicidade | Lançamento duplicado | Estorno |

## Saldo Contábil vs. Saldo Bancário
```
Saldo contábil: registros internos da empresa
Saldo bancário: posição real na instituição financeira

Diferenças comuns:
- Cheques não compensados
- Depósitos em trânsito
- Taxas bancárias não registradas
- Juros/encargos não contabilizados
```

## Dependencies
- `dominios/financeiro/contas-a-pagar.md`
- `dominios/financeiro/contas-a-receber.md`
- `dominios/financeiro/fluxo-de-caixa.md`

## Related Documents
- `dominios/financeiro/pagamentos-digitais.md`
- `dominios/contabil/escrituracao-contabil.md`

