---
id: tributos-irpj-csll
type: knowledge
tags: [tributos, irpj, csll, federal, lucro, renda]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar IRPJ e CSLL, tributos federais sobre o lucro das pessoas jurídicas, seus regimes de apuração e regras de c...
- **Principais responsabilidades**: Explicar alíquotas, adicional e regimes de apuração; Detalhar adições, exclusões e compensação de prejuízos; Cobrir LALUR e obrigações acessórias
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, irpj, csll, federal, lucro, renda
- **Restrições/Regras**: Alíquotas e regras sujeitas a alteração legislativa; Instituições financeiras têm CSLL diferenciada

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-irpj-csll` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# IRPJ/CSLL — Imposto de Renda e Contribuição Social sobre o Lucro

## Purpose
Documentar IRPJ e CSLL, tributos federais sobre o lucro das pessoas jurídicas, seus regimes de apuração e regras de cálculo.

## Responsibilities
- Explicar alíquotas, adicional e regimes de apuração
- Detalhar adições, exclusões e compensação de prejuízos
- Cobrir LALUR e obrigações acessórias

## Dependencies
- `regimes-tributarios.md` — enquadramento por regime
- `pis-cofins.md` — tributos federais correlatos
- `reforma-tributaria.md` — impacto da reforma

## Conteúdo

### IRPJ — Imposto de Renda Pessoa Jurídica
**Competência**: Federal (CF, art. 153, III)

#### Alíquotas
| Base de Cálculo | Alíquota |
|---|---|
| Até R$ 20.000/mês | 15% |
| Acima de R$ 20.000/mês | 15% + 10% adicional |

O adicional de 10% incide sobre a parcela que exceder R$ 20.000/mês (R$ 60.000/trimestre).

### CSLL — Contribuição Social sobre o Lucro Líquido
**Competência**: Federal (CF, art. 154, I)

#### Alíquotas
| Atividade | Alíquota |
|---|---|
| Empresas em geral | 9% |
| Instituições financeiras | 15% (2026) |
| Seguradoras | 15% |

### Regimes de Tributação
| Regime | IRPJ | CSLL | Obrigatoriedade |
|---|---|---|---|
| Lucro Real | 15%+10% | 9% | Receita > R$ 78M |
| Lucro Presumido | 15%+10% sobre presumido | 9% sobre presumido | Receita ≤ R$ 78M |
| Lucro Arbitrado | 15%+10% sobre arbitrado | 9% sobre arbitrado | Inadimplência fiscal |
| Simples Nacional | No DAS | No DAS | ME/EPP |

### Percentuais de Presunção (Lucro Presumido)
| Atividade | IRPJ | CSLL |
|---|---|---|
| Comércio/Indústria | 8% | 12% |
| Serviços em geral | 32% | 32% |
| Serviços hospitalares | 8% | 12% |
| Transporte de carga | 8% | 12% |
| Demais transportes | 16% | 12% |

### Lucro Real — Adições e Exclusões
**Adições**: Multas fiscais, doações não dedutíveis, despesas com brindes, juros sobre capital próprio, excesso de depreciação.

**Exclusões**: Dividendos recebidos, equivalência patrimonial positiva, reversão de provisões, subvenções para investimento.

### Compensação de Prejuízos
- **Limite**: 30% do lucro tributável do período
- **Prazo**: Indefinido (sem limite temporal)
- **Controle**: LALUR Parte B
- **Restrição**: Não compensa prejuízos anteriores à opção pelo Lucro Real

### Regimes de Apuração (Lucro Real)
| Regime | Descrição |
|---|---|
| Trimestral | Apuração em 31/03, 30/06, 30/09, 31/12 |
| Anual | Apuração em 31/12 com estimativa mensal |

### Obrigações Acessórias
- **ECF** — Escrituração Contábil Fiscal (substitui DIPJ)
- **ECD** — Escrituração Contábil Digital
- **LALUR** — Livro de Apuração do Lucro Real
- **DIRF** — Declaração do IR Retido na Fonte

### Regras
- Apuração: trimestral ou anual
- Compensação de prejuízos: apenas no Lucro Real
- Retenção na fonte: IRRF, PIS, COFINS, CSLL

## Constraints
- Alíquotas e regras sujeitas a alteração legislativa
- Instituições financeiras têm CSLL diferenciada

## Related Documents
- `regimes-tributarios.md` — Regimes de tributação
- `pis-cofins.md` — Tributos federais
- `reforma-tributaria.md` — Impactos da reforma

