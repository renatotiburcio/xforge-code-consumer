---
id: sped-overview
type: dominio
tags: [sped, escrituracao, digital, receita-federal]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Visao geral do Sistema Publico deEscrituração Digital (SPED) e seus modulos.
- **Principais responsabilidades**: Mapear todos os modulos do SPED; Explicar fluxo de validacao e transmissao; Documentar requisitos de certificacao digital
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: sped, escrituracao, digital, receita-federal
- **Restrições/Regras**: Obrigatorio certificacao digital e-CNPJ (A1 ou A3); Arquivos em formato TXT com layout definido pelo SPED

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `sped-overview` |
| Tipo | dominio |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 11 |


# SPED — Visao Geral

## Purpose
Visao geral do Sistema Publico deEscrituração Digital (SPED) e seus modulos.

## Responsibilities
- Mapear todos os modulos do SPED
- Explicar fluxo de validacao e transmissao
- Documentar requisitos de certificacao digital

## Dependencies
- `nfe.md`, `nfce.md`, `cte.md`, `mdfe.md`, `nfse.md` — Documentos fiscais
- `efd-icms-ipi.md`, `efd-contribuicoes.md` — EFD
- `ecd.md`, `ecf.md` — SPED Contabil
- `esocial-geral.md` — eSocial

## Constraints
- Obrigatorio certificacao digital e-CNPJ (A1 ou A3)
- Arquivos em formato TXT com layout definido pelo SPED
- Validacao pelo PVA antes da transmissao
- Transmissao via Receitanet ou webservice

## O que e SPED
Sistema Publico de Escrituração Digital (Decreto 6.022/2007) que moderniza a interacao fisco-contribuinte nas tres esferas de governo (federal, estadual, municipal). Informatiza obrigacoes acessorias e usa certificacao digital para validade juridica.

## Modulos do SPED

### SPED Contabil
| Modulo | Descricao | Prazo |
|--------|-----------|-------|
| ECD | Escrituracao Contabil Digital | Ultimo dia util de maio |
| ECF | Escrituracao Contabil Fiscal | Ultimo dia util de julho |

### SPED Fiscal
| Modulo | Descricao | Prazo |
|--------|-----------|-------|
| EFD ICMS/IPI | Escrituracao Fiscal Digital ICMS/IPI | Definido por UF |
| EFD Contribuicoes | EFD PIS/COFINS | Definido por legislacao |

### Documentos Fiscais Eletronicos
| Modulo | Descricao | Emissor |
|--------|-----------|---------|
| NF-e | Nota Fiscal Eletronica (modelo 55) | Empresa |
| NFC-e | Nota Fiscal de Consumidor Eletronica | Empresa |
| CT-e | Conhecimento de Transporte Eletronico (modelo 57) | Transportador |
| MDF-e | Manifesto de Documentos Fiscais Eletronico | Transportador |
| NFS-e | Nota Fiscal de Servico Eletronica | Prestador |
| BP-e | Bilhete de Passagem Eletronico | Transportador |

### Obrigacoes Trabalhistas/Previdenciarias
| Modulo | Descricao | Prazo |
|--------|-----------|-------|
| eSocial | Escrituracao Digital Obrigacoes | Variavel por evento |
| EFD-Reinf | Retencoes e Outras Info Fiscais | Mensal |
| DCTFWeb | Debitos e Creditos Tributarios | 15 dia util 2 mes |

## Certificacao Digital
| Tipo | Validade | Armazenamento | Uso |
|------|----------|---------------|-----|
| e-CNPJ A1 | 1 ano | Software (pfx) | NF-e, eSocial, SPED |
| e-CNPJ A3 | 1-3 anos | Token/Cartao | NF-e, eSocial, SPED |
| e-CPF | 1-3 anos | Token/Cartao | Contador responsavel |

## PVA — Programa Validador e Assinador
Fluxo padrao:
```
1. Gerar arquivo TXT (layout SPED)
2. Importar no PVA
3. Validar (verificar erros)
4. Corrigir se necessario
5. Assinar digitalmente (e-CNPJ)
6. Transmitir via Receitanet
```

## Penalidades
| Infracao | Multa |
|----------|-------|
| Atraso na entrega | 1% ao mes (minimo R$ 500) |
| Omissao de informacoes | R$ 1.500 por arquivo |
| Incorrecao de informacoes | R$ 800 por arquivo |
| Nao atendimento a intimatacao | R$ 5.000 por mes |

## Retificacao
- Dentro do prazo: sem multa
- Apos o prazo: multa por arquivo retificado
- Utilizar codigo de finalidade 1 (retificacao) no registro 0000
- Referenciar o recibo do arquivo original

## Related Documents
- `nfe.md` — Nota Fiscal Eletronica
- `nfce.md` — NFC-e
- `cte.md` — CT-e
- `mdfe.md` — MDF-e
- `nfse.md` — NFS-e
- `efd-icms-ipi.md` — EFD ICMS/IPI
- `efd-contribuicoes.md` — EFD Contribuicoes
- `ecd.md` — ECD
- `ecf.md` — ECF
- `esocial-geral.md` — eSocial
- `esocial-layout.md` — Layout eSocial
