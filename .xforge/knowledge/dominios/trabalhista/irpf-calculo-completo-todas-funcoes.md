---
id: irpf-calculo-completo-todas-funcoes
type: conhecimento
tags: [trabalhista, irrf, calculo, ferias, 13o, rescisao, todas-funcoes]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre IRRF - Cálculo Completo em Todas as Funções
- **Seções principais**: Base Legal, Tabela 2025 (Referência), Tabela Semestral (13º e Férias), 1. Salário Mensal
- **Tags**: trabalhista, irrf, calculo, ferias, 13o, rescisao, todas-funcoes
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `irpf-calculo-completo-todas-funcoes` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 11 |


# IRRF - Cálculo Completo em Todas as Funções

## Base Legal
- Lei 7.713/1988
- Lei 14.848/2024
- Portaria RFB nº 2.246/2025

## Tabela 2025 (Referência)

| Faixa | De (R$) | Até (R$) | Alíquota | Dedução |
|:-----:|--------:|---------:|:--------:|--------:|
| 1ª | 0,00 | 2.259,20 | Isento | R$ 0,00 |
| 2ª | 2.259,21 | 2.826,65 | 7,5% | R$ 169,44 |
| 3ª | 2.826,66 | 3.751,05 | 15,0% | R$ 381,44 |
| 4ª | 3.751,06 | 4.664,68 | 22,5% | R$ 662,77 |
| 5ª | Acima de 4.664,68 | - | 27,5% | R$ 896,00 |

## Tabela Semestral (13º e Férias)

| Faixa | De (R$) | Até (R$) | Alíquota | Dedução |
|:-----:|--------:|---------:|:--------:|--------:|
| 1ª | 0,00 | 1.129,60 | Isento | R$ 0,00 |
| 2ª | 1.129,61 | 1.413,33 | 7,5% | R$ 84,72 |
| 3ª | 1.413,34 | 1.875,53 | 15,0% | R$ 190,72 |
| 4ª | 1.875,54 | 2.332,34 | 22,5% | R$ 331,39 |
| 5ª | Acima de 2.332,34 | - | 27,5% | R$ 448,00 |

## 1. Salário Mensal

### Fórmula
```
IRRF Mensal = (Base IRRF × Alíquota) - Dedução
Base IRRF = Salário Bruto - INSS - Dependentes - Pensão
```

### Exemplos Completos

#### Salário R$ 2.000 (ISENTO)
1. INSS: R$ 2.000 × 9% - 22,77 = R$ 157,23
2. Base: R$ 2.000 - 157,23 = R$ 1.842,77
3. Faixa: 1ª (até R$ 2.259,20) = ISENTO
4. **IRRF: R$ 0,00**

#### Salário R$ 3.000
1. INSS: R$ 3.000 × 12% - 106,59 = R$ 253,41
2. Base: R$ 3.000 - 253,41 = R$ 2.746,59
3. Faixa: 2ª (até R$ 2.826,65)
4. IRRF: R$ 2.746,59 × 7,5% - 169,44 = R$ 36,56
5. **IRRF: R$ 36,56**

#### Salário R$ 5.000
1. INSS: R$ 5.000 × 14% - 190,40 = R$ 509,60
2. Base: R$ 5.000 - 509,60 = R$ 4.490,40
3. Faixa: 4ª (até R$ 4.664,68)
4. IRRF: R$ 4.490,40 × 22,5% - 662,77 = R$ 347,57
5. **IRRF: R$ 347,57**

#### Salário R$ 8.000, 3 dependentes
1. INSS: R$ 8.000 × 14% - 190,40 = R$ 929,60
2. Base: R$ 8.000 - 929,60 - (3 × 189,59) = R$ 6.501,23
3. Faixa: 5ª (acima de R$ 4.664,68)
4. IRRF: R$ 6.501,23 × 27,5% - 896,00 = R$ 891,84
5. **IRRF: R$ 891,84**

## 2. Décimo Terceiro Salário

### Cálculo Proporcional
```
13º Bruto = Salário / 12 × Meses trabalhados
INSS 13º = (13º Bruto × Alíquota) - Dedução
Base IRRF 13º = 13º Bruto - INSS 13º - Dependentes
IRRF 13º = (Base × Alíquota Semestral) - Dedução Semestral
```

### 1ª Parcela (até 30/11)
- Valor: 50% do 13º bruto
- Descontos: NENHUM

### 2ª Parcela (até 20/12)
- Valor: 50% restante - INSS - IRRF

### Exemplo: Salário R$ 3.000, ano cheio

**1ª Parcela:**
- Bruto: R$ 3.000 × 50% = R$ 1.500,00
- Líquido: **R$ 1.500,00**

**2ª Parcela:**
- Bruto: R$ 3.000 × 50% = R$ 1.500,00
- INSS: R$ 1.500 × 7,5% = R$ 112,50
- Base IRRF: R$ 1.500 - 112,50 = R$ 1.387,50
- Faixa semestral: 1ª (até R$ 1.129,60)... mas R$ 1.387,50 > R$ 1.129,60
- Faixa correta: 2ª (R$ 1.129,61 a R$ 1.413,33)
- IRRF: R$ 1.387,50 × 7,5% - 84,72 = R$ 19,34
- Líquido: R$ 1.500 - 112,50 - 19,34 = **R$ 1.368,16**

### Exemplo: Salário R$ 8.000, 2 dependentes

**1ª Parcela:**
- Bruto: R$ 8.000 × 50% = R$ 4.000,00
- Líquido: **R$ 4.000,00**

**2ª Parcela:**
- Bruto: R$ 8.000 × 50% = R$ 4.000,00
- INSS: R$ 4.000 × 14% - 190,40 = R$ 369,60
- Base IRRF: R$ 4.000 - 369,60 - (2 × 189,59) = R$ 3.251,22
- Faixa semestral: 3ª (R$ 1.413,34 a R$ 1.875,53)... mas R$ 3.251,22 > R$ 2.332,34
- Faixa correta: 5ª (acima de R$ 2.332,34)
- IRRF: R$ 3.251,22 × 27,5% - 448,00 = R$ 445,59
- Líquido: R$ 4.000 - 369,60 - 445,59 = **R$ 3.184,81**

## 3. Férias

### Férias Integrais (30 dias)
```
Férias Bruto = Salário
1/3 Constitucional = Salário × 1/3
Total Bruto = Salário + 1/3 = Salário × 4/3
INSS = (Total Bruto × Alíquota) - Dedução
Base IRRF = Total Bruto - INSS - Dependentes
IRRR = (Base × Alíquota Semestral) - Dedução Semestral
```

### Exemplo: Salário R$ 3.000, 30 dias, 0 dependentes

1. Bruto: R$ 3.000 + R$ 1.000 = R$ 4.000,00
2. INSS: R$ 4.000 × 14% - 190,40 = R$ 369,60
3. Base: R$ 4.000 - 369,60 = R$ 3.630,40
4. Faixa semestral: 5ª (acima de R$ 2.332,34)
5. IRRF: R$ 3.630,40 × 27,5% - 448,00 = R$ 546,36
6. **Líquido: R$ 3.054,04**

### Férias Parceladas (10+10+10)
Cada parcela = Salário / 30 × 10 + 1/3
- Cada parcela tem INSS e IRRF próprios
- Mais favorável pois usa tabela semestral

### Com Abono Pecuniário (20 dias)
- Férias: Salário / 30 × 20 + 1/3
- Abono: Salário / 30 × 10 + 1/3 (SEM INSS/IRRF)
- INSS incide só sobre férias
- IRRF incide só sobre férias

## 4. Rescisão

### Aviso Prévio Indenizado
```
Dias = 30 + 3 por ano (máx 90)
Valor = Salário / 30 × Dias
INSS = (Valor × Alíquota) - Dedução
IRRF = (Base × Alíquota Semestral) - Dedução Semestral
```

### Exemplo: Salário R$ 3.000, 3 anos de casa, aviso indenizado

1. Dias: 30 + 9 = 39
2. Aviso: R$ 3.000 / 30 × 39 = R$ 3.900,00
3. INSS: R$ 3.900 × 14% - 190,40 = R$ 355,60
4. Base: R$ 3.900 - 355,60 = R$ 3.544,40
5. Faixa semestral: 4ª (R$ 1.875,54 a R$ 2.332,34)... mas R$ 3.544,40 > R$ 2.332,34
6. Faixa correta: 5ª
7. IRRF: R$ 3.544,40 × 27,5% - 448,00 = R$ 526,71
8. **IRRF aviso: R$ 526,71**

## 5. Horas Extras

```
Valor HE = (Salário / 220) × Adicional %
INSS HE = (Valor HE × Alíquota) - Dedução
IRRF HE = (Base HE × Alíquota) - Dedução
```

### Exemplo: Salário R$ 3.000, 10 HE normais

1. Hora: R$ 3.000 / 220 = R$ 13,64
2. HE: R$ 13,64 × 50% = R$ 6,82
3. Total 10 HE: R$ 68,18
4. INSS: R$ 68,18 × 7,5% = R$ 5,11 (aprox)
5. IRRF: Calculado junto com salário mensal

## 6. Tabela Comparativa de Impacto

| Salário Bruto | INSS | IRRF | Líquido | Carga Total |
|-------------:|-----:|-----:|--------:|:-----------:|
| R$ 2.000 | R$ 157,23 | R$ 0,00 | R$ 1.842,77 | 7,86% |
| R$ 3.000 | R$ 253,41 | R$ 36,56 | R$ 2.710,03 | 9,67% |
| R$ 5.000 | R$ 509,60 | R$ 347,57 | R$ 4.142,83 | 17,14% |
| R$ 8.000 | R$ 929,60 | R$ 1.028,14 | R$ 6.042,26 | 24,47% |
| R$ 10.000 | R$ 1.215,43 | R$ 1.626,72 | R$ 7.157,85 | 28,42% |

## 7. Motor de Cálculo em .NET

```csharp
public class IrrfCalculator
{
    public static decimal Calculate(decimal baseIrrf, bool semestral = false)
    {
        if (semestral)
        {
            if (baseIrrf <= 1129.60m) return 0;
            if (baseIrrf <= 1413.33m) return baseIrrf * 0.075m - 84.72m;
            if (baseIrrf <= 1875.53m) return baseIrrf * 0.15m - 190.72m;
            if (baseIrrf <= 2332.34m) return baseIrrf * 0.225m - 331.39m;
            return baseIrrf * 0.275m - 448.00m;
        }
        
        if (baseIrrf <= 2259.20m) return 0;
        if (baseIrrf <= 2826.65m) return baseIrrf * 0.075m - 169.44m;
        if (baseIrrf <= 3751.05m) return baseIrrf * 0.15m - 381.44m;
        if (baseIrrf <= 4664.68m) return baseIrrf * 0.225m - 662.77m;
        return baseIrrf * 0.275m - 896.00m;
    }
}
```

## Fontes Oficiais
- Lei 14.848/2024
- Portaria RFB nº 2.246/2025
- Tabela IRRF Sincronizada
