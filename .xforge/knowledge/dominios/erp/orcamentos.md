---
id: erp-orcamentos
type: knowledge
tags: [erp, orcamentos, proposta-comercial, aprovacao, desconto, pipeline, conversao-pedido]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Módulo de Orçamentos
- **Principais responsabilidades**: Criar orçamentos com dados do cliente, itens (produto/serviço), quantidades, preços, descontos, condições de pagamento e validade.; Gerenciar tipos...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, orcamentos, proposta-comercial, aprovacao, desconto, pipeline, conversao-pedido
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-orcamentos` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Módulo de Orçamentos

## Propósito

Documentar o módulo de orçamentos do ERP, cobrindo criação de propostas comerciais, tipos de orçamento, alçadas de aprovação, controle de revisões, conversão em pedido, relatórios de pipeline e integração com CRM, estoque e financeiro.

## Responsabilidades

- Criar orçamentos com dados do cliente, itens (produto/serviço), quantidades, preços, descontos, condições de pagamento e validade.
- Gerenciar tipos de orçamento: venda de produtos, prestação de serviços, projeto (engenharia/construção), manutenção (recorrente), exportação.
- Aplicar alçadas de aprovação por valor e percentual de desconto (ex: até R$ 10k e 5% = vendedor; acima = supervisor/gerente/diretoria).
- Controlar revisões: cada alteração gera nova versão com histórico (antes/depois, data, usuário, motivo).
- Converter orçamento aprovado em pedido de venda automaticamente, mantendo vinculação com rastreabilidade.
- Controlar status: em elaboração, enviado, aprovado, recusado, expirado, convertido.
- Consultar disponibilidade de estoque ao inserir itens (🟢 disponível, 🟡 parcial, 🔴 indisponível).
- Simular impacto financeiro: parcelas, fluxo de caixa projetado, margem bruta estimada.
- Apurar relatórios: orçamentos por vendedor/cliente, pipeline por etapa, taxa de conversão, expirados (perda de oportunidade).
- Integrar com CRM (oportunidade → orçamento → pedido), estoque (consulta e reserva) e financeiro (condição de pagamento, análise de crédito).

## Dependências

- **fluxo-vendas.md** — Conversão em pedido, reserva de estoque, faturamento.
- **crm.md** — Oportunidades, pipeline, histórico de interações.
- **estoque.md** — Consulta de disponibilidade, reserva de estoque.

## Restrições

- Validade padrão: 15 a 30 dias (configurável por tipo, cliente ou vendedor).
- Orçamentos não podem ser fracionados para contornar alçadas de aprovação.
- Desconto impacta margem de lucro e comissão do vendedor (calculado sobre valor líquido).
- Orçamento em si não gera obrigação fiscal; a obrigação nasce no faturamento (emissão de NF-e).
- Taxa de conversão benchmark: varejo 25-35%, indústria 35-50%, serviços 40-60%, projetos 20-35%.
- CPC 47 (IFRS 15): orçamento aprovado representa o contrato comercial; receita reconhecida na entrega/prestação.

## Relacionados

- [fluxo-vendas.md](fluxo-vendas.md) — Pipeline de vendas e pedidos.
- [crm.md](crm.md) — Gestão de relacionamento com cliente.
- [estoque.md](estoque.md) — Controle de estoque e disponibilidade.

