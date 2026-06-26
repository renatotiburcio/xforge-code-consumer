---
id: clean-architecture
type: knowledge
tags: [arquitetura, clean-architecture, dotnet, camadas]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Clean Architecture
- **Principais responsabilidades**: Organizar o código em 4 camadas com dependências unidirecionais; Garantir que o Domain não dependa de nenhuma outra camada; Centralizar a configura...
- **Seções principais**: Propósito, Responsabilidades, Diagrama de Camadas, Regras
- **Tags**: arquitetura, clean-architecture, dotnet, camadas
- **Restrições/Regras**: Domain não depende de nada; Application depende apenas de Domain

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `clean-architecture` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 8 |


# Clean Architecture

## Propósito
Definir a estrutura em camadas do sistema ERP, garantindo separação de responsabilidades, testabilidade e independência de frameworks.

## Responsabilidades
- Organizar o código em 4 camadas com dependências unidirecionais
- Garantir que o Domain não dependa de nenhuma outra camada
- Centralizar a configuração de DI no Composition Root

## Diagrama de Camadas

```
+-----------------------------------------------------------------+
|                        Presentation                              |
|                    (Controllers, Pages, Views)                    |
+-----------------------------------------------------------------+
|                        Application                                |
|              (Use Cases, DTOs, Validators, CQRS)                  |
+-----------------------------------------------------------------+
|                          Domain                                  |
|           (Entities, Value Objects, Aggregates,                   |
|            Domain Events, Specifications, Interfaces)             |
+-----------------------------------------------------------------+
|                       Infrastructure                              |
|         (EF Core, Repositories, External Services,                |
|          File System, Email, etc.)                                |
+-----------------------------------------------------------------+
```

## Regras
| Camada | Responsabilidade | Dependências |
|--------|-----------------|--------------|
| **Domain** | Entidades, regras de negócio, interfaces | Nenhuma |
| **Application** | Use cases, DTOs, validação, CQRS | Domain |
| **Infrastructure** | Implementações (DB, APIs, arquivos) | Domain, Application |
| **Presentation** | UI, Controllers, Pages | Application |

- Domain não depende de nada
- Application depende apenas de Domain
- Infrastructure implementa interfaces do Domain
- Presentation depende de Application
- Dependency Injection no Composition Root

## Estrutura de Solução

```
ERP.sln
src/
  ERP.Domain/           Entities/, ValueObjects/, Aggregates/, Events/, Specifications/, Interfaces/, Services/
  ERP.Application/      Commands/, Queries/, DTOs/, Interfaces/, Mappings/
  ERP.Infrastructure/   Persistence/, Services/, External/
  ERP.Web/              Controllers/, Pages/, ViewModels/, Program.cs
tests/
  ERP.Domain.Tests/
  ERP.Application.Tests/
  ERP.Infrastructure.Tests/
  ERP.Web.Tests/
```

## Composition Root (Program.cs)

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddControllers();
var app = builder.Build();
app.UseExceptionHandler("/error");
app.UseRouting();
app.MapControllers();
app.Run();
```

## Dependências
- [design-patterns-erp.md](design-patterns-erp.md) — Repository, Unit of Work, CQRS
- [design-patterns-gof.md](design-patterns-gof.md) — Strategy, Factory

## Restrições
- Nenhuma camada interna pode referenciar uma camada externa
- Domain não pode usar EF Core, HTTP ou qualquer biblioteca de infraestrutura
- Interfaces de repositório ficam no Domain; implementações na Infrastructure

