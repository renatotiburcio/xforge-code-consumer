---
id: proj-visao-geral
type: projeto
tags: [projeto, visao, escopo, erp, brasil]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Definir identidade, escopo e objetivos do projeto ERP — sistema ERP brasileiro completo.
- **Principais responsabilidades**: Estabelecer escopo funcional e não-funcional; Definir público-alvo e segmentos atendidos; Documentar pilares tecnológicos e de negócio
- **Seções principais**: Purpose, Responsibilities, Constraints, Scope
- **Tags**: projeto, visao, escopo, erp, brasil
- **Restrições/Regras**: Segmento: varejo, atacarejo, distribuição; Brasil: obrigações fiscais, contábeis, trabalhistas

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `proj-visao-geral` |
| Tipo | projeto |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 10 |


# Visão Geral do Projeto ERP

## Purpose
Definir identidade, escopo e objetivos do projeto ERP — sistema ERP brasileiro completo.

## Responsibilities
- Estabelecer escopo funcional e não-funcional
- Definir público-alvo e segmentos atendidos
- Documentar pilares tecnológicos e de negócio

## Constraints
- Segmento: varejo, atacarejo, distribuição
- Brasil: obrigações fiscais, contábeis, trabalhistas
- Tecnologia: .NET 10, Blazor, PostgreSQL, Docker

## Scope

### Módulos Principais
| Módulo | Descrição |
|--------|-----------|
| PDV/Frente de Caixa | Vendas, NFC-e/SAT, pagamentos |
| Faturamento | NF-e, NFS-e, CT-e, MDF-e |
| Estoque | Custos, inventário, movimentações |
| Financeiro | Contas a pagar/receber, fluxo de caixa |
| Fiscal | EFD ICMS/IPI, EFD Contribuições, SPED |
| Contábil | Partidas dobradas, DRE, Balanço, ECD, ECF |
| RH/Folha | eSocial, folha, férias, 13º, INSS, IRRF |
| Compras | Cotação, pedido, recebimento |
| CRM | Clientes, pipeline, histórico |
| Produção | Ordens, roteiros, apontamentos |
| Agronegócio | LCDPR, ITR, safras |

### Obrigações Legais Atendidas
- **Fiscais:** NF-e, NFC-e, SAT, CT-e, MDF-e, NFS-e, EFD ICMS/IPI, EFD Contribuições
- **Contábeis:** ECD, ECF, DRE, Balanço
- **Trabalhistas:** eSocial (todos os grupos), FGTS, DIRF, DCTFWeb, INSS, IRRF
- **Pix/Open Finance:** Pagamentos instantâneos, boletos CNAB

## Related Documents
- `projeto/stack-tecnologico.md` — Stack técnico detalhado
- `arquitetura/clean-architecture.md` — Arquitetura limpa
- `decisoes/adr-001-tech-stack.md` — Decisão de tecnologia

## Dependencies
- .NET 10, Blazor Server/WASM
- PostgreSQL 17 com EF Core
- Docker, Kubernetes
- Certificação digital e-CNPJ

## References
- Backend: ASP.NET Core, Minimal APIs, CQRS, XForge.MediatR
- Frontend: Blazor componentes reutilizáveis, Fluent UI
- Infra: Docker Compose, Azure Container Apps
- Fontes: Receita Federal, Portal SPED, Portal eSocial

## Dependencies
- `arquitetura/clean-architecture.md`
- `projeto/stack-tecnologico.md`
- `decisoes/adr-001-tech-stack.md`

## Related Documents
- `projeto/stack-tecnologico.md`
- `arquitetura/clean-architecture.md`
- `glossario/termos-tecnicos.md`

## Notas
Versão 2.0 — conhecimento consolidado e reestruturado para RAG otimizado.

