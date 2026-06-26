---
id: proj-stack
type: projeto
tags: [projeto, tecnologia, stack, dotnet, blazor]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar a stack tecnológica completa do projeto ERP.
- **Principais responsabilidades**: Definir tecnologias, frameworks e ferramentas; Mapear versões e compatibilidade; Guiar onboarding de desenvolvedores
- **Seções principais**: Purpose, Responsibilities, Stack Principal, Constraints
- **Tags**: projeto, tecnologia, stack, dotnet, blazor
- **Restrições/Regras**: Certificado e-CNJ (A1/A3) obrigatório para NF-e/eSocial; Assinatura digital via PKI Brazil

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `proj-stack` |
| Tipo | projeto |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# Stack Tecnológico — ERP

## Purpose
Documentar a stack tecnológica completa do projeto ERP.

## Responsibilities
- Definir tecnologias, frameworks e ferramentas
- Mapear versões e compatibilidade
- Guiar onboarding de desenvolvedores

## Stack Principal

### Backend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| .NET / C# | 10 | Runtime e linguagem |
| ASP.NET Core | 10 | APIs, SignalR, Middleware |
| EF Core | 10 | ORM, migrations PostgreSQL |
| XForge.MediatR | 12 | CQRS, comandos e queries |
| FluentValidation | 11 | Validação de entrada |
| Serilog | 4 | Logging estruturado |
| QuestPDF | 2025 | Geração de PDF (DANFE, relatórios) |
| YARP | 2.3 | API Gateway / reverse proxy |

### Frontend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Blazor | 10 | UI interativa (Server + WASM) |
| MudBlazor / Fluent UI | 8 | Componentes de UI |
| Blazored FluentValidation | 2.2 | Validação client-side |

### Dados
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| PostgreSQL | 17 | Banco de dados principal |
| Redis | 7 | Cache distribuído, sessões |
| RabbitMQ / MassTransit | 8 | Mensageria, eventos |

### Infraestrutura
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Docker | 28 | Containers |
| Docker Compose | 2.30 | Orquestração local |
| GitHub Actions | — | CI/CD pipelines |
| Azure Container Apps | 1.0 | Produção cloud |
| Kubernetes | 1.32 | Orquestração (alternativa) |

### Qualidade
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| xUnit | 2.9 | Testes unitários |
| NSubstitute | 5 | Mocking |
| FluentAssertions | 7 | Asserções legíveis |
| Testcontainers | 4 | Testes de integração com containers |
| Moq | 4 | Mocking (alternativo) |
| Coverlet | 6 | Code coverage |
| SonarQube | — | Análise estática |

## Constraints
- Certificado e-CNJ (A1/A3) obrigatório para NF-e/eSocial
- Assinatura digital via PKI Brazil
- SPED exige arquivos TXT com layout fixo

## Dependencies
- `projeto/visao-geral.md`
- `arquitetura/clean-architecture.md`
- `padroes/coding-standards.md`

## Related Documents
- `arquitetura/deploy-net.md`
- `arquitetura/observabilidade.md`
- `dominios/tecnologia/docker.md`

