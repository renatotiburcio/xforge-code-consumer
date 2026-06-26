# Research-Document-Execute Rules — ENFORCEMENT

## Visão Geral

Sistema de duas fases com LOOP OBRIGATÓRIO:
- **Fase 1 (/research)**: Análise com IA robusta → gera 7 arquivos padronizados
- **Fase 2 (/document-execute)**: Execução com IA local → loop automático até completar

---

## FASE 1: /research — Análise Padronizada

### Obrigatório
1. Ler fontes (URL → playwright-mcp, pasta → read, PDF → pdf skill)
2. Gerar EXATAMENTE 7 arquivos em `.xforge/project/`:
   - BACKLOG.md, SPRINTS.md, ROADMAP.md, ARCHITECTURE.md, DECISIONS.md, STATUS.md, TASKS/
3. Formato: tabelas + listas (nunca parágrafos)
4. Economia: 500 tokens por fonte, 5000 tokens total

### Validação
- [ ] Todos os 7 arquivos foram criados
- [ ] BACKLOG.md tem tarefas P0-P3
- [ ] Cada tarefa tem ID, título, passos, critérios
- [ ] Nenhum arquivo excede 500 tokens

---

## FASE 2: /document-execute — Loop Obrigatório

### FLUXO (seguir EXATAMENTE esta ordem)

```
INÍCIO:
  1. Ler BACKLOG.md + STATUS.md
  2. Verificar checkpoint em .xforge/checkpoints/document-execute.json
  3. Se checkpoint existe → retomar de lá
  4. Se não existe → começar do P0 mais alto

LOOP:
  1. Selecionar próxima tarefa P0 ou P1 pendente
  2. Ler TASKS/TXXX-nome.md
  3. Executar TODOS os passos
  4. Validar TODOS os critérios de aceite
  5. Se falhar → retry 3x → se ainda falhar → blocked
  6. Marcar tarefa como "done" no BACKLOG.md
  7. Salvar checkpoint
  8. VOLTA AO INÍCIO DO LOOP (próxima tarefa)

FIM (apenas quando):
  - TODAS as tarefas P0 e P1 estão "done"
  - OU usuário explicitamente pede para parar
```

### REGRAS INEGOCIÁVEIS

| # | Regra | Violação = falha |
|---|-------|-----------------|
| 1 | **NUNCA PARAR** até P0+P1 completos | Agente falhou |
| 2 | **CHECKPOINT após cada tarefa** | Perde progresso |
| 3 | **CONTINUAR sem perguntar** | Fica travado |
| 4 | **UMA tarefa por vez** | Código bagunçado |
| 5 | **VALIDAR antes de avançar** | Erros propagam |

### Gestão de Contexto

```
Se contexto > 80%:
  1. Salvar checkpoint COMPLETO
  2. Resumir: "Completei T001-T005, 5/20"
  3. Carregar APENAS checkpoint + próxima tarefa
  4. CONTINUAR

Se contexto > 95%:
  1. Salvar checkpoint
  2. Informar: "Checkpoint salvo. Envie qualquer mensagem para retomar."
  3. PARAR (único caso permitido de parar)

Retomada:
  1. Verificar se .xforge/checkpoints/document-execute.json existe
  2. Se existe → ler checkpoint → retomar de onde parou
  3. NÃO recomeçar do zero
```

### Checkpoint Format

```json
{
  "lastTaskCompleted": "T005",
  "completedTasks": ["T001", "T002", "T003", "T004", "T005"],
  "nextTask": "T006",
  "blockedTasks": [],
  "stats": {"total": 20, "done": 5, "pending": 14, "blocked": 1},
  "timestamp": "2026-06-12T10:00:00Z"
}
```

---

## Validação Final

Após cada tarefa:
- [ ] Critérios de aceite: TODOS passaram
- [ ] Build: compila sem erros
- [ ] Testes: existentes continuam passando
- [ ] Padrões: projeto seguidos
- [ ] Checkpoint: salvo
- [ ] BACKLOG.md: status atualizado
- [ ] CONTINUAÇÃO: próxima tarefa selecionada
