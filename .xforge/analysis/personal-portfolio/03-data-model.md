# Data Model - Personal Portfolio

## Sem Banco de Dados

Este eh um site estatico sem persistencia. Todos os dados estao hardcoded no HTML.

## "Modelos" (conteudo hardcoded)

### Profile
| Campo | Tipo | Exemplo |
|-------|------|---------|
| name | string | "Joao Silva" |
| title | string | "Full-Stack Developer" |
| bio | text | "10+ anos construindo..." |
| email | string (mailto) | "joao@example.com" |
| linkedin | string (URL) | "https://linkedin.com/in/joao" |
| github | string (URL) | "https://github.com/joao" |

### Project (x6+)
| Campo | Tipo | Exemplo |
|-------|------|---------|
| title | string | "ERP Multitenant" |
| description | text | "Sistema ERP modular com 6 dominios..." |
| tech | array<string> | ["Node.js", "PostgreSQL", "React"] |
| url | string (URL) | "https://github.com/joao/erp" |
| thumbnail | string (path) | "assets/projects/erp.png" |

### Experience (x3+)
| Campo | Tipo | Exemplo |
|-------|------|---------|
| role | string | "Senior Full-Stack Developer" |
| company | string | "Acme Corp" |
| period | string | "2020 - Atual" |
| description | text | "Lideranca tecnica de squad..." |
| stack | array<string> | ["React", "Node.js", "AWS"] |

## Atualizacao

Para adicionar/editar projetos ou experiencias: editar `index.html` direto (RN-001). Commit + push = deploy automatico.
