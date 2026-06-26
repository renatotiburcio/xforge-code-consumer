---
id: nfe
type: knowledge
tags: [fiscal, nfe, nota-fiscal, eletronico, sefaz]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, regras e eventos da Nota Fiscal Eletrônica (NF-e, modelo 55), documento fiscal eletrônico que...
- **Principais responsabilidades**: Definir o layout XML da NF-e (versão 4.00); Documentar tipos de operação (entrada/saída), CFOP, CST e status; Cobrir eventos: cancelamento, carta d...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, nfe, nota-fiscal, eletronico, sefaz
- **Restrições/Regras**: Assinatura digital obrigatória; Armazenamento do XML por no mínimo 5 anos

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `nfe` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 9 |


# NF-e — Nota Fiscal Eletrônica

## Purpose
Documentar a estrutura, regras e eventos da Nota Fiscal Eletrônica (NF-e, modelo 55), documento fiscal eletrônico que substitui a nota fiscal em papel (modelo 1/1A) para operações comerciais de mercadorias.

## Responsibilities
- Definir o layout XML da NF-e (versão 4.00)
- Documentar tipos de operação (entrada/saída), CFOP, CST e status
- Cobrir eventos: cancelamento, carta de correção, manifestação do destinatário
- Referenciar DANFE como representação gráfica

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3) para assinatura
- WebService da SEFAZ para autorização
- Consulta pública via chave de acesso (44 dígitos)

## Constraints
- Assinatura digital obrigatória
- Armazenamento do XML por no mínimo 5 anos
- Validação no webservice antes da emissão
- DANFE obrigatório para acompanhar o trânsito da mercadoria

## Layout Principal (infNFe)
- **ide**: cUF, cNF, natOp, mod(55), serie, nNF, dhEmi, tpNF(0=entrada/1=saída), idDest, tpImp, tpEmis, finNFe, indFinal, indPres
- **emit**: CNPJ, xNome, xFant, enderEmit, IE, CRT(1=Simples/2=Simples excesso/3=Normal)
- **dest**: CNPJ/CPF, xNome, enderDest, indIEDest(1=contribuinte/2=isento/9=não contribuinte)
- **det**: nItem, prod(cProd, cEAN, xProd, NCM, CFOP, uCom, qCom, vUnCom, vProd), imposto(ICMS, IPI, PIS, COFINS, ICMSUFDest, FCP)
- **total**: ICMSTot(vBC, vICMS, vBCST, vST, vProd, vNF, vTotTrib)
- **transp**: modFrete(0=emitente/1=destinatário/2=terceiros/9=sem frete), transporta, veicTransp, vol
- **cobr**: fat(nFat, vOrig, vDesc, vLiq), dup(nDup, dVenc, vDup)
- **pag**: detPag(tPag, vPag, indPag, card)
- **infAdic**: infAdFisco, infCpl

## Chave de Acesso (44 dígitos)
| cUF(2) | AAMM(4) | CNPJ(14) | mod(2) | serie(3) | nNF(9) | tpEmis(1) | cNF(8) | cDV(1) |

## Status da NF-e
| Código | Descrição |
|--------|-----------|
| 100 | Autorizado o uso |
| 101 | Cancelamento homologado |
| 102 | Inutilização homologada |
| 110 | Uso denegado |
| 301 | Denegada — irregularidade fiscal do emitente |
| 302 | Denegada — destinatário não habilitado |

## Eventos
- **Cancelamento** (evCancNFe): até 24h em alguns estados, até 168h em outros
- **Carta de Correção** (evCCeNFe): erros não tributários, até 720h
- **EPEC**: emissão em contingência
- **Manifestação do Destinatário** (evDest): ciência, confirmação, desconhecimento, operação não realizada

## Related Documents
- [DANFE](danfe-dacte.md) — representação gráfica da NF-e
- [NFC-e](nfce.md) — nota fiscal de consumidor eletrônico
- [CT-e](cte.md) — conhecimento de transporte eletrônico
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital
