---
id: integracao-sefaz-pgfn
type: conhecimento
tags: [fiscal, integracao, sefaz, pgfn, cnd, gov]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Integrações com Órgãos Governamentais
- **Seções principais**: SEFAZ (Secretaria da Fazenda), PGFN (Procuradoria-Geral da Fazenda Nacional), eSocial, REINF
- **Tags**: fiscal, integracao, sefaz, pgfn, cnd, gov
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `integracao-sefaz-pgfn` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 6 |


# Integrações com Órgãos Governamentais

## SEFAZ (Secretaria da Fazenda)

### Serviços Web
| Serviço | Uso |
|---------|-----|
| NFe/NFCe | Emissão e consulta de notas |
| CT-e | Conhecimento de transporte |
| MDF-e | Manifesto de documentos |
| GNRE | Guia nacional de recolhimento |
| DARE | Documento de arrecadação |

### Endpoint NFe (exemplo MG)
```
https://hnfe.fazenda.mg.gov.br/nfe2/services/NfeAutorizacao
```

### Certificado Digital
- A1: arquivo .pfx (2 anos)
- A3: token USB/cartaão (1-3 anos)
- Obrigatório para transmissão

## PGFN (Procuradoria-Geral da Fazenda Nacional)

### Consulta CND
```
GET https://www8.receita.fazenda.gov.br/SimplesNacional/CertidaoNegativaDebitos
```

### Tipos de Certidão
| Tipo | Descrição |
|------|-----------|
| CND | Certidão Negativa de Débitos |
| CNDI | Certidão Negativa de Débitos com Efeitos de CND |
| CDN | Certidão de Débitos de Tributos Federais |

### Validade
- CND: 180 dias da emissão
- Pode ser consultada via webservice
- QR Code para verificação

## eSocial

### Web Services
| Ambiente | URL |
|----------|-----|
| Produção | https://www3.esocial.gov.br/servicos/employer |
| Homologação | https://homologacao.esocial.gov.br/servicos/employer |

### Certificado
- Certificado digital A1 ou A3
- e-CPF ou e-CNPJ
- Cadeia de certificação ICP-Brasil

## REINF

### Obrigação
- Contribuições previdenciárias sobre receitas
- Retenções na fonte
- Substitui GFIP e DCTF para contribuições

### Eventos
| Evento | Descrição |
|--------|-----------|
| R-2010 | Serviços tomados |
| R-2020 | Serviços prestados |
| R-2030 | Produção rural |
| R-2040 | Associação desportiva |
| R-2060 | Contribuição previdenciária |

## DCTFWeb

### Substitui
- DIRF (desde 2024)
- GFIP (para empresas obrigadas ao eSocial)

### Eventos
| Evento | Descrição |
|--------|-----------|
| S-1299 | Fechamento períodico eSocial |
| S-1299 | Fechamento SST |
| Composição | Tributos federais e contribuições |

## Boleto/GNRE

### GNRE (Guia Nacional de Recolhimento)
- Pagamento de tributos estaduais
- Cada estado tem regras próprias
- GNRE único ou múltiplo
- Pagamento via Pix ou boleto
