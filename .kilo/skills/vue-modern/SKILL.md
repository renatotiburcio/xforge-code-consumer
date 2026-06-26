---
name: vue-modern
description: Especialista em Vue 3 moderno (Vite + TypeScript + Composition API + Tailwind + Pinia + Vue Router). Cobre SPA, Nuxt 3 (SSR/SSG), component patterns, reactivity, forms, testing e deploy. Use para qualquer projeto Vue.
whenToUse: Use quando o usuario pedir "app Vue", "Vue 3", "Vue com Vite", "Vue com TypeScript", "Nuxt 3", "frontend Vue", "Vue com Tailwind", "Vue com Pinia". NAO use para React (use react-modern) ou Angular (use angular-modern).
---

# vue-modern

## Filosofia

**Vue = o melhor dos dois mundos.** Template HTML familiar + reatividade granular + Composition API para logica complexa. Mais simples que React, mais flexivel que Angular.

## Stack Padrao (Vue 3 / 2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Framework | **Vue 3.4+** | Composition API, `<script setup>`, reactivity |
| Build | **Vite 5+** | Rapido, HMR |
| Linguagem | **TypeScript estrito** | Type safety |
| Styling | **Tailwind CSS v4** OU **UnoCSS** | Utility-first |
| Components | **shadcn-vue** (opcional) | Copy-paste, Tailwind |
| State (global) | **Pinia** | Oficial, substitui Vuex |
| Server state | **TanStack Query (Vue)** ou **VueUse** | Cache, refetch |
| Forms | **VeeValidate + Zod** | Validacao type-safe |
| Routing | **Vue Router 4+** | Oficial |
| SSR/SSG | **Nuxt 3** (quando necessario) | File-based, fullstack |
| Tests | **Vitest + Vue Test Utils** | Rapido |
| Lint/Format | **ESLint + Prettier** | Obrigatorio |
| Deploy | **Vercel, Netlify, Cloudflare Pages** | Vite nativo |

## Decisoes de Arquitetura

### 1. SPA vs SSR/SSG
- **Vue 3 + Vite (SPA)**: app puramente client-side, sem SEO
- **Nuxt 3**: SSR, SSG, file-based routing, API routes, fullstack
- **Escolha**: SEO/performance -> Nuxt; SPA puro -> Vue+Vite

### 2. Component API: Composition (recomendado) vs Options
- **Composition API + `<script setup>`** (default 2024+): mais simples, melhor TS
- **Options API** (legado): evite para novos projetos

### 3. State Management
- **Local state**: `ref()`, `reactive()`
- **Shared state**: Pinia stores
- **Server state**: TanStack Query Vue (ou use `useFetch` no Nuxt)
- **Evite Vuex** (substituido pelo Pinia)

### 4. Reactivity
- `ref()` para primitivos
- `reactive()` para objetos
- `computed()` para valores derivados
- `watch()` / `watchEffect()` para side effects
- `shallowRef()` para arrays/objetos grandes

### 5. Styling
- **Tailwind CSS v4**: utility-first
- **UnoCSS**: alternativa mais rapida
- **CSS Modules**: escopo local
- **Vue SFC `<style scoped>`**: para Vue-only

### 6. Data Fetching
- **Nuxt**: `useFetch`, `useAsyncData` (SSR-aware)
- **SPA**: TanStack Query Vue
- **Composables customizados**: encapsular logica de fetch

## Estrutura de Pastas (Vue 3 + Vite)

```
/
├── public/
├── src/
│   ├── assets/
│   ├── components/        # Componentes globais
│   │   ├── ui/
│   │   └── features/
│   ├── composables/       # Composables (use* functions)
│   ├── views/             # Paginas (rota -> componente)
│   ├── stores/            # Pinia stores
│   ├── router/            # Vue Router config
│   ├── types/             # TypeScript types
│   ├── lib/               # Utilitarios, api clients
│   ├── App.vue
│   ├── main.ts
│   └── style.css          # Tailwind directives
├── index.html
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Estrutura de Pastas (Nuxt 3)

```
/
├── app/
│   ├── app.vue            # Root component
│   ├── pages/             # File-based routing
│   ├── components/
│   ├── composables/
│   ├── layouts/
│   ├── middleware/
│   ├── plugins/
│   ├── stores/
│   └── assets/
├── public/
├── server/
│   ├── api/               # API routes (Nitro)
│   └── middleware/
├── nuxt.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial

```bash
# Vue 3 + Vite
npm create vue@latest my-app -- --typescript --router --pinia --vitest
cd my-app
npm install
npm install -D tailwindcss@4 @tailwindcss/vite

# Nuxt 3
npx nuxi@latest init my-app
cd my-app
npm install
npm install -D @nuxtjs/tailwindcss
```

## Padroes Obrigatorios

- **`<script setup>`** em todos os componentes
- **TypeScript estrito**
- **Composables** para logica reutilizavel
- **Pinia** para state global
- **Props tipadas**: `defineProps<{ name: string }>()`
- **Emits tipados**: `defineEmits<{ change: [value: string] }>()`
- **Refs desestruturados** com `toRefs` ou `storeToRefs` (Pinia)
- **Acessibilidade**: ARIA, keyboard nav
- **Code splitting**: `defineAsyncComponent` para componentes grandes

## Anti-patterns

- Options API em projetos novos
- `reactive()` para primitivos (use `ref`)
- Mutacao direta de arrays/objetos reativos (use spread)
- `watch()` sem dependencias ou com dependencias erradas
- Props sem tipo
- Componentes > 250 linhas
- Logica complexa no template (mova para `<script setup>`)
- Vuex em projetos novos (use Pinia)

## Exemplo: Componente com Composition API

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
  userId: string
}>()

const userStore = useUserStore()
const searchTerm = ref('')

const filteredUsers = computed(() =>
  userStore.users.filter(u => u.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
)
</script>

<template>
  <div class="space-y-4">
    <input v-model="searchTerm" type="text" placeholder="Buscar..."
           class="px-4 py-2 border rounded" />
    <ul class="divide-y">
      <li v-for="user in filteredUsers" :key="user.id" class="p-4">
        {{ user.name }}
      </li>
    </ul>
  </div>
</template>
```

## Validacao

```bash
npm run build      # Vite/Nuxt build
npm run lint       # ESLint
npm run test       # Vitest
npx tsc --noEmit   # Type check
```

## Comandos

```
/criar-projeto app Vue 3 de gestao de tarefas
/criar-projeto dashboard em Vue com Pinia
/criar-projeto site institucional com Nuxt 3
/analisar-projeto --stack vue
```

## Quando Escalar para Nuxt

- SEO e meta tags dinamicas
- SSR/SSG para performance
- API routes (BFF)
- Multi-tenant com middleware
- Streaming UI
- ISR

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com `vue`, `vite`/`nuxt`, `tailwindcss`
2. `vite.config.ts` ou `nuxt.config.ts`
3. `tsconfig.json` estrito
4. `src/main.ts` + `src/App.vue` (Vue) OU `app/app.vue` (Nuxt)
5. Composables em `src/composables/` (ou `app/composables/`)
6. Pinia stores em `src/stores/`
7. Router config em `src/router/` (Vue) ou `app/pages/` (Nuxt)
8. Componentes em `src/components/` ou `app/components/`
9. README com setup e scripts
