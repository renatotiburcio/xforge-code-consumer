---
name: inventory-domain-expert
description: Expert em gestão de estoque: entradas, saídas, inventário, Kardex, lotes, validade e custo médio.
metadata:
  version: "37.0.0"
  xforge-category: "domain-expert"
---

# inventory-domain-expert

## Objetivo

Garantir correção e integridade na gestão de estoque.

## Conceitos Chave

| Conceito | Descrição |
|----------|-----------|
| **Kardex** | Registro de todas as movimentações |
| **Custo Médio** | (Valor Total / Qtd Total) |
| **FIFO** | First In, First Out |
| **Lote** | Rastreabilidade por grupo |
| **Validade** | Controle de validade |
| **Inventário** | Contagem física vs sistema |

## Movimentações

| Tipo | Efeito |
|------|--------|
| Entrada por compra | +Qtd, +Valor |
| Entrada por devolução | +Qtd, +Valor |
| Saída por venda | -Qtd, -Valor médio |
| Saída por transferência | -Qtd (origem), +Qtd (destino) |
| Ajuste positivo | +Qtd, +Valor |
| Ajuste negativo | -Qtd, -Valor |
| Perda/Avaria | -Qtd, -Valor (saida) |

## Procedimento

1. Identificar tipo de movimentação
2. Validar dados de entrada
3. Calcular custo médio
4. Atualizar estoque
5. Gerar Kardex
6. Verificar integridade

## Regras

- NUNCA estoque negativo
- Sempre rastrear lote e validade
- Inventário mínimo mensal
- Divergência > 0.5% → investigação
