---
id: cte
type: knowledge
tags: [fiscal, cte, transporte, carga, eletronico, dacte]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, regras e eventos do Conhecimento de Transporte Eletrônico (CT-e, modelo 57), documento fiscal...
- **Principais responsabilidades**: Definir o layout XML do CT-e (versão 3.00); Documentar tipos de CT-e (normal, substituição, complemento, redespacho); Cobrir modal rodoviário, segu...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, cte, transporte, carga, eletronico, dacte
- **Restrições/Regras**: Assinatura digital obrigatória; Armazenamento do XML por no mínimo 5 anos

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `cte` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 12 |


# CT-e — Conhecimento de Transporte Eletrônico

## Purpose
Documentar a estrutura, regras e eventos do Conhecimento de Transporte Eletrônico (CT-e, modelo 57), documento fiscal eletrônico que documenta a prestação de serviço de transporte de cargas entre municípios e estados.

## Responsibilities
- Definir o layout XML do CT-e (versão 3.00)
- Documentar tipos de CT-e (normal, substituição, complemento, redespacho)
- Cobrir modal rodoviário, seguro, carga e documentos transportados
- Explicar integração com MDF-e e DACTE

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3)
- WebService da SEFAZ para autorização
- RNTRC obrigatório para transportadores rodoviários

## Constraints
- Assinatura digital obrigatória
- Armazenamento do XML por no mínimo 5 anos
- DACTE obrigatório para acompanhar a carga em trânsito
- Cancelamento: até 720h (30 dias), sem eventos vinculados

## Conceito
O CT-e substituiu os conhecimentos de transporte em papel (modelos 7, 8, 9, 10, 11, 26, 27). É emitido por transportadores de carga (ETC, TAC, cooperativas) e documenta a prestação de serviço de transporte rodoviário, aéreo, ferroviário, aquaviário, dutoviário ou multimodal.

## Tipos de CT-e (tpCTe)
| Código | Descrição |
|--------|-----------|
| 0 | Complemento de Valores |
| 1 | Normal |
| 2 | Substituição |
| 3 | Redespacho |
| 4 | Redespacho Intermediário |
| 5 | Serviço Vinculado a Multimodal |

## Layout Principal (infCte)
- **ide**: cUF, cCT, CFOP, natOp, mod(57), serie, nCT, dhEmi, tpImp, tpEmis, tpCTe, modal(01=rodoviário/02=aéreo/03=aquaviário/04=ferroviário/05=dutoviário/06=multimodal), tpServ, cMunIni/Fim, UFIni/Fim, toma3/toma4
- **emit**: CNPJ, IE, xNome, xFant, enderEmit
- **rem**: CNPJ/CPF, IE, xNome, enderReme, infNF, infNFe(chave), infOutros
- **dest**: CNPJ/CPF, IE, xNome, enderDest, ISUF
- **vPrest**: vTPrest, vRec, Comp(xNome, vComp)
- **imp**: ICMS(ICMS00/20/45/60/90/OutraUF/SN), vTotTrib, infAdFisco
- **infCTeNorm**: infCarga(vCarga, proPred, infQ), infDoc(infNF, infNFe, infOutros), seg(respSeg, xSeg, nApol), infModal

## Modal Rodoviário
- RNTRC obrigatório (8 dígitos, módulo 11)
- CIOT obrigatório para TAC/cooperativa
- Veículos: placa, RENAVAM, tara, capKG, capM3, tpProp(P=próprio/T=terceiro), tpRod, tpCar
- Motoristas: xNome, CPF
- Lacres: lacRodo

## Eventos do CT-e
- **Cancelamento** (110111): até 720h, justificativa mín. 15 caracteres
- **Carta de Correção** (110110): até 30 correções por evento, máx. 20 eventos por CT-e. Não altera valores, destinatário, remetente ou data
- **EPEC**: emissão prévia em contingência
- **Prestação em Desacordo**: registrado pelo tomador, impede cancelamento
- **GTV**: guia de transporte de valores

## DACTE — Documento Auxiliar do CT-e
- Representação gráfica simplificada em papel A4
- Contém: chave de acesso, código de barras Code 128, QR Code
- Obrigatório para acompanhar a carga
- Informações: emitente, tomador, remetente, destinatário, carga, veículos, valores, ICMS

## Integração com MDF-e
- CT-e referenciado no MDF-e via grupo infDoc/infMunDescarga/infCTe (chave)
- Cada CT-e pode estar vinculado a apenas um MDF-e
- CT-e deve estar autorizado antes da inclusão no MDF-e

## Related Documents
- [MDF-e](mdfe.md) — manifesto de documentos fiscais eletrônico
- [DANFE/DACTE](danfe-dacte.md) — documentos auxiliares
- [NF-e](nfe.md) — nota fiscal eletrônica (carga transportada)
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital
