---
id: tabela-irrf-2025
type: conhecimento
tags: [trabalhista, irrf, imposto-renda, faixas, 2025]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Tabela IRRF 2025 - Imposto de Renda Retido na Fonte
- **Seções principais**: Base Legal, Tabela Progressiva (Mensal - Rendimento Mensal), Base de Cálculo do IRRF, Cálculo Completo
- **Tags**: trabalhista, irrf, imposto-renda, faixas, 2025
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tabela-irrf-2025` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# Tabela IRRF 2025/2026 - Imposto de Renda Retido na Fonte

## Base Legal
- Lei 7.713/1988
- Lei 14.848/2024 (nova tabela com faixa isenta)
- Portaria RFB nº 2.246/2025

## Tabela Progressiva (Mensal - Rendimento Mensal)

| Faixa | Base de Cálculo (R$) | Alíquota | Parcela a Deduzir |
|:-----:|---------------------:|:--------:|------------------:|
| 1ª | Até 2.259,20 | Isento | R$ 0,00 |
| 2ª | 2.259,21 a 2.826,65 | 7,5% | R$ 169,44 |
| 3ª | 2.826,66 a 3.751,05 | 15,0% | R$ 381,44 |
| 4ª | 3.751,06 a 4.664,68 | 22,5% | R$ 662,77 |
| 5ª | Acima de 4.664,68 | 27,5% | R$ 896,00 |

## Base de Cálculo do IRRF

### Fórmula
```
Base IRRF = Salário Bruto - INSS - Dependentes - Pensão Alimentícia
```

### Deduções
| Dedução | Valor Mensal (2025) |
|---------|-------------------:|
| Dependente | R$ 189,59 por dependente |
| Pensão alimentícia judicial | Valor integral |
| Previdência social (INSS) | Valor efetivamente pago |
| Previdência complementar | Valor contribuído |

## Cálculo Completo

### Exemplo 1: Salário R$ 5.000,00 (solteiro, 0 dependentes)

1. **INSS:** R$ 5.000,00 × 14% - R$ 190,40 = R$ 509,60
2. **Base IRRF:** R$ 5.000,00 - R$ 509,60 = R$ 4.490,40
3. **Faixa:** 4ª (R$ 3.751,06 a R$ 4.664,68)
4. **IRRF:** R$ 4.490,40 × 22,5% - R$ 662,77 = **R$ 347,57**

### Exemplo 2: Salário R$ 3.000,00 (solteiro, 0 dependentes)

1. **INSS:** R$ 3.000,00 × 12% - R$ 106,59 = R$ 253,41
2. **Base IRRF:** R$ 3.000,00 - R$ 253,41 = R$ 2.746,59
3. **Faixa:** 1ª (até R$ 2.259,20)... mas R$ 2.746,59 > R$ 2.259,20
4. **Faixa correta:** 2ª (R$ 2.259,21 a R$ 2.826,65)
5. **IRRF:** R$ 2.746,59 × 7,5% - R$ 169,44 = **R$ 36,56**

### Exemplo 3: Salário R$ 2.000,00 (solteiro, 0 dependentes)

1. **INSS:** R$ 2.000,00 × 9% - R$ 22,77 = R$ 157,23
2. **Base IRRF:** R$ 2.000,00 - R$ 157,23 = R$ 1.842,77
3. **Faixa:** 1ª (até R$ 2.259,20) = **ISENTO**

### Exemplo 4: Salário R$ 7.000,00 (casado, 2 dependentes, pensão R$ 500)

1. **INSS:** R$ 7.000,00 × 14% - R$ 190,40 = R$ 789,60
2. **Deduções:** R$ 789,60 (INSS) + R$ 379,18 (2 dep × R$ 189,59) + R$ 500,00 (pensão) = R$ 1.668,78
3. **Base IRRF:** R$ 7.000,00 - R$ 1.668,78 = R$ 5.331,22
4. **Faixa:** 5ª (acima de R$ 4.664,68)
5. **IRRF:** R$ 5.331,22 × 27,5% - R$ 896,00 = **R$ 571,09**

## Tabela Semestral (13º Salário e Férias)

### 13º Salário
- Base: R$ 1.518,00 (salário mínimo 2025)
- Faixa isenta: até R$ 4.547,00 (3 × salário mínimo)
- Tabela semestral é mais favorável

### Férias + 1/3
- Base: remuneração de férias
- Faixa isenta: até R$ 2.259,20

## Diferença para Tabela 2024

| Faixa | 2024 | 2025/2026 | Mudança |
|-------|------|------|---------|
| Isento até | R$ 2.112,00 | R$ 2.259,20 | +7% |
| 7,5% até | R$ 2.824,00 | R$ 2.826,65 | +0,09% |
| 15% até | R$ 3.751,05 | R$ 3.751,05 | 0% |
| 22,5% até | R$ 4.664,68 | R$ 4.664,68 | 0% |
| 27,5% acima | R$ 4.664,68 | R$ 4.664,68 | 0% |

*Observação: A tabela IRRF 2025 vigente continua válida para 2026. Não houve alteração legislativa nas faixas.*

## Fontes Oficiais
- Lei 14.848/2024
- Portaria RFB nº 2.246/2025
- Tabela IRRF Sincronizada (Receita Federal)
