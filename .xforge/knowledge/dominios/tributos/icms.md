---
id: tributos-icms
type: knowledge
tags: [tributos, icms, estadual, substituicao-tributaria, difal]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar o ICMS, principal tributo estadual brasileiro, suas alíquotas, regimes e obrigações acessórias.
- **Principais responsabilidades**: Explicar conceito, base de cálculo e alíquotas do ICMS; Detalhar substituição tributária, DIFAL e FCP; Listar regimes especiais e obrigações acessó...
- **Seções principais**: Purpose, Responsabilities, Dependencies, Conteúdo
- **Tags**: tributos, icms, estadual, substituicao-tributaria, difal
- **Restrições/Regras**: Cada UF legisla sobre alíquotas internas e incentivos; Convênios CONFAZ e Ajustes SINIEF regulam operações interestad...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-icms` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# ICMS — Imposto sobre Circulação de Mercadorias e Serviços

## Purpose
Documentar o ICMS, principal tributo estadual brasileiro, suas alíquotas, regimes e obrigações acessórias.

## Responsabilities
- Explicar conceito, base de cálculo e alíquotas do ICMS
- Detalhar substituição tributária, DIFAL e FCP
- Listar regimes especiais e obrigações acessórias

## Dependencies
- `regimes-tributarios.md` — enquadramento por regime
- `pis-cofins.md` — interação com PIS/COFINS
- `ipi-iss.md` — tributos correlatos

## Conteúdo

### Conceito
O ICMS é o principal tributo estadual, previsto no art. 155 da CF e regulado pela Lei Kandir (LC 87/1996). Incide sobre circulação de mercadorias e serviços de transporte e comunicação. É **não cumulativo** (crédito na entrada, débito na saída).

### Alíquotas
| Tipo | Alíquota |
|---|---|
| Interna (maioria UFs) | 17% ou 18% |
| Interestadual (origem N/NE/CO/ES) | 7% |
| Interestadual (destino S/SE) | 12% |
| Importados | 4% (ou interna da UF) |
| ST (Substituição Tributária) | Variável (MVA/Pauta) |

### Base de Cálculo
```
Base = Valor da operação + Frete + Seguro + Despesas acessórias – Descontos condicionais
```

### Substituição Tributária (ST)
- Antecipa o ICMS para operações subsequentes
- Responsável: primeiro da cadeia (industrial/importador)
- Cálculo por **MVA** (Margem de Valor Agregado) ou **Pauta**
- Recolhimento via guia própria ou DIFAL

### Diferencial de Alíquotas (DIFAL)
- Aplica-se a operações interestaduais para consumidor final (não contribuinte)
- Partilha entre UF de origem e destino (EC 87/2015)
- A partir de 2026: 100% para UF de destino
- Inclui **FCP** (Fundo de Combate à Pobreza) em alguns estados

### Regimes Especiais
| Regime | Descrição |
|---|---|
| Simples Nacional | ICMS incluído no DAS |
| Crédito Presumido | Incentivo fiscal outorgado |
| Diferimento | Postergação do recolhimento |
| Isenção | Conforme legislação estadual |
| Imunidade | Não incidência constitucional (livros, jornais) |

### Obrigações Acessórias
- **EFD ICMS/IPI** (Sped Fiscal) — Blocos C e E
- **DIFAL** — guia própria (GNRE)
- **GIA** — em alguns estados

### Regras
- Apuração mensal (geralmente)
- Crédito de ICMS na entrada: direito a compensação
- Prazos definidos por cada UF
- Reforma Tributária: ICMS será substituído pelo IBS até 2033

## Constraints
- Cada UF legisla sobre alíquotas internas e incentivos
- Convênios CONFAZ e Ajustes SINIEF regulam operações interestaduais

## Related Documents
- `regimes-tributarios.md` — Simples Nacional e regimes
- `ipi-iss.md` — IPI e ISS
- `reforma-tributaria.md` — Substituição por IBS

