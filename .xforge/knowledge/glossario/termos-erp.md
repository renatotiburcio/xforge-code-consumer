---
id: glossario-005
type: glossary
tags: [erp, negocio, pdv, estoque, financeiro, fiscal, crm, producao]
owner: 
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Glossário de Termos de ERP e Negócio
- **Seções principais**: Apontamento, Boleto, CNAB, Comissão
- **Tags**: erp, negocio, pdv, estoque, financeiro, fiscal, crm, producao
- **Tipo**: glossary | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `glossario-005` |
| Tipo | glossary |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner |  |
| Total de seções | 24 |


# Glossário de Termos de ERP e Negócio

## Apontamento
Registro da produção efetuada em uma Ordem de Produção. Informa: quantidade produzida, tempo gasto, máquina utilizada, operador, eventuais perdas ou refugos. Alimenta o controle de estoque (entrada de produto acabado) e o cálculo de custo de produção. Relacionado: Ordem de Produção, Roteiro, Produção, Estoque, Custo.

## Boleto
Título de cobrança bancária regulamentado pela FEBRABAN. Formas de registro: com registro (enviado ao banco via CNAB) e sem registrado. Pode ser gerado via API bancária ou por sistema próprio. Status: emitido, registrado, pago, vencido, cancelado. Relacionado: CNAB, Contas a Receber, PIX, Faturamento, Gateway de Pagamento.

## CNAB
**Cenário Nacional de Padrões para Automação Bancária.** Padrão de arquivo (CNAB 240 ou 400) utilizado para troca de informações entre empresas e bancos. Usado para: emissão de boletos, conciliação bancária, pagamento de fornecedores/funcionários, recebimento via boleto. Relacionado: Boleto, PIX, Open Finance, Contas a Pagar, Contas a Receber, Conciliação.

## Comissão
Remuneração variável paga a vendedores, representantes ou intermediários por vendas realizadas ou metas atingidas. Pode ser por percentual sobre o valor da venda ou valor fixo por unidade. Integra a base de cálculo de INSS, IRRF e FGTS. Relacionado: PDV, Faturamento, CRM, S-1010, S-1200, Rescisão.

## Conciliação Bancária
Processo de comparar os registros financeiros internos (contas a pagar, contas a receber) com os extratos bancários. Identifica divergências, pagamentos não registrados e recebimentos não conciliados. Pode ser automatizada via CNAB ou Open Finance. Relacionado: CNAB, Fluxo de Caixa, Contas a Pagar, Contas a Receber, Open Finance.

## Contas a Pagar
Obrigações financeiras da empresa com fornecedores, prestadores de serviço, impostos e despesas operacionais. Registrado no Passivo Circulante. Gestão eficiente evita juros, multas e perda de crédito. Relacionado: Fluxo de Caixa, CNAB, Fornecedor, DRE, Working Capital.

## Contas a Receber
Direitos de recebimento da empresa provenientes de vendas a prazo, contratos e outros créditos. Registrado no Ativo Circulante. Gestão inclui controle de vencimentos, cobrança e conciliação. Relacionado: Faturamento, Boleto, PIX, CNAB, Fluxo de Caixa, Inadimplência.

## CRM
**Customer Relationship Management.** Módulo ou sistema de gestão do relacionamento com clientes. Armazena dados de contato, histórico de interações, oportunidades de venda, funil de vendas e pós-venda. Integrado ao módulo de vendas e faturamento. Relacionado: PDV, Faturamento, Comissão, Pipeline, Marketing.

## Estoque
Conjunto de bens destinados à venda (mercadorias), produção (matéria-prima, insumos) ou consumo (material de escritório). Controlado por: entradas (compras, produção), saídas (vendas, consumo) e saldo. Métodos de avaliação: PEPS, UEPS, Custo Médio. Relacionado: NF-e, CMV, Balanço Patrimonial, Inventário, Produção.

## Faturamento
Receita bruta gerada pela venda de produtos ou prestação de serviços. Inclui emissão de NF-e/NFC-e, geração de duplicatas/boletos, registro contábil e financeiro. Base para cálculo de impostos sobre vendas (ICMS, PIS, COFINS, ISS). Relacionado: NF-e, NFC-e, Contas a Receber, DRE, ICMS, PIS, COFINS.

## Fluxo de Caixa
Controle de entradas e saídas de recursos financeiros em um período. Projeção de disponibilidade para honrar compromissos. Tipos: operacional (vendas, compras), investimento (aquisição de ativos), financiamento (empréstimos, dividendos). Relacionado: DFC, Contas a Pagar, Contas a Receber, Capital de Giro, DRE.

## Frente de Caixa
Estabelecimento comercial onde são realizadas as vendas ao consumidor. Inclui: balança, leitor de código de barras, impressora fiscal (NFC-e/SAT), terminal de pagamento (TEF), registro de operações. Relacionado: PDV, NFC-e, SAT, TEF, Estoque, Faturamento.

## GED
**Gerenciamento Eletrônico de Documentos.** Sistema para armazenamento, indexação, busca e controle de versão de documentos digitais (contratos, notas fiscais XML, laudos, relatórios). Pode incluir assinatura digital e workflow de aprovação. Relacionado: NF-e, XML, Assinatura Digital, Workflow, Arquivo.

## Inventário
Levantamento físico de todos os itens em estoque para conferência com os registros contábeis e fiscais. Obrigatório para elaboração do Balanço Patrimonial. Divergências ajustadas via nota de entrada/saída. Relacionado: Estoque, Balanço Patrimonial, CMV, NF-e, Perda.

## Nota Fiscal (NF-e/NFC-e)
Documento fiscal eletrônico que formaliza a venda de produto ou serviço. NF-e (modelo 55) para operações entre PJ; NFC-e (modelo 65) para venda ao consumidor final. Contém: emitente, destinatário, produtos, impostos, totais, chave de acesso (44 dígitos). Relacionado: Faturamento, CFOP, ICMS, PIS, COFINS, SPED, Estoque.

## Open Finance
Evolução do Open Banking no Brasil, regululado pelo Banco Central. Permite compartilhamento de dados financeiros entre instituições via APIs padronizadas. Casos de uso: iniciação de pagamento PIX, consulta de saldo, oferta de crédito, conciliação bancária automática. Relacionado: PIX, CNAB, Conciliação Bancária, API, Banco Central.

## Ordem de Produção (OP)
Documento que formaliza a fabricação de um produto. Contém: produto a ser produzido, quantidade, matéria-prima necessária (BOM), roteiro de fabricação, prazo e recursos alocados. Gera movimentações de estoque (consumo de insumos, entrada de produto acabado). Relacionado: Roteiro, Apontamento, Estoque, Produção, MRP.

## PIX
Sistema de pagamento instantâneo criado pelo Banco Central (BCB). Transferências em tempo real (24/7) via chave PIX (CPF, e-mail, telefone, chave aleatória). Substitui TED/DOC para pagamentos de baixo valor. Integrado ao Open Finance. Relacionado: Open Finance, Boleto, Contas a Pagar, Contas a Receber, Gateway de Pagamento.

## Plano de Contas
Estrutura hierárquica que organiza todas as contas contábeis da empresa (ativos, passivos, receitas, despesas). Serve de base para escrituração, classificação e elaboração das demonstrações financeiras. Relacionado: Partida Dobrada, ECD, Lançamento Contábil, Centro de Custo.

## PDV
**Ponto de Venda.** Terminal utilizado para registrar vendas ao consumidor final. Inclui: emissão de NFC-e ou CF-e (SAT), pagamento (dinheiro, cartão, PIX), controle de estoque em tempo real, integração com retaguarda. Relacionado: Frente de Caixa, NFC-e, SAT, TEF, Estoque, Faturamento.

## Produção
Módulo responsável pelo planejamento e controle da fabricação de produtos. Inclui: MRP (Planejamento de Necessidades de Materiais), Ordens de Produção, Roteiros de Fabricação, Apontamento, Controle de Qualidade. Integrado com Estoque, Compras e Financeiro. Relacionado: Ordem de Produção, Roteiro, Apontamento, Estoque, MRP.

## Roteiro de Fabricação
Sequência de operações e etapas necessárias para fabricar um produto. Define: centros de trabalho, tempos padrão, ferramentas, insumos por etapa, parâmetros de qualidade. Base para cálculo de custo de produção e capacidade produtiva. Relacionado: Ordem de Produção, Produção, Apontamento, Estoque, MRP.

## TEF
**Transferência Eletrônica de Fundos.** Sistema que integra o PDV/POS com as administradoras de cartão de crédito/débito. Padrões: TEF Discado, TEF Dedicado, IPOS. Permite pagamento via cartão no ponto de venda com autorização online. Relacionado: PDV, Frente de Caixa, Gateway de Pagamento, NFC-e, Faturamento.

## Venda
Transação comercial de produtos ou serviços. No ERP, envolve: orçamento, pedido, faturamento (NF-e), baixa de estoque, geração de conta a receber, comissionamento. Pode ser presencial (PDV), e-commerce ou B2B. Relacionado: PDV, Faturamento, NF-e, Estoque, Contas a Receber, Comissão, CRM.

