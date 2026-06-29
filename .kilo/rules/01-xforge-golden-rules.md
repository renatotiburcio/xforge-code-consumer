# XForge Golden Rules

## Regra de ouro 0 - Stack-agnostic por padrao (Adicionado 2026-06-14)

O sistema NAO assume stack. Cada projeto tem seu proprio stack.

**Obrigatorio**:

- Detectar stack antes de sugerir patterns.
- Perguntar ao usuario quando ambiguo (max 3 opcoes).
- Diretores especialistas sao OPT-IN por stack.
- Comandos genericos (create-project, create-api, analyze-project) suportam TODOS os stacks suportados.

**Proibido**:

- Assumir .NET/C#/Blazor/EF Core por default.
- Sugerir MediatR/AutoMapper/EF Core em projetos nao-.NET.
- Forcar Clean Architecture em stacks onde nao faz sentido (ex: HTML+Tailwind standalone).

---

## Regra de ouro 1 - SOLID e SRP (todos os stacks)

Todo codigo deve respeitar SOLID.

SRP eh obrigatorio:

```text
cada arquivo deve ter uma unica responsabilidade
```

## Proibido

- arquivo fazendo multiplas responsabilidades;
- services gigantes;
- handlers com regra, persistencia, validacao e mapping misturados;
- Program.cs / main.ts / main.go / app.py poluido;
- classes/funcoes utilitarias genericas sem coesao;
- duplicacao de regra de negocio.

## Obrigatorio

- separar responsabilidades;
- usar extensions / modules / packages para manter entry point limpo;
- separar validacao, regra, persistencia, mapping, endpoint e resposta;
- criar arquivos pequenos, coesos e testaveis;
- aplicar Clean Code.

---

## Regra de ouro 2 - Pacotes estaveis (todos os stacks)

Nunca usar versao preview, beta, rc, alpha, nightly ou experimental em projeto produtivo.

## Obrigatorio

Antes de instalar ou atualizar pacotes:

1. verificar a ultima versao estavel;
2. ignorar versoes preview;
3. registrar a versao escolhida;
4. justificar caso uma versao nao seja a ultima estavel;
5. validar compatibilidade;
6. compilar sem warnings.

## Aplica-se tambem a pacotes fixados

Mesmo pacotes que parecam ja definidos devem ser verificados:

- **.NET / NuGet**: EF Core, Pomelo.EntityFrameworkCore.MySql, Swashbuckle, QuestPDF, OpenTelemetry, Serilog, XForge.MediatR, AutoMapper
- **Node / npm**: Tailwind, React, Next, Angular, Vue, Svelte, Express, Fastify, NestJS, Prisma, Drizzle, Zod, TypeScript
- **Python / PyPI**: FastAPI, Django, Flask, SQLAlchemy, Pydantic, pytest, ruff, mypy
- **Go / modules**: gin, echo, fiber, sqlc, testify, golangci-lint
- **Rust / crates**: actix-web, axum, rocket, sqlx, diesel, tokio, serde
- **qualquer pacote NuGet, npm, PyPI, Go modules, Cargo, RubyGems, Packagist**

---

## Regra de ouro 3 - Padroes por stack (NAO forcados, opt-in)

### 3.1 .NET (somente quando stack == .NET)

- **XForge.MediatR obrigatorio** para CQRS/mediator (NAO usar MediatR oficial).
  - Referencia: `https://github.com/renatotiburcio/XForge.MediatR`
- **AutoMapper obrigatorio** (NAO usar Mapster).
  - Validar ultima versao estavel.
- Mapping nao deve conter regra de negocio.
- Profiles devem ser coesos e testaveis.
- Projetos existentes com Mapster devem gerar plano de migracao para AutoMapper.
- Projetos existentes com MediatR oficial devem gerar plano de migracao para XForge.MediatR.

### 3.2 React / Next.js (somente quando stack == React/Next)

- TypeScript obrigatorio.
- Hooks para estado, Context ou Zustand/Jotai para global state.
- TanStack Query (React Query) para server state.
- Zod para validacao de schema.
- React Hook Form para formularios complexos.
- Tailwind CSS para styling.
- ESLint + Prettier obrigatorios.

### 3.3 Angular (somente quando stack == Angular)

- Standalone components (Nao usar NgModules exceto quando obrigatorio).
- Signals para estado (a partir de Angular 17).
- RxJS para async.
- Tailwind CSS ou Angular Material para UI.
- TypeScript strict mode obrigatorio.

### 3.4 HTML+Tailwind standalone (somente quando stack == HTML estatico)

- Tailwind via CDN para prototipos OU build local para producao.
- Vanilla JS ou Alpine.js para interatividade simples.
- Sem build pipeline complexo (maximo: htmlhint + tailwindcss-classnames).
- HTML semantico obrigatorio.
- Acessibilidade (WCAG 2.1 AA) obrigatoria.

### 3.5 Node.js (Express/Fastify/NestJS)

- TypeScript obrigatorio.
- Zod para validacao.
- Prisma/Drizzle/TypeORM para ORM.
- Jest ou Vitest para testes.
- ESLint + Prettier.

### 3.6 Python (FastAPI/Django/Flask)

- Type hints obrigatorios.
- Pydantic para validacao.
- pytest + pytest-cov para testes.
- ruff + mypy para lint/type.
- SQLAlchemy 2.0+ ou SQLModel para ORM.

### 3.7 Go

- standard library preferida.
- go vet + staticcheck + golangci-lint.
- testify para testes.
- sqlc ou sqlx para DB.

### 3.8 Rust

- tokio para async.
- thiserror para erros de lib, anyhow para erros de app.
- cargo clippy -- -D warnings.
- cargo test + cargo audit.

---

## Regra de ouro 4 - Documentacao (todos os stacks)

- README por projeto com setup rapido (5 min para rodar).
- Docstrings/XML comments/JSDoc/docstrings Python em APIs publicas.
- OpenAPI/Swagger para APIs REST.
- Diagramas C4 (L1, L2, L3) para sistemas com mais de 3 modulos.

---

## Regra de ouro 5 - Lazy-Loading de Skills (Adicionado 2026-06-27)

Skills com corpo > 2000 chars devem carregar apenas metadata no system prompt.
Conteudo completo carregado sob demanda via tool skill.

**Obrigatorio**:
- System prompt inclui: name + description + metadata (sempre < 500 chars por skill)
- Body completo carregado APENAS quando skill tool e invocado
- Configuracao em .xforge/config/skill-loading.json

**Proibido**:
- Carregar body completo de todas as skills no system prompt
- Skills com > 5000 chars sem lazy-loading

---

## Regra de ouro 6 - Instrucoes por Diretorio (Adicionado 2026-06-27)

AGENTS.md em subdirectorios sao carregados dinamicamente quando o agente acessa arquivos naquele diretorio.

**Obrigatorio**:
- AGENTS.md por diretorio para monorepos
- Carregamento via indUp (sobe na arvore ate encontrar)
- Max depth: 3 niveis
- Instrucoes do diretorio tem precedencia sobre as do root

**Proibido**:
- Duplicar instrucoes de root em subdirectorios
- Instrucoes genericas que nao se aplicam ao dominio do diretorio

---

## Regra de ouro 7 - Protecao de Arquivos Sensiveis (Adicionado 2026-06-27)

Arquivos .env, .env.*, .key, .pem, .p12 SEMPRE requerem aprovacao explicita.

**Obrigatorio**:
- *.env, *.env.* -> ask (nunca allow broad)
- *.key, *.pem, *.p12 -> ask
- .env.example -> allow (documentacao)
- Protecao built-in, nao configuravel

**Proibido**:
- ead: allow broad que bypass .env
- Agente ler .env sem confirmacao humana

---

## Regra de ouro 8 - Permissoes com Glob Patterns (Adicionado 2026-06-27)

Comandos bash e operacoes de arquivo usam glob patterns para permissoes.
Ultima regra matching vence.

**Obrigatorio**:
- Broad fallbacks primeiro, excecoes depois
- Padroes: *, git *, src/*, *.env
- Windows: case-insensitive; Unix: case-sensitive
- Usar forward slashes em padroes (cross-platform)

**Proibido**:
- Catch-all apos regras especificas (inverte precedencia)
- Padroes sem ordem logica

---

## Regra de ouro 9 - Think-Then-Do (Adicionado 2026-06-27)

Tarefas complexas devem seguir o ciclo: Analisar -> Planejar -> Executar -> Revisar.

**Obrigatorio**:
1. **Analisar**: Identificar o problema, entender contexto
2. **Planejar**: Listar passos antes de executar
3. **Executar**: Implementar um passo por vez
4. **Revisar**: Validar resultado antes de prosseguir

**Proibido**:
- Implementar sem planejar (tarefas > 3 passos)
- Pular revisao pos-implementacao
- Token desperdio em abordagens erradas

---

## Regra de ouro 10 - Nomenclatura Simples (Adicionado 2026-06-27)

Variaveis, funcoes e parametros devem usar nomes de palavra unica quando possivel.

**Obrigatorio**:
- Nomes padrao: pid, cfg, err, opts, dir, oot, child, state, 	imeout
- Multi-word apenas quando ambiguo
- Evitar: inputPID, existingClient, connectTimeout, workerPath

**Proibido**:
- camelCase compounds desnecessarios
- Nomes > 2 palavras quando 1 e' suficiente