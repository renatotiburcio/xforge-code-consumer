---
id: efd-icms-ipi
type: knowledge
tags: [fiscal, efd, sped, icms, ipi, escrituracao, bloco]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, blocos, registros e regras da EFD ICMS/IPI (SPED Fiscal), arquivo digital que contém informaç...
- **Principais responsabilidades**: Definir a estrutura completa dos blocos e registros; Documentar obrigados, prazos e regras de validação; Cobrir registros principais (0000, C100, C...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, efd, sped, icms, ipi, escrituracao, bloco
- **Restrições/Regras**: Arquivo em formato TXT com layout definido; Assinatura digital obrigatória

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `efd-icms-ipi` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 11 |


# EFD ICMS/IPI — Escrituração Fiscal Digital (SPED Fiscal)

## Purpose
Documentar a estrutura, blocos, registros e regras da EFD ICMS/IPI (SPED Fiscal), arquivo digital que contém informações sobre operações de ICMS e IPI, substituindo os livros fiscais em papel.

## Responsibilities
- Definir a estrutura completa dos blocos e registros
- Documentar obrigados, prazos e regras de validação
- Cobrir registros principais (0000, C100, C170, C190, D100, E100, E110, H005, K200)
- Explicar inventário (Bloco H) e CIAP (Bloco G)

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3) para assinatura
- PVA (Programa Validador e Assinador) para validação
- Receitanet para transmissão
- Dados de documentos fiscais, apuração e inventário

## Constraints
- Arquivo em formato TXT com layout definido
- Assinatura digital obrigatória
- Validação no PVA antes de transmissão
- Manter documentação por 5 anos
- Retificação dentro do prazo sem multa

## Obrigatoriedade
**Obrigados:** Contribuintes de ICMS (comerciantes, indústrias, transportadores, comunicação) e contribuintes de IPI (indústrias).
**Dispensados:** Optantes pelo Simples Nacional (exceto se a UF exigir).

## Blocos do Arquivo
- **Bloco 0** — Abertura e Cadastros: 0000(abertura), 0005(dados complementares), 0100(contabilista), 0150(participantes), 0190(unidades), 00200(itens), 0300(bens ativo), 0400(natureza operação), 0500(plano contas), 0600(centro custos)
- **Bloco C** — Documentos Fiscais: C100(NF/CT), C170(itens), C190(analítico), C300(resumo diário), C350(NF consumidor), C400(ECF), C420(totalizadores), C460(doc ECF), C500(energia), C600(consolidação), C700(NF-e/NFC-e), C800(CF-e SAT)
- **Bloco D** — Transporte: D100(CT), D190(analítico), D300(resumo), D350(SAT), D400(resumo movimento), D500(comunicação)
- **Bloco E** — Apuração: E100(período ICMS), E110(apur. ICMS), E111(ajuste), E115(inf. adicionais), E116(obrigações), E200/210(ICMS ST), E300/310(DIFAL), E500/510(IPI)
- **Bloco G** — CIAP: G110(ativo permanente), G125(movimento bem)
- **Bloco H** — Inventário: H005(totais), H010(inventário)
- **Bloco 1** — Obrigações Estaduais: 1010(ICMS ST), 1100(créditos ICMS)
- **Bloco 9** — Controle: 9001(abertura), 9900(registros), 9999(encerramento)

## Registros Principais
- **0000**: CNPJ, nome, UF, IE, município, período, versão leiaute
- **C100**: IND_OPER(0=entrada/1=saída), IND_EMIT(0=próprio/1=terceiros), COD_MOD(55=NF-e), COD_SIT, CHV_NFE, DT_DOC, VL_DOC, VL_ICMS, VL_IPI
- **C170**: NUM_ITEM, COD_ITEM, QTD, UNID, VL_ITEM, CFOP, COD_NCM, VL_BC_ICMS, ALIQ_ICMS, VL_ICMS, ALIQ_PIS, VL_PIS, ALIQ_COFINS, VL_COFINS
- **C190**: CST_ICMS, CFOP, ALIQ_ICMS, VL_OPR, VL_BC_ICMS, VL_ICMS, VL_BC_ICMS_ST, VL_ICMS_ST, VL_IPI
- **D100**: Conhecimento de transporte (CT-e)
- **E100**: Período de apuração do ICMS
- **E110**: VL_TOT_DEBITOS, VL_TOT_CREDITOS, VL_AJ_APUR, VL_ICMS_RECOLHER
- **H005**: DT_INV, VL_INV (totais do inventário)
- **K200**: Controle de estoque (bloco K — quando exigido)

## Prazo de Entrega
- **Mensal:** até o dia 20 do mês seguinte ao período de apuração
- **Anual (inventário):** no período de apuração de janeiro do ano seguinte

## Livros Substituídos
| Livro | Bloco |
|-------|-------|
| Registro de Entradas | C |
| Registro de Saídas | C |
| Registro de Inventário | H |
| Registro de Apuração ICMS | E |
| Registro de Apuração IPI | E |

## Validações
- Validar no PVA antes de transmitir
- Assinatura digital obrigatória (e-CNPJ)
- Cruzamento com EFD Contribuições (chaves NF-e)
- Contadores no bloco 9 devem bater com quantidade real

## Related Documents
- [EFD Contribuições](efd-contribuicoes.md) — escrituração PIS/COFINS
- [NF-e](nfe.md) — nota fiscal eletrônica
- [CT-e](cte.md) — conhecimento de transporte eletrônico
- [SPED Overview](../obrigacoes/sped-overview.md) — visão geral do SPED
