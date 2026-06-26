---
id: crm-pipeline
type: knowledge
tags: [crm, pipeline, kanban]
owner: commercial-team
version: "1.0"
updated: "2026-06-13"
---
# Pipeline de Vendas

## Campos obrigatorios
- Lead / Conta
- Estagio
- Valor estimado
- Probabilidade (%)
- Data esperada de fechamento
- Proprietario (vendedor)
- Origem (marketing, indicacao, prospeccao)
- Proximo passo (data + descricao)

## Calculo de comissao
```
Comissao Base = Valor Vendido * % Comissao por Estagio
Bonus Meta = (Total Vendido > Meta) ? Bonus : 0
Comissao Total = Comissao Base + Bonus Meta
```

## KPIs principais
- **Win Rate**: % de oportunidades ganhas
- **Ticket Medio**: receita total / numero de vendas
- **Cycle Time**: dias entre criacao e fechamento
- **Forecast Accuracy**: real vs projetado
- **CAC** (Custo de Aquisicao): investimento marketing / clientes novos
- **LTV** (Lifetime Value): receita media * tempo medio de retencao