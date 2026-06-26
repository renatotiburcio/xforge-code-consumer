---
name: next-modern
description: Especialista em Next.js 14+ (App Router + TypeScript + Tailwind + Server Components + Server Actions). Cobre SSR, SSG, ISR, Route Handlers, Middleware, Image Optimization, Streaming e deploy em Vercel/Node/self-hosted. Use para qualquer projeto Next.js.
whenToUse: Use quando o usuario pedir "app Next.js", "Next.js com App Router", "Next.js com TypeScript", "Next.js fullstack", "Next.js com SSR", "Next.js com API routes", "Next.js com Server Actions", "Next.js + Tailwind". NAO use para SPA puro (use react-modern) ou Angular (use angular-modern).
---

# next-modern

## Filosofia

**Next.js = React com superpoderes de servidor.** Server Components, Server Actions, streaming, file-based routing e otimizacoes automaticas. Use quando precisa de SSR, SEO, performance maxima ou fullstack em um unico projeto.

## Stack Padrao (Next.js 15+)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Framework | **Next.js 15+ (App Router)** | Server Components, streaming |
| Linguagem | **TypeScript estrito** | Type safety |
| Styling | **Tailwind CSS v4** | Utility-first, suporte first-class |
| Components | **shadcn/ui** (opcional) | Copy-paste, RSC-compatible |
| State (client) | **Zustand** ou **Jotai** | Para state client-side persistente |
| Server state | **TanStack Query** ou **RSC + fetch** | RSC elimina 80% do data fetching |
| Forms (server) | **Server Actions + Zod** | Sem API routes para forms |
| DB | **Prisma, Drizzle, ou lib do provider** | Type-safe |
| Auth | **Auth.js (NextAuth v5)**, **Clerk**, **Lucia** | Pick conforme caso |
| Tests | **Vitest + Testing Library + Playwright** | Unit + E2E |
| Lint/Format | **ESLint + Prettier** | Next.js ja vem com config |
| Deploy | **Vercel (default)**, **Node standalone**, **Docker** | Vercel eh o path of least resistance |

## Decisoes de Arquitetura

### 1. Router: App Router (recomendado) vs Pages Router
- **App Router (default 2024+)**: Server Components, layouts, streaming, Server Actions
- **Pages Router (legado)**: NAO use para projetos novos

### 2. Rendering Strategy
- **Static (default)**: SSG, melhor performance
- **Dynamic**: SSR por request
- **ISR**: revalidate com `revalidate` ou `revalidateTag`
- **Streaming**: `loading.tsx`, `Suspense` boundaries
- **Escolha automaticamente** baseado em dados:
  - Sem cookies/headers/searchParams -> Static
  - Com dados que mudam raramente -> ISR
  - Com dados por usuario -> Dynamic

### 3. Data Fetching
- **RSC + fetch nativo** (default): cache automatico, deduplicacao
- **TanStack Query**: para client-side mutations e real-time
- **Server Actions**: para forms e mutations
- **Route Handlers (`route.ts`)**: para APIs publicas/webhooks

### 4. Forms
- **Server Actions + Zod** (recomendado): zero API routes
- **React Hook Form + Zod**: para forms client-side complexos
- **Conform**: alternativa type-safe

### 5. Auth
- **Auth.js (NextAuth v5)**: open-source, OAuth, credentials
- **Clerk**: managed, UI components prontos
- **Lucia**: minimalista, mais controle
- **Supabase Auth**: se ja usa Supabase

### 6. ORM
- **Prisma**: maduro, migrations, Studio
- **Drizzle**: SQL-like, type-safe, mais leve
- **Supabase**: se usa Supabase como backend

## Estrutura de Pastas (App Router)

```
/
├── app/
│   ├── (auth)/                 # Route group (sem afetar URL)
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (marketing)/
│   │   ├── page.tsx            # /
│   │   └── about/
│   │       └── page.tsx        # /about
│   ├── dashboard/
│   │   ├── layout.tsx          # Shared layout
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   └── settings/
│   │       └── page.tsx
│   ├── api/
│   │   └── webhooks/
│   │       └── route.ts        # POST /api/webhooks
│   ├── actions/                # Server Actions
│   │   └── users.ts
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home
│   ├── loading.tsx
│   ├── error.tsx
│   ├── not-found.tsx
│   ├── globals.css
│   └── icon.tsx                # Favicon
├── components/
│   ├── ui/
│   └── features/
├── lib/
│   ├── db.ts                   # Prisma client
│   ├── auth.ts
│   └── utils.ts
├── server/
│   ├── queries/                # RSC data fetching
│   └── actions/                # Server Actions
├── public/
├── middleware.ts               # Auth, redirects, headers
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial

```bash
# Criar projeto
npx create-next-app@latest my-app --typescript --tailwind --app --src-dir
cd my-app

# Dependencias core
npm install @tanstack/react-query zustand zod
npm install react-hook-form @hookform/resolvers
npm install -D vitest @testing-library/react playwright

# Auth
npm install next-auth@beta

# DB
npm install prisma @prisma/client
npx prisma init
```

## Padroes Obrigatorios

- **Server Components por default**: `'use client'` APENAS quando necessario
- **Co-locate data fetching**: queries dentro de `app/` ou `server/queries/`
- **`'use client'` minimo**: state, effects, browser APIs
- **TypeScript estrito**: `strict: true`
- **Metadata API**: `export const metadata` ou `generateMetadata`
- **Image Optimization**: `<Image>` em vez de `<img>`
- **Font Optimization**: `next/font`
- **Loading UI**: `loading.tsx` em rotas com data fetching
- **Error boundaries**: `error.tsx` em niveis apropriados
- **SEO**: metadata, OpenGraph, JSON-LD quando relevante
- **Acessibilidade**: ARIA, keyboard nav, semantica HTML

## Anti-patterns

- `'use client'` em paginas inteiras sem necessidade
- Data fetching client-side desnecessario (use RSC)
- `<img>` ao inves de `<Image>`
- Inline styles ao inves de Tailwind
- `useEffect` para data fetching
- Mutacoes client-side para coisas que podem ser Server Actions
- Fetch sem `cache` strategy explicita
- Pages Router para projetos novos

## Validacao

```bash
npm run build       # Next.js build (valida tipos, SSR, etc)
npm run lint        # ESLint
npm run test        # Vitest
npx tsc --noEmit    # Type check
npx playwright test # E2E
```

## Comandos

```
/criar-projeto app Next.js de e-commerce
/criar-projeto blog com Next.js e MDX
/criar-projeto dashboard fullstack com Next.js + Prisma + Auth.js
/analisar-projeto --stack nextjs
```

## Quando Usar Vite/React Puro (react-modern)

- App puramente client-side (sem SSR/SSG)
- Backend ja separado (consumir API REST/GraphQL)
- Site institucional simples sem SEO

## Quando Usar Astro (criar skill separado se necessario)

- Sites de conteudo (blogs, docs, marketing)
- Ilhas de interatividade (maioria estatico, alguns componentes React)
- Performance maxima com zero JS

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com `next`, `react`, `tailwindcss` corretos
2. `next.config.ts` com config necessaria
3. `tsconfig.json` estrito
4. `app/layout.tsx` (root layout com html/body)
5. `app/page.tsx` (home)
6. `app/globals.css` com Tailwind directives
7. Paginas em `app/<route>/page.tsx`
8. Server Actions em `app/actions/` ou `server/actions/`
9. Componentes em `components/`
10. (Opcional) `middleware.ts` para auth
11. (Opcional) `prisma/schema.prisma` se usando DB
12. README com setup, env vars, scripts
