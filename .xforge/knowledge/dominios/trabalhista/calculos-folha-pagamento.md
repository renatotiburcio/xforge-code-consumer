---
id: calculos-folha-pagamento
type: conhecimento
tags: [trabalhista, folha, calculo, inss, irrf, ferias, 13o, rescisao]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Cálculos completos de folha de pagamento — salário líquido, férias, 13º, rescisão, INSS progressivo e IRRF
- **Seções principais**: Salário Líquido, Férias com 1/3, 13º Salário, Rescisão (justa/injusta), INSS progressivo, IRRF progressivo
- **Tags**: trabalhista, folha, calculo, inss, irrf, ferias, 13o, rescisao

## Quick Reference

| Item | Fórmula/Regra |
|------|---------------|
| Salário Líquido | Bruto - INSS - IRRF |
| Férias | (Salário/30) × Dias + 1/3 |
| 13º | (Bruto/12) × Meses trabalhados |
| INSS | Progressivo: 7.5% a 14% (tabela 2025) |
| IRRF | Progressivo: isento até R$2.259,20 |

# Cálculos de Folha de Pagamento

## 1. Salário Líquido

### Fórmula
```
Salário Líquido = Salário Bruto - INSS - IRRF
```

### Passo-a-Passo
1. Calcular INSS (tabela progressiva)
2. Calcular base do IRRF = Salário Bruto - INSS - Dependentes - Pensão
3. Calcular IRRF (tabela progressiva)
4. Salário Líquido = Salário Bruto - INSS - IRRF

## 2. Férias

### Cálculo
```
Férias = Salário / 30 × Dias de Férias
Adicional 1/3 = Férias × 1/3
Total = Férias + Adicional 1/3
```

### Exemplo: 30 dias de férias, salário R$ 3.000
- Férias: R$ 3.000,00
- Adicional 1/3: R$ 1.000,00
- **Total bruto: R$ 4.000,00**

### Abono pecuniário (venda de 10 dias)
```
Abono = Salário / 30 × 10
1/3 sobre abono = Abono × 1/3
```

### INSS sobre Férias
- Incide sobre: férias + 1/3
- Não incide sobre abono pecuniário

### IRRF sobre Férias
- Base: férias + 1/3 - INSS - dependentes
- Tabela semestral (mais favorável)

## 3. Décimo Terceiro Salário

### Cálculo (proporcional)
```
13º = Salário / 12 × Meses trabalhados
```

### Regras
- Mínimo 15 dias no mês = mês cheio
- Admissão no dia 15+ = conta como mês cheio
- Demissão sem justa causa = proporcional

### Exemplo: Admissão 01/03/2025, salário R$ 3.000
- Meses trabalhados: 10 (março a dezembro)
- 13º: R$ 3.000,00 / 12 × 10 = **R$ 2.500,00**

### INSS sobre 13º
- Incide sobre o 13º bruto
- Tabela progressiva normal

### IRRF sobre 13º
- Base: 13º - INSS - dependentes
- Tabela semestral

## 4. Rescisão

### Tipos de Rescisão

#### a) Demissão sem Justa Causa
```
Verbas devidas:
- Saldo de salário
- Aviso prévio (30 dias + 3 por ano, máx 90)
- 13º proporcional
- Férias vencidas + 1/3
- Férias proporcionais + 1/3
- Multa 40% FGTS
- Avos proporcionais
```

#### b) Demissão por Justa Causa
```
Verbas devidas:
- Saldo de salário
- Férias vencidas + 1/3 (sem 1/3 constitucional)

NÃO devidas:
- Aviso prévio
- 13º proporcional
- Férias proporcionais
- Multa 40% FGTS
- Seguro-desemprego
```

#### c) Pedido de Demissão
```
Verbas devidas:
- Saldo de salário
- 13º proporcional
- Férias proporcionais + 1/3
- Férias vencidas + 1/3

NÃO devidas:
- Aviso prévio (ou indenizado se dispensado)
- Multa 40% FGTS
- Seguro-desemprego
```

#### d) Acordo (Art. 484-A CLT)
```
Verbas devidas:
- Saldo de salário
- Aviso prévio (metade)
- 13º proporcional
- Férias proporcionais + 1/3
- Multa 20% FGTS (metade)
- Saque FGTS (50%)
```

### Fórmulas de Rescisão

#### Saldo de Salário
```
Saldo = Salário / 30 × Dias trabalhados no mês
```

#### Aviso Prévio
```
Aviso = 30 dias + 3 dias por ano de serviço (máx 90 dias)
Indenizado = Aviso × Salário / 30
```

#### 13º Proporcional
```
13º = Salário / 12 × Meses trabalhados
```

#### Férias Proporcionais
```
Férias = Salário / 12 × Meses trabalhados (mín 14 dias = 1 mês)
```

#### Multa FGTS
```
Multa = Saldo FGTS × 40%
```

## 5. Horas Extras

### Fórmula
```
Valor Hora Extra = (Salário / 220) × Adicional %
```

### Adicionais Mínimos
| Tipo | Adicional |
|------|:---------:|
| Hora extra normal | 50% |
| Hora extra domingo/feriado | 100% |
| Hora noturna (22h-5h) | 20% |

### Exemplo: Salário R$ 3.000, 10 horas extras normais
- Valor hora: R$ 3.000 / 220 = R$ 13,64
- Hora extra: R$ 13,64 × 50% = R$ 6,82
- Total 10 HE: R$ 6,82 × 10 = **R$ 68,18**

## 6. Adicionais

### Insalubridade
| Grau | Alíquota |
|------|:--------:|
| Mínimo | 10% |
| Médio | 20% |
| Máximo | 40% |

Base: salário mínimo

### Periculosidade
- Alíquota: 30%
Base: salário base (sem adicionais)

## 7. Benefícios

### Vale Transporte
- Desconto: até 6% do salário base
- Empresa paga diferença
- Obrigatório para deslocamento casa-trabalho

### Vale Refeição/Alimentação
- Não há desconto obrigatório
- Pode ser descontado se previsto em acordo
- Não tem natureza salarial (maioria)

### Plano de Saúde
- Empresa pode descontar até 6% do salário
- Dependentes incluídos

## Resumo de Incidências

| Verba | INSS | IRRF | FGTS |
|-------|:----:|:----:|:----:|
| Salário | Sim | Sim | Sim |
| Férias | Sim | Sim | Sim |
| 1/3 férias | Sim | Sim | Sim |
| 13º | Sim | Sim | Sim |
| Hora extra | Sim | Sim | Sim |
| Adicional noturno | Sim | Sim | Sim |
| Adicional insalubridade | Sim | Sim | Sim |
| Adicional periculosidade | Sim | Sim | Sim |
| Vale transporte | Não | Não | Não |
| Vale refeição | Não | Não | Não |
| Abono pecuniário | Não | Sim | Sim |
| Aviso prévio indenizado | Sim | Sim | Sim |
