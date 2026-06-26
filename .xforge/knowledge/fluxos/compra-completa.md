---
id: compra-completa
type: fluxo
tags: [compras, procure-to-pay, 3-way-match, estoque, contas-pagar]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Fluxo de Compra Completa (Procure-to-Pay)
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: compras, procure-to-pay, 3-way-match, estoque, contas-pagar
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `compra-completa` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Fluxo de Compra Completa (Procure-to-Pay)

## Propósito
Documentar o fluxo ponta a ponta de compras: da necessidade interna ao pagamento ao fornecedor, incluindo 3-way match, controle fiscal e integrações.

## Etapas

1. **Requisição**: Solicitante identifica necessidade, preenche requisição com centro de custo, descrição, quantidade, prioridade (Normal/Urgente). Tipos: consumo, matéria-prima, ativo imobilizado, serviço.
2. **Aprovação Hierárquica**: Alçadas por valor — até R$5mil (gestor), até R$25mil (gerente), até R$100mil (diretor), acima (CEO/Proibido fracionar requisições).
3. **Cotação (RFQ)**: Enviada a mínimo 3 fornecedores. Critérios ponderados: preço (30-40%), prazo (15-25%), pagamento (15-20%), qualidade (15-20%), garantia e frete. Sistema gera tabela comparativa.
4. **Pedido de Compra**: Melhor cotação selecionada → PO emitido com fornecedor, itens, condições de pagamento, prazo de entrega, frete (CIF/FOB). Status: Em Aberto → Aprovado.
5. **Recebimento**: Conferência quantitativa (contagem física, lotes, tolerância ±5%) e qualitativa (inspeção visual, conformidade técnica). Divergências geram ficha de não-conformidade.
6. **NF-e de Entrada**: Importação do XML, validação na SEFAZ, confronto com pedido. Classificação fiscal: CFOP (1.101/2.101), CST ICMS/IPI/PIS/COFINS. Créditos apurados conforme regime (Lucro Real).
7. **3-Way Match**: Conciliação tripla — PO × Recebimento × NF-e. Pagamento só liberado com três documentos conciliados dentro da tolerância configurável.
8. **Pagamento**: Títulos gerados automaticamente com vencimentos conforme condição negociada. Formas: PIX, TED, boleto, cartão corporativo. Descontos por antecipação quando viáveis. Retenções de IRRF, INSS, CSLL, PIS, COFINS, ISS conforme serviço.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Quantidade > pedido? | Sim | Receber excedente com PO complementar ou recusar |
| Preço diferente? | Sim | Bloquear e acionar comprador |
| Qualidade divergente? | Sim | Quarentena → devolução ou aceite com desconto |
| 3-Way Match OK? | Não | Pagamento bloqueado |

## Integrações

- **Estoque**: entrada automática com custo de aquisição (preço + frete + seguro + impostos não recuperáveis), custo médio recalculado
- **Fiscal**: NF-e entrada, escrituração SPED Fiscal (Bloco C/E), apuração créditos ICMS/IPI/PIS/COFINS
- **Financeiro**: contas a pagar, conciliação bancária (CNAB/OFX/API), controle de vencimentos
- **Produção**: MRP gera requisições de compra automáticas para matéria-prima
- **eSocial/EFD-Reinf**: retenções de INSS, IRRF sobre serviços de terceiros

## Documentos Relacionados

- [Fluxo de Vendas](venda-completa.md)
- [Ordem de Produção](producao-ordem.md)
- [PDV/Frente de Caixa](pdv-venda.md)

