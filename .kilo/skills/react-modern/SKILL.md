---
name: react-modern
description: Especialista em React moderno (Vite + TypeScript + Tailwind + TanStack Query + Zod + React Hook Form). Cobre SPA, Vite, CRA, state management, component patterns, performance, testing e deploy. Use para qualquer projeto React standalone.
whenToUse: Use quando o usuario pedir "app React", "SPA em React", "React com Vite", "React com TypeScript", "frontend React", "React com Tailwind", "React com shadcn/ui", "React com TanStack Query". NAO use para Next.js (use next-modern) ou Angular (use angular-modern).
---

# react-modern

## Filosofia

**React puro, sem opiniao de framework fullstack.** Para SSR, SSG, routing server-side e API routes, use `next-modern`. Para SPA com API backend separado, use este skill.

## Stack Padrao (2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Build | **Vite 5+** | Rapido, ESM nativo, HMR instantaneo |
| Linguagem | **TypeScript estrito** | Type safety, melhor DX |
| Styling | **Tailwind CSS v4** | Utility-first, design system via tokens |
| Components | **shadcn/ui** (opcional) | Copy-paste, sem vendor lock-in |
| State (global) | **Zustand** ou **Jotai** | Mais simples que Redux |
| Server state | **TanStack Query v5** | Cache, refetch, dedupe |
| Forms | **React Hook Form + Zod** | Performance + validacao tipada |
| Routing | **React Router 6+** | Standard de mercado |
| Tests | **Vitest + Testing Library** | Rapido, ESM nativo |
| Lint/Format | **ESLint + Prettier** | Obrigatorio |
| Deploy | **Vercel, Netlify, Cloudflare Pages** | Suporte Vite nativo |

## Decisoes de Arquitetura

### 1. Bundler: Vite (recomendado) vs CRA vs Next
- **Vite** (default 2026): rapido, leve, dev server em < 1s
- **CRA** (legado): NAO use para projetos novos
- **Next.js**: use `next-modern` skill (SSR/SSG/API routes)

### 2. Routing
- **React Router 6+**: SPA tradicional
- **TanStack Router**: type-safe, alternativo moderno
- **Wouter**: minimalista, 1.5KB

### 3. State Management
- **Local state**: `useState`, `useReducer`
- **Shared state**: Context API (apenas para auth, theme)
- **Global state**: Zustand (simples) ou Jotai (atom-based)
- **Server state**: TanStack Query (SEMPRE para data fetching)
- **Evite Redux** exceto em apps muito grandes com state complexo

### 4. Styling
- **Tailwind CSS v4** (default): utility-first
- **CSS Modules**: para escopo local sem Tailwind
- **Styled Components / Emotion**: raramente necessario
- **shadcn/ui**: componentes copiáveis com Tailwind + Radix

### 5. Data Fetching
- **TanStack Query** (default): cache, refetch, mutations
- **SWR**: alternativa mais simples
- **Native fetch + useEffect**: NAO use para production
- **Axios**: NAO use (fetch nativo + TanStack Query)

### 6. Forms
- **React Hook Form + Zod**: performance, type-safe
- **Formik**: legado, evite
- **Native form**: apenas forms triviais

## Estrutura de Pastas (recomendada)

```
/
├── public/
│   └── assets/
├── src/
│   ├── components/        # Componentes reutilizaveis
│   │   ├── ui/            # Primitivos (Button, Input, Card)
│   │   └── features/      # Componentes de feature
│   ├── pages/             # Paginas (rota -> componente)
│   ├── hooks/             # Custom hooks
│   ├── lib/               # Utilitarios, api clients
│   ├── stores/            # Estado global (Zustand)
│   ├── types/             # TypeScript types
│   ├── routes.tsx         # Definicao de rotas
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css          # Tailwind directives
├── index.html
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial

```bash
# Criar projeto com Vite
npm create vite@latest my-app -- --template react-ts
cd my-app

# Dependencias core
npm install react-router-dom @tanstack/react-query zustand
npm install react-hook-form zod @hookform/resolvers
npm install -D tailwindcss@4 @tailwindcss/vite
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
npm install -D eslint prettier eslint-config-prettier
```

## Padroes Obrigatorios

- **TypeScript estrito**: `strict: true` no tsconfig
- **Componentes funcionais**: SEM classes
- **Hooks customizados**: encapsular logica reutilizavel
- **Props tipadas**: `interface Props { ... }` ou `type Props = { ... }`
- **Nomes descritivos**: `UserList`, `useUserSearch`, `formatCurrency`
- **Evite prop drilling**: use Context ou Zustand
- **Memoizacao consciente**: useMemo/useCallback APENAS quando necessario
- **Acessibilidade**: ARIA labels, keyboard nav, contraste
- **Responsividade mobile-first**: Tailwind ja cuida
- **Code splitting**: `React.lazy` + `Suspense` para rotas

## Anti-patterns

- `useEffect` para data fetching (use TanStack Query)
- Prop drilling > 2 niveis (use Context/Zustand)
- Re-renders desnecessarios (use `memo`, `useMemo`, `useCallback` conscientemente)
- Inline styles ao inves de Tailwind
- `any` em TypeScript
- Componentes > 250 linhas (quebrar)
- Mutacao direta de state (`state.foo = 1`)
- `useEffect` sem dependencias ou com dependencias erradas

## Validacao

```bash
npm run build      # Vite build
npm run lint       # ESLint
npm run test       # Vitest
npm run preview    # Preview build
npx tsc --noEmit   # Type check
```

## Comandos

```
/criar-projeto app React de gestao de tarefas
/criar-projeto dashboard em React com graficos
/criar-projeto landing page em React (use minimal-html-tailwind se for simples)
/analisar-projeto --stack react
```

## Quando Escalar para Next.js

- SEO e OG meta tags dinamicas
- SSR/SSG para performance
- API routes (BFF pattern)
- Multi-tenant com middleware
- Streaming UI

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com dependencias corretas
2. `vite.config.ts` com plugins (React, Tailwind v4)
3. `tsconfig.json` estrito
4. `tailwind.config.ts` (se v3) ou `@import` no CSS (se v4)
5. `src/main.tsx` + `src/App.tsx`
6. `src/routes.tsx` (se multi-page)
7. Componentes em `src/components/`
8. Paginas em `src/pages/`
9. Hooks customizados em `src/hooks/`
10. Testes em `src/__tests__/` ou co-localizados
11. README com setup e scripts
