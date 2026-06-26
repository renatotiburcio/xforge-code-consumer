---
name: svelte-modern
description: Especialista em Svelte 4+ e SvelteKit (TypeScript + Tailwind). Cobre Svelte puro, SvelteKit fullstack, runes (Svelte 5), stores, transitions, SSR, form actions e deploy. Use para qualquer projeto Svelte/SvelteKit.
whenToUse: Use quando o usuario pedir "app Svelte", "SvelteKit", "Svelte 5", "Svelte com TypeScript", "frontend Svelte", "Svelte com Tailwind", "Svelte fullstack". NAO use para React (use react-modern), Vue (use vue-modern) ou Angular (use angular-modern).
---

# svelte-modern

## Filosofia

**Svelte = compilador, nao framework em runtime.** Codigo mais limpo, bundle minimo, sem Virtual DOM. SvelteKit adiciona SSR, routing, API routes e tudo fullstack. A melhor opcao para performance maxima.

## Stack Padrao (Svelte 5+ / 2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Framework | **Svelte 5+ (runes)** OU **Svelte 4+** | Runes: state, derived, effect |
| Fullstack | **SvelteKit** (default para apps) | SSR, file-based routing, API |
| Linguagem | **TypeScript estrito** | Type safety |
| Styling | **Tailwind CSS v4** | Utility-first |
| State | **Runes ($state, $derived)** + **Svelte stores** | Compilador otimiza |
| Server state | **SvelteKit load functions** | SSR-aware, type-safe |
| Forms | **SvelteKit form actions + Zod** | Built-in, progressive enhancement |
| Routing | **SvelteKit file-based** | $app/stores, $page |
| Tests | **Vitest + @testing-library/svelte** + **Playwright** | Unit + E2E |
| Lint/Format | **ESLint + Prettier** + **prettier-plugin-svelte** | Obrigatorio |
| Deploy | **Vercel, Netlify, Cloudflare Pages, Node** | Adapter pattern |

## Decisoes de Arquitetura

### 1. Svelte puro vs SvelteKit
- **Svelte 5+ puro**: app client-side, sem SSR (raro)
- **SvelteKit (default 2026)**: SSR/SSG, file-based routing, API routes, form actions
- **Escolha**: SvelteKit para qualquer app nao-trivial

### 2. Svelte 5 Runes vs Svelte 4 reatividade
- **Svelte 5+ (runes)**: `$state`, `$derived`, `$effect`, `$props`, `$bindable`
- **Svelte 4 (legado)**: `let`, `$:`, `export let`
- **Use Svelte 5** para projetos novos

### 3. State Management
- **Local**: `$state(...)` (runes)
- **Derived**: `$derived(...)` ou `$derived.by(() => ...)`
- **Side effects**: `$effect(() => ...)`
- **Global**: Svelte stores (`writable`, `readable`, `derived`) + `getContext`/`setContext`
- **Server state**: SvelteKit `load` functions (SSR-aware)

### 4. Styling
- **Tailwind CSS v4**: utility-first
- **Svelte scoped styles**: `<style>` no componente (escopo automatico)
- **CSS custom properties**: para theming

### 5. Data Fetching
- **SvelteKit load functions**: `+page.ts`, `+layout.ts`, `+page.server.ts`
- **Universal load**: roda em SSR + client
- **Server load**: roda so no server (acesso a DB direto)
- **Form actions**: para mutations com progressive enhancement

## Estrutura de Pastas (SvelteKit)

```
/
├── src/
│   ├── routes/                    # File-based routing
│   │   ├── +layout.svelte         # Root layout
│   │   ├── +layout.ts             # Root load
│   │   ├── +page.svelte           # Home (/)
│   │   ├── +page.ts               # Home load
│   │   ├── about/
│   │   │   ├── +page.svelte
│   │   │   └── +page.ts
│   │   └── dashboard/
│   │       ├── +layout.svelte     # Auth guard
│   │       ├── +page.svelte
│   │       ├── +page.server.ts    # Server load (DB)
│   │       └── +page.server.ts    # Form actions
│   ├── lib/
│   │   ├── components/            # Componentes reutilizaveis
│   │   ├── server/                # Server-only code (DB, auth)
│   │   │   ├── db.ts
│   │   │   └── auth.ts
│   │   ├── stores/                # Svelte stores
│   │   ├── utils/
│   │   └── types/
│   ├── hooks.client.ts
│   ├── hooks.server.ts
│   ├── app.html                   # HTML template
│   ├── app.d.ts                   # TypeScript types
│   └── app.css                    # Tailwind imports + globals
├── static/                        # Assets estaticos
├── tests/                         # E2E (Playwright)
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial

```bash
# Criar projeto SvelteKit
npx sv create my-app
# Selecionar: SvelteKit minimal, TypeScript, Tailwind, Vitest, Playwright
cd my-app
npm install
npm run dev
```

## Padroes Obrigatorios

- **Svelte 5 runes** (default): `$state`, `$derived`, `$effect`, `$props`
- **TypeScript estrito** em `.svelte`, `.ts`
- **SvelteKit load functions** para data fetching
- **Form actions** para forms (progressive enhancement)
- **Scoped styles** em componentes (`<style>` block)
- **Tailwind** para layout/utility
- **Acessibilidade**: ARIA, keyboard nav, semantica
- **A11y warnings**: tratar warnings do compilador

## Anti-patterns

- Svelte 4 syntax em projetos novos (use runes)
- Mutacao direta de `$state` (use `.update()` para stores)
- `+page.ts` para data que precisa de auth (use `+page.server.ts`)
- Inline styles > 50 linhas (mova para `<style>` ou Tailwind)
- Componentes > 250 linhas
- Logica complexa no template
- Fetch em `onMount` quando pode ser `load`

## Exemplo: Componente Svelte 5 com Runes

```svelte
<script lang="ts">
  import { enhance } from '$app/forms'

  interface Props {
    userId: string
  }

  let { userId }: Props = $props()

  let searchTerm = $state('')
  let users = $state<User[]>([])

  let filteredUsers = $derived(
    users.filter(u => u.name.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  $effect(() => {
    fetch(`/api/users?q=${searchTerm}`)
      .then(r => r.json())
      .then(data => users = data)
  })
</script>

<div class="space-y-4">
  <input bind:value={searchTerm} type="text" placeholder="Buscar..."
         class="px-4 py-2 border rounded" />
  <ul class="divide-y">
    {#each filteredUsers as user (user.id)}
      <li class="p-4">{user.name}</li>
    {/each}
  </ul>
</div>
```

## Exemplo: Form Action (SvelteKit)

```typescript
// src/routes/users/+page.server.ts
import { z } from 'zod'
import { fail, type Actions } from '@sveltejs/kit'

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
})

export const actions: Actions = {
  create: async ({ request, locals }) => {
    const formData = await request.formData()
    const result = schema.safeParse(Object.fromEntries(formData))
    if (!result.success) {
      return fail(400, { errors: result.error.flatten() })
    }
    await db.user.create({ data: result.data })
    return { success: true }
  },
}
```

## Validacao

```bash
npm run build      # SvelteKit build
npm run check      # svelte-check (type + a11y)
npm run lint       # ESLint
npm run test       # Vitest
npm run test:e2e   # Playwright
```

## Comandos

```
/criar-projeto app SvelteKit de blog
/criar-projeto dashboard com Svelte 5 runes
/criar-projeto site institucional com SvelteKit
/analisar-projeto --stack svelte
```

## Quando Escolher Svelte

- Performance eh critica (bundle minimo, sem Virtual DOM)
- App fullstack com file-based routing
- Quer simplicidade maxima
- Equipe prefere menos JS no client

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com `@sveltejs/kit`, `svelte`, `vite`, `tailwindcss`
2. `svelte.config.js` com adapter (auto, vercel, cloudflare, node)
3. `vite.config.ts`
4. `tsconfig.json` estrito
5. `src/app.html` (HTML template)
6. `src/app.css` com Tailwind
7. `src/routes/+layout.svelte` (root layout)
8. `src/routes/+page.svelte` (home)
9. Componentes em `src/lib/components/`
10. Server code em `src/lib/server/`
11. Stores em `src/lib/stores/`
12. README com setup, scripts, deploy
