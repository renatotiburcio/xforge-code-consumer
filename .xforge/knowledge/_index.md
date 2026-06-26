---
id: summary-l1
type: resumo
tags: [resumo, nivel-1, visao-geral, projeto, erp, template]
owner: project-team
version: 4.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Base de conhecimento reutilizavel para projetos ERP brasileiros, construida com .NET e Blazor, cobrindo obrigacoes fi...
- **Principais responsabilidades**: **Fiscais:** NF-e, NFC-e, SAT, CT-e, MDF-e, NFS-e, EFD ICMS/IPI, EFD Contribuicoes; **Contabeis:** ECD, ECF, DRE, Balanco Patrimonial; **Trabalhist...
- **Seções principais**: Proposito, Escopo Funcional, Stack Tecnologico, Arquitetura
- **Tags**: resumo, nivel-1, visao-geral, projeto, erp, template
- **Tipo**: resumo | **Versão**: 4.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `summary-l1` |
| Tipo | resumo |
| Versão | 4.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 8 |


# Resumo Nivel 1 — Visao Geral do Projeto

## Proposito
Base de conhecimento reutilizavel para projetos ERP brasileiros, construida com .NET e Blazor, cobrindo obrigacoes fiscais, contabeis e trabalhistas do Brasil.

## Escopo Funcional

### Modulos Principais
| Modulo | Descricao |
|--------|-----------|
| PDV/Frente de Caixa | Vendas, NFC-e/SAT, pagamentos |
| Faturamento | NF-e, NFS-e, CT-e, MDF-e |
| Estoque | Custos, inventario, movimentacoes |
| Financeiro | Contas a pagar/receber, fluxo de caixa |
| Fiscal | EFD ICMS/IPI, EFD Contribuicoes, SPED |
| Contabil | Partidas dobradas, DRE, Balanco, ECD, ECF |
| RH/Folha | eSocial, folha, ferias, 13o, INSS, IRRF |
| Compras | Cotacao, pedido, recebimento |
| CRM | Clientes, pipeline, historico |
| Producao | Ordens, roteiros, apontamentos |
| Agronegocio | LCDPR, ITR, safras |

### Obrigacoes Legais
- **Fiscais:** NF-e, NFC-e, SAT, CT-e, MDF-e, NFS-e, EFD ICMS/IPI, EFD Contribuicoes
- **Contabeis:** ECD, ECF, DRE, Balanco Patrimonial
- **Trabalhistas:** eSocial (todos os grupos), FGTS, DIRF, DCTFWeb, INSS, IRRF
- **Pagamentos:** PIX, Open Finance, boletos CNAB

## Stack Tecnologico
| Camada | Tecnologia |
|--------|------------|
| Backend | .NET, ASP.NET Core, EF Core, XForge.MediatR |
| Frontend | Blazor Server/WASM/Auto |
| Dados | PostgreSQL, Redis, RabbitMQ |
| Infra | Docker, CI/CD, Cloud Containers |
| Qualidade | xUnit, Testcontainers, SonarQube |

## Arquitetura
- **Padrao:** Clean Architecture (Domain — Application — Infrastructure — Presentation)
- **CQRS:** XForge.MediatR para comandos e queries
- **Multi-tenancy:** Shared database com discriminator + RLS
- **Auth:** JWT + refresh tokens + role-based

## Estrutura do Conhecimento
| Categoria | Descricao | Documentos |
|-----------|-----------|------------|
| `projeto/` | Visao geral e stack | 2 |
| `arquitetura/` | Design patterns, arquitetura, deploy | 7 |
| `dominios/fiscal/` | Documentos fiscais, SPED, EFD | 9 |
| `dominios/contabil/` | Contabilidade, ECD, ECF, lancamentos | 9 |
| `dominios/trabalhista/` | eSocial, CLT, folha, INSS, IRRF | 13 |
| `dominios/financeiro/` | Contas a pagar/receber, fluxo, conciliacao | 5 |
| `dominios/tributos/` | Regimes, ICMS, PIS/COFINS, reforma | 7 |
| `dominios/erp/` | PDV, estoque, vendas, compras, producao | 11 |
| `decisoes/` | ADRs (decisoes arquiteturais) | 6 |
| `fluxos/` | Fluxos end-to-end de processos | 7 |
| `padroes/` | Padroes de codigo e melhores praticas | 10 |
| `glossario/` | Termos tecnicos e de negocio | 5 |
| `compliance/` | Normas, seguranca, privacidade | 1 |

## Navegacao
- **Nivel 1 (este documento):** Visao geral do projeto
- **Nivel 2:** Resumos por dominio (ver `dominios/_index.md`)
- **Nivel 3:** Conhecimento granular (arquivos individuais)

## RAG Index
- Documentos: **786** (99 only in knowledge, 687 in .kilo + .xforge)
- Chunks: **1.859**
- Formato: YAML front matter + secoes padronizadas
- Chunking recomendado: 200-800 tokens por chunk

## Related Documents
- `projeto/visao-geral.md` — Visao detalhada
- `projeto/stack-tecnologico.md` — Stack completo
- `dominios/_index.md` — Resumos por dominio (Nivel 2)