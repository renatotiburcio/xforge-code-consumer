# Checkpoint & Resume — XForge Engineer

## Visão Geral

Quando o contexto atinge o limite mesmo após compactação, o agente salva um **checkpoint** com o estado completo da tarefa e continua em uma nova sessão. Isso permite tarefas ilimitadas que excedem qualquer janela de contexto.

## O Problema

```
Tarefa grande → Contexto enche → Compactação automática → Ainda enche → PARA ❌
```

## A Solução

```
Tarefa grande → Contexto enche → Salva checkpoint → Nova sessão → Retoma → Continua ✅
```

## Como Funciona

### 1. Detecção de Limite

Quando o contexto atinge 95% (ou quando o agente percebe que não pode continuar):

```
⚠️ Context limit approaching. Saving checkpoint...
```

### 2. Salvar Checkpoint

O checkpoint contém:
```json
{
  "taskId": "criar-modulo-fiscal",
  "status": "in_progress",
  "progress": "60%",
  "completedSteps": [
    "Criar entidades (FiscalEntry, FiscalRule)",
    "Criar services (FiscalService, TaxCalculator)",
    "Criar endpoints CRUD"
  ],
  "currentStep": "Criar validações FluentValidation",
  "remainingSteps": [
    "Criar testes unitários",
    "Criar testes de integração",
    "Adicionar documentação Swagger",
    "Rodar quality gates"
  ],
  "context": {
    "filesCreated": ["FiscalEntry.cs", "FiscalRule.cs", "FiscalService.cs"],
    "filesModified": ["AppDbContext.cs", "Program.cs"],
    "decisionsMade": ["Usar XForge.MediatR", "PostgreSQL como banco"],
    "errors": [],
    "knowledgeUsed": ["dominios/fiscal/nfe.md", "dominios/fiscal/efd-icms-ipi.md"]
  },
  "timestamp": "2026-06-11T15:30:00Z",
  "sessionOrigin": "ses_149cb291fffex4uVhCvhPzEoDM"
}
```

### 3. Nova Sessão — Retomada

O agente detecta checkpoint pendente e pergunta:

```
📋 Checkpoint encontrado: criar-modulo-fiscal (60% completo)

Próximo passo: Criar validações FluentValidation

Retomar de onde parou? (sim/não/ver detalhes)
```

### 4. Continuação

O agente retoma exatamente de onde parou, com contexto mínimo:
- Lê apenas o checkpoint
- Lê os arquivos relevantes para o próximo passo
- Continua a execução

## Formato do Checkpoint

### Arquivo
```
.xforge/checkpoints/<task-id>.json
```

### Estrutura
```json
{
  "version": "1.0.0",
  "taskId": "string",
  "status": "in_progress | blocked | completed",
  "progress": "percentage",
  "completedSteps": ["step1", "step2"],
  "currentStep": "step3",
  "remainingSteps": ["step4", "step5"],
  "context": {
    "filesCreated": [],
    "filesModified": [],
    "decisionsMade": [],
    "errors": [],
    "knowledgeUsed": []
  },
  "timestamp": "ISO 8601",
  "sessionOrigin": "session_id"
}
```

## Regras

1. **Sempre salvar checkpoint** quando contexto atingir 90%+
2. **Checkpoint mínimo**: pelo menos 1 checkpoint a cada 30 minutos de trabalho
3. **Retomada automática**: Se há checkpoint pendente, retomar automaticamente (não perguntar)
4. **Limite de retomadas**: Máximo 10 retomadas por tarefa (depois, reavaliar abordagem)
5. **Limpeza**: Checkpoints completados são arquivados em `.xforge/checkpoints/archive/`

## Integração com Split Architecture

### Router Layer (gemma4-26b)
- Detecta: "retomar tarefa" ou "continuar de onde parou"
- Classifica: needsWorker = true
- Carrega checkpoint automaticamente

### Worker Layer (qwen3-coder-30b)
- Lê checkpoint
- Retoma execução
- Salva novo checkpoint se necessário

## Exemplo de Fluxo Completo

```
Sessão 1:
  → Usuário: "Criar módulo fiscal completo"
  → Agente: Cria entidades, services, endpoints (60%)
  → Contexto enche → Salva checkpoint
  → Agente: "Checkpoint salvo. Continuarei na próxima sessão."

Sessão 2:
  → Agente detecta checkpoint pendente
  → Agente: "Retomando módulo fiscal (60%)..."
  → Cria validações, testes (90%)
  → Contexto enche → Salva novo checkpoint

Sessão 3:
  → Agente detecta checkpoint pendente
  → Agente: "Retomando módulo fiscal (90%)..."
  → Cria documentação, roda quality gates (100%)
  → Marca como completed
  → Agente: "✅ Módulo fiscal completo! 3 sessões, 100% feito."
```

## Métricas

| Métrica | Meta |
|---------|------|
| Checkpoints por sessão | 0-1 (ideal: nenhum) |
| Retomadas bem-sucedidas | > 95% |
| Perda de contexto entre sessões | < 5% |
| Tempo médio de retomada | < 30s |
