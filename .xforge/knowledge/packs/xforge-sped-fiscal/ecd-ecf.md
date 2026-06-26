---
title: "ECD e ECF \u2014 Escrituracoes Contabeis Digitais"
summary: "ECD escrituracao contabil digital e ECF fiscal digital, prazos, blocos, validacoes"
keywords: ["sped", "ecd", "ecf", "contabil", "escrituracao", "irpj", "csll"]
trustScore: 80
lastValidated: 2026-06-13
id: knowledge-sped-ecd-ecf
type: knowledge
---

# ECD e ECF \u2014 Escrituracoes Contabeis Digitais

## ECD \u2014 Escrituracao Contabil Digital

### O que e

Arquivo digital que substitui os livros contabeis em papel:
- Diario
- Razao
- Caixa

Obrigatorio para todas as empresas regidas pela **CPC 00 (NBC TG 00)** e optantes pelo Lucro Real.

### Prazos

| Tipo | Prazo |
|------|-------|
| Anual (PJ em geral) | Ultimo dia util de maio |
| Eventos | Mes da ocorrencia (sucessao, cisao, etc) |
| Recuperacao judicial | Mensal |

### Blocos

| Bloco | Conteudo |
|-------|----------|
| 0 | Abertura + dados cadastrais |
| I | Lancamentos contabeis (razao) |
| J | Demonstracoes financeiras |
| 9 | Encerramento |

### Registros principais

```
0 - Identificacao
  0000  Abertura do arquivo
  0001  Abertura do bloco 0
  0007  Outras inscricoes
  0020  Dados do contador (CRC + CNPJ)
  0150  Tabela de contas referenciais

I - Lancamentos
  I001  Abertura do bloco I
  I010  Parametros de escrituracao
  I020  Campos adicionais
  I030  Termo de abertura do livro
  I050  Plano de contas
  I051  Indicador de movimentacao da conta
  I100  Centro de custos
  I150  Saldos periodicos
  I155  Detalhe dos saldos
  I200  Lancamento contabil
  I250  Partidas do lancamento
  I300  Balancete verificacao (opcional)
  I310  Detalhe balancete

J - Demonstracoes
  J001  Abertura do bloco J
  J100  Balanco patrimonial
  J150  DRE - Demonstracao do Resultado
  J200  DLP - Demonstracao dos Lucros/Prejuizos Acumulados
  J210  DMPL - Demonstracao das Mutacoes do PL
  J800  Outras informacoes

9 - Encerramento
  9001  Abertura do bloco 9
  9900  Registros do arquivo
  9999  Encerramento do arquivo
```

### Plano de contas referencial

- Ativo (1)
- Passivo (2)
- Patrimonio Liquido (3)
- Receita (4)
- Despesa/Custo (5)
- Apuracao (6)

A ECD exige o **plano de contas referencial** (RFB publica tabela).

## ECF \u2014 Escrituracao Contabil Fiscal

### O que e

A ECF registra a apuracao do IRPJ e CSLL para PJ optantes pelo **Lucro Real** (obrigatoria) ou **Lucro Presumido/Arbitrado** (tambem obrigatoria para essas).

### Prazos

| Tipo | Prazo |
|------|-------|
| Anual (PJ normal) | Ultimo dia util de julho |
| Saida do Lucro Real | 30 dias do fato |
| Evento societario (cisao, incorporacao) | Mes subsequente |

### Blocos

| Bloco | Conteudo |
|-------|----------|
| 0 | Abertura + dados |
| C | Lucro Real (LALUR) |
| F | Lucro Presumido / Arbitrado |
| M | Lucro Liquido |
| N | IRPJ e CSLL |
| P | Lucro Presumido |
| Q | Demonstracoes |
| T | Transito (legado) |
| U | Imunes e Isentas |
| W | Cooperativas |
| X | Operacoes no Exterior |
| Y | Pessoas Físicas (caso especial) |
| 9 | Encerramento |

### Apuracao Lucro Real (Bloco C)

```
Receita Liquida
- Custos
- Despesas Operacionais
= Lucro Contabil
+/- Ajustes LALUR (exclusoes, adicoes, compensacoes)
= Lucro Real
x 15% = IRPJ (ate R$ 20k/mes lucro)
x 10% adicional (acima R$ 20k/mes)
- IRRF ja recolhido
- IRPJ antecipado
- Prejuizos fiscais compensaveis (ate 30%)
= IRPJ a pagar

CSLL = Base x 9%
```

### Bloco M - Lucro Liquido

| Registro | Conteudo |
|----------|----------|
| M001 | Abertura |
| M010 | Equacao do lucro liquido |
| M300 | Demonstracao do resultado |
| M350 | Resultado antes do IRPJ/CSLL |
| M410 | Lucro Liquido |

### PGDAS-D x ECF

A ECD/ECF e **separada** do PGDAS-D (Simples Nacional). PJs do Simples NAO entregam ECF, usam PGDAS-D e DEFIS.

### Validacoes

- Conciliacao automatica com ECD (Bloco K da EFD ICMS)
- Cruzamento com EFD Contribuicoes (Bloco M)
- Cruzamento com NF-e (Bloco C)
- SPED Contribuicoes para PJ Lucro Real

## Penalidades

| Falta | Multa |
|-------|-------|
| Atraso ECD | 0.5% do lucro liquido (min R$ 500) |
| Atraso ECF | 0.25% do lucro liquido (min R$ 500) |
| Informacoes incorretas | 3% a 5% do valor omitido |
| Omissao | ate 150% do tributo nao pago |

## Cuidados

- ECD deve ser **fechada** antes da ECF (referencia cruzada)
- Backup por 5 anos
- Substituicao tributaria: ajustes especificos no Bloco C
- Operacoes com exterior: Bloco X obrigatorio
- Inabilitados: ECD pode ser feita com escritura contábil simplificada