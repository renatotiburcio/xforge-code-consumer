---
id: contabil-avaliacao-estoque
type: domain
tags: [contabil, estoque, avaliacao, peps, cmps, ueps, cmv, cpc-16, nbc-tg-16]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Avaliação de Estoque
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, estoque, avaliacao, peps, cmps, ueps, cmv, cpc-16, nbc-tg-16
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-avaliacao-estoque` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# Avaliação de Estoque

## Propósito

Definir os métodos de avaliação de estoques, critérios de registro e tratamento contábil de perdas e ajustes, em conformidade com CPC 16 (NBC TG 16), Lei 6.404/76 e legislação fiscal.

## Responsabilidades

**Conceito:** Estoque são bens mantidos para venda, em processo de produção ou como materiais a serem consumidos na produção/prestação de serviços.

**Classificação por Tipo de Empresa:**

| Comercial | Industrial | Serviços |
|-----------|------------|----------|
| Mercadorias para revenda | Produtos acabados | Materiais de consumo |
| | Produtos em fabricação | Serviços em andamento |
| | Matérias-primas | |
| | Materiais auxiliares | |

**Métodos de Avaliação (CPC 16):**

| Método | Descrição | Aceito Fiscal? |
|--------|-----------|----------------|
| **PEPS** (Primeiro a Entrar, Primeiro a Sair) | Primeiros itens adquiridos são os primeiros vendidos | Sim |
| **UEPS** (Último a Entrar, Primeiro a Sair) | Últimos itens adquiridos são os primeiros vendidos | **Não** |
| **Custo Médio Ponderado** | Média ponderada dos custos | Sim |
| **Custo Específico** | Custo identificado por item | Sim |
| **VRL** (Valor Realizável Líquido) | Preço estimado de venda (-) custos de venda | Sim (quando menor) |

**Regra:** UEPS **não é aceito** para fins fiscais no Brasil (IN RFB 1.700/2017).

**Custo de Aquisição:**
`
Custo = Preço de compra (-) deduções + transporte + manuseio + custos diretamente atribuíveis (-) créditos tributários recuperáveis
`

**Custo Médio Ponderado Móvel:**
`
Nova Média = (Estoque Atual × Custo Anterior) + (Entrada × Custo Atual) / Quantidade Total

Exemplo: 100 un × R$ 10 = R$ 1.000 + 50 un × R$ 12 = R$ 600
Nova Média = R$ 1.600 / 150 = R$ 10,67/un
`

**Redução ao Valor Recuperável (Impairment):**
`
Se Custo > VRL:
  Provisão = Custo - VRL
  D: Despesa (Resultado) / C: Provisão (Ativo)
VRL = Preço estimado de venda - Custos de venda - Custos de acabamento
`

**Provisão para Estoques:** Obrigatória para itens obsoletos, danificados, lentos ou vencidos.

**Perdas de Estoque:**

| Tipo | Registro |
|------|----------|
| Perda normal (quebras) | CMV |
| Perda anormal (roubo, incêndio) | Outras despesas operacionais |
| Vencimento | Despesa |

**Inventário:** Obrigatório no mínimo 1 vez por ano. Tipos: periódico, permanente, rotativo, geral. Ganho no inventário → outras receitas; perda → outras despesas.

**Integração com CMV:** A baixa de estoque na venda gera o lançamento de CMV (D: CMV / C: Estoque), impactando diretamente o resultado bruto.

## Dependências

- **escrituracao-contabil.md** — lançamentos de compra, CMV e ajuste
- **contabilidade-custos.md** — métodos de custeio e formação de preço
- **ecd.md** — registro H005/H010 (inventário no SPED Fiscal)

## Restrições

- Avaliação pelo custo ou VRL, o que for menor
- UEPS proibido fiscalmente
- Provisão para perdas obrigatória quando identificada
- Inventário anual obrigatório
- Documentação de inventário: laudo, relatório, planilha

## Documentos Relacionados

- NBC TG 16 / CPC 16 (Estoques)
- Lei 6.404/76, Art. 183
- IN RFB 1.700/2017
- SPED Fiscal — Registros H005, H010
