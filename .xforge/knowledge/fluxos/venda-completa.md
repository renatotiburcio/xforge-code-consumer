---
id: venda-completa
type: fluxo
tags: [vendas, faturamento, nf-e, comissão, recebimento]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Fluxo de Venda Completa
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: vendas, faturamento, nf-e, comissão, recebimento
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `venda-completa` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Fluxo de Venda Completa

## Propósito
Documentar o fluxo ponta a ponta de vendas no ERP , desde a cotação até o recebimento e comissionamento, incluindo pontos de decisão e integrações.

## Etapas

1. **Cotação**: Vendedor consulta cadastro do cliente e tabela de preços, monta orçamento com itens, condições de pagamento e validade (padrão 15-30 dias). Envia ao cliente por PDF/email.
2. **Aprovação**: Orçamentos que excedem limites de desconto/valor passam por alçadas hierárquicas (vendedor até diretor comercial). Sistema registra identidade e data/hora de cada aprovador.
3. **Pedido de Venda**: Orçamento aprovado é convertido automaticamente em pedido. Status inicia como "Em Aberto". Dados incluem cliente, vendedor, CFOP, CST, NCM, alíquotas de ICMS/IPI/PIS/COFINS.
4. **Crédito e Reserva**: Financeiro aprova limite de crédito. Sistema reserva estoque. Se indisponível → bloquear, backorder ou gerar requisição de produção.
5. **Separação e Expedição**: Romaneio de picking gerado. Conferência quantitativa com leitor de código de barras. Embalagem, etiquetagem e romaneio de entrega.
6. **Faturamento (NF-e)**: Geração automática a partir do pedido. Assinatura digital (certificado A1/A3), validação XSD, transmissão à SEFAZ via webservice. Se falha → contingência (FS-DA, SVC, EPEC).
7. **Transporte**: Emissão de CT-e ou MDF-e vinculado à NF-e. Rastreamento com comprovante de entrega (POD).
8. **Recebimento**: Títulos gerados automaticamente no contas a receber. Formas: boleto, PIX, cartão. Conciliação bancária via CNAB/OFX. Juros (1%/mês) e multa (2%) por atraso.
9. **Comissão**: Calculada sobre valor líquido, recebido ou margem de contribuição. Regras por produto, cliente, vendedor, faixa de valor, meta. Pagamento no faturamento ou recebimento.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Crédito aprovado? | Não | Pedido bloqueado |
| Estoque disponível? | Não | Backorder / produzir |
| Transmissão SEFAZ OK? | Não | Contingência |
| Pagamento recebido? | Não | Cobrança com juros+multa |
| Devolução solicitada? | Sim | NF-e devolução (CFOP 5.201) |

## Integrações

- **Estoque**: reserva/estorno automático de mercadorias
- **Fiscal**: emissão NF-e/NFC-e, CT-e, MDF-e; SPED Fiscal; DIFAL/substituição tributária
- **Financeiro**: títulos a receber, conciliação bancária, cobrança
- **Contábil**: CPC 47 (receita), CPC 48 (instrumentos financeiros)
- **eSocial**: S-2210 (CAT) se acidente no transporte
- **CRM**: pipeline de vendas, follow-up automático, histórico de interações

## Documentos Relacionados

- [Fluxo de Compras](compra-completa.md)
- [Ordem de Produção](producao-ordem.md)
- [PDV/Frente de Caixa](pdv-venda.md)

