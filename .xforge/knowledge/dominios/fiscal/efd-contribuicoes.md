---
id: efd-contribuicoes
type: knowledge
tags: [fiscal, efd, sped, pis, cofins, contribuicoes, escrituracao]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, blocos, registros e regras da EFD Contribuições, arquivo digital que registra operações que i...
- **Principais responsabilidades**: Definir a estrutura completa dos blocos e registros; Documentar obrigados, prazos e regimes tributários; Cobrir registros principais (0000, A100, C...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, efd, sped, pis, cofins, contribuicoes, escrituracao
- **Restrições/Regras**: Arquivo em formato XML conforme leiaute técnico; Assinatura digital obrigatória

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `efd-contribuicoes` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 12 |


# EFD Contribuições — Escrituração Fiscal Digital (PIS/COFINS)

## Purpose
Documentar a estrutura, blocos, registros e regras da EFD Contribuições, arquivo digital que registra operações que impactam a apuração do PIS/Pasep e da COFINS nos regimes cumulativo e não cumulativo.

## Responsibilities
- Definir a estrutura completa dos blocos e registros
- Documentar obrigados, prazos e regimes tributários
- Cobrir registros principais (0000, A100, C100, C170, D100, M200, M400, M600, M800)
- Explicar regime cumulativo vs não-cumulativo e CSTs

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3) para assinatura
- Programa validador (ReCEF) para validação
- Dados de documentos fiscais e apuração PIS/COFINS

## Constraints
- Arquivo em formato XML conforme leiaute técnico
- Assinatura digital obrigatória
- Validação no ReCEF antes de transmissão
- Manter documentação por 5 anos
- Prazo: até o 10º dia útil do mês subsequente

## Obrigatoriedade
**Obrigados:** 1) Lucro Real — todas as empresas; 2) Lucro Presumido — todas as empresas; 3) Simples Nacional — apenas com PIS/COFINS retidos na fonte; 4) Pessoas jurídicas com receita bruta > R$ 78 milhões no ano anterior.
**Isentos:** ME/EPP do Simples Nacional (exceto retenção na fonte), entidades sem fins lucrativos.

## Blocos do Arquivo
- **Bloco 0** — Identificação: 0000(abertura), 0110(regimes apuração), 0111(receita bruta mensal), 0150(participantes), 0200(itens), 0400(natureza operação), 0900(composição receitas)
- **Bloco A** — Serviços ISS: A100(NF serviço), A170(itens)
- **Bloco C** — Mercadorias: C100(NF-e/NFC-e), C170(itens), C180/C190(consolidação), C400(ECF), C500(energia), C800(CF-e SAT)
- **Bloco D** — Serviços ICMS: D100(transporte), D300(comunicação), D500(telecom)
- **Bloco F** — Demais Documentos: F100(demais operações), F120(bens ativo), F130(créditos presumidos), F200(aquisição com crédito)
- **Bloco I** — Instituições Financeiras: I100(consolidação), I200(analítico)
- **Bloco M** — Apuração: M100(PIS apuração), M105(detalhamento BC), M110(ajustes), M200(PIS consolidada), M400(receitas isentas PIS), M500(COFINS apuração), M600(COFINS consolidada), M700(receitas isentas COFINS), M800(receitas sem incidência)
- **Bloco P** — JCP: P100(apuração JCP)
- **Bloco 1** — Controle: 1010(créditos PIS), 1020(créditos COFINS), 1100/1200/1300/1500(retenções)
- **Bloco 9** — Encerramento: 9900(registros), 9999(total linhas)

## Registros Principais
- **0000**: CNPJ, nome, UF, IE, município, período, versão leiaute
- **0110**: Regime apuração — 1=cumulativo, 2=não cumulativo, 3=ambos
- **0111**: Receita bruta mensal (Lucro Presumido)
- **A100**: Documento de serviço (ISS) com PIS/COFINS retido
- **C100**: NF-e/NFC-e — modelo, situação, chave, valor, indicador operação
- **C170**: Itens — CST PIS/COFINS, base de cálculo, alíquota, valor
- **D100**: Documento de serviço ICMS (transporte)
- **M200**: PIS consolidada — VL_BC_CONT, ALIQ_PIS, VL_PIS
- **M400**: Receitas isentas/não alcançadas — PIS
- **M600**: COFINS consolidada — VL_BC_CONT, ALIQ_COFINS, VL_COFINS
- **M800**: Receitas sem incidência — PIS/COFINS

## Regime Cumulativo vs Não-Cumulativo
| Regime | PIS | COFINS | Crédito |
|--------|-----|--------|---------|
| Cumulativo | 0,65% | 3,00% | Sem direito a crédito |
| Não cumulativo | 1,65% | 7,60% | Direito a crédito nas entradas |

## Alíquotas Monofásicas
| Produto | PIS | COFINS |
|---------|-----|--------|
| Combustíveis | 1,65% | 7,60% |
| Veículos novos | 0,76% | 4,00% |
| Autopeças | 0,76% | 4,00% |
| Perfumaria/cosméticos | 0,76% | 4,00% |

## CSTs PIS/COFINS (Principais)
- **01**: Tributável (BC × alíquota normal)
- **02**: Tributável (BC × alíquota diferenciada)
- **04**: Monofásica (alíquota zero)
- **06**: Alíquota zero
- **07**: Isenta
- **08**: Sem incidência
- **09**: Suspensão
- **49**: Outras operações de saída
- **50-67**: Ambos os regimes (créditos)
- **70-75**: Aquisição sem crédito
- **98**: Outras operações de entrada
- **99**: Outras operações

## Validações
- Registros obrigatórios mínimos por bloco
- Consistência entre blocos (0110 × M100/M500, 0200 × C170, 0150 × C100)
- Cruzamento com EFD ICMS/IPI (chaves NF-e)
- Contadores no bloco 9 devem bater com quantidade real

## Related Documents
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital ICMS/IPI
- [NF-e](nfe.md) — nota fiscal eletrônica
- [SPED Overview](../obrigacoes/sped-overview.md) — visão geral do SPED
