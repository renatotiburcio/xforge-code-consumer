# Guia de Ingestão de Conhecimento

## 1. Objetivo

Explicar **como alimentar o RAG e a memória** do XForge de forma prática e repetível.

## 2. Visão Geral do Fluxo

```
Você tem informação nova
│
├─ É um arquivo? → Coloque em .xforge/knowledge/<dominio>/
├─ É uma URL? → Coloque em .xforge/knowledge-inbox/urls/
├─ É um repositório? → Coloque em .xforge/knowledge-inbox/repositories/
├─ É legado? → Coloque em .xforge/knowledge-inbox/legacy-engineers/
│
Rode: .\.kilo\automation\scripts\rag\index-local.ps1
│
Consulte: .\.kilo\automation\scripts\rag\query-local.ps1 -Query "..." -Top 5
```

---

## 3. Como Adicionar Conhecimento

### 3.1 Conhecimento de Domínio Técnico

**Onde:** `.xforge/knowledge/<dominio>/`

**Estrutura de arquivo:**

```markdown
# [Título do Conhecimento]

## Fonte
[URL oficial ou referência]

## Quando usar
[Em que situações este conhecimento se aplica]

## Regras
- Regra 1
- Regra 2

## Exemplos
[Código ou exemplos práticos]

## Referências
- [Link 1](url)
- [Link 2](url)
```

**Exemplo de caminho:**
- `.xforge/knowledge/dotnet/efcore-migrations.md`
- `.xforge/knowledge/kilocode/uso-operacional.md`
- `.xforge/knowledge/projeto/regras-negocio.md`

### 3.2 Conhecimento de Fonte Externa (URL)

**Passo 1:** Crie um arquivo em `.xforge/knowledge-inbox/urls/` com o conteúdo extraído.

**Passo 2:** Processe para `.xforge/knowledge/<dominio>/`.

**Passo 3:** Reindexe.

### 3.3 Conhecimento de Repositório

**Passo 1:** Clone ou copie para `.xforge/knowledge-inbox/repositories/`.

**Passo 2:** Extraia documentação relevante.

**Passo 3:** Processe para `.xforge/knowledge/<dominio>/`.

**Passo 4:** Reindexe.

---

## 4. Como Adicionar Memória

### 4.1 Preferências do Projeto

**Onde:** `.xforge/memory/project-preferences.md`

**Quando:** Após decisões sobre stack, padrões ou processo.

### 4.2 Decisões Conhecidas

**Onde:** `.xforge/memory/known-decisions.md`

**Quando:** Após cada decisão técnica ou de negócio relevante.

### 4.3 Contexto Atual

**Onde:** `.xforge/memory/current-context.md`

**Quando:** Quando o contexto do projeto muda (nova fase, novo módulo, mudança de prioridade).

### 4.4 Erros Conhecidos

**Onde:** `.xforge/memory/known-errors.md`

**Quando:** Após resolver um erro recorrente ou difícil.

### 4.5 Regras de Negócio

**Onde:** `.xforge/memory/business-rules.md`

**Quando:** Ao descobrir ou confirmar uma regra de negócio do domínio.

---

## 5. Como Criar um ADR

**Onde:** `.xforge/decisions/ADR-XXXX-titulo.md`

**Template:**

```markdown
# ADR-XXXX: [Título Curto]

## Status
accepted

## Data
YYYY-MM-DD

## Contexto
[Por que esta decisão foi necessária. Qual problema estava sendo resolvido.]

## Decisão
[O que foi decidido. Seja específico e direto.]

## Alternativas Consideradas
- **Alternativa 1:** [Descrição] — [Por que não foi escolhida]
- **Alternativa 2:** [Descrição] — [Por que não foi escolhida]

## Consequências
- **Positivas:** [Impacto positivo]
- **Negativas:** [Impacto negativo ou trade-off aceito]

## Fontes
- [Referência oficial 1](url)
- [Referência oficial 2](url)
```

---

## 6. Como Reindexar

Após adicionar qualquer conhecimento ou memória:

```powershell
cd terminal
.\.kilo\automation\scripts\rag\index-local.ps1
```

Para verificar o que foi indexado:

```powershell
.\.kilo\automation\scripts\rag\report-index.ps1
```

Para consultar:

```powershell
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "sua pergunta" -Top 5
```

Para consultar por tipo:

```powershell
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "ef core migrations" -Top 5 -SourceType knowledge
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "decisao terminal" -Top 5 -SourceType memory
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "regra connection string" -Top 5 -SourceType rules
```

---

## 7. Tipos de Source-Type no RAG

| Source-Type | Pasta | Peso | Trust |
|-------------|-------|------|-------|
| commands | `.kilo/commands/` | 1.25 | high |
| rules | `.kilo/rules/` | 1.20 | high |
| project-dna | `.xforge/project-dna/` | 1.25 | high |
| memory | `.xforge/memory/` | 1.20 | high |
| agents | `.kilo/agents/` | 1.15 | high |
| skills | `.kilo/skills/` | 1.10 | high |
| official | `.xforge/engineer/official-knowledge-seeds/` | 1.20 | high |
| knowledge | `.xforge/knowledge/` | 1.00 | medium |
| engineer-docs | `.xforge/engineer/` | 0.95 | medium |
| root-docs | `AGENTS.md`, `README.md`, `.xforge/docs/INSTALL.md` | 1.00 | high |
| unknown | qualquer outro | 0.75 | low |

---

## 8. Boas Práticas

1. **Escreva para ser encontrado** — use termos que você usaria para buscar
2. **Cite fontes oficiais** — sempre que possível, referencie documentação oficial
3. **Seja específico** — "EF Core migrations com PostgreSQL" é melhor que "banco de dados"
4. **Atualize, não acumule** — se conhecimento ficou desatualizado, atualize ou marque como deprecated
5. **Reindexe sempre** — conhecimento sem índice é conhecimento perdido
6. **Use o source-type certo** — ajuda a filtrar resultados relevantes

---

## 9. Troubleshooting

| Problema | Solução |
|----------|---------|
| RAG não encontra informação | Verifique se reindexou após adicionar. Verifique se o arquivo está nas fontes do config.json |
| Resultados irrelevantes | Use filtro por source-type. Reformule a query com termos mais específicos |
| Índice corrompido | Rode `clear-index.ps1` e depois `index-local.ps1` |
| Segredo detectado | O chunk com segredo é automaticamente removido. Verifique `secret-scan-report.md` |
