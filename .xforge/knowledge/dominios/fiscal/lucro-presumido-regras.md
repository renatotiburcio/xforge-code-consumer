---
id: lucro-presumido-regras
type: conhecimento
tags: [fiscal, lucro-presumido, presuncao, irpj, csll, pis, cofins]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Lucro Presumido - Regras Completas
- **Seções principais**: Base Legal, Conceito, Quem Pode Optar, Base de Cálculo Presumida
- **Tags**: fiscal, lucro-presumido, presuncao, irpj, csll, pis, cofins
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `lucro-presumido-regras` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 13 |


# Lucro Presumido - Regras Completas

## Base Legal
- Lei 9.249/1995
- Lei 9.718/1998
- Lei 10.637/2002 (PIS/COFINS)

## Conceito

O Lucro Presumido é um regime tributário que aplica alíquotas sobre uma base de cálculo presumida (percentual da receita bruta), sem necessidade de apurar o lucro real.

## Quem Pode Optar

### Requisitos
- Receita bruta nos últimos 12 meses ≤ R$ 78.000.000,00
- Não estar excluído (atividade de financeira, seguro, etc.)
- Não ter lucro real obrigatório

### Atividades Permitidas
- Comércio em geral
- Indústria
- Serviços em geral
- Transporte (exceto carga)
- Locação de bens

### Atividades Excluídas
- Bancos e financeiras
- Seguradoras
- Corretoras de valores
- Mining
- Produção/proibidas

## Base de Cálculo Presumida

### Para IRPJ e CSLL

| Atividade | Presunção | Base IRPJ | Base CSLL |
|-----------|:---------:|:---------:|:---------:|
| Comércio | 8% | 32% | 32% |
| Indústria | 8% | 32% | 32% |
| Serviços em geral | 32% | 32% | 32% |
| Transporte de passageiros | 16% | 32% | 32% |
| Transporte de cargas | 8% | 32% | 32% |
| Serviços hospitalares | 8% | 32% | 32% |
| Sociedade profissional | 32% | 32% | 32% |
| Locação de bens | 32% | 32% | 32% |

## Alíquotas

### IRPJ
| Faixa | Alíquota |
|-------|:--------:|
| Até R$ 20.000/mês | 15% |
| Acima de R$ 20.000/mês | 10% adicional |

### CSLL
| Tipo | Alíquota |
|------|:--------:|
| Empresas em geral | 9% |
| Entidades financeiras | 15% |

### PIS (Lucro Presumido)
| Tipo | Alíquota | Base |
|------|:--------:|------|
| Receita bruta | 0,65% | Receita bruta |

### COFINS (Lucro Presumido)
| Tipo | Alíquota | Base |
|------|:--------:|------|
| Receita bruta | 3,00% | Receita bruta |

## Cálculo Mensal

### IRPJ
```
Base IRPJ = Receita Bruta × Presunção
IRPJ = Base IRPJ × 15%
Se Base IRPJ > R$ 20.000/mês → adicional 10%
```

### CSLL
```
Base CSLL = Receita Bruta × Presunção
CSLL = Base CSLL × 9%
```

### PIS
```
PIS = Receita Bruta × 0,65%
```

### COFINS
```
COFINS = Receita Bruta × 3,00%
```

## Exemplo: Empresa de Comércio

### Dados
- Receita bruta mensal: R$ 200.000,00
- Atividade: Comércio

### Cálculo

| Tributo | Base | Presunção | Alíquota | Valor |
|---------|-----:|:---------:|:--------:|------:|
| IRPJ | R$ 200.000 | 32% | 15% | R$ 9.600,00 |
| IRPJ adicional | R$ 200.000 × 32% = R$ 64.000 | - | 10% | R$ 4.400,00 |
| CSLL | R$ 200.000 | 32% | 9% | R$ 5.760,00 |
| PIS | R$ 200.000 | - | 0,65% | R$ 1.300,00 |
| COFINS | R$ 200.000 | - | 3,00% | R$ 6.000,00 |
| **Total** | | | | **R$ 27.060,00** |

**Carga tributária: 13,53%**

## Exemplo: Empresa de Serviços

### Dados
- Receita bruta mensal: R$ 100.000,00
- Atividade: Consultoria

### Cálculo

| Tributo | Base | Presunção | Alíquota | Valor |
|---------|-----:|:---------:|:--------:|------:|
| IRPJ | R$ 100.000 | 32% | 15% | R$ 4.800,00 |
| CSLL | R$ 100.000 | 32% | 9% | R$ 2.880,00 |
| PIS | R$ 100.000 | - | 0,65% | R$ 650,00 |
| COFINS | R$ 100.000 | - | 3,00% | R$ 3.000,00 |
| **Total** | | | | **R$ 11.330,00** |

**Carga tributária: 11,33%**

## Lucro Presumido Trimestral

### Regra
- Apuração trimestral (Janeiro-Março, Abril-Junho, etc.)
- Adicional de IRPJ: 10% sobre excedente de R$ 60.000/trimestre

### Exemplo Trimestral
- Receita trimestral: R$ 600.000
- Base IRPJ: R$ 600.000 × 32% = R$ 192.000
- IRPJ: R$ 192.000 × 15% = R$ 28.800
- Adicional: (R$ 192.000 - R$ 60.000) × 10% = R$ 13.200
- **IRPJ total: R$ 42.000**

## Diferença para Lucro Real

| Aspecto | Lucro Presumido | Lucro Real |
|---------|----------------|------------|
| Base IRPJ | Receita × 32% | Lucro contábil ajustado |
| Base CSLL | Receita × 32% | Lucro contábil ajustado |
| PIS/COFINS | 0,65% / 3,00% (não dedutível) | 1,65% / 7,60% (dedutível) |
| Escrituração | Simplificada | Completa |
| Obligatoriedade | Opcional (se ≤ R$ 78M) | Obrigatório (se > R$ 78M) |

## Vantagens do Lucro Presumido

1. **Simplicidade**: cálculo mais fácil
2. **Previsibilidade**: impostos fixos sobre receita
3. **Menor custo contábil**: menos obrigações
4. **Cash flow**: impostos proporcionais à receita

## Desvantagens do Lucro Presumido

1. **PIS/COFINS não dedutível**: 3,65% sobre receita
2. **Presunção pode ser maior que lucro real**: paga mais
3. **Sem crédito de PIS/COFINS**: não recupera
4. **Lucro baixo**: pode ser prejudicado

## Fontes Oficiais
- Lei 9.249/1995
- Lei 9.718/1998
- Lei 10.637/2002
- Portal da Receita Federal
