# Autonomous Experiment Loop — XForge Engineer

## Visão Geral

Inspirado no [karpathy/autoresearch](https://github.com/karpathy/autoresearch). O agente roda um loop autônomo de experimentos: tenta uma mudança, mede o resultado, keeps ou discards, e repete. O humano programe o agente (program.md), o agente executa.

## O Loop

```
LOOP FOREVER:

1. Ler estado atual (git status, último xfs, experimentos anteriores)
2. Escolher uma ideia de experimento (baseado em gaps, erros, oportunidades)
3. Implementar a mudança (editar código)
4. Fazer commit
5. Rodar scoring: .\.kilo\automation\scripts\score.ps1
6. Ler resultado (xfs, status)
7. SE xfs melhorou (keep):
   → Avançar branch, registrar em results.tsv
   → Adicionar ao knowledge base (lição aprendida)
   → Continuar para próximo experimento
8. SE xfs piorou (discard):
   → Reverter commit (git reset --hard HEAD~1)
   → Registrar falha em results.tsv
   → Analisar por que falhou
   → Gerar nova ideia baseada no fracasso
9. SE crash:
   → Tentar consertar (máx 3 tentativas)
   → Se não conseguir: descartar e seguir
10. Repetir

NEVER STOP: O loop roda até o humano interromper.
```

## Regras do Loop

### 1. Métrica Única
O agente otimiza APENAS para `xfs` (XForge Score). Não pode criar métricas paralelas ou manipular a pontuação.

### 2. Budget Fixo
Cada experimento tem um budget fixo de tempo:
- **Mudanças simples** (< 10 linhas): 5 minutos
- **Mudanças médias** (10-50 linhas): 15 minutos
- **Mudanças complexas** (> 50 linhas): 30 minutos

Se exceder o budget, descartar e registrar como timeout.

### 3. Histórico Obrigatório
Cada experimento deve ser registrado em `results.tsv` com:
- commit hash
- xfs score
- status (keep/discard/crash/timeout)
- descrição do que tentou
- timestamp

### 4. Nunca Parar
O agente NÃO pode:
- Perguntar "devo continuar?"
- Pausar o loop
- Esperar confirmação humana

O agente PODE:
- Pedir ajuda quando estiver completamente stuck (máx 1 vez por sessão)
- Mudar de estratégia se a atual não está funcionando
- Revisitar experimentos anteriores que quase funcionaram

### 5. Aprendizado
Após cada experimento (keep ou discard):
- Se keep: documentar o que funcionou e por quê
- Se discard: documentar o que falhou e por quê
- Atualizar error-patterns-graph.json se aplicável
- Atualizar preferências do usuário se aplicável

## Exemplo de Fluxo

```
Experimento 1: Baseline
  → xfs: 0.750 (baseline)
  → Status: keep (primeiro registro)

Experimento 2: Adicionar FluentValidation
  → xfs: 0.820 (+0.070)
  → Status: keep (+7% correctness)

Experimento 3: Migrar para Redis cache
  → xfs: 0.780 (-0.040)
  → Status: discard (complexidade não justificou ganho)

Experimento 4: Otimizar queries N+1
  → xfs: 0.850 (+0.030 vs último keep)
  → Status: keep (+3% performance)

... continuar indefinidamente
```

## Integração com Split Architecture

### Router Layer (qwen2.5:7b)
- Detecta: "iniciar loop de experimentos"
- Classifica: needsWorker = true
- Estima: complexidade XL

### Worker Layer (qwen2.5:72b)
- Executa o loop
- Implementa mudanças
- Roda scoring
- Decide keep/discard
- Registra resultado

## Métricas

| Métrica | Meta |
|---------|------|
| Experimentos por hora | 4-8 |
| Taxa de sucesso (keep) | > 30% |
| Melhoria média por keep | > 2% xfs |
| Crash rate | < 10% |
| Tempo médio por experimento | 10-15 min |
