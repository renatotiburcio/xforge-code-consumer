# Session Memory — XForge Engineer

## Visão Geral

Sistema de memória de longo prazo que persiste preferências, decisões e padrões do usuário entre sessões. Quando o usuário retorna, o sistema já conhece suas preferências e não precisa perguntar novamente.

## Ciclo Obrigatório de Memória

Todo workflow deve seguir este ciclo:

1. **memory-recover** — Recuperar memória relevante antes de agir
2. **memory-apply** — Aplicar preferências e decisões conhecidas
3. **task-execute** — Executar a tarefa
4. **memory-detect-learning** — Detectar se houve aprendizado
5. **memory-save** — Salvar aprendizado (se houver)
6. **memory-index** — Reindexar memória
7. **audit-trail** — Registrar na trilha de auditoria

## Aprender com Acertos

Salvar:
- problema encontrado
- solução aplicada
- arquivos afetados
- testes que passaram
- por que funcionou

## Aprender com Erros

Salvar:
- erro encontrado
- causa raiz
- tentativa que falhou
- correção final
- como evitar novamente

## Core Rules

1. Check `.xforge/memory/index.json` before reading deep memory files.
2. Check `.xforge/project-dna/PROJECT-DNA.md` for project identity and conventions.
3. Check `.xforge/decisions/ADR-INDEX.md` before changing architecture.
4. Check `.xforge/knowledge/INDEX.json` before opening large knowledge files.
5. Save memory only when the task creates learning that should influence future decisions.
6. Memory entries must include source, date, trust level and reason.
7. Sensitive memory must stay local and must not be sent to cloud providers.
8. Conflicting memory must be reported instead of silently overwritten.

## Do Not Save

- temporary command output
- obvious facts already visible in code
- speculative conclusions
- secrets, API keys, senhas, dados pessoais sensíveis
- noisy implementation details unlikely to matter later
- dumps de dados temporários

## Estrutura de Memória

```
.xforge/memory/
├── user-profile.json          ← Perfil do usuário (preferências, role, projetos)
├── session-history.json       ← Resumo das últimas 20 sessões
├── decisions-log.json         ← Decisões tomadas (tech choices, patterns)
├── preferences.json           ← Preferências explícitas e aprendidas
└── corrections.json           ← Correções do usuário (o que aceitou/recusou)
```

## 1. User Profile

```json
{
  "version": "1.0.0",
  "user": {
    "name": "Renato",
    "role": "Full-Stack Developer",
    "projects": ["XForge ERP"],
    "expertise": ["Brazilian fiscal", ".NET", "Blazor"],
    "preferredLanguage": "pt-BR"
  },
  "hardware": {
    "gpu": "16GB VRAM",
    "ram": "32GB DDR4",
    "cpu": "Ryzen 7 5700G"
  },
  "aiConfig": {
    "router": "qwen2.5:7b",
    "worker": "qwen2.5:72b",
    "contextBudget": 32768,
    "offlineFirst": true
  }
}
```

## 2. Preferences (Aprendidas)

O sistema aprende preferências implicitamente:

```json
{
  "version": "1.0.0",
  "learned": [
    {
      "id": "PREF-001",
      "category": "code-style",
      "preference": "Sempre usar XForge.MediatR, nunca MediatR oficial",
      "source": "user-correction",
      "confidence": 0.95,
      "learnedAt": "2026-06-11"
    },
    {
      "id": "PREF-002",
      "category": "code-style",
      "preference": "Sempre usar AutoMapper, nunca Mapster",
      "source": "user-correction",
      "confidence": 0.95,
      "learnedAt": "2026-06-11"
    },
    {
      "id": "PREF-003",
      "category": "workflow",
      "preference": "Sempre rodar testes antes de commit",
      "source": "observed-pattern",
      "confidence": 0.80,
      "learnedAt": "2026-06-11"
    },
    {
      "id": "PREF-004",
      "category": "output-format",
      "preference": "Gostar de tabelas comparativas no decision support",
      "source": "observed-pattern",
      "confidence": 0.70,
      "learnedAt": "2026-06-11"
    },
    {
      "id": "PREF-005",
      "category": "tech-choice",
      "preference": "Prefere PostgreSQL para produção, SQLite para dev",
      "source": "observed-pattern",
      "confidence": 0.85,
      "learnedAt": "2026-06-11"
    }
  ],
  "explicit": [
    {
      "id": "PE-001",
      "statement": "Nunca usar packages preview/alpha/beta",
      "category": "safety",
      "addedAt": "2026-06-10"
    },
    {
      "id": "PE-002",
      "statement": "Sempre atualizar docs/index.html após mudanças significativas",
      "category": "workflow",
      "addedAt": "2026-06-09"
    }
  ]
}
```

## 3. Decisions Log

```json
{
  "version": "1.0.0",
  "decisions": [
    {
      "id": "DEC-001",
      "date": "2026-06-11",
      "context": "Cache strategy for API",
      "options": ["Redis", "Memory", "Híbrido"],
      "chosen": "Híbrido",
      "reason": "Multi-instance production",
      "outcome": "positive"
    },
    {
      "id": "DEC-002",
      "date": "2026-06-10",
      "context": "Split architecture for local AI",
      "options": ["Single model 128k", "Router+Worker 32k"],
      "chosen": "Router+Worker 32k",
      "reason": "3-4x faster on CPU",
      "outcome": "positive"
    }
  ]
}
```

## 4. Session History

```json
{
  "version": "1.0.0",
  "sessions": [
    {
      "id": "ses_149cb291fffex4uVhCvhPzEoDM",
      "date": "2026-06-11",
      "summary": "Implementou 16 sistemas: Split arch, intelligent quality, interaction intelligence",
      "filesChanged": 25,
      "tasksCompleted": 27,
      "decisionsMade": 5,
      "keyLearnings": ["Split architecture is optimal for 16GB VRAM", "User wants all improvements implemented"]
    }
  ]
}
```

## Integração com o Agente

### No Início de Cada Sessão

```
1. Ler user-profile.json → saber quem é o usuário
2. Ler preferences.json → saber preferências aprendidas
3. Ler session-history.json → saber contexto das últimas sessões
4. Ler decisions-log.json → saber decisões anteriores
5. Aplicar preferências automaticamente (não perguntar o que já sabe)
```

### Durante a Sessão

```
- Quando usuário corrige o agente → registrar em preferences.json
- Quando usuário aceita sugestão → aumentar confidence da preferência
- Quando usuário recusa sugestão → diminuir confidence ou remover
- Quando tomada decisão → registrar em decisions-log.json
```

### No Fim de Cada Sessão

```
1. Salvar resumo da sessão em session-history.json
2. Atualizar preferências aprendidas
3. Registrar decisões tomadas
4. Salvar profile atualizado
```

## Métricas

| Métrica | Meta |
|---------|------|
| Perguntas que poderiam ser evitadas | Reduzir 40% |
| Preferências corretamente aprendidas | > 85% |
| Decisões consistentes com histórico | > 90% |
| Tempo de onboarding em nova sessão | < 5s |
