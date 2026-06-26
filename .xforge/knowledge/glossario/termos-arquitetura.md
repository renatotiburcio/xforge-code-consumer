---
id: glossario-004
type: glossary
tags: [arquitetura, design-patterns, dotnet, clean-architecture, cqrs, ddd, web-api]
owner: 
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Glossário de Termos de Arquitetura e Técnicos
- **Seções principais**: Aggregate (Agregado), API Gateway, Blazor Server, Blazor WASM
- **Tags**: arquitetura, design-patterns, dotnet, clean-architecture, cqrs, ddd, web-api
- **Tipo**: glossary | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `glossario-004` |
| Tipo | glossary |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner |  |
| Total de seções | 26 |


# Glossário de Termos de Arquitetura e Técnicos

## Aggregate (Agregado)
Conjunto de entidades e objetos de valor tratados como uma única unidade de consistência em DDD. O Aggregate Root é a única entidade acessível externamente. Exemplo: `Sale` (raiz) contém `SaleItem` (entidades internas). Garante invariantes de negócio. Relacionado: Entity, Value Object, Repository, DDD, Invariant.

## API Gateway
Ponto de entrada único para um sistema distribuído (microservices). Rotear requisições, aplica autenticação, rate limiting, load balancing e agregação de respostas. Exemplos: YARP, Ocelot (Azure API Management). Relacionado: Microservices, REST, gRPC, CORS, Middleware, JWT.

## Blazor Server
Modelo de hospedagem do Blazor onde a UI executa no servidor (ASP.NET Core). Interações do usuário são processadas via SignalR em tempo real. Não requer WebAssembly no browser. Latência maior que WASM para interações. Relacionado: Blazor WASM, SignalR, Razor Components, WebAssembly, ASP.NET Core.

## Blazor WASM
Modelo de hospedagem do Blazor onde a aplicação .NET é executada diretamente no browser via WebAssembly. Download inicial maior, mas interações mais rápidas após carregamento. Funciona offline. Relacionado: Blazor Server, WebAssembly, Razor Components, PWA, ASP.NET Core.

## CORS
**Cross-Origin Resource Sharing.** Mecanismo HTTP que permite ou bloqueia requisições de origens diferentes (domínio, protocolo, porta). Configurado no servidor via headers (`Access-Control-Allow-Origin`). Fundamental em APIs REST consumidas por SPAs. Relacionado: REST, HTTP, Middleware, OAuth2, ASP.NET Core.

## CQRS
**Command Query Responsibility Segregation.** Padrão que separa o modelo de escrita (Commands) do modelo de leitura (Queries). Commands alteram estado via Handlers validados; Queries consultam Read Models otimizados. Benefícios: escalabilidade independente, otimização de consultas. Usa XForge.MediatR para implementação. Relacionado: DDD, Repository, XForge.MediatR, Event Sourcing, Clean Architecture.

## Clean Architecture
Padrão arquitetural de Robert C. Martin com camadas concêntricas: Domain (centro, zero dependências), Application (casos de uso), Infrastructure (implementações), Presentation (UI). Inversão de dependência via DI no Composition Root. Favorece testabilidade e manutenibilidade. Relacionado: DDD, SOLID, DI, Repository, CQRS, ASP.NET Core.

## Domain Event
Evento que representa algo que aconteceu no domínio de negócio (ex: `SaleCreatedEvent`, `StockReducedEvent`). Disparado por Aggregates durante `SaveChangesAsync`. Processado por handlers que atualizam Read Models, enviam emails, etc. Não confundir com Integration Events (inter-módulo/serviço). Relacionado: Aggregate, CQRS, Event Sourcing, Observer, XForge.MediatR.

## DDD
**Domain-Driven Design.** Abordagem de design de software que alinha o código ao domínio de negócio. Conceitos-chave: Bounded Contexts, Aggregates, Value Objects, Domain Events, Repositories, Ubiquitous Language. Indicado para domínios complexos com muitas regras de negócio. Relacionado: CQRS, Clean Architecture, Aggregate, Value Object, Repository, Specification.

## DI / IoC
**Dependency Injection / Inversion of Control.** Princípio SOLID onde dependências são fornecidas (injetadas) ao invés de criadas internamente. IoC Container gerencia ciclo de vida e resolução. Em .NET: `Microsoft.Extensions.DependencyInjection`. Service lifetimes: Singleton, Scoped, Transient. Relacionado: SOLID, Clean Architecture, Repository, Middleware, ASP.NET Core.

## Entity
Objeto de domínio com identidade única que persiste ao longo do tempo. Representa por tabela de banco de dados. Pode emitir Domain Events. Contrasta com Value Object (identidade por valor). Exemplos: `Product`, `Sale`, `Customer`. Relacionado: Aggregate, Value Object, Repository, Domain Event, DDD.

## gRPC
Framework de RPC (Remote Procedure Call) de alto desempenho baseado em HTTP/2 e Protocol Buffers. Ideal para comunicação síncrona entre microservices. Alternativa ao REST para chamadas internas de baixa latência. Suporta streaming bidirecional. Relacionado: REST, API Gateway, Microservices, SignalR, CORS.

## JWT
**JSON Web Token.** Padrão (RFC 7519) para tokens de acesso seguros entre partes. Estrutura: header.payload.signature. Contém claims (usuário, roles, expiração). Usado em autenticação stateless. Validado via middleware no servidor. Relacionado: OAuth2, OpenID Connect, REST, API Gateway, Middleware.

## Mediator
Padrão de projeto que centraliza comunicação entre objetos via um mediador. Em .NET, implementado pela biblioteca XForge.MediatR. Commands e Queries são enviados ao mediador, que roteia ao handler correspondente. Desacopla remetente do destinatário. Relacionado: CQRS, Observer, Command, Clean Architecture, ASP.NET Core.

## Middleware
Componente da pipeline de requisição HTTP no ASP.NET Core que processa e/ou repassa a requisição. Exemplos: autenticação, CORS, logging, tratamento de erros, rate limiting. Ordem de registro importa. Relacionado: DI, CORS, JWT, REST, ASP.NET Core.

## OAuth2
Protocolo de autorização que permite que aplicações acessem recursos em nome do usuário sem expor credenciais. Fluxos: Authorization Code (web apps), Client Credentials (machine-to-machine), Device Code, PKCE (SPAs/mobile). Relacionado: JWT, OpenID Connect, REST, API Gateway, ASP.NET Core.

## OpenID Connect
Camada de autenticação sobre o OAuth2 que adiciona identidade (ID Token). Permite Single Sign-On (SSO) e obtenção de informações do perfil do usuário via endpoint `/userinfo`. Usado com IdentityServer, Auth0, Azure AD. Relacionado: OAuth2, JWT, SSO, REST, API Gateway.

## Razor Components
Modelo de UI do Blazor para criar componentes web reutilizáveis em .NET. Componentes combinam markup Razor (HTML + C#) com lógica de negócio. Podem ser renderizados no servidor (Blazor Server) ou no cliente (Blazor WASM). Relacionado: Blazor Server, Blazor WASM, WebAssembly, ASP.NET Core.

## Repository
Padrão que abstrai o acesso a dados, fornecendo interface semelhante a uma coleção para manipular Aggregates. Interface definida no Domain; implementação no Infrastructure (EF Core). Métodos: `GetByIdAsync`, `AddAsync`, `Update`, `Remove`. Relacionado: Aggregate, UoW, DDD, Clean Architecture, EF Core.

## REST
**Representational State Transfer.** Estilo arquitetural para APIs web baseado em recursos (URIs), métodos HTTP (GET, POST, PUT, DELETE), statelessness e representações (JSON/XML). Padrão predominante para APIs públicas. Relacionado: CORS, JWT, gRPC, API Gateway, ASP.NET Core.

## SignalR
Biblioteca ASP.NET Core para comunicação em tempo real via WebSockets (com fallback para Server-Sent Events e Long Polling). Usada em Blazor Server, notificações, dashboards ao vivo, chat. Alternativa ao gRPC para cenários de push. Relacionado: Blazor Server, WebSocket, gRPC, ASP.NET Core.

## SOLID
Cinco princípios de design orientado a objetos: Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), Dependency Inversion (DIP). Favorece código extensível, testável e de fácil manutenção. Relacionado: Clean Architecture, DI, Repository, DDD, Design Patterns.

## Specification
Padrão de projeto que encapsula regras de negócio como objetos reutilizáveis. Usado para consultas (predicados) e validações. Pode ser combinado (And, Not). Implementado como `Expression<Func<T, bool>>` para tradução em EF Core. Relacionado: DDD, Repository, CQRS, Clean Architecture, EF Core.

## Unit of Work (UoW)
Padrão que mantém uma lista de objetos afetados por uma transação de negócio e coordena a escrita das mudanças. No EF Core, o `DbContext` já implementa UoW. Garante atomicidade: tudo ou nada. Relacionado: Repository, Aggregate, CQRS, EF Core, Clean Architecture.

## Value Object
Objeto de domínio definido por seus atributos, sem identidade única. Imutável por natureza. Dois Value Objects com mesmos valores são iguais. Exemplos: `Money`, `Address`, `Cpf`, `Email`. Reduz complexidade em Aggregates. Relacionado: Entity, Aggregate, DDD, Clean Architecture.

## WebAssembly (WASM)
Formato binário de instrução para execução em navegadores web. Permite rodar código .NET (Blazor WASM), C/C++, Rust no browser com performance próxima de nativo. Alternativa ao JavaScript para aplicações web complexas. Relacionado: Blazor WASM, Razor Components, ASP.NET Core.

