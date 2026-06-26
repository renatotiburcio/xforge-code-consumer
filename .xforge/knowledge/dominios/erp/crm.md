---
id: erp-crm
type: knowledge
tags: [erp, crm, clientes, pipeline-vendas, interacoes, segmentacao, relatorios]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre CRM — Gestão de Relacionamento com o Cliente
- **Principais responsabilidades**: Manter cadastro completo de clientes: dados pessoais (CPF/CNPJ, RG/IE), endereço, contato, dados bancários, segmento, limite de crédito.; Gerenciar...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, crm, clientes, pipeline-vendas, interacoes, segmentacao, relatorios
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-crm` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# CRM — Gestão de Relacionamento com o Cliente

## Propósito

Documentar o módulo de CRM do ERP, cobrindo cadastro de clientes, pipeline de vendas, histórico de interações, segmentação, relatórios e integração com o fluxo de vendas e orçamentos.

## Responsabilidades

- Manter cadastro completo de clientes: dados pessoais (CPF/CNPJ, RG/IE), endereço, contato, dados bancários, segmento, limite de crédito.
- Gerenciar pipeline de vendas: prospecção → contato inicial → proposta/orçamento → negociação → fechamento (pedido) → pós-venda.
- Registrar histórico de interações: ligações, e-mails, reuniões, visitas, orçamentos enviados, pedidos realizados, ocorrências e reclamações.
- Configurar follow-up automático: lembretes de orçamentos sem resposta, clientes sem compra, renovação de contratos.
- Segmentar clientes por perfil: região, porte, segmento de mercado, frequência de compra, ticket médio.
- Apurar relatórios: funil de vendas por estágio, taxa de conversão, vendedor × cliente, sazonalidade, motivos de recusa.
- Integrar com vendas: oportunidades → orçamentos → pedidos → faturamento → financeiro.
- Controlar limite de crédito: consulta na aprovação de orçamento/pedido, bloqueio automático se excedido.

## Dependências

- **fluxo-vendas.md** — Conversão de oportunidade em orçamento e pedido.
- **orcamentos.md** — Propostas comerciais vinculadas a oportunidades do CRM.
- **faturamento.md** — Faturamento e geração de contas a receber por cliente.

## Restrições

- Cadastro de cliente deve incluir CNPJ/CPF válido e situação cadastral consultada.
- Limite de crédito deve ser respeitado na aprovação de pedidos (configurável por cliente).
- Dados pessoais de clientes (CPF, RG, endereço) estão sujeitos à LGPD.
- Histórico de interações deve ser mantido para rastreabilidade comercial.
- Segmentação deve permitir filtros combinados para campanhas e análises.

## Relacionados

- [fluxo-vendas.md](fluxo-vendas.md) — Pipeline de vendas e faturamento.
- [orcamentos.md](orcamentos.md) — Orçamentos e propostas comerciais.
- [faturamento.md](faturamento.md) — Emissão de documentos fiscais.

