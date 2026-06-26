---
id: tailwind-css-completo
type: conhecimento
tags: [tailwind, css, utility-first, responsive, dark-mode, components, v4]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Tailwind CSS - Guia Completo
- **Seções principais**: Conceito, Setup, Layout, Responsividade
- **Tags**: tailwind, css, utility-first, responsive, dark-mode, components, v4
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tailwind-css-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# Tailwind CSS - Guia Completo

## Conceito

Tailwind CSS é um framework CSS utility-first que fornece classes prontas para estilização, eliminando a necessidade de escrever CSS customizado.

## Setup

### CDN (rápido)
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### npm
```bash
npm install -D tailwindcss
npx tailwindcss init
```

### Configuração
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#10b981',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

## Layout

### Flexbox
```html
<!-- Flex container -->
<div class="flex">Item 1 Item 2 Item 3</div>
<div class="flex justify-center items-center">Centered</div>
<div class="flex justify-between items-center">Space between</div>
<div class="flex flex-wrap gap-4">Wrapped with gap</div>

<!-- Flex items -->
<div class="flex-1">Grow</div>
<div class="flex-shrink-0">No shrink</div>
<div class="w-1/3">One third</div>
```

### Grid
```html
<!-- Grid container -->
<div class="grid grid-cols-3 gap-4">3 columns</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">Responsive</div>
<div class="grid grid-flow-col auto-cols-max">Auto columns</div>

<!-- Grid items -->
<div class="col-span-2">Span 2 columns</div>
<div class="row-span-2">Span 2 rows</div>
```

### Container
```html
<div class="container mx-auto px-4">Centered container</div>
<div class="max-w-7xl mx-auto">Max width container</div>
```

## Responsividade

### Breakpoints
| Prefixo | Largura | Exemplo |
|---------|---------|---------|
| (none) | < 640px | `text-sm` |
| `sm:` | ≥ 640px | `sm:text-base` |
| `md:` | ≥ 768px | `md:grid-cols-2` |
| `lg:` | ≥ 1024px | `lg:flex` |
| `xl:` | ≥ 1280px | `xl:container` |
| `2xl:` | ≥ 1536px | `2xl:text-2xl` |

### Exemplos
```html
<!-- Mobile-first -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <!-- 1 col mobile, 2 sm, 3 md, 4 lg -->
</div>

<!-- Show/hide -->
<div class="hidden md:block">Desktop only</div>
<div class="block md:hidden">Mobile only</div>

<!-- Padding responsivo -->
<div class="p-4 md:p-8 lg:p-12">Responsive padding</div>
```

## Tipografia

```html
<!-- Tamanhos -->
<h1 class="text-4xl font-bold">Title</h1>
<h2 class="text-2xl font-semibold">Subtitle</h2>
<p class="text-base">Body</p>
<small class="text-sm">Small</small>

<!-- Cores -->
<p class="text-gray-900">Dark text</p>
<p class="text-gray-500">Muted text</p>
<p class="text-blue-600">Link color</p>
<p class="text-red-500">Error text</p>

<!-- Alinhamento -->
<p class="text-left">Left</p>
<p class="text-center">Center</p>
<p class="text-right">Right</p>

<!-- Fonte -->
<p class="font-light">Light</p>
<p class="font-normal">Normal</p>
<p class="font-medium">Medium</p>
<p class="font-semibold">Semibold</p>
<p class="font-bold">Bold</p>
```

## Cores

### Background
```html
<div class="bg-white">White</div>
<div class="bg-gray-100">Light gray</div>
<div class="bg-blue-500">Blue</div>
<div class="bg-green-500">Green</div>
<div class="bg-red-500">Red</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-500">Gradient</div>
```

### Text
```html
<p class="text-black">Black</p>
<p class="text-white">White</p>
<p class="text-gray-600">Gray</p>
<p class="text-blue-500">Blue</p>
<p class="text-green-600">Green</p>
<p class="text-red-500">Red</p>
```

### Border
```html
<div class="border border-gray-300">Gray border</div>
<div class="border-2 border-blue-500">Blue thick border</div>
<div class="border-t border-gray-200">Top border only</div>
```

## Espaçamento

### Margin
```html
<div class="m-4">All sides 1rem</div>
<div class="mx-auto">Horizontal auto</div>
<div class="mt-8">Top 2rem</div>
<div class="mb-4">Bottom 1rem</div>
<div class="ml-2">Left 0.5rem</div>
<div class="mr-6">Right 1.5rem</div>
<div class="mx-4 my-2">Horizontal 1rem, vertical 0.5rem</div>
```

### Padding
```html
<div class="p-4">All sides 1rem</div>
<div class="px-6">Horizontal 1.5rem</div>
<div class="py-8">Vertical 2rem</div>
<div class="pt-4">Top 1rem</div>
<div class="pb-2">Bottom 0.5rem</div>
```

## Componentes

### Botões
```html
<!-- Básico -->
<button class="bg-blue-500 text-white px-4 py-2 rounded">Button</button>

<!-- Com hover -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Button
</button>

<!-- Outlined -->
<button class="border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white py-2 px-4 rounded">
  Outlined
</button>

<!-- Ghost -->
<button class="text-blue-500 hover:bg-blue-50 py-2 px-4 rounded">
  Ghost
</button>

<!-- Disabled -->
<button class="bg-gray-300 text-gray-500 cursor-not-allowed py-2 px-4 rounded" disabled>
  Disabled
</button>
```

### Cards
```html
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-xl font-semibold mb-2">Card Title</h3>
  <p class="text-gray-600 mb-4">Card content goes here.</p>
  <button class="bg-blue-500 text-white px-4 py-2 rounded">
    Action
  </button>
</div>
```

### Formulários
```html
<div class="space-y-4">
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
    <input type="text" 
           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
           placeholder="Enter name">
  </div>
  
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
    <input type="email" 
           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
           placeholder="Enter email">
  </div>
  
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Message</label>
    <textarea class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="4"></textarea>
  </div>
  
  <button class="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
</div>
```

### Tabelas
```html
<table class="min-w-full divide-y divide-gray-200">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    <tr>
      <td class="px-6 py-4 whitespace-nowrap">John Doe</td>
      <td class="px-6 py-4 whitespace-nowrap">john@example.com</td>
    </tr>
  </tbody>
</table>
```

### Modals
```html
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
  <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
    <h3 class="text-xl font-semibold mb-4">Modal Title</h3>
    <p class="text-gray-600 mb-6">Modal content here.</p>
    <div class="flex justify-end space-x-2">
      <button class="px-4 py-2 border rounded">Cancel</button>
      <button class="px-4 py-2 bg-blue-500 text-white rounded">Confirm</button>
    </div>
  </div>
</div>
```

## Dark Mode

```html
<!-- Configuração -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 class="dark:text-white">Title</h1>
  <p class="dark:text-gray-300">Content</p>
</div>

<!-- Toggle -->
<button id="theme-toggle" class="dark:hidden">🌙</button>
<button id="theme-toggle" class="hidden dark:block">☀️</button>
```

```javascript
// Toggle dark mode
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}
```

## Animações

```html
<!-- Transitions -->
<button class="transition duration-300 ease-in-out hover:bg-blue-700">Hover me</button>

<!-- Animate -->
<div class="animate-pulse">Loading...</div>
<div class="animate-spin">⏳</div>
<div class="animate-bounce">🔄</div>

<!-- Custom -->
<style>
@keyframes slide-in {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
.animate-slide-in { animation: slide-in 0.3s ease-out; }
</style>
```

## Utility Classes Essenciais

| Categoria | Classes |
|-----------|---------|
| Display | `block`, `inline`, `inline-block`, `flex`, `grid`, `hidden` |
| Position | `relative`, `absolute`, `fixed`, `sticky` |
| Overflow | `overflow-auto`, `overflow-hidden`, `overflow-scroll` |
| Z-index | `z-0`, `z-10`, `z-20`, `z-30`, `z-40`, `z-50` |
| Opacity | `opacity-0`, `opacity-50`, `opacity-100` |
| Shadow | `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl` |
| Rounded | `rounded`, `rounded-md`, `rounded-lg`, `rounded-full` |
| Cursor | `cursor-pointer`, `cursor-not-allowed`, `cursor-grab` |

## Fontes Oficiais
- tailwindcss.com
- tailwindcss.com/docs
- tailwindcss.com/components
