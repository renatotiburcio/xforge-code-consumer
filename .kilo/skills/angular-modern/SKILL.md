---
name: angular-modern
description: Especialista em Angular 17+ (standalone components + signals + Tailwind). Cobre Angular CLI, standalone-first architecture, signals, RxJS, control flow, dependency injection, routing, forms, testing e deploy. Use para qualquer projeto Angular.
whenToUse: Use quando o usuario pedir "app Angular", "Angular 17+", "Angular standalone", "Angular com Signals", "Angular com Tailwind", "Angular enterprise", "Angular SPA". NAO use para React (use react-modern) ou Vue (criar vue-modern).
---

# angular-modern

## Filosofia

**Angular = batteries-included, opinionated, enterprise-grade.** TypeScript-first, DI forte, RxJS, signals (2024+), standalone components. Use para apps enterprise, dashboards complexos, ou quando a equipe ja conhece Angular.

## Stack Padrao (Angular 17+)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Framework | **Angular 17+ (standalone-first)** | Componentes sem NgModule |
| Linguagem | **TypeScript estrito** | Type safety |
| Styling | **Tailwind CSS v4** OU **Angular Material** | Tailwind para custom, Material para enterprise UI |
| State | **Signals (default)** + **RxJS** | Signals para state sincrono, RxJS para async |
| Forms | **Reactive Forms (FormBuilder)** | Type-safe, escalavel |
| Routing | **Angular Router** | Lazy loading via `loadComponent` |
| HTTP | **HttpClient + interceptors** | Built-in |
| Tests | **Jasmine/Karma** OU **Jest** + **Cypress/Playwright** | Pick Jest se preferir moderno |
| Lint/Format | **ESLint + Prettier** | Angular CLI ja configura |
| Build | **Angular CLI (esbuild + Vite)** | Rapido |
| Deploy | **Static (Firebase, S3, Cloudflare)**, **SSR (Angular Universal)** | Escolha conforme SEO |

## Decisoes de Arquitetura

### 1. Componentes: Standalone (recomendado) vs NgModule
- **Standalone (default 2024+)**: mais simples, lazy loading granular
- **NgModule (legado)**: NAO use para projetos novos
- **Hybrid**: aceitavel em migracao gradual

### 2. State: Signals (recomendado) vs RxJS vs Services
- **Signals** (Angular 17+): state sincrono, computed, effect
- **RxJS**: para streams async, debounce, combineLatest
- **Services with Subjects**: legavel, mas signals sao mais simples
- **NgRx**: APENAS para apps MUITO grandes com state complexo

### 3. Styling
- **Tailwind CSS v4**: design custom, utility-first
- **Angular Material**: UI components prontos, enterprise look
- **PrimeNG**: alternativa rica ao Material
- **SCSS** (default Angular): para temas e variaveis

### 4. Forms
- **Reactive Forms** (recomendado): `FormBuilder`, `FormGroup`, validators
- **Template-driven**: para forms muito simples
- **Typed Forms** (Angular 14+): `FormGroup<{ name: FormControl<string> }>`

### 5. Routing
- **File-based**: NAO existe no Angular (vs Next.js)
- **Configuracao em `app.routes.ts`**: `loadComponent` para lazy loading
- **Functional route guards**: `CanActivateFn` (recomendado)
- **Functional interceptors**: `HttpInterceptorFn` (recomendado)

### 6. Backend Communication
- **HttpClient + interceptors**: para JWT, errors, loading
- **Apollo Client** (GraphQL): se backend GraphQL
- **TanStack Query Angular**: alternativa moderna para cache


## Estrutura de Pastas (Standalone-First)

```
/
├── src/
│   ├── app/
│   │   ├── core/                  # Singleton services, guards, interceptors
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts
│   │   │   │   └── api.service.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   └── error.interceptor.ts
│   │   │   └── models/
│   │   ├── shared/                # Componentes, pipes, directives reutilizaveis
│   │   │   ├── components/
│   │   │   ├── pipes/
│   │   │   ├── directives/
│   │   │   └── validators/
│   │   ├── features/              # Feature modules (lazy loaded)
│   │   │   ├── dashboard/
│   │   │   │   ├── dashboard.component.ts
│   │   │   │   ├── dashboard.component.html
│   │   │   │   ├── dashboard.component.scss
│   │   │   │   ├── dashboard.routes.ts
│   │   │   │   └── services/
│   │   │   └── users/
│   │   │       ├── user-list.component.ts
│   │   │       ├── user-form.component.ts
│   │   │       └── services/
│   │   ├── app.component.ts       # Root standalone component
│   │   ├── app.config.ts          # ApplicationConfig (providers)
│   │   └── app.routes.ts          # Root routes
│   ├── assets/
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   ├── styles.scss                # Global styles + Tailwind imports
│   ├── main.ts                    # bootstrapApplication(AppComponent, appConfig)
│   └── index.html
├── public/
├── angular.json
├── tsconfig.json
├── package.json
└── README.md
```

## Setup Inicial

```bash
# Criar projeto
npx -p @angular/cli@latest ng new my-app --standalone --routing --style=scss --ssr=false
cd my-app

# Tailwind v4
npm install -D tailwindcss@4
# Adicionar @import "tailwindcss" no styles.scss

# Dependencias uteis
npm install @angular/material  # opcional
npm install -D @ngrx/signals    # opcional, para state complexo

# Testing (alternativa ao Jasmine default)
npm install -D jest @types/jest @angular-builders/jest
```

## Padroes Obrigatorios

- **Standalone components por default**: SEM `NgModule`
- **Signals para state local**: `signal()`, `computed()`, `effect()`
- **RxJS para async**: `HttpClient`, `interval`, WebSockets
- **OnPush change detection**: `changeDetection: ChangeDetectionStrategy.OnPush`
- **Typed Forms**: `FormGroup<{...}>`
- **Strict TypeScript**: `strict: true` no tsconfig
- **TrackBy em `*ngFor`**: otimizar re-renders
- **Async pipe**: para observables no template (auto-unsubscribe)
- **Lazy loading**: `loadComponent` e `loadChildren`
- **Acessibilidade**: ARIA, keyboard nav, contraste
- **i18n**: `@angular/localize` se app multi-idioma

## Anti-patterns

- NgModule para projetos novos (use standalone)
- Subscribe manual sem unsubscribe (use AsyncPipe ou takeUntilDestroyed)
- `any` em TypeScript
- Componentes > 300 linhas (quebrar)
- Logica de negocio no template (mover para componente/servico)
- Mutacao direta de signals (`signal.set()` eh ok; `signal.mutate` para arrays/objetos)
- Re-renders desnecessarios (use OnPush + immutable updates)
- Inline templates > 50 linhas (mover para arquivo HTML)
- Estado compartilhado via @Input/@Output com mais de 2 niveis (use services/signals)

## Exemplo: Componente Standalone com Signals

```typescript
import { Component, signal, computed, ChangeDetectionStrategy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-list.component.html',
  styleUrl: './user-list.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserListComponent {
  private http = inject(HttpClient);
  searchTerm = signal('');
  users = toSignal(this.http.get<User[]>('/api/users'), { initialValue: [] });
  filteredUsers = computed(() =>
    this.users().filter(u => u.name.toLowerCase().includes(this.searchTerm().toLowerCase()))
  );
}
```

## Exemplo: app.config.ts (Standalone)

```typescript
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([authInterceptor])),
    provideAnimations(),
  ],
};
```

## Validacao

```bash
ng build               # Production build
ng test                # Unit tests
ng lint                # ESLint
ng e2e                 # E2E (Cypress ou Playwright)
npx tsc --noEmit       # Type check
```

## Comandos

```
/criar-projeto app Angular de gestao de tarefas
/criar-projeto dashboard enterprise com Angular + Material
/criar-projeto app Angular standalone com Signals
/analisar-projeto --stack angular
```

## Quando Escalar para Nx

- Multi-app monorepo
- Compartilhamento de libraries entre apps
- Micro-frontends
- CI distribuido com affected commands

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `package.json` com `@angular/core`, `@angular/cli`, etc.
2. `angular.json` com build config
3. `tsconfig.json` estrito
4. `src/main.ts` com `bootstrapApplication`
5. `src/app/app.component.ts` (standalone)
6. `src/app/app.config.ts` (providers)
7. `src/app/app.routes.ts` (rotas raiz)
8. Features em `src/app/features/<feature>/`
9. Services em `src/app/core/services/`
10. Componentes shared em `src/app/shared/components/`
11. (Opcional) `src/environments/`
12. (Opcional) `src/styles.scss` com Tailwind
13. README com setup, scripts, convencoes
