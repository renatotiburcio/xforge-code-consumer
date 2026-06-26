---
name: loop-decomposicao-validacao
description: Workflow principal do LDV. Orquestra deep-request-analyzer -> task-decomposer -> executor-tarefas com retry e consolidacao.
type: workflow
version: 1.0.0
agent: code
---

# Loop de Decomposicao com Validacao (LDV)

## Visao Geral

O LDV e o motor de autonomia nivel 4 do XForge. Ele recebe qualquer solicitacao, decompoe em tarefas atomicas, executa com validacao e retry, e consolida o resultado final.

## Diagrama de Fluxo

`
Usuario solicita
       |
       v
[1] deep-request-analyzer (B-026)
       | produz AnalysisResult
       v
[2] Verifica requiresHumanReview
       | sim -> Aguarda humano -> Retorna ao passo 1
       | nao -> Continua
       v
[3] task-decomposer (B-027)
       | produz DecompositionResult (DAG)
       v
[4] Valida DAG (sem ciclos, conectado)
       | invalido -> Reporta erro -> Fim
       | valido -> Continua
       v
[5] Calcula ordenacao topologica
       | produz executionOrder[]
       v
[6] Para cada tarefa na executionOrder:
       |
       v
  [6.1] executor-tarefas (B-031)
         | executa tarefa atomica
         | produz TaskExecutionResult
         v
  [6.2] Avalia resultado
         | completed -> Marca concluida -> Proxima tarefa
         | failed -> Tenta retry (ate maxRetries)
         | skipped -> Marca skipped -> Proxima tarefa
         v
  [6.3] Se retry esgotado:
         | Tarefa critica -> Escalacao humana -> Pausa loop
         | Tarefa normal -> Marca failed -> Continua
         v
[7] Consolidacao
       | Verifica todas as tarefas completed
       | Gera relatorio final
       | Atualiza memoria e backlog
       v
[8] Retorna resultado ao usuario
`

## Passo 1: Analise (deep-request-analyzer)

**Agente**: deep-request-analyzer (B-026)
**Entrada**: Solicitacao bruta do usuario
**Saida**: AnalysisResult

### Acoes
1. Classificar intencao
2. Estimar complexidade
3. Identificar dependencias e riscos
4. Extrair criterios de aceite
5. Produzir AnalysisResult

### Saida esperada
- AnalysisResult.requestId
- AnalysisResult.intent.primary
- AnalysisResult.complexity.level
- AnalysisResult.acceptanceCriteria[]
- AnalysisResult.requiresHumanReview

## Passo 2: Gate Humano

**Condicao**: AnalysisResult.requiresHumanReview == true

### Se true
1. Apresentar AnalysisResult ao usuario
2. Solicitar aprovacao ou ajustes
3. Se aprovado: continuar ao passo 3
4. Se ajustado: retornar ao passo 1 com solicitacao ajustada
5. Se rejeitado: encerrar loop com status=cancelled

### Se false
- Continuar diretamente ao passo 3

## Passo 3: Decomposicao (task-decomposer)

**Agente**: task-decomposer (B-027)
**Entrada**: AnalysisResult
**Saida**: DecompositionResult

### Acoes
1. Decompor em tarefas atomicas
2. Estabelecer DAG de dependencias
3. Atribuir agentes recomendados
4. Definir criterios de sucesso por tarefa
5. Calcular ordenacao topologica

### Saida esperada
- DecompositionResult.totalTasks
- DecompositionResult.dag.nodes[]
- DecompositionResult.dag.edges[]
- DecompositionResult.executionOrder[]

## Passo 4: Validacao do DAG

**Responsabilidade**: workflow (validacao automatica)

### Validacoes
1. **Sem ciclos**: executar detecao de ciclos no DAG
2. **Conectado**: todas as tarefas alcancaveis
3. **Atomicidade**: cada tarefa com responsabilidade unica
4. **Rastreabilidade**: cada tarefa referencia criterios do AnalysisResult

### Se invalido
- Reportar erro especifico
- Sugerir correcoes ao task-decomposer
- Tentar re-decompor (max 2 vezes)
- Se persistir: escalar para humano

### Se valido
- Continuar ao passo 5

## Passo 5: Ordenacao Topologica

**Algoritmo**: Kahn's algorithm ou DFS-based topological sort

### Saida
- executionOrder[]: lista ordenada de task IDs
- parallelGroups[]: grupos de tarefas que podem rodar em paralelo

## Passo 6: Execucao com Retry

**Agente**: executor-tarefas (B-031)
**Estrategia**: executar na ordem topologica, respeitando dependencias

### Para cada tarefa

1. Verificar dependencias concluidas
2. Invocar executor-tarefas com a tarefa
3. Aguardar TaskExecutionResult
4. Avaliar:
   - completed: marcar concluida, avancar
   - failed: verificar retry
   - skipped: marcar skipped, avancar

### Politica de Retry

| Tentativa | Acao |
|-----------|------|
| 1 | Execucao normal |
| 2 | Re-executar com contexto do erro |
| 3 | Re-executar com abordagem alternativa |
| >3 | Escalacao (se critica) ou skip (se normal) |

### Tarefas Criticas
- Seguranca, LGPD, dados sensivos: maxRetries=1, escalacao automatica
- Arquitetura: maxRetries=2, escalacao se falhar
- Outras: maxRetries=3, marcar failed e continuar

## Passo 7: Consolidacao

### Acoes
1. Verificar status de todas as tarefas
2. Gerar relatorio final:
   - Total de tarefas
   - Concluidas com sucesso
   - Falhas (e razoes)
   - Skipped
   - Duracao total
3. Atualizar .xforge/memory/sessions/ com resultado
4. Atualizar .xforge/backlog/BACKLOG.md se necessario
5. Registrar licoes aprendidas (B-034 feedback-capture)

### Saida Final

`json
{
  "loopId": "LOOP-YYYYMMDD-NNN",
  "requestId": "REQ-YYYYMMDD-NNN",
  "status": "completed|partial|failed|cancelled",
  "summary": {
    "totalTasks": 0,
    "completed": 0,
    "failed": 0,
    "skipped": 0,
    "durationMs": 0
  },
  "tasks": [ ...TaskExecutionResult... ],
  "lessons": [ ...licoes aprendidas... ]
}
`

## Passo 8: Reportar ao Usuario

1. Apresentar resumo executivo
2. Listar arquivos criados/modificados
3. Reportar erros e warnings
4. Sugerir proximos passos

## Tratamento de Erros

| Erro | Acao |
|------|------|
| AnalysisResult invalido | Solicitar re-formulacao ao usuario |
| DAG com ciclo | Tentar re-decompor (max 2x) |
| Tarefa falhou (retry esgotado) | Escalar ou skip conforme criticidade |
| Timeout (>30min/tarefa) | Sugerir decomposicao da tarefa |
| Agente indisponivel | Tentar agente alternativo |
| Erro de sistema | Abortar loop, preservar estado |

## Metricas Coletadas

- Tempo total de execucao
- Taxa de sucesso (%)
- Numero de retries por tarefa
- Tarefas que precisaram escalacao
- Licoes aprendidas geradas

## Integracoes

- **B-026**: deep-request-analyzer (entrada)
- **B-027**: task-decomposer (decomposicao)
- **B-028**: sdd-generator (documentacao por tarefa)
- **B-029**: este workflow (orquestracao)
- **B-030**: comando /decompor (interface publica)
- **B-031**: executor-tarefas (execucao)
- **B-032**: checklist-validacao (validacao)
- **B-033**: testes LDV (cobertura)
- **B-034**: feedback-capture (aprendizado)

## Execucao via Script

O LDV pode ser executado diretamente via Python scripts, sem necessidade de orquestracao por agente:

\\\ash
# Executar loop completo
python .xforge/automation/scripts/ldv_cli.py "sua solicitacao aqui"

# Apenas analisar (sem decompor/executar)
python .xforge/automation/scripts/ldv_cli.py --analyze-only "sua solicitacao aqui"

# Verificar status de uma execucao anterior
python .xforge/automation/scripts/ldv_cli.py --status .xforge/ldv-state.json

# Usar engine diretamente (modo avancado)
python .xforge/automation/scripts/ldv_engine.py analyze "sua solicitacao aqui" --output analysis.json
python .xforge/automation/scripts/ldv_engine.py decompose analysis.json --output decomposition.json
python .xforge/automation/scripts/ldv_engine.py run "sua solicitacao aqui" --output result.json
python .xforge/automation/scripts/ldv_engine.py status .xforge/ldv-state.json
python .xforge/automation/scripts/ldv_engine.py retry .xforge/ldv-state.json --task T-003
\\\

Os estados sao salvos em \.xforge/ldv-state.json\ por padrao e podem ser inspecionados ou retomados.
