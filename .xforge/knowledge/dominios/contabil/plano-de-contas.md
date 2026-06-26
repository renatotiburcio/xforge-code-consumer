---
id: contabil-plano-de-contas
type: domain
tags: [contabil, plano-de-contas, sped, ecd, rfb, erp]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Plano de Contas
- **Principais responsabilidades**: **Ativo:** Circulante (caixa, clientes, estoques, impostos a recuperar) e Não Circulante (realizável LP, investimentos, imobilizado, intangível); *...
- **Seções principais**: Propósito, Responsabilidades, Regras de Codificação, Dependências
- **Tags**: contabil, plano-de-contas, sped, ecd, rfb, erp
- **Restrições/Regras**: Cada nível acrescenta dígitos ao código anterior; Código analítico (último nível) é usado nos lançamentos

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-plano-de-contas` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 6 |


# Plano de Contas

## Propósito

Definir a estrutura de contas contábeis utilizada pela empresa para classificação e registro de todos os fatos patrimoniais, atendendo às exigências legais (Lei 6.404/76, NBC TG 26) e do SPED Contábil (ECD).

## Responsabilidades

O plano de contas organiza em níveis hierárquicos todas as contas utilizadas na escrituração:

**Estrutura em 5 níveis:**

| Nível | Tipo | Exemplo |
|-------|------|---------|
| 1 | Grupo geral | 1 — Ativo |
| 2 | Subgrupo | 1.01 — Ativo Circulante |
| 3 | Conta | 1.01.02 — Caixa e Equivalentes |
| 4 | Subconta | 1.01.02.001 — Caixa Geral |
| 5 | Detalhamento | 1.01.02.001.01 — Caixa Matriz |

**Classificação principal:**

- **Ativo:** Circulante (caixa, clientes, estoques, impostos a recuperar) e Não Circulante (realizável LP, investimentos, imobilizado, intangível)
- **Passivo:** Circulante (fornecedores, obrigações fiscais e trabalhistas, empréstimos CP) e Não Circulante (exigível LP, provisões)
- **Patrimônio Líquido:** Capital social, reservas de capital, reservas de lucros, lucros/prejuízos acumulados, (-) ações em tesouraria
- **Receitas:** Bruta, deduções (devoluções, abatimentos, ICMS, PIS, COFINS), líquida
- **Despesas:** CMV, operacionais (administrativas, comerciais, pessoal), financeiras, não operacionais

**Plano de Contas Referencial (RFB):** A ECD exige vinculação ao plano referencial da Receita Federal. O módulo deve permitir mapeamento entre o plano interno e o plano referencial.

**Exemplo — Empresa Comercial:**

`
1     ATIVO
1.01  Ativo Circulante
1.01.01  Caixa e Equivalentes
1.01.01.001  Caixa Geral
1.01.01.002  Banco Conta Movimento
1.01.02  Contas a Receber
1.01.02.001  Duplicatas a Receber
1.01.03  Estoques
1.01.03.001  Mercadorias para Revenda
1.01.04  Impostos a Recuperar
1.01.04.001  ICMS a Recuperar
1.01.04.002  PIS a Recuperar
1.01.04.003  COFINS a Recuperar
1.02  Ativo Não Circulante
1.02.01  Imobilizado
1.02.01.001  Máquinas e Equipamentos
1.02.01.002  (-) Depreciação Acumulada
2     PASSIVO
2.01  Passivo Circulante
2.01.01  Fornecedores
2.01.02  Obrigações Fiscais
2.01.02.001  ICMS a Recolher
2.01.02.002  PIS a Recolher
2.01.02.003  COFINS a Recolher
2.01.03  Obrigações Trabalhistas
2.01.03.001  Salários a Pagar
2.02  Patrimônio Líquido
2.02.01  Capital Social
2.02.02  Reservas de Lucros
2.02.03  Lucros Acumulados
3     RECEITAS  (3.01 Bruta / 3.02 Deduções)
4     DESPESAS  (4.01 CMV / 4.02 Operacionais / 4.03 Financeiras)
`

## Regras de Codificação

- Cada nível acrescenta dígitos ao código anterior
- Código analítico (último nível) é usado nos lançamentos
- Código sintético (níveis superiores) é usado em relatórios
- Alterações no plano exigem mapeamento retroativo quando afetam a ECD
- Plano referencial RFB deve ser atualizado conforme instruções normativas vigentes

## Dependências

- **contabilidade-geral.md** — princípios contábeis e classificação de contas
- **escrituracao-contabil.md** — estrutura dos lançamentos
- **ecd.md** — registro I050 e I051 (plano de contas e referencial na ECD)

## Restrições

- Deve seguir estrutura mínima da NBC TG 26
- Vinculação ao plano referencial RFB é obrigatória para ECD
- Código de aglutinação (registro I052) exigido para contas do SPED
- Não é permitida compensação entre ativos e passivos

## Documentos Relacionados

- Lei 6.404/76, Art. 178 (estrutura do Balanço)
- NBC TG 26 (Apresentação das Demonstrações Contábeis)
- Manual ECD — Registros I050, I051, I052
- Instrução Normativa RFB — Plano de Contas Referencial
