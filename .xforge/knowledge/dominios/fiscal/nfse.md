---
id: nfse
type: knowledge
tags: [fiscal, nfse, servico, iss, municipal, eletronico]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, regras e variações da Nota Fiscal de Serviço Eletrônica (NFS-e), documento fiscal eletrônico ...
- **Principais responsabilidades**: Definir o layout XML do padrão nacional NFS-e; Documentar a relação RPS → NFS-e; Cobrir ISS, lista de serviços (LC 116/2003) e regimes tributários
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, nfse, servico, iss, municipal, eletronico
- **Restrições/Regras**: Não há layout nacional único (cada município define seu emissor); Alíquota de ISS: 2% a 5% (conforme LC 116/2003)

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `nfse` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 14 |


# NFS-e — Nota Fiscal de Serviço Eletrônica

## Purpose
Documentar a estrutura, regras e variações da Nota Fiscal de Serviço Eletrônica (NFS-e), documento fiscal eletrônico para serviços sujeitos ao ISS, com layout municipal variável e padrão nacional em convergência.

## Responsibilities
- Definir o layout XML do padrão nacional NFS-e
- Documentar a relação RPS → NFS-e
- Cobrir ISS, lista de serviços (LC 116/2003) e regimes tributários
- Explicar integração com prefeituras e Emissor Nacional

## Dependencies
- Inscrição Municipal do prestador
- Certificado digital (varia por município)
- WebService da prefeitura ou Emissor Nacional (https://www.nfse.gov.br/EmissorNacional)
- Ambiente de Dados Nacional (ADN) para repositório central

## Constraints
- Não há layout nacional único (cada município define seu emissor)
- Alíquota de ISS: 2% a 5% (conforme LC 116/2003)
- Cancelamento varia por município
- DANFSe definido pela Nota Técnica 008/2026

## Conceito
A NFS-e documenta a prestação de serviços sujeitos ao ISS (Imposto Sobre Serviços). Diferente da NF-e (estadual), a NFS-e é municipal. O padrão nacional está em convergência via Ambiente de Dados Nacional (ADN) e Emissor Nacional.

## Diferenças NF-e vs NFS-e
| Aspecto | NF-e | NFS-e |
|---------|------|-------|
| Layout | Nacional (único) | Varia por município (padrão em convergência) |
| Tributo | ICMS | ISS |
| Alíquota | 17-18% | 2-5% |
| Transmissão | WebService SEFAZ | WebService município / Emissor Nacional |
| Modelo | 55 | Varia |

## Layout do XML (Padrão Nacional)
- **InfNfse**: Numero, CodigoVerificacao, DataEmissao, IdentificacaoRps(Numero, Serie, Tipo), NaturezaOperacao, RegimeEspecialTributacao, OptanteSimplesNacional, IncentivadorCultural, Status
- **Servico/Valores**: ValorServicos, ValorDeducoes, ValorPis, ValorCofins, ValorInss, ValorIr, ValorCsll, OutrasRetencoes, ValorIss, Aliquota, DescontoIncondicionado, DescontoCondicionado, IssRetido
- **Servico**: ItemListaServico(LC 116), CodigoCnae, CodigoTributacaoMunicipio, Discriminacao, CodigoMunicipio, ExigibilidadeISS
- **PrestadorServico**: Cnpj, InscricaoMunicipal, RazaoSocial, NomeFantasia, Endereco, Contato
- **TomadorServico**: CpfCnpj, InscricaoMunicipal, RazaoSocial, Endereco, Contato
- **IntermediarioServico**: IdentificacaoIntermediario, RazaoSocial
- **ConstrucaoCivil**: CodigoObra, ART

## Lista de Serviços (LC 116/2003)
Principais códigos: 01.01 Análise e desenvolvimento de sistemas, 01.02 Programação, 01.03 Processamento de dados, 01.08 Licenciamento de software, 01.09 SaaS, 04.01 Medicina, 07.01 Advocacia, 10.01 Engenharia, 17.01 Assessoria de imprensa, 22.01 Vigilância. Lista completa em https://www.gov.br/nfse/pt-br.

## Natureza da Operação
| Código | Descrição |
|--------|-----------|
| 1 | Tributação no município |
| 2 | Tributação fora do município |
| 3 | Isenção |
| 4 | Imune |
| 5 | Exigibilidade suspensa |
| 6 | Incidente sobre parcela da obra |
| 7 | Não incidência |

## Regime Especial de Tributação
| Código | Descrição |
|--------|-----------|
| 1 | Municipal padrão |
| 2 | Estimativa |
| 3 | Sociedade profissionais |
| 4 | Cooperativa |
| 5 | MEI |
| 6 | Microempresa/empresa pequena |

## RPS → NFS-e
O RPS (Recibo Provisório de Serviços) é convertido em NFS-e. Tipos de RPS: 1=RPS, 2=RPS Conjugada, 3=Cupom. A conversão pode ser online (tempo real) ou em lote, conforme o município.

## DANFSe — Documento Auxiliar da NFS-e
- Representação gráfica padronizada pela Nota Técnica 008/2026 (SE/CGNFS-e)
- Padrão nacional para visualização e impressão

## Integração com Prefeituras
- **Ambiente de Dados Nacional (ADN)**: repositório central de NFS-es
- **API de integração**: para sistemas emitirem NFS-e
- **Webservices municipais**: para municípios conveniados ao padrão nacional
- **Emissor Nacional**: https://www.nfse.gov.br/EmissorNacional

## Related Documents
- [NF-e](nfe.md) — nota fiscal eletrônica (mercadorias)
- [EFD Contribuições](efd-contribuicoes.md) — escrituração PIS/COFINS
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital
