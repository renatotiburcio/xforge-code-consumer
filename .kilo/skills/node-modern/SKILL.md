---
name: node-modern
description: Especialista em Node.js backend moderno (TypeScript + Express/Fastify/NestJS + Zod + Prisma/Drizzle + JWT + OpenAPI). Cobre API REST, GraphQL, microservices, queue workers, real-time (WebSocket/Socket.IO), e deploy (Docker, PM2, serverless).
whenToUse: Use quando o usuario pedir "API Node.js", "backend Node", "Express API", "Fastify API", "NestJS", "microservico Node", "worker Node", "GraphQL com Node", "API com TypeScript". NAO use para .NET (use dotnet-standards) ou Python (use python-modern).
---

# node-modern

## Filosofia

**Node.js = o canivete suico de backend.** Ecossistema gigante, assincronismo natural, deploy simples. Use para APIs REST, GraphQL, microservices, workers, real-time, BFF.

## Stack Padrao (2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Runtime | **Node.js 20+ LTS** | ESM nativo, performance |
| Linguagem | **TypeScript estrito** | Type safety |
| Framework | **Fastify** (rapido) / **Express** (popular) / **NestJS** (enterprise) | Escolha conforme caso |
| Validacao | **Zod** (default) / **Joi** / **class-validator** | Type-safe schemas |
| ORM | **Prisma** (maduro) / **Drizzle** (SQL-first) / **TypeORM** (legado) | Escolha conforme DB |
| Auth | **jose** + **passport** OU **@nestjs/jwt** | JWT + refresh tokens |
| OpenAPI | **zod-to-openapi** / **@nestjs/swagger** | Doc automatica |
| Queue | **BullMQ** (Redis) / **Inngest** | Background jobs |
| Real-time | **Socket.IO** / **ws** / **@nestjs/websockets** | WebSocket |
| Tests | **Vitest** (rapido) / **Jest** (popular) | Unit + integration |
| Lint/Format | **ESLint + Prettier** | Obrigatorio |
| Logging | **Pino** (rapido) / **Winston** | Estruturado |
| Deploy | **Docker**, **PM2**, **Vercel**, **AWS Lambda**, **Cloudflare Workers** | Multi-target |

## Decisoes de Arquitetura

### 1. Framework: Fastify vs Express vs NestJS vs Hono
- **Fastify** (recomendado 2026): 3x mais rapido que Express, schema-first
- **Express** (legado, popular): vasto ecossistema, mas lento
- **NestJS** (enterprise): opinionated, DI forte, similar a Spring/Angular
- **Hono** (edge-first): ultra-leve, Cloudflare Workers/Deno/Bun
- **Koa**: minimalista, sem opiniao

### 2. ORM: Prisma vs Drizzle vs TypeORM vs Knex
- **Prisma** (default): migrations, Studio, type generation
- **Drizzle** (SQL-first): type-safe, leve, mais controle
- **TypeORM** (legado): decorator-based, evite para projetos novos
- **Knex** (query builder): para queries complexas

### 3. Module System
- **ESM** (default 2024+): `import/export`, melhor para TypeScript
- **CommonJS** (legado): `require/module.exports`

### 4. API Style
- **REST + OpenAPI** (default)
- **GraphQL** (Apollo Server, Mercurius, GraphQL Yoga)
- **tRPC** (type-safe end-to-end, sem schema separado)
- **gRPC** (microservices)

### 5. Auth
- **JWT + refresh tokens** (recomendado): `jose` para assinar/verificar
- **Sessions** (server-side): Redis store
- **OAuth 2.0 / OIDC**: `openid-client`, `@auth/express`
- **Passport**: estrategia-based, mas verbose


## Estrutura de Pastas (Fastify + Drizzle)

```
/
├── src/
│   ├── server.ts                 # Entry point
│   ├── app.ts                    # Fastify app factory
│   ├── config/
│   │   ├── env.ts                # Zod-validated env
│   │   └── database.ts
│   ├── modules/                  # Feature modules
│   │   └── user/
│   │       ├── user.schema.ts    # Zod schemas
│   │       ├── user.service.ts
│   │       ├── user.repository.ts
│   │       ├── user.routes.ts
│   │       └── user.test.ts
│   ├── plugins/                  # Fastify plugins
│   │   ├── auth.ts
│   │   ├── cors.ts
│   │   └── rate-limit.ts
│   ├── lib/
│   │   ├── errors.ts
│   │   ├── logger.ts
│   │   └── db.ts                 # Drizzle client
│   └── types/
├── drizzle/                      # Migrations
│   └── meta/
├── tests/                        # Integration + E2E
│   └── helpers/
├── .env.example
├── drizzle.config.ts
├── tsconfig.json
├── package.json
├── Dockerfile
└── README.md
```

## Estrutura de Pastas (NestJS)

```
/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── modules/
│   │   └── user/
│   │       ├── user.module.ts
│   │       ├── user.controller.ts
│   │       ├── user.service.ts
│   │       ├── user.repository.ts
│   │       ├── dto/
│   │       ├── entities/
│   │       └── user.controller.spec.ts
│   ├── common/
│   │   ├── guards/
│   │   ├── filters/
│   │   ├── interceptors/
│   │   ├── decorators/
│   │   └── pipes/
│   ├── config/
│   └── database/
├── test/
├── nest-cli.json
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial (Fastify + Drizzle)

```bash
mkdir my-api && cd my-api
npm init -y
npm install fastify @fastify/cors @fastify/jwt @fastify/swagger
npm install drizzle-orm postgres
npm install zod
npm install -D typescript @types/node tsx drizzle-kit vitest
npx tsc --init
```

## Padroes Obrigatorios

- **TypeScript estrito** com `strict: true`
- **ESM** (default)
- **Zod** para validacao de input/env/schema
- **Repository pattern** para acesso a dados
- **Dependency injection** (manual ou framework)
- **Structured logging** (Pino)
- **Error handling centralizado**
- **Env vars validadas** com Zod no startup
- **Health check** endpoint
- **Graceful shutdown** (SIGTERM handler)
- **OpenAPI** gerado de schemas
- **Testes**: unit + integration + E2E

## Anti-patterns

- `any` em TypeScript
- Callbacks (use Promises/async-await)
- `console.log` em producao (use logger)
- Try/catch sem re-throw ou log
- Mutacao de parametros de funcao
- SQL injection (use ORM ou queries parametrizadas)
- Sync I/O em handler
- Falta de validation de input
- Hardcoded secrets (use env vars)
- `process.env.X` sem validation (use Zod)

## Exemplo: Fastify + Zod + Drizzle

```typescript
// src/modules/user/user.schema.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
})

export type CreateUserInput = z.infer<typeof createUserSchema>

// src/modules/user/user.routes.ts
import type { FastifyInstance } from 'fastify'
import { createUserSchema } from './user.schema'
import { UserService } from './user.service'

export async function userRoutes(app: FastifyInstance) {
  const service = new UserService(app.db)

  app.post('/users', async (req, reply) => {
    const input = createUserSchema.parse(req.body)
    const user = await service.create(input)
    return reply.code(201).send(user)
  })

  app.get('/users', async (req) => {
    return service.list()
  })
}

// src/modules/user/user.service.ts
import type { CreateUserInput } from './user.schema'
import type { Database } from '../../lib/db'

export class UserService {
  constructor(private db: Database) {}

  async create(input: CreateUserInput) {
    return this.db.insert(users).values(input).returning()
  }

  async list() {
    return this.db.select().from(users)
  }
}
```

## Validacao

```bash
npm run build      # tsc
npm run lint       # ESLint
npm run test       # Vitest
npx tsc --noEmit   # Type check
npm audit          # Vulnerabilidades
```

## Comandos

```
/criar-api API de gestao de usuarios com Node + Fastify + JWT
/criar-api microservico com NestJS + Prisma + PostgreSQL
/criar-api GraphQL com Node + Apollo + Prisma
/criar-projeto worker de processamento de filas com BullMQ
```

## Quando Escalar

- **Microservices**: decompor por dominio, usar mensageria (RabbitMQ, Kafka, Redis Streams)
- **Serverless**: AWS Lambda, Cloudflare Workers, Vercel Functions
- **Edge**: Hono + Cloudflare Workers
- **Real-time**: Socket.IO, ws, Server-Sent Events
- **GraphQL**: Apollo Server, Mercurius, GraphQL Yoga

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com framework escolhido + TypeScript + Zod + ORM
2. `tsconfig.json` estrito
3. `src/server.ts` (entry point)
4. `src/config/env.ts` (Zod-validated env)
5. Modulos em `src/modules/<feature>/`
6. Schemas Zod separados da logica
7. Repositorios para acesso a dados
8. Logger estruturado (Pino)
9. OpenAPI gerado
10. Testes (unit + integration)
11. Dockerfile
12. `.env.example` com todas vars
13. README com setup, env vars, scripts
