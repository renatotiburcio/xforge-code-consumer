# Handoff Checklist - Personal Portfolio

## Handoff Approval

- **Documento**: sdd-personal-portfolio-2026-06-14
- **Stack detectado**: HTML+Tailwind standalone
- **Clarity score**: 95/100
- **Aprovador**: (a definir)
- **Data**: 2026-06-14

## Pre-Implementation

- [x] Brief completo (problema, objetivo, fora de escopo)
- [x] 5 RFs com IDs estaveis
- [x] 3 RNFs com metricas (perf >= 95, a11y >= 95, SEO = 100)
- [x] 2 RNS (editavel sem rebuild, links noopener)
- [x] 2 User Stories com Given-When-Then
- [x] C4 L1 com 4 nos
- [x] 2 diagramas (C4 + sequence)
- [x] Decisoes arquiteturais documentadas
- [x] OpenAPI 3.1 (mesmo sendo opcional)
- [x] Wireframes textuais de 3 telas
- [x] Estados por secao (loading, empty, error, success)
- [x] Plano de testes (htmlhint, tailwindcss-classnames, pa11y, Lighthouse)
- [x] LGPD: sem cookies, sem tracking (opcional Plausible)
- [x] Plano de rollback (git revert)
- [x] 3 gaps identificados com mitigacao

## Implementation

- [ ] `index.html` criado com semantic HTML
- [ ] Tailwind CDN configurado
- [ ] Mobile-first responsive
- [ ] WCAG 2.1 AA (contraste, focus, ARIA)
- [ ] Meta tags SEO completas
- [ ] `loading=lazy` em imagens
- [ ] Smooth scroll configurado

## Validation

- [ ] htmlhint 0 errors
- [ ] tailwindcss-classnames 0 errors
- [ ] pa11y 0 violations
- [ ] Lighthouse >= 95 (perf, a11y, best practices, SEO)
- [ ] Testado em mobile (DevTools, dispositivo real)
- [ ] W3C HTML validator clean

## Deploy

- [ ] GitHub Pages configurado (Settings > Pages > main branch)
- [ ] HTTPS funcionando
- [ ] Custom domain (opcional)
- [ ] README com URL publica

## Pos-Deploy

- [ ] Compartir URL no LinkedIn
- [ ] Adicionar URL no resume/CV
- [ ] Monitorar Google Search Console (opcional)
