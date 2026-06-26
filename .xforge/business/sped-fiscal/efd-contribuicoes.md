---
title: "EFD Contribuicoes \u2014 PIS COFINS"
summary: "EFD Contribuicoes: PIS, COFINS, blocos M, A, C, D, F, I, P, registros e apuracao"
keywords: ["sped", "efd-contribuicoes", "pis", "cofins", "bloco-m", "apuracao"]
trustScore: 82
lastValidated: 2026-06-13
id: knowledge-sped-efd-contribuicoes
type: knowledge
---

# EFD Contribuicoes \u2014 PIS COFINS

## O que e

A EFD Contribuicoes registra:
- PIS (Programa Integracao Social)
- COFINS (Contribuicao para Financiamento da Seguridade Social)
- IRPJ/CSLL em casos especificos (Lucro Presumido ou Arbitrado que optem)

## Aliquotas 2024

| Regime | PIS | COFINS | Total |
|--------|-----|--------|-------|
| Cumulativo (Lucro Presumido/MEI) | 0.65% | 3.00% | 3.65% |
| Nao-cumulativo (Lucro Real) | 1.65% | 7.60% | 9.25% |
| Importacao (geral) | 1.65% | 7.60% | 9.25% |
| Importacao (medicamentos) | 2.10% | 9.65% | 11.75% |

## Prazos

| Tipo | Prazo |
|------|-------|
| Mensal | Dia 25 do mes seguinte |
| Substituicao | Ate o decimo dia do 2o mes subsequente |

## Blocos

| Bloco | Conteudo | Quando usar |
|-------|----------|-------------|
| 0 | Abertura, identificacao | Sempre |
| A | Servicos tomados e prestados | PJ prestadora de servico |
| C | Documentos fiscais I (entradas/saidas) | Sempre |
| D | Documentos fiscais II (CT-e, NF servico) | Condicional |
| F | Demais documentos (frete, energia) | Condicional |
| I | Operacoes das industrias | PJ industrial |
| M | Apuracao do PIS/COFINS | Sempre |
| P | Apuracao IRPJ/CSLL | Lucro Presumido/Arbitrado |
| 1 | Informacoes complementares | Opcional |
| 9 | Encerramento | Sempre |

## Bloco M (Apuracao) \u2014 registros chave

| Registro | Conteudo |
|----------|----------|
| M001 | Abertura do bloco |
| M100 | Credito de PIS/PASEP |
| M105 | Detalhamento de credito por NCM |
| M110 | Ajustes de credito PIS |
| M200 | Contribuicao para PIS (apuracao) |
| M210 | Detalhamento da contribuicao PIS |
| M400 | Credito de COFINS |
| M500 | Contribuicao para COFINS |
| M600 | Consolidacao da contribuicao |
| M800 | Receitas isentas |
| M810 | Detalhamento de receitas isentas |

## Apuracao nao-cumulativa (Lucro Real)

**Creditos recuperaveis:**

| Credito | Base legal |
|---------|-----------|
| Bens para revenda | Art. 3o Lei 10.637/2002 |
| Bens para uso/consumo | Art. 3o (com limitacoes) |
| Servicos tomados | Art. 3o (lista) |
| Energia eletrica | Sim (consumo) |
| Alugueis | Sim (predios) |
| Maquinas/equipamentos | Sim (incorporados ao ativo) |

**Apuracao:**

```
Base PIS = Receita Bruta - Exclusoes - Creditos
PIS a pagar = Base x 1.65%

Base COFINS = Receita Bruta - Exclusoes - Creditos
COFINS a pagar = Base x 7.60%
```

## Apuracao cumulativa (Lucro Presumido)

- **Sem creditos** sobre aquisicoes
- Incide sobre receita bruta x 3.65% (PIS + COFINS)
- Faturamento mensal ate R$ 4.8M (Simples Nacional) e isento

## Regime monofasico (combustiveis, farmacia, autopeças)

Substituicao tributaria concentrada em 1 agente:
- Fabricante/importador paga PIS/COFINS
- Revendedor **nao paga** novamente
- Registra CFOP 5656/5667 (devolucao) e CST 04

## Validacoes comuns

| Erro | Causa |
|------|-------|
| CFOP + CST incompativel | Ex: CFOP 1102 com CST 70 |
| Total de creditos > receita | Erro de classificacao |
| NCM nao permite credito | Lista restrita |
| Periodo invalido | Formato AAA-MM |

## Cuidados

- Conciliar mensalmente com a EFD ICMS (Bloco E)
- Atividades mistas (industria + comercio) precisam de registros nos 2 regimes
- Eventos de FUSION/AQUISICAO exigem informacoes adicionais
- EFD Contribuicoes **substitui** a DIRF e parte da DIPJ (extintas)