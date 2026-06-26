---
id: simples-nacional-regras
type: conhecimento
tags: [fiscal, simples-nacional, anexo, faixa, fator-r, isencao]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Simples Nacional - Regras Completas
- **Seções principais**: Base Legal, Limites de Faturamento, Anexos, Tabela do Anexo I (Comércio)
- **Tags**: fiscal, simples-nacional, anexo, faixa, fator-r, isencao
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `simples-nacional-regras` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# Simples Nacional - Regras Completas

## Base Legal
- Lei Complementar 123/2006
- Lei Complementar 155/2016
- Resolução CGSN nº 140/2018

## Limites de Faturamento

| Critério | Limite Anual |
|----------|:------------:|
| Faturamento bruto | R$ 4.800.000,00 |
| Receita bruta (12 meses) | Até R$ 4.800.000,00 |

## Anexos

| Anexo | Atividade | Faixa | Alíquota |
|:-----:|-----------|:-----:|:--------:|
| I | Comércio | 1-6 | 4% a 19% |
| II | Indústria | 1-6 | 4,5% a 30% |
| III | Serviços (baixa mão de obra) | 1-6 | 6% a 33% |
| IV | Serviços (mão de obra) | 1-6 | 4,5% a 33% |
| V | Serviços (profissionais) | 1-6 | 14,5% a 33% |

## Tabela do Anexo I (Comércio)

| Faixa | Receita Bruta (R$) | Alíquota | Dedução |
|:-----:|-------------------:|:--------:|--------:|
| 1ª | Até 180.000,00 | 4,0% | R$ 0,00 |
| 2ª | 180.000,01 a 360.000,00 | 7,3% | R$ 5.940,00 |
| 3ª | 360.000,01 a 720.000,00 | 9,5% | R$ 13.860,00 |
| 4ª | 720.000,01 a 1.800.000,00 | 10,7% | R$ 22.500,00 |
| 5ª | 1.800.000,01 a 3.600.000,00 | 14,3% | R$ 87.300,00 |
| 6ª | 3.600.000,01 a 4.800.000,00 | 19,0% | R$ 378.000,00 |

## Tabela do Anexo III (Serviços)

| Faixa | Receita Bruta (R$) | Alíquota | Dedução |
|:-----:|-------------------:|:--------:|--------:|
| 1ª | Até 180.000,00 | 6,0% | R$ 0,00 |
| 2ª | 180.000,01 a 360.000,00 | 11,2% | R$ 9.360,00 |
| 3ª | 360.000,01 a 720.000,00 | 13,5% | R$ 17.640,00 |
| 4ª | 720.000,01 a 1.800.000,00 | 16,0% | R$ 35.640,00 |
| 5ª | 1.800.000,01 a 3.600.000,00 | 21,0% | R$ 125.640,00 |
| 6ª | 3.600.000,01 a 4.800.000,00 | 33,0% | R$ 648.000,00 |

## Fator R

### Conceito
- Para empresas de serviços (Anexo III/V)
- Se massa salarial ≥ 28% do faturamento → Anexo V migra para Anexo III
- Reduz alíquota significativamente

### Cálculo
```
Fator R = Massa Salarial (12 meses) / Receita Bruta (12 meses)
Se Fator R ≥ 28% → usa Anexo III
Se Fator R < 28% → usa Anexo V
```

### Impacto
| Fator R | Anexo | Alíquota faixa 1 |
|:-------:|:-----:|:----------------:|
| < 28% | V | 14,5% |
| ≥ 28% | III | 6,0% |

## Fórmula de Cálculo

### Passo 1: Identificar Anexo
- Comércio → Anexo I
- Indústria → Anexo II
- Serviços → Anexo III, IV ou V

### Passo 2: Calcular Alíquota Nominal
```
Alíquota Nominal = (Receita Bruta × Alíquota Tabela - Dedução) / Receita Bruta
```

### Passo 3: Calcular Alíquota Efetiva
```
Alíquota Efetiva = (Receita Bruta × Alíquota Nominal - Dedução) / Receita Bruta
```

### Fórmula Geral
```
Alíquota = (RBT12 × AlíqTab - Ded) / RBT12
```
Onde:
- RBT12 = Receita Bruta dos últimos 12 meses
- AlíqTab = Alíquota da tabela
- Ded = Parcela a deduzir

## Exemplo de Cálculo

### Empresa de Comércio, receita R$ 300.000/ano

1. Anexo: I (comércio)
2. Faixa: 2ª (R$ 180.000,01 a R$ 360.000,00)
3. Alíquota: 7,3%
4. Dedução: R$ 5.940,00
5. Cálculo: (R$ 300.000 × 7,3% - R$ 5.940) / R$ 300.000
6. = (R$ 21.900 - R$ 5.940) / R$ 300.000
7. = R$ 15.960 / R$ 300.000
8. **Alíquota efetiva: 5,32%**

### Empresa de Serviços, receita R$ 200.000/ano, fator R = 30%

1. Anexo: III (fator R ≥ 28%)
2. Faixa: 2ª (R$ 180.000,01 a R$ 360.000,00)
3. Alíquota: 11,2%
4. Dedução: R$ 9.360,00
5. Cálculo: (R$ 200.000 × 11,2% - R$ 9.360) / R$ 200.000
6. = (R$ 22.400 - R$ 9.360) / R$ 200.000
7. = R$ 13.040 / R$ 200.000
8. **Alíquota efetiva: 6,52%**

## Isenções e Benefícios

### Isenção de Impostos Federais
- IRPJ
- CSLL
- PIS
- COFINS
- IPI (em alguns casos)

### Contribuições Mantidas
- INSS patronal
- FGTS
- RAT
- Sistema S

### Créditos de ICMS
- Empresas do Anexo I e II podem ter crédito de ICMS
- Limite conforme faturamento

## Obrigações Acessórias

| Obrigação | Prazo |
|-----------|-------|
| DAS (guia única) | Dia 20 do mês seguinte |
| GFIP | Mensal (se tiver empregados) |
| DIRF | Anual |
| SPED Contribuições | Mensal |
| SPED Fiscal | Mensal |

## Restrições

| Restrição | Observação |
|-----------|------------|
| Contrato com órgão público | Pode ter limite |
| Exercer mais de uma atividade | Sim, mas tributação separada |
| Ter sócio PJ | Sim |
| Franquia | Sim |

## Fontes Oficiais
- Lei Complementar 123/2006
- Resolução CGSN nº 140/2018
- Portal do Simples Nacional
