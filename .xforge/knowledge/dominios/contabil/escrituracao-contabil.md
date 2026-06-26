---
id: contabil-escrituracao
type: domain
tags: [contabil, escrituracao, partidas-dobradas, lancamentos, competencia]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Escrituração Contábil
- **Principais responsabilidades**: Data do lançamento; Conta(s) debitada(s); Conta(s) creditada(s)
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, escrituracao, partidas-dobradas, lancamentos, competencia
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-escrituracao` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# Escrituração Contábil

## Propósito

Registrar todos os fatos administrativos que afetam o patrimônio da entidade pelo método das partidas dobradas, em conformidade com a Lei 6.404/76, Código Civil (Art. 1.179) e NBC TG 23.

## Responsabilidades

**Método das Partidas Dobradas:** Para cada lançamento, o total dos débitos é igual ao total dos créditos.

**Estrutura do Lançamento:**
1. Data do lançamento
2. Conta(s) debitada(s)
3. Conta(s) creditada(s)
4. Histórico claro e completo
5. Valor
6. Centro de custo (quando aplicável)

**Fórmulas de Lançamento:**

| Fórmula | Descrição |
|---------|-----------|
| 1ª | Uma conta debitada, uma conta creditada |
| 2ª | Uma conta debitada, duas ou mais creditadas |
| 3ª | Duas ou mais debitadas, uma creditada |
| 4ª | Duas ou mais debitadas, duas ou mais creditadas |

**Exemplos de Lançamentos:**

*Venda de mercadoria (R$ 10.000,00, a prazo):*
`
D: Contas a Receber          R$ 10.000,00
C: Receita Bruta de Vendas   R$ 10.000,00
`

*Compra de mercadoria (R$ 5.000,00 + ICMS R$ 900,00):*
`
D: Estoque - Mercadorias     R$ 5.000,00
D: ICMS a Recuperar          R$   900,00
C: Fornecedores              R$ 5.900,00
`

*CMV (R$ 5.000,00):*
`
D: CMV                       R$ 5.000,00
C: Estoque - Mercadorias     R$ 5.000,00
`

*Pagamento de salários (R$ 20.000,00 + INSS R$ 4.400,00 + FGTS R$ 1.600,00):*
`
D: Despesas com Pessoal      R$ 20.000,00
D: INSS a Recolher           R$  4.400,00
D: FGTS a Recolher           R$  1.600,00
C: Banco Conta Movimento     R$ 26.000,00
`

*Depreciação mensal (R$ 500,00):*
`
D: Despesas - Depreciação    R$   500,00
C: Depreciação Acumulada     R$   500,00
`

*Recebimento de cliente (R$ 10.000,00):*
`
D: Banco Conta Movimento     R$ 10.000,00
C: Contas a Receber          R$ 10.000,00
`

*Provisão para devedores duvidosos (R$ 2.000,00):*
`
D: Despesas - PDD            R$ 2.000,00
C: Provisão para DD          R$ 2.000,00
`

**Lançamentos de Abertura e Encerramento:**

*Abertura:*
`
D: Ativo (contas)           R$ XXX
C: Passivo + PL (contas)    R$ XXX
`

*Encerramento de resultado:*
`
D: Receitas (todas)          R$ XXX
C: Apuração do Exercício     R$ XXX

D: Apuração do Exercício     R$ XXX
C: Despesas (todas)          R$ XXX

Se lucro:
D: Apuração do Exercício     R$ XXX
C: Lucros Acumulados         R$ XXX
`

**Regime de Competência vs. Caixa:**

| Aspecto | Competência | Caixa |
|---------|-------------|-------|
| Receita | Quando auferida | Quando recebida |
| Despesa | Quando incorrida | Quando paga |
| Obrigatório | Sim (empresas) | Não |
| Resultado | Mais preciso | Menos preciso |

## Dependências

- **plano-de-contas.md** — estrutura de contas para classificação
- **contabilidade-geral.md** — princípios do regime de competência
- **lancamentos-automatizados.md** — geração automática de lançamentos

## Restrições

- Escrituração em partidas dobradas obrigatória
- Em língua portuguesa e moeda nacional
- Sem rasuras, emendas ou borrões
- Sem espaços em branco
- Regime de competência obrigatório para empresas
- Manutenção por mínimo 5 anos (10 anos para S.A. aberta)

## Documentos Relacionados

- Lei 6.404/76, Cap. XVII
- Código Civil, Art. 1.179 a 1.190
- Resolução CFC 1.330/2011
- NBC TG 23 (Políticas Contábeis)
