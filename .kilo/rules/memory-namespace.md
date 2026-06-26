---
id: memory-namespace
priority: high
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-21
updated: 2026-06-21
related-rules: [01-xforge-golden-rules, 02-genius-council-framework, knowledge-rules, session-memory, project-recognition]
related-dr: [DR-0180, DR-0034, DR-0052, DR-0130]
---

# Memory Namespace Rule (DR-0180)

> **Precedencia**: amplifica `session-memory.md` e `knowledge-rules.md`. Quando em conflito, esta regra vence para casos cross-project.

## 1. Mandato

Toda memoria, knowledge e learning do `.xforge/` DEVE ser:

1. **Escopada por projeto** (active project context)
2. **Stack-aware** (aplicabilidade por stack)
3. **Auditavel** (origem, confianca, TTL)
4. **Isolada** entre projetos por default
5. **Promovivel** cross-project apenas via DR + human approval

## 2. Por que existe

Sistemas complexos falham quando:

- Memoria cross-project vaza contexto de um cliente/projeto para outro
- Knowledge .NET e injetado em projeto Python (vies)
- Learning de um teste se torna "preferencia global" sem validacao
- Project DNA mente sobre o stack (falso positivo: ferramenta != projeto)

Esta regra institucionaliza **isolation by default, sharing by exception**.

## 3. As 3 camadas de memoria (Fase 2 - Bounded Contexts)

```
.xforge/memory/
  _template/         # read-only, base canonica do template (encoding, formato, idioma)
  _user/             # preferencias cross-project do usuario (Renato, PT-BR, OpenRouter)
  _project/<id>/     # estado do projeto ativo (stack, conventions, learning)
```

**Fase 1 (atual)**: separa logicamente via `project-preferences.md` vs `current-context.md` vs `user-profile` (em JSON).

**Fase 2 (futuro)**: filesystem com 3 diretorios.

## 4. Stack-aware Knowledge (applicabilityScope)

Toda entry em `.xforge/knowledge/INDEX.json` DEVE ter campo `applicabilityScope`:

| Valor | Significado | Exemplo |
|-------|-------------|---------|
| `["*"]` | Universal (default) | clean-architecture.md, lgpd.md |
| `["dotnet"]` | Apenas projetos .NET | xforge-mediatr, automapper, blazor-* |
| `["python"]` | Apenas Python | fastapi-patterns, pydantic-v2 |
| `["node"]` | Apenas Node | express-patterns, prisma-orm |
| `["fiscal"]` | Apenas dominio fiscal | nfe-playbooks, sped-icms |
| `["contabil"]` | Apenas contabil | ecd, plano-contas |

**Regra**: router filtra entries com `applicabilityScope` nao compativel com o stack do projeto ativo. Entries com `["*"]` sao sempre carregadas.

## 5. Project DNA Authority

Apenas 1 fonte da verdade para o stack do projeto:

- `.xforge/project-dna/PROJECT-DNA.md` (gerado por `purify.ps1`)
- `.xforge/memory/project-preferences.md` (gerado por `purify.ps1`)

**Proibido** outros arquivos declararem stack:
- `kilo.jsonc` (config, nao DNA)
- `AGENTS.md` (instrucoes, nao DNA)
- `learning.jsonl` (preferencias, nao DNA)

## 6. Cross-project Learning - politica estrita

| Acao | Permitido? | Condicao |
|------|-----------|----------|
| Learning de projeto A afeta projeto B (mesma sessao) | NAO | sempre isolado |
| Learning consolidado cross-project | APENAS via DR | human review obrigatorio |
| Knowledge compartilhado | APENAS via `applicabilityScope: ["*"]` | review + source canonica |
| User preference compartilhada | SIM | e cross-project por natureza |
| Stack detection result | APENAS projeto ativo | nunca vaza |

## 7. Template/Consumer separation (Fase 0)

Quando o usuario clona o template XForge:

- **NÃO** deve herdar audit, decisions internas, sessions, learning do time
- **DEVE** herdar apenas: `.kilo/`, scripts de manutencao, manifest, knowledge INDEX, decisoes canonicas
- **`xforge init --consumer`** aplica esse reset
- **`xforge reset memory`** aplica em projeto ja clonado
- **Manifesto**: `.xforge/template-only.json` declara o que e template-only

## 8. Compliance LGPD

Memoria isolada por projeto reduz risco de:

- Vazamento de dados pessoais entre clientes
- Cross-contamination de segredos comerciais
- Exposição indevida em logs/audits

**Obrigatorio**: `learning.jsonl` NAO deve conter dados pessoais. Se capturar, deve ser sanitizado antes de salvar.

## 9. Enforcement

| Momento | Verificacao | Ferramenta |
|---------|-------------|------------|
| Pre-commit | Project DNA coerente com stack detectado | `purify.ps1` |
| Pre-push | Knowledge INDEX tem `applicabilityScope` | validator |
| Pre-merge | Memory namespace respeitado | doctor.ps1 |
| Sprint review | Cross-project learning justificado | DR audit |
| User clone | Template/consumer separation aplicada | `init-consumer.ps1` |

## 10. Quando NAO aplicar

- Knowledge canonica do template (encoding, idioma) - sempre compartilhada
- User preferences do Renato (cross-project) - sempre compartilhada
- Documentacao de rules/skills do template - sempre compartilhada
- ADRs que regem o template (DR-0001..0006, DR-0180) - sempre compartilhados

## 11. Referencias

- DR-0180 - Stack-Aware Context + Memory Namespace (este design)
- DR-0034 - Multi-Stack Architecture (stack-agnostic base)
- DR-0052 - Bounded Contexts (DDD)
- DR-0130 - Knowledge Router auto-update
- Regra `01-xforge-golden-rules.md` - Regra 0 stack-agnostic
- Regra `session-memory.md` - ciclo de memoria
- Regra `knowledge-rules.md` - trust score + origem
- Regra `curation-rules.md` - dedup + compressao
- Regra `project-recognition` (skill) - deteccao de projeto
- Skill `stack-aware-context/SKILL.md` - filtragem por stack


## 13. Template Mode vs Consumer Mode (DR-0211)

O sistema XForge tem dois modos distintos que afetam como a memoria e o git sao gerenciados:

### Template Mode
- Voce esta no repo XForge-Development-New e quer evoluir o template
- .git remote aponta para https://github.com/renatotiburcio/xforge-enterprise-development-os.git
- Use git pull/push normalmente
- Paths template-only estao presentes (audit, decisions, sessions, learning, backlog, roadmap, sprints)

### Consumer Mode
- Voce clonou o template para criar um projeto
- Use .xforge/scripts/init-project.ps1 para separar do template
- O script remove .git, cria novo repo, purifica memory, remove template-only paths
- O foco e o projeto, nao o template

### Regra
- Nunca faca git push em um consumer sem antes rodar init-project.ps1
- Nunca edite paths template-only em um consumer
- Sempre use init-project.ps1 ao clonar para um novo projeto

Ver: DR-0211, .xforge/template-only.json (secao modes)
## 12. TL;DR

| Quando | O que fazer |
|--------|-------------|
| Criar knowledge entry | adicionar `applicabilityScope` |
| Salvar learning | verificar se e user-level ou project-level |
| Detectar projeto | usar `stack-detector.ps1`, nao chutar |
| Operar em projeto | carregar apenas knowledge compativel |
| Clone do template | aplicar `init-consumer.ps1` ou `reset-memory.ps1` |
| Cross-project learning | abrir DR + human review |

