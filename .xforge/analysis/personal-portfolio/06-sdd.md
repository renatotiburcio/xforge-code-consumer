# SDD - Personal Portfolio Landing Page

## 1. Metadata
- **ID**: SDD-personal-portfolio-2026-06-14
- **Autor**: XForge Engineer (fullstack-analysis-architect)
- **Data**: 2026-06-14
- **Versao**: 1.0.0
- **Status**: Draft
- **Stack**: HTML+Tailwind standalone

## 2. Context
Portfolio pessoal para profissionais de tecnologia divulgarem seu trabalho. Substitui dependencia de plataformas SaaS pagas (Wix, Squarespace) por um arquivo HTML estatico que pode ser hospedado gratuitamente em GitHub Pages.

## 3. Personas & Cenarios
(ver 00-brief.md para detalhes completos)

## 4. Requisitos
(ver 01-requirements.md)

## 5. Arquitetura
(ver 02-architecture.md para C4 L1)

Stack: HTML+Tailwind (CDN), sem build, sem backend.

## 6. Modelo de Dados
(ver 03-data-model.md)

Sem DB. Conteudo hardcoded.

## 7. API Contract
(ver 04-api-contract.yaml)

Sem API backend propria. Opcional: Formspree para form.

## 8. UI/UX
(ver 05-ui-flows.md para wireframes)

4 secoes: Hero, Projetos, Experiencia, Contato. Mobile-first. WCAG 2.1 AA.

## 9. Testes

| Tipo | Cobertura | Ferramenta |
|------|-----------|------------|
| HTML lint | 100% | htmlhint |
| Tailwind classes | 100% | tailwindcss-classnames |
| Accessibility | 100% | pa11y-ci + axe-core |
| Performance | n/a (manual) | Lighthouse |
| Visual regression | optional | Percy/Playwright |

## 10. Observabilidade

N/A para site estatico. Pode-se usar:
- Google Analytics (privacy-friendly: Plausible)
- GitHub Pages deployment status

## 11. Seguranca & LGPD

- Sem coleta de dados
- Form (se Formspree): LGPD compliant via DPA do Formspree
- Sem cookies
- Sem third-party tracking (opcional Plausible)

## 12. Plano de Entrega

### Fase 1 (v1.0.0) - 1 dia
- [ ] `index.html` completo
- [ ] README com instrucoes
- [ ] Deploy GitHub Pages
- [ ] Lighthouse >= 95

### Fase 2 (v1.1.0) - opcional
- [ ] Form com Formspree
- [ ] Adicionar 3+ projetos reais
- [ ] Screenshots reais dos projetos

### Rollback

Site estatico = trivial. `git revert` ou push de versao anterior.

### Riscos
- Risco baixo (1 arquivo, sem deps)
- Dependencia externa: Tailwind CDN (mitigacao: usar build local se cair)
