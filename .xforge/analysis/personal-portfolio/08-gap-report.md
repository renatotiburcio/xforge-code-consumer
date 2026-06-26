# Gap Report - Personal Portfolio

## Gaps Identificados

### Gap 1: Sem testes automatizados em CI
- **Descricao**: Nao ha GitHub Actions rodando Lighthouse + pa11y em cada PR
- **Impacto**: Medio - regressoes de performance/a11y nao sao detectadas
- **Mitigacao**: Adicionar `.github/workflows/lighthouse.yml` com budget enforcement
- **Esforco**: 2h

### Gap 2: Sem dark mode
- **Descricao**: Site so tem tema claro, muitos usuarios preferem dark
- **Impacto**: Baixo - portfolio pessoal, nao eh critico
- **Mitigacao**: Adicionar `dark:` variants do Tailwind + toggle
- **Esforco**: 1h

### Gap 3: Sem internacionalizacao
- **Descricao**: Hardcoded em pt-BR, recrutadores internacionais nao entendem
- **Impacto**: Baixo-Medio - reduz alcance
- **Mitigacao**: i18n via vanilla JS ou migrar para Astro (multi-idioma nativo)
- **Esforco**: 4h (vanilla) ou migrar projeto (1 dia)

## Nao-Gaps (decisoes explicitas)

- **Sem backend**: Decisao arquitetural (zero ops, zero custo)
- **Sem CMS**: Decisao arquitetural (RN-001: editar HTML direto)
- **Sem testes E2E**: Site de 1 pagina, visual review manual eh suficiente
- **Sem SSR/SSG**: Tailwind CDN + GitHub Pages eh estatico por definicao
