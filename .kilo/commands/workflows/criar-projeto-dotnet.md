---
description: Cria projeto .NET novo usando padrões XForge e perguntando interativamente features desejadas.
agent: code
---

# /criar-projeto-dotnet

## Objetivo

Criar projeto .NET novo usando documentação padrão XForge.

## Fluxo interativo

Perguntar:

1. Tipo do projeto:
   - Minimal API
   - Worker
   - Blazor
   - Class Library
   - Package NuGet
   - Fullstack API + Blazor

2. Arquitetura:
   - Clean Architecture
   - Modular Monolith
   - Package Library
   - Microservice

3. Features:
   - Auth
   - Swagger/OpenAPI
   - EF Core
   - Repository
   - Result Pattern
   - Global Error Handler
   - Health Checks
   - Serilog/OpenTelemetry
   - Tests
   - Docker
   - GitHub Actions
   - QuestPDF
   - Background Jobs

4. Banco:
   - MySQL
   - PostgreSQL
   - SQL Server
   - SQLite
   - InMemory

5. Frontend:
   - Blazor Server
   - Blazor WebAssembly
   - Blazor Hybrid
   - Nenhum

## Resultado

- criar estrutura;
- criar docs;
- criar memória inicial;
- criar PROJECT-DNA;
- criar backlog inicial.


## Frontend padrão

- Blazor
- Tailwind CSS v4
- utility-first
- design tokens
- responsividade
- acessibilidade
- UX enterprise


## Regra de destino REV14

O novo projeto/app deve ser criado dentro do root ativo do projeto atual.

Nunca criar uma pasta irmã fora do workspace ativo.

Antes de criar, detectar:

- root ativo;
- solution existente;
- padrão de pastas;
- destino correto: `src/`, `src/`, `modules/` ou `packages/`.

Se houver dúvida, perguntar interativamente o destino.


## Golden Rules obrigatórias REV17

- Aplicar SOLID.
- Aplicar SRP.
- Cada arquivo deve ter uma única responsabilidade.
- Usar apenas pacotes estáveis.
- Verificar última versão estável antes de instalar.
- Não usar MediatR.
- Usar XForge.MediatR como padrão obrigatório para CQRS/Mediator.
