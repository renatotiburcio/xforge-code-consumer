---
id: contabil-ecd
type: domain
tags: [contabil, ecd, sped-contabil, sped, escrituracao-digital, rfb]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ECD — Escrituração Contábil Digital
- **Principais responsabilidades**: Anual: último dia útil de maio do exercício seguinte; Eventual: 30 dias após evento (fusão, cisão, incorporação, extinção); Assinatura digital com ...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, ecd, sped-contabil, sped, escrituracao-digital, rfb
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-ecd` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# ECD — Escrituração Contábil Digital

## Propósito

Definir a estrutura, obrigatoriedade e requisitos da Escrituração Contábil Digital (SPED Contábil), que substitui os livros contábeis em papel (Diário, Razão, Balancetes) por versão digital transmitida à Receita Federal.

## Responsabilidades

**Conceito:** A ECD é a versão digital dos livros contábeis — Livro Diário, Livro Razão, Balancetes Diários e Balanço — transmitida anualmente pelo SPED.

**Obrigatoriedade:**

>Obrigadas: empresas do Lucro Real, Lucro Presumido que distribuam lucros isentos acima do limite, SCP.
>Dispensadas: Microempresas e EPP optantes pelo Simples Nacional (exceto faturamento > R$ 3,6 milhões), órgãos públicos.

**Livros Contidos na ECD:**

| Livro | Descrição |
|-------|-----------|
| Livro Diário (Completo) | Todos os lançamentos em ordem cronológica |
| Livro Razão | Saldos por conta individual |
| Balancetes Diários e Balanços | Balancetes mensais e balanço anual |
| Livros Auxiliares | Quando aplicável |

**Principais Registros:**

| Registro | Descrição |
|----------|-----------|
| I001 | Abertura do arquivo digital |
| I010 | Identificação da escrituração |
| I030 | Termo de abertura do livro |
| I050 | Plano de contas |
| I051 | Plano de contas referencial (RFB) |
| I052 | Indicação de códigos de aglutinação |
| I075 | Tabela de histórico padronizado |
| I100 | Centro de custos |
| I150 | Saldo periódico (identificação da data) |
| I155 | Detalhamento dos saldos periódicos |
| I200 | Lançamento contábil |
| I250 | Partidas do débito e crédito |
| I300 | Balancete (identificação da data) |
| I350 | Saldo das contas de resultado antes do encerramento |
| I550 | Totais para impressão |
| J001 | Abertura do bloco J |
| J005 | Demonstrações contábeis |
| J100 | Balanço Patrimonial |
| J150 | DRE |
| J210 | DLPA |
| J800 | Outras informações |
| J900 | Encerramento do arquivo |
| J930 | Signatários |

**Demonstrações Contábeis na ECD:** BP, DRE, DLPA, DFC (S.A. aberta), DVA (S.A. aberta), Notas Explicativas.

**Prazo de Entrega:**
- Anual: último dia útil de maio do exercício seguinte
- Eventual: 30 dias após evento (fusão, cisão, incorporação, extinção)

**Requisitos Técnicos:**
- Assinatura digital com certificado e-CNPJ (A1 ou A3) do contador
- Validação pelo PVA (Programa Validador do SPED)
- Plano de contas referencial RFB obrigatório
- Mapeamento ECD → ECF obrigatório para Lucro Real
- Saldos devem conferir com a ECF
- Escrituração em ordem cronológica, sem retificação sem justificativa

## Dependências

- **plano-de-contas.md** — registros I050, I051, I052
- **escrituracao-contabil.md** — lançamentos (I200, I250)
- **demonstracoes-contabeis.md** — J005 a J215
- **ecf.md** — mapeamento ECD → ECF
- **centro-de-custo.md** — registro I100

## Restrições

- Certificado digital A1 ou A3 obrigatório
- Leiaute vigente definido pela RFB
- Manter escrituração por 5 anos (S.A. aberta: 10 anos)
- Retificação permitida dentro do prazo sem multa

## Documentos Relacionados

- Lei 11.638/2007, Lei 11.941/2010
- Manual de Orientação da ECD (SPED)
- IN RFB — Plano de Contas Referencial
- Manual ECD — Registros I001-I550, J001-J950
