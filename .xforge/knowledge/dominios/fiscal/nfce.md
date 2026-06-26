---
id: nfce
type: knowledge
tags: [fiscal, nfce, consumidor, eletronico, varejo, qrcode]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, regras e integração da Nota Fiscal de Consumidor Eletrônica (NFC-e, modelo 65), documento fis...
- **Principais responsabilidades**: Definir o layout XML da NFC-e (versão 4.00, baseado no layout NF-e); Documentar diferenças em relação à NF-e e ao SAT; Cobrir QR Code, contingência...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, nfce, consumidor, eletronico, varejo, qrcode
- **Restrições/Regras**: Transmissão online obrigatória (sem contingência na maioria dos estados); QR Code obrigatório no DANFE

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `nfce` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 13 |


# NFC-e — Nota Fiscal de Consumidor Eletrônica

## Purpose
Documentar a estrutura, regras e integração da Nota Fiscal de Consumidor Eletrônica (NFC-e, modelo 65), documento fiscal para vendas ao consumidor final no varejo, alternativa ao cupom fiscal (ECF) e ao SAT.

## Responsibilities
- Definir o layout XML da NFC-e (versão 4.00, baseado no layout NF-e)
- Documentar diferenças em relação à NF-e e ao SAT
- Cobrir QR Code, contingência e integração com PDV
- Listar estados que adotam NFC-e

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3)
- WebService da SEFAZ da UF correspondente
- Impressora térmica (ESC/POS) para DANFE NFC-e

## Constraints
- Transmissão online obrigatória (sem contingência na maioria dos estados)
- QR Code obrigatório no DANFE
- Cancelamento: até 30 minutos após emissão
- Destinatário opcional para compras abaixo de R$ 200

## Conceito
A NFC-e substitui o cupom fiscal impresso (ECF) em vários estados, reduzindo custos de hardware fiscal e permitindo fiscalização em tempo real. Utiliza assinatura digital do emissor e transmissão via WebService.

## Diferenças NFC-e vs NF-e
| Aspecto | NF-e | NFC-e |
|---------|------|-------|
| Modelo | 55 | 65 |
| Destinatário | Obrigatório | Opcional (varejo) |
| DANFE | A4 completo | Simplificado (QR Code) |
| Contingência | Sim | Não (online obrigatório) |
| Cancelamento | Até 24h/168h | Até 30 min |

## Diferenças NFC-e vs SAT (CF-e)
| Aspecto | NFC-e | SAT |
|---------|-------|-----|
| Uso | Múltiplos estados | Apenas São Paulo |
| Equipamento | Software + certificado | Hardware SAT dedicado |
| Assinatura | Certificado do emitente | Pelo equipamento SAT |
| Offline | Sim (contingência) | Não |

## Layout (simplificado vs NF-e)
- **ide**: mod(65), tpImp(4=NFC-e/5=DANFE NFC-e), tpEmis(1=normal/9=offline), indFinal(1=sim)
- **dest**: CPF/CNPJ opcional, xNome opcional
- **pag**: detPag(tPag, vPag, card com tpIntegra=1 TEF/2 POS)
- Mesmos grupos de impostos da NF-e (ICMS, PIS, COFINS)

## QR Code
- Composição: `https://[URL_SEFAZ]/nfce/qrcode?p=[chave]|[versaoQR]|[ambiente]|[cIdToken]|[cHashQRCode]`
- Hash: SHA-1 da concatenação de chave + versaoQR + ambiente + cIdToken
- Consulta pública via QR Code no DANFE

## Contingência
| tpEmis | Tipo |
|--------|------|
| 1 | Normal |
| 2 | FS-IA |
| 9 | Off-line NFC-e |

## Integração com PDV
- Arquitetura: PDV → Módulo NFC-e → WebService SEFAZ
- Comunicação síncrona (enviNFe → retEnviNFe) ou assíncrona (via nRec)
- Bibliotecas: ACBr.Net (.NET), JNF-e (Java), erpbrasil.assinatura (Python), sped-nfe (PHP)

## Estados com NFC-e (2026)
AC, AL, AM, AP, BA, CE, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, TO. SP utiliza SAT.

## Related Documents
- [NF-e](nfe.md) — nota fiscal eletrônica (modelo 55)
- [SAT/CF-e](sat-cfe.md) — cupom fiscal eletrônico de São Paulo
- [DANFE](danfe-dacte.md) — documento auxiliar da NF-e
