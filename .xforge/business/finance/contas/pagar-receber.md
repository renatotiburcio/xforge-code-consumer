---
id: contas-pagar-receber
type: knowledge
tags: [contas-pagar, contas-receber, aging]
owner: finance-team
version: "1.0"
updated: "2026-06-13"
---
# Contas a Pagar e Receber

## Status de titulo
- 10 - Aberto (previsto)
- 20 - Programado (data agendada)
- 30 - Pago / Recebido
- 40 - Vencido
- 50 - Cancelado
- 60 - Em protesto / Cobranca
- 90 - Baixado (perda)

## Aging list (faixas)
- A vencer: 0-30 dias
- Vencido 1-30: amarelo
- Vencido 31-60: laranja
- Vencido 61-90: vermelho
- Vencido 90+: critico (protesto, perda)

## Calculo de provisoes
```
Perdas estimadas = sum( titulo.valor * provisao[faixa] )
Ex: 31-60 = 30%, 61-90 = 50%, 90+ = 100%
```

## Multa e juros
- Multa: 2% sobre valor original
- Juros: 1% ao mes (pro-rata dias)
- Total = Original * (1 + 0.02) * (1 + 0.01 * dias/30)