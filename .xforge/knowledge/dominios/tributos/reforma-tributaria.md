---
id: tributos-reforma-tributaria
type: knowledge
tags: [tributos, reforma, cbs, ibs, imposto-seletivo, transicao]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar a Reforma Tributária do consumo, seus novos tributos, cronograma de transição e impacto nos sistemas.
- **Principais responsabilidades**: Explicar os novos tributos (CBS, IBS, IS); Detalhar o cronograma de transição 2026-2033; Cobrir regimes diferenciados, cashback e split payment
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, reforma, cbs, ibs, imposto-seletivo, transicao
- **Restrições/Regras**: Alíquotas definitivas dependem de regulamentação; Transição exige manutenção de sistemas antigo e novo em paralelo

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-reforma-tributaria` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# Reforma Tributária Brasileira — EC 132/2023 e LC 214/2025

## Purpose
Documentar a Reforma Tributária do consumo, seus novos tributos, cronograma de transição e impacto nos sistemas.

## Responsibilities
- Explicar os novos tributos (CBS, IBS, IS)
- Detalhar o cronograma de transição 2026-2033
- Cobrir regimes diferenciados, cashback e split payment

## Dependencies
- `regimes-tributarios.md` — impacto nos regimes atuais
- `icms.md` — ICMS → IBS
- `pis-cofins.md` — PIS/COFINS → CBS
- `ipi-iss.md` — IPI → IS, ISS → IBS

## Conteúdo

### Visão Geral
A Reforma Tributária substitui **5 tributos** (PIS, COFINS, IPI, ICMS, ISS) por **3 novos**: **CBS** (federal), **IBS** (estadual/municipal) e **Imposto Seletivo** (IS). Base legal: EC 132/2023 e LC 214/2025.

### Cronograma de Transição
| Ano | CBS | IBS | PIS/COFINS | ICMS/ISS |
|---|---|---|---|---|
| 2026 | 0,9% (piloto) | 0,1% (piloto) | Redução | Normal |
| 2027 | Substitui P/COF | — | Extinto | Normal |
| 2028-2032 | Plena | Transição crescente | — | Redução |
| 2033 | Plena | Substitui ICMS/ISS | — | Extinto |

### CBS — Contribuição sobre Bens e Serviços
- **Competência**: Federal
- **Substitui**: PIS e COFINS
- **Alíquota referência**: ~8,8%
- **Regime**: Não cumulativo com créditos amplos
- **Split Payment**: Desconto automático pelo banco

### IBS — Imposto sobre Bens e Serviços
- **Competência**: Estadual e Municipal (Comitê Gestor do IBS)
- **Substitui**: ICMS e ISS
- **Alíquota referência**: ~17,2%
- **Princípio do destino**: Tributo cobrado no local de consumo
- **Split Payment**: Desconto automático pelo banco

### Imposto Seletivo (IS)
- **Competência**: Federal
- **Substitui**: IPI (parcialmente)
- **Incidência**: Bens prejudiciais à saúde e meio ambiente
- **Exemplos**: Cigarros, bebidas, veículos poluentes, minérios
- **Função**: Extravasora (desestimular consumo)

### Alíquota de Referência
| Tributo | Alíquota |
|---|---|
| CBS | ~8,8% |
| IBS | ~17,2% |
| **Total IVA dual** | **~26,5%** |

### Regimes Diferenciados
| Setor | Redução |
|---|---|
| Saúde, Educação | 60% |
| Transporte público | 60% |
| Produtos agropecuários | 60% |
| Cesta básica nacional | Alíquota zero |
| Imóveis | Redução |
| ZFM | Manutenção |

### Cashback
- Devolução parcial de IBS e CBS para famílias de baixa renda
- Foco: energia elétrica, gás, combustíveis, alimentação
- Implementação progressiva

### Split Payment
- Desconto automático do tributo no momento do pagamento
- Banco desconta CBS/IBS/IS e repassa ao fisco
- Plataforma Pública desenvolvida pela RFB e Comitê Gestor do IBS
- Documentação técnica publicada em junho/2026

### Impacto para ERPs
1. Novos tributos: campos de CBS, IBS, IS em NF-e/NFS-e
2. Alíquotas variáveis por tipo de bem/serviço e localidade
3. Integração com plataforma de split payment
4. Lógica de regimes diferenciados
5. Transição longa (2026-2033): suportar dois modelos simultaneamente

## Constraints
- Alíquotas definitivas dependem de regulamentação
- Transição exige manutenção de sistemas antigo e novo em paralelo

## Related Documents
- `regimes-tributarios.md` — Impacto nos regimes
- `icms.md` — ICMS → IBS
- `pis-cofins.md` — PIS/COFINS → CBS
- `ipi-iss.md` — IPI → IS, ISS → IBS

