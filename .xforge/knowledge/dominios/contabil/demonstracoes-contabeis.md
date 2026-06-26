---
id: contabil-demonstracoes
type: domain
tags: [contabil, demonstracoes, dre, bp, dfc, dmpl, dva, notas-explicativas, lei-6404]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Demonstrações Contábeis
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, demonstracoes, dre, bp, dfc, dmpl, dva, notas-explicativas, lei-6404
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-demonstracoes` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# Demonstrações Contábeis

## Propósito

Apresentar a situação patrimonial, financeira e econômica da entidade conforme Lei 6.404/76 (Art. 176), Lei 11.638/2007, NBC TG 26 (CPC 26) e demais normas aplicáveis.

## Responsabilidades

**1. Balanço Patrimonial (BP)** — Obrigatório para todas as empresas.

| ATIVO | PASSIVO |
|-------|---------|
| **Circulante** | **Circulante** |
| Caixa e equivalentes | Fornecedores |
| Contas a receber | Obrigações trabalhistas |
| Estoques | Obrigações fiscais |
| Despesas antecipadas | Dividendos a pagar |
| **Não Circulante** | **Não Circulante** |
| Realizável longo prazo | Empréstimos longo prazo |
| Investimentos | Provisões |
| Imobilizado | Resultados exercícios futuros |
| Intangível | **Patrimônio Líquido** |
| | Capital social |
| | Reservas de capital |
| | Reservas de lucros |
| | Lucros/prejuízos acumulados |

Compensação entre ativo e passivo: **proibida**. ATIVO = PASSIVO + PL.

**2. Demonstração do Resultado do Exercício (DRE)**

`
(+) Receita Operacional Bruta
(-) Deduções (devoluções, abatimentos, ICMS, PIS, COFINS)
(=) Receita Operacional Líquida
(-) CMV / CPS
(=) Lucro Bruto
(-) Despesas Operacionais (vendas, administrativas, financeiras)
(=) Resultado Operacional
(+/-) Resultado Não Operacional
(=) Resultado antes do IRPJ/CSLL
(-) Provisão IRPJ
(-) Provisão CSLL
(=) Lucro/Prejuízo Líquido do Exercício
`

*Exemplo numérico:*
`
RECEITA BRUTA                          R$ 1.000.000
(-) Deduções (17%)                     R$  (170.000)
= RECEITA LÍQUIDA                      R$   830.000
(-) CMV                                R$  (400.000)
= LUCRO BRUTO                          R$   430.000
(-) Despesas com Vendas                R$   (50.000)
(-) Despesas Administrativas           R$  (120.000)
(-) Despesas com Pessoal               R$  (150.000)
= RESULTADO OPERACIONAL                R$   110.000
(+/-) Resultado Financeiro             R$   (10.000)
= RESULTADO ANTES IR/CSLL              R$   100.000
(-) IRPJ (15% + adicional)             R$   (25.000)
(-) CSLL (9%)                          R$    (9.000)
= LUCRO LÍQUIDO                        R$    66.000
`

**3. DLPA** — Demonstrativo dos Lucros ou Prejuízos Acumulados (S.A.)

`
(+) Saldo acumulado exercício anterior
(+) Lucro líquido do exercício
(-) Transferências para reservas (Legal, Estatutária, Contingências)
(-) Dividendos propostos
(-) Juros sobre Capital Próprio
(=) Saldo acumulado exercício seguinte
`

**4. DFC** — Demonstração dos Fluxos de Caixa (obrigatória para S.A. aberta e empresas com PL > R$ 2 milhões)

*Fluxo das Operações:* Lucro líquido + depreciação ± variação de ativos/passivos operacionais
*Fluxo dos Investimentos:* Aquisição/venda de ativos de longo prazo
*Fluxo do Financiamento:* Empréstimos, amortizações, dividendos pagos

Método direto (preferido) ou método indireto (mais comum).

**5. DVA** — Demonstração do Valor Adicionado (obrigatória para S.A. aberta)

`
(+) Receitas
(-) Insumos adquiridos de terceiros
(=) Valor adicionado bruto
(-) Depreciação/amortização
(+) Valor adicionado recebido de terceiros
(=) VALOR ADICIONADO A DISTRIBUIÇÃO
  (-) Pessoal, Tributos, Juros, Dividendos, Lucros retidos
`

**6. Notas Explicativas** — Obrigatórias para todas as empresas.

Conteúdo mínimo (16 itens): identificação (CNPJ, atividade), base de preparação (regime competência, moeda), práticas contábeis (estoques, depreciação, PDD, contingências, receitas), composição de caixa, clientes, estoques, imobilizado, intangível, empréstimos, provisões, patrimônio líquido, resultado, instrumentos financeiros, eventos subsequentes, partes relacionadas.

## Dependências

- **lei-sa-6404-1976.md** — base legal das demonstrações (Art. 176-188)
- **normas-contabeis.md** — NBC TG 26 / CPC 26
- **escrituracao-contabil.md** — regime de competência como base de reconhecimento

## Restrições

- Demonstrações comparativas (exercício atual e anterior) obrigatórias
- Elaboração anual no encerramento do exercício social
- Reconhecimento pelo regime de competência
- Não compensar ativos com passivos
- Assinatura do contador e do administrador obrigatória
- Prescrição: 10 anos (S.A. aberta), 5 anos (S.A. fechada), 3 anos (limitadas)

## Documentos Relacionados

- Lei 6.404/76, Art. 176-188
- Lei 11.638/2007
- NBC TG 26 / CPC 26
- CFC Resolução 1.111/2007
- CPC 03 (DFC), CPC 09 (DVA)
