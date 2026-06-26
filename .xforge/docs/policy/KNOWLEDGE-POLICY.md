# Política de Conhecimento XForge

## 1. Objetivo

Definir claramente **onde cada tipo de informação deve viver** no template XForge, evitando duplicação, confusão e degradação da base de conhecimento.

## 2. Princípio Fundamental

> **Conhecimento sem política vira ruído. Ruído gera decisões ruins.**

Cada informação tem **um lugar certo**, **um formato certo** e **um ciclo de vida certo**.

---

## 3. Mapa de Decisão Rápido

```
Nova informação
│
├─ É uma restrição operacional obrigatória?
│  └─ SIM → .kilo/rules/
│
├─ É uma capacidade executável com workflow próprio?
│  └─ SIM → .kilo/skills/
│
├─ É um fato persistente sobre o projeto/decisão/preferência?
│  └─ SIM → .xforge/memory/
│
├─ É conhecimento reutilizável e explicativo (como fazer, por quê)?
│  └─ SIM → .xforge/knowledge/
│
├─ É uma decisão arquitetural com contexto e consequências?
│  └─ SIM → .xforge/decisions/ (ADR)
│
├─ É a identidade estável do projeto?
│  └─ SIM → .xforge/project-dna/PROJECT-DNA.md
│
└─ É trabalho planejado (tarefa/objetivo/entrega)?
   └─ SIM → .xforge/backlog/ ou .xforge/sprints/ ou .xforge/roadmap/
```

---

## 4. O Que Entra em Cada Camada

### 4.1 `.kilo/rules/` — Regras Operacionais

**Natureza:** Restrições obrigatórias. O que **deve** ou **não deve** ser feito.

**Formato:** `.md` com lista de regras claras, sem ambiguidade.

**Exemplos:**
- "Nunca colocar connection string hardcoded"
- "Todo PR deve ter review antes do merge"
- "Usar Fluent API para configurações complexas no EF Core"
- "Não usar `async void` exceto em event handlers"

**Ciclo de vida:** Regras são atualizadas quando práticas mudam. Regras antigas são removidas ou marcadas como deprecated.

**Quando criar:** Quando um padrão se torna obrigatório após validação.

**Quando NÃO usar:** Para conhecimento explicativo (→ knowledge) ou para fatos sobre o projeto (→ memory).

---

### 4.2 `.kilo/skills/` — Capacidades Executáveis

**Natureza:** Workflows com passos definidos que um agente pode executar.

**Formato:** `.md` com objetivo, quando usar, passos de execução, saída esperada.

**Exemplos:**
- `efcore-migrations` — Workflow completo para criar/revisar/aplicar migrations
- `stryker-mutation-testing` — Workflow para configurar e interpretar mutation tests
- `lgpd-compliance-check` — Workflow para verificar conformidade LGPD

**Ciclo de vida:** Skills são promovidas de `draft` → `validated` → `promoted`. Skills sem uso são arquivadas.

**Quando criar:** Quando um procedimento se repete e pode ser padronizado.

**Quando NÃO usar:** Para conhecimento estático (→ knowledge) ou para regras simples (→ rules).

---

### 4.3 `.xforge/knowledge/` — Conhecimento Reutilizável

**Natureza:** Conteúdo explicativo, referencial, "como fazer" e "por quê". Conhecimento que pode ser consultado por qualquer agente a qualquer momento.

**Formato:** `.md` com estrutura clara (Quando usar, Regras, Exemplos, Referências).

**Subdivisões:**
- `.xforge/knowledge/packs/` — Knowledge packs por domínio técnico (dotnet, efcore, blazor, etc.)
- `.xforge/knowledge/<dominio>/` — Conhecimento específico do projeto organizado por área

**Exemplos:**
- "EF Core — Padrões de Migração" (como estruturar, revisar e aplicar migrations)
- "Blazor — Padrões de Estado" (como gerenciar estado em componentes)
- "PostgreSQL — Índices e Performance" (quando criar índices, tipos, análise de query plan)

**Ciclo de vida:** Conhecimento é versionado. Quando fica desatualizado, recebe marcação de `deprecated` e é substituído.

**Fontes oficiais:** Sempre preferir documentação oficial (Microsoft Learn, documentação do PostgreSQL, etc.)

**Quando criar:** Quando o conhecimento é reutilizável em múltiplos contextos e projetos.

**Quando NÃO usar:** Para fatos específicos do projeto atual (→ memory) ou para regras obrigatórias (→ rules).

---

### 4.4 `.xforge/memory/` — Memória Persistente do Projeto

**Natureza:** Fatos persistentes, decisões tomadas, preferências, contexto vivo. O que o sistema "sabe" sobre o projeto.

**Formato:** `.md` com data, contexto, decisão e consequências.

**Subdivisões:**
- `project-preferences.md` — Preferências técnicas e de processo
- `known-decisions.md` — Decisões tomadas com contexto
- `current-context.md` — Contexto vivo (o que está acontecendo agora)
- `known-errors.md` — Erros conhecidos e soluções
- `business-rules.md` — Regras de negócio do domínio

**Exemplos:**
- "Decidido usar PostgreSQL em vez de MySQL para o módulo fiscal (2026-06-01)"
- "Preferência: RAG lexical local é obrigatório, embeddings são opcionais"
- "Erro conhecido: EF Core migration falha com SQLite em ambiente de teste"

**Ciclo de vida:** Memória nunca é deletada. Informações desatualizadas são movidas para seções de histórico com marcação de `superseded`.

**Quando criar:** Após cada decisão, descoberta ou mudança de contexto relevante.

**Quando NÃO usar:** Para conhecimento reutilizável genérico (→ knowledge) ou para regras operacionais (→ rules).

---

### 4.5 `.xforge/decisions/` — Decisões Arquiteturais (ADRs)

**Natureza:** Decisões arquiteturais significativas com contexto completo, alternativas consideradas e consequências.

**Formato:** `.md` seguindo template ADR (Architecture Decision Record).

**Estrutura:**
```markdown
# ADR-XXXX: [Título]

## Status
proposed | accepted | deprecated | superseded

## Contexto
[O que levou a esta decisão]

## Decisão
[O que foi decidido]

## Alternativas Consideradas
[O que foi avaliado e por quê não foi escolhido]

## Consequências
[Impacto positivo e negativo]

## Fontes
[Referências oficiais que embasaram a decisão]
```

**Ciclo de vida:** `proposed` → `accepted` → `deprecated` (quando substituída) | `superseded` (quando versão nova existe).

**Quando criar:** Quando uma decisão arquitetural significativa é tomada (escolha de tecnologia, padrão, estrutura).

---

### 4.6 `.xforge/project-dna/` — DNA do Projeto

**Natureza:** Identidade estável do projeto. O que define o projeto em uma frase.

**Formato:** `.md` preenchido durante `/analisar-projeto`.

**Conteúdo:**
- Nome do projeto
- Domínio de negócio
- Stack tecnológico
- Arquitetura
- Módulos
- Data stores
- Frontend
- Testes
- CI/CD
- Restrições de segurança
- Convenções de código
- Riscos conhecidos

**Ciclo de vida:** Atualizado quando a identidade do projeto muda significativamente.

---

### 4.7 `.xforge/backlog/` — Backlog

**Natureza:** Lista priorizada de trabalho pendente.

**Formato:** `.md` com itens priorizados.

---

### 4.8 `.xforge/sprints/` — Sprints

**Natureza:** Planejamento de sprints com objetivos e entregas.

**Formato:** `.md` por sprint.

---

### 4.9 `.xforge/roadmap/` — Roadmap

**Natureza:** Visão estratégica de médio/longo prazo.

**Formato:** `.md` com fases e marcos.

---

## 5. Matriz de Decisão Detalhada

| Informação | Local | Formato | Ciclo de Vida |
|---|---|---|---|
| Restrição obrigatória | `.kilo/rules/` | Lista de regras | Atualizada/removida |
| Workflow executável | `.kilo/skills/` | Passos + saída | draft → promoted |
| Conhecimento explicativo | `.xforge/knowledge/` | Como fazer + referências | Versionado |
| Fato do projeto | `.xforge/memory/` | Data + contexto + decisão | Nunca deletado |
| Decisão arquitetural | `.xforge/decisions/` | ADR completo | proposed → accepted |
| Identidade do projeto | `.xforge/project-dna/` | DNA estável | Atualizado raramente |
| Trabalho planejado | `.xforge/backlog/` | Lista priorizada | Sprint a sprint |
| Planejamento sprint | `.xforge/sprints/` | Objetivos + entregas | Sprint a sprint |
| Visão estratégica | `.xforge/roadmap/` | Fases + marcos | Trimestral |

---

## 6. Regras de Qualidade

### 6.1 Todo conhecimento deve ter:
- **Título claro** — sem ambiguidade
- **Data de criação** — para rastreabilidade
- **Fonte** — de onde veio (URL oficial, decisão, experiência)
- **Status** — draft, validated, promoted, deprecated
- **Estrutura consistente** — seguir o template do tipo

### 6.2 Proibições:
- Nunca duplicar informação entre camadas
- Nunca colocar segredos (API keys, passwords) em knowledge ou memory
- Nunca usar knowledge para regras obrigatórias (→ rules)
- Nunca usar memory para conhecimento genérico (→ knowledge)

---

## 7. Fluxo de Ingestão

Veja o guia completo em `.xforge/docs/ingestion/INGESTION-GUIDE.md`.

---

## 8. Histórico

| Data | Versão | Mudança |
|------|--------|---------|
| 2026-06-08 | 1.0.0 | Criação inicial da política |
