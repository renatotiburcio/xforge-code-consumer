---
id: historico-salario-minimo
type: conhecimento
tags: [trabalhista, salario-minimo, historico, 2010-2026]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Salário Mínimo - Histórico Completo 2010-2026
- **Seções principais**: Base Legal, Tabela Completa, Evolução em 10 Anos, Reajuste Acima da Inflação
- **Tags**: trabalhista, salario-minimo, historico, 2010-2026
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `historico-salario-minimo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# Salário Mínimo - Histórico Completo 2010-2026

## Base Legal
- Art. 7º, IV da Constituição Federal
- Lei 8.213/1991
- Lei Complementar 194/2022

## Tabela Completa

| Ano | Valor | Reajuste | IPCA | Fonte |
|-----|-------|----------|------|-------|
| 2010 | R$ 510,00 | +12,45% | 10,06% | Decreto 7.069/2009 |
| 2011 | R$ 545,00 | +6,86% | 6,50% | Decreto 7.449/2010 |
| 2012 | R$ 622,00 | +14,13% | 5,84% | Decreto 7.655/2011 |
| 2013 | R$ 678,00 | +9,00% | 5,91% | Decreto 7.855/2012 |
| 2014 | R$ 724,00 | +6,78% | 6,41% | Decreto 8.138/2013 |
| 2015 | R$ 788,00 | +8,84% | 6,41% | Decreto 8.373/2014 |
| 2016 | R$ 880,00 | +11,68% | 10,67% | Decreto 8.689/2016 |
| 2017 | R$ 937,00 | +6,48% | 2,95% | Decreto 8.997/2016 |
| 2018 | R$ 954,00 | +1,81% | 2,78% | Decreto 9.255/2017 |
| 2019 | R$ 998,00 | +4,61% | 4,31% | Decreto 9.665/2018 |
| 2020 | R$ 1.039,00 | +4,11% | 4,52% | Decreto 10.155/2019 |
| 2021 | R$ 1.100,00 | +5,87% | 8,34% | Decreto 10.609/2020 |
| 2022 | R$ 1.212,00 | +10,18% | 10,06% | Decreto 10.884/2021 |
| 2023 | R$ 1.320,00 | +8,91% | 5,78% | Decreto 11.178/2022 |
| 2024 | R$ 1.412,00 | +6,97% | 4,62% | Decreto 11.864/2024 |
| 2025 | R$ 1.518,00 | +7,51% | 4,87% | Decreto 12.345/2024 |
| 2026 | R$ 1.625,00 | ~7,05% | ~5,00% | Estimativa |

## Evolução em 10 Anos

| Indicador | 2016 | 2026 | Variação |
|-----------|-----:|-----:|:--------:|
| Salário mínimo | R$ 880 | R$ 1.625 | +84,66% |
| Acumulado IPCA | R$ 880 | R$ 1.520 | +72,73% |
| Diferença real | - | R$ 105 | +7,24% |

## Reajuste Acima da Inflação

### LC 194/2022
- Define que reajuste deve ser ≥ IPCA acumulado
- Diferença entre reajuste e IPCA é "diferencial"
- Recursos federais cobrem a diferença

### Fórmula
```
Novo Salário = Salário Anterior × (1 + Reajuste)
Diferencial = Novo Salário - (Salário Anterior × (1 + IPCA))
Recursos Federais = Diferencial × Massa Salarial
```

## Impactos no Cálculo de Folha

### INSS (Proporção)
As faixas do INSS são proporcionais ao salário mínimo:
- 1ª faixa: 1x salário mínimo
- 2ª faixa: ~1,8x salário mínimo
- 3ª faixa: ~2,7x salário mínimo
- Teto: ~5,4x salário mínimo

### IRRF (Faixa Isenta)
A faixa isenta é proporcional ao salário mínimo:
- 2020: 1,83x salário mínimo
- 2025: 1,49x salário mínimo
- Tendência: diminuir proporcionalmente

### Outros Benefícios
- BPC/LOAS: 1 salário mínimo
- Aposentadoria mínima: 1 salário mínimo
- Vale transporte: 6% do salário mínimo
- FGTS: 8% sobre salário mínimo

## Projeções

### Para Sistemas de TI
- Tabelas devem ser parametrizadas por ano
- Motor de cálculo deve aceitar múltiplas tabelas
- Atualização anual obrigatória
- Histórico preservado para cálculos retroativos

### Para SPED/eSocial
- Eventos devem usar tabela do ano de referência
- Correção retroativa quando tabela muda
- Validação por período de competência

## Fontes Oficiais
- Constituição Federal, art. 7º
- Lei 8.213/1991
- DECRETO do Ministério do Trabalho (anual)
- TCU (auditorias)
