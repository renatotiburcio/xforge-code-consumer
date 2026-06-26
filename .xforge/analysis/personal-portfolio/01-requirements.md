# Requirements - Personal Portfolio Landing Page

## Requisitos Funcionais (RF)

| ID | Titulo | Prioridade | Dependencia |
|----|--------|------------|-------------|
| RF-001 | Exibir hero section com nome, titulo profissional e CTA | P0 | - |
| RF-002 | Listar 6+ projetos com thumbnail, titulo, descricao, link | P0 | - |
| RF-003 | Exibir timeline de experiencia profissional | P0 | - |
| RF-004 | Secao de skills (tags visuais) | P1 | - |
| RF-005 | Secao de contato (mailto + LinkedIn + GitHub) | P0 | - |

## Requisitos Nao-Funcionais (RNF)

| ID | Titulo | Metrica | Criterio |
|----|--------|---------|----------|
| RNF-001 | Performance | Lighthouse Performance | >= 95 |
| RNF-002 | Acessibilidade | Lighthouse A11y + pa11y | >= 95, WCAG 2.1 AA |
| RNF-003 | SEO | Meta tags + JSON-LD | Lighthouse SEO >= 100 |

## Regras de Negocio (RN)

| ID | Titulo | Exemplo |
|----|--------|---------|
| RN-001 | Conteudo do portfolio deve ser editavel sem rebuild | Editar `index.html` direto |
| RN-002 | Links externos abrem em nova aba com `rel=noopener` | `<a target="_blank" rel="noopener">` |

## User Stories

### US-001 (Visitante) - Ver portfolio
- **Given** que o visitante acessa o site pela primeira vez
- **When** a pagina carrega
- **Then** o hero section aparece com nome, titulo e CTA "Ver Projetos"
- **And** a pagina carrega em < 2s (LCP)

### US-002 (Recrutador) - Avaliar skills
- **Given** que o recrutador quer validar skills rapido
- **When** ele rola ate a secao "Skills"
- **Then** ve tags visuais com tecnologias dominadas
- **And** clica em um projeto para ver detalhes
