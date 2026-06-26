---
id: mdfe
type: knowledge
tags: [fiscal, mdfe, manifesto, transporte, carga, consolidacao]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, regras e eventos do Manifesto de Documentos Fiscais Eletrônico (MDF-e, modelo 58), documento ...
- **Principais responsabilidades**: Definir o layout XML do MDF-e (versão 3.00); Documentar tipos de emitente e uso (transporte de cargas); Cobrir integração com CT-e e NF-e
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, mdfe, manifesto, transporte, carga, consolidacao
- **Restrições/Regras**: Todo MDF-e deve ser encerrado após conclusão do transporte; CT-e/NF-e deve estar autorizado antes da inclusão

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `mdfe` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 14 |


# MDF-e — Manifesto de Documentos Fiscais Eletrônico

## Purpose
Documentar a estrutura, regras e eventos do Manifesto de Documentos Fiscais Eletrônico (MDF-e, modelo 58), documento que agrupa múltiplos CT-es e NF-es referentes a uma mesma operação de transporte de cargas.

## Responsibilities
- Definir o layout XML do MDF-e (versão 3.00)
- Documentar tipos de emitente e uso (transporte de cargas)
- Cobrir integração com CT-e e NF-e
- Explicar encerramento, DAMDFE e eventos

## Dependencies
- Certificado digital e-CNPJ (A1 ou A3)
- WebService da SEFAZ para autorização
- CT-es e/ou NF-es autorizados previamente
- RNTRC obrigatório para transportadores rodoviários

## Constraints
- Todo MDF-e deve ser encerrado após conclusão do transporte
- CT-e/NF-e deve estar autorizado antes da inclusão
- DAMDFE obrigatório para acompanhar o transporte
- Armazenamento do XML por no mínimo 5 anos

## Conceito
O MDF-e foi criado para simplificar a fiscalização do transporte de cargas, reunindo em um único documento todas as informações fiscais da carga transportada. Instituído pelo Ajuste SINIEF 06/2012, é obrigatório para transporte interestadual com múltiplos documentos fiscais.

## Quando Usar
- Transporte interestadual com mais de um CT-e ou NF-e
- Transportador autônomo (TAC) com múltiplas coletas/entregas
- Empresa de transporte consolidando documentos de uma viagem
- Transporte de carga própria com múltiplas NF-es
- CT-e Globalizado (tpEmit=3)

## Tipos de Emitente (tpEmit)
| Código | Descrição |
|--------|-----------|
| 1 | Transportador de Cargas (ETC) |
| 2 | Transportador de Carga Própria |
| 3 | Emissor de CT-e Globalizado |

## Layout Principal (infMDF)
- **ide**: cUF, tpEmit, mod(58), serie, nMDF, cMDF, cDV, modal(1=rodoviário/2=aéreo/3=aquaviário/4=ferroviário), dhEmis, tpEmis, UFIni, UFFim, infMunCarreg, infPercurso
- **emit**: CNPJ, IE, xNome, xFant, enderEmit
- **infModal/rodo**: RNTRC, veicTracao(placa, RENAVAM, tara, tpRod, tpCar), veicReboque(até 3), condutores(nome, CPF), lacRodo
- **infDoc**: infMunDescarga → infCTe(chCTe), infNFe(chNFe), infMDFeTransp
- **seg**: respSeg, xSeg, nApol, nAver, vCarga
- **prodPred**: tpCarga, xProd, cEAN, NCM, infLotacao
- **tot**: qCTe, qNFe, vCarga, cUnid(01=KG/02=TON), qCarga

## Integração com CT-e e NF-e
- **CT-e no MDF-e**: via infDoc/infMunDescarga/infCTe (chave 44 dígitos). Cada CT-e vinculado a apenas um MDF-e
- **NF-e no MDF-e**: via infDoc/infMunDescarga/infNFe (chave 44 dígitos). Para carga própria (tpEmit=2)
- **NF-e no CT-e**: via rem/infNFe ou infCTeNorm/infDoc/infNFe

## Fluxo Completo de Transporte
1. Remetente emite NF-e
2. Transportador emite CT-e (referenciando NF-e)
3. CT-e autorizado pela SEFAZ
4. Transportador emite MDF-e (agrupando CT-es/NF-es)
5. MDF-e autorizado pela SEFAZ
6. Início do transporte (com DAMDFE)
7. Fiscalização consulta MDF-e
8. Chegada ao destino
9. Encerramento do MDF-e (evento)

## Eventos do MDF-e
- **Encerramento** (110116): obrigatório após conclusão. Informa data, UF e município
- **Exclusão** (110115): cancelamento antes do encerramento, justificativa mín. 15 caracteres
- **Inclusão de Condutor** (110114): adiciona motoristas após emissão
- **Inclusão de NF-e**: adiciona NF-es após emissão com município de descarga
- **Pagamento de Frete**: registra informações de pagamento

## DAMDFE — Documento Auxiliar do MDF-e
- Representação gráfica em papel A4
- Contém: chave de acesso, código de barras, QR Code
- Informações: emitente, UF início/fim, municípios carregamento/descarga, veículos, condutores, totais, seguro, lacres

## Status do MDF-e
| Código | Descrição |
|--------|-----------|
| 100 | Autorizado o uso |
| 101 | Cancelamento homologado |
| 300 | Uso denegado |

## Related Documents
- [CT-e](cte.md) — conhecimento de transporte eletrônico
- [NF-e](nfe.md) — nota fiscal eletrônica
- [DANFE/DACTE](danfe-dacte.md) — documentos auxiliares
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital
