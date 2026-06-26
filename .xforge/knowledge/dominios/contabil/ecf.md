---
id: contabil-ecf
type: domain
tags: [contabil, ecf, sped-fiscal, irpj, csll, lalur, sped, rfb]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ECF — Escrituração Contábil Fiscal
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, ecf, sped-fiscal, irpj, csll, lalur, sped, rfb
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-ecf` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# ECF — Escrituração Contábil Fiscal

## Propósito

Apresentar todas as informações para cálculo da base de cálculo do IRPJ e da CSLL, substituindo a DIPJ. Parte integrante do SPED Fiscal contábil.

## Responsabilidades

**Obrigatoriedade:**

>Obrigadas: empresas do Lucro Real, Lucro Presumido com escrituração contábil, imunes/isentas com lucros acima do limite, SCP.
>Dispensadas: Simples Nacional, órgãos públicos.

**Estrutura por Blocos:**

| Bloco | Conteúdo |
|-------|----------|
| 0 | Identificação, referência, escrituração |
| Y | Informações gerais (societário, exterior, dirigentes) |
| C | Informações das contas contábeis e saldos |
| E, J | Plano de contas e mapeamento |
| K | Saldos das contas contábeis e referenciais |
| L | Lucro Líquido — Lucro Real |
| M | LALUR / LACS |
| N | Cálculo do IRPJ e CSLL |
| P | Lucro Presumido |
| Q | Livro Caixa |
| T | Lucro Arbitrado |
| U | Imunes / Isentas |
| X | Informações econômicas |

**Principais Registros:**

| Registro | Descrição |
|----------|-----------|
| Y001 | Abertura do arquivo |
| Y500 | Identificação do contribuinte |
| Y540 | Quadro societário |
| Y570 | Demonstrativo de investimentos |
| Y600 | Data de ocorrência dos eventos |
| Y612 | Rendimentos de dirigentes |
| Y620 | Participações societárias |
| Y672 | Operações com o exterior — Lucro Real |
| Y720 | Prejuízo acumulado — compensação |
| X001-X700 | Mapeamento ECD → ECF e saldos das demonstrações |
| W000-W700 | Termos e signatários |
| Z001-Z002 | Encerramento e assinatura digital |

**LALUR / LACS:**

O Livro de Apuração do Lucro Real (LALUR) e da CSLL (LACS) integram a ECF pelo Bloco M.

*Adições ao lucro contábil (IRPJ):* despesas não dedutíveis, lucro de coligadas no exterior, doações não incentivadas, multas, resultado negativo de equivalência patrimonial.

*Exclusões do lucro contábil:* dividendos recebidos, equivalência patrimonial positiva já tributada, prejuízo compensado, incentivos fiscais.

*Compensação de prejuízos:* limite de 30% do lucro real do período, sem limite temporal.

**Prazo de Entrega:** Último dia útil de julho do exercício seguinte. Evento especial: 3 meses.

**Requisitos:** Assinatura digital (e-CNPJ + e-CPF do contador), saldos conferindo com ECD, mapeamento ECD → ECF obrigatório, plano de contas referencial obrigatório.

## Dependências

- **ecd.md** — mapeamento de registros ECD para ECF (bloco X)
- **plano-de-contas.md** — plano referencial
- **demonstracoes-contabeis.md** — base de cálculo do lucro

## Restrições

- Saldos devem conferir exatamente com a ECD
- Retificação dentro do prazo sem multa
- Limite de compensação de prejuízo: 30% do lucro real
- Certificado digital A1 ou A3 obrigatório

## Documentos Relacionados

- ECF — Receita Federal
- Perguntas e Respostas ECF (RFB)
- Layout ECF (SPED)
- IN RFB — Instruções normativas vigentes
