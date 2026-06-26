---
id: vendas-pedido
type: knowledge
tags: [vendas, pedido, orcamento]
owner: commercial-team
version: "1.0"
updated: "2026-06-13"
---
# Ciclo do Pedido de Venda

1. **Orcamento**: lista de itens + condicoes (prazo, pagamento, entrega)
2. **Aprovacao interna**: limite por valor/regiao/condicao
3. **Pedido confirmado**: bloqueio de estoque
4. **Separacao**: picking no estoque
5. **Conferencia**: checagem vs pedido
6. **Expedicao**: NF-e + transporte
7. **Entrega**: comprovante de recebimento
8. **Faturamento**: titulo a receber + comissao

## Status de pedido
- 10 - Em orcamento
- 20 - Orcamento aprovado
- 30 - Pedido confirmado
- 40 - Em separacao
- 50 - Faturado
- 60 - Em transporte
- 70 - Entregue
- 90 - Cancelado