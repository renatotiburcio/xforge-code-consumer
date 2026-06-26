---
name: procurement-purchasing-expert
description: Expert em compras: solicitação, cotação, aprovação, ordem de compra, contratos e avaliação de fornecedores.
metadata:
  version: "1.0.0"
  xforge-category: "domain-expert"
---

# procurement-purchasing-expert

## Objetivo

Gerenciar o ciclo completo de compras empresariais com rastreabilidade e conformidade.

## Ciclo de Compras

```
Solicitação → Cotação → Aprovação → Ordem de Compra → Recebimento → Faturamento → Pagamento
```

## Fases Detalhadas

### 1. Solicitação de Compra (SC)
- Solicitante preenche: item, quantidade, especificação, urgência
- Aprovação do gestor do setor
- Verificação de estoque (existe? pode transferir?)
- SC Number sequencial

### 2. Cotação
- Mínimo 3 cotações para valores acima de R$ 10.000
- Formato: RFQ (Request for Quadrilho) ou portal de compras
- Cotação deve conter: item, unidade, quantidade, valor unitário, prazo entrega, validade
- Anexo de proposta comercial do fornecedor

### 3. Aprovação
| Valor | Aprovação |
|-------|-----------|
| Até R$ 1.000 | Gestor do setor |
| R$ 1.001 - R$ 10.000 | Diretor do setor |
| R$ 10.001 - R$ 50.000 | Conselho |
| Acima R$ 50.000 | Diretoria Executiva |

### 4. Ordem de Compra (OC)
- Número sequencial
- Referência à SC e cotação
- Dados do fornecedor: CNPJ, razão social, endereço
- Itens com código, descrição, quantidade, valor, total
- Condições: pagamento, frete, garantia
- Prazo de entrega

### 5. Recebimento
- Conferência física (quantidade e qualidade)
- Nota fiscal vs OC vs pedido
- Registro de divergências
- Aprovação do recebimento

### 6. Conciliação 3-Way
- Ordem de Compra = Nota Fiscal = Recebimento
- Divergências geram bloqueio de pagamento

## Avaliação de Fornecedores

| Critério | Peso | Métrica |
|----------|:----:|---------|
| Qualidade | 30% | % de peças aprovadas |
| Prazo | 25% | % de entregas no prazo |
| Preço | 20% | Comparativo de mercado |
| Confiabilidade | 15% | Histórico de entregas |
| Suporte | 10% | Tempo de resposta |

## Procedimento

1. Receber solicitação
2. Verificar estoque/transferência
3. Criar RFQ e cotar
4. Avaliar cotações
5. Aprovar conforme matrix
6. Gerar OC
7. Acompanhar entrega
8. Conferir recebimento
9. Conciliar 3-way
10. Liberar pagamento

## Regras

- Toda compra > R$ 10.000 exige 3 cotações
- OC sempre referenciar SC
- Recebimento sempre conferido fisicamente
- Conciliação 3-way obrigatória
- Fornecedores avaliados semestralmente
