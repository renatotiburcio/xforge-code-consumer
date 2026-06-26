---
name: ciclo-aprendizado
description: Workflow periodico de aprendizado. Coleta feedbacks, extrai licoes, atualiza knowledge graph e ajusta trust scores.
type: workflow
version: 1.0.0
agent: code
---

# Ciclo de Aprendizado (ACE)

## Visao Geral

O Ciclo de Aprendizado e o coracao do ACE (Aprendizado Continuo Estruturado). Ele processa feedbacks acumulados, extrai licoes, atualiza o knowledge graph e garante que o XForge melhore a cada execucao.

## Diagrama de Fluxo

`
Feedbacks acumulados (feedback-log.jsonl)
       |
       v
[1] Coleta de Feedbacks
       | le entradas desde ultima execucao
       v
[2] Extracao de Licoes (lesson-extractor, B-035)
       | agrupa por taskType + error.type
       | identifica padroes recorrentes
       | extrai solucoes validadas
       v
[3] Atualizacao do Knowledge Graph (B-036)
       | adiciona novos erros/solucoes
       | atualiza trust scores
       | remove licoes expiradas (>90 dias)
       v
[4] Ajuste de Trust Scores
       | sobe: licao aplicada com sucesso
       | cai: licao ignorada + erro persiste
       | expira: sem ocorrencia em 90 dias
       v
[5] Relatorio de Aprendizado
       | total de licoes extraidas
       | novos anti-patterns
       | regras de ouro atualizadas
       | erros recorrentes detectados
       v
[6] Disponibilizacao
       | lesson-applier (B-037) usa licoes atualizadas
       | proximo LDV loop ja usa conhecimento novo
`

## Passo 1: Coleta de Feedbacks

**Responsabilidade**: workflow
**Entrada**: .xforge/learning/feedback-log.jsonl
**Saida**: Lista de feedbacks desde ultima execucao

### Acoes
1. Ler feedback-log.jsonl.
2. Filtrar entradas com timestamp > ultimaExtracao.
3. Se nao houver novos feedbacks, encerrar ciclo.
4. Contar total de novos feedbacks.

### Saida esperada
- Lista de novos FeedbackEntry
- Contadores por result (SUCCESS, FAIL, PARTIAL)

## Passo 2: Extracao de Licoes

**Agente**: lesson-extractor (B-035)
**Entrada**: Novos feedbacks
**Saida**: Lista de Lesson objects

### Acoes
1. Agrupar feedbacks por taskType + error.type.
2. Identificar erros recorrentes (2+ ocorrencias).
3. Extrair solucoes validadas.
4. Gerar anti-patterns e regras de ouro.
5. Calcular trust scores.

### Saida esperada
- Lista de Lesson objects (JSON)
- Relatorio de extracao

## Passo 3: Atualizacao do Knowledge Graph

**Responsabilidade**: workflow
**Entrada**: Lesson objects
**Saida**: errors-solutions-graph.json atualizado

### Acoes
1. Ler errors-solutions-graph.json atual.
2. Para cada nova licao:
   - Se ja existe: atualizar trust score e frequencia.
   - Se nova: adicionar ao graph.
3. Remover licoes expiradas (>90 dias sem ocorrencia).
4. Atualizar indices (byTaskType, byErrorType, byTag).
5. Salvar graph atualizado.

### Saida esperada
- errors-solutions-graph.json atualizado
- Contadores: adicionadas, atualizadas, removidas

## Passo 4: Ajuste de Trust Scores

**Responsabilidade**: workflow
**Entrada**: Lesson objects + feedbacks recentes
**Saida**: Trust scores atualizados

### Regras de Ajuste

| Evento | Efeito no Trust |
|--------|-----------------|
| Licao aplicada com sucesso | +5 pontos |
| Licao aplicada mas erro persistiu | -10 pontos |
| Licao ignorada + erro ocorreu | -15 pontos |
| Nova ocorrencia do mesmo erro | +2 pontos (frequencia) |
| 30 dias sem ocorrencia | -1 ponto (decaimento) |
| 90 dias sem ocorrencia | Remocao da licao |

### Limites
- Trust score minimo: 0
- Trust score maximo: 100
- Trust score para remocao automatica: < 10

## Passo 5: Relatorio de Aprendizado

**Responsabilidade**: workflow
**Saida**: .xforge/learning/lessons-extracted.md

### Secoes do Relatorio

1. **Resumo**: total de feedbacks processados, licoes extraidas, graph atualizado.
2. **Novos Anti-Patterns**: lista de anti-patterns descobertos.
3. **Regras de Ouro Atualizadas**: regras com trust score alterado.
4. **Erros Recorrentes**: erros que aparecem 2+ vezes.
5. **Licoes Expiradas**: licoes removidas por inatividade.
6. **Metricas**: taxa de sucesso media, taxa de erro, top-5 erros.

## Passo 6: Disponibilizacao

**Responsabilidade**: workflow
**Saida**: Licoes disponiveis para lesson-applier

### Acoes
1. Verificar que errors-solutions-graph.json esta valido.
2. Atualizar feedback-stats.json.
3. Registrar timestamp da ultima extracao.
4. Notificar que novas licoes estao disponiveis.

## Frequencia de Execucao

| Gatilho | Frequencia |
|---------|------------|
| Automatico | A cada 10 feedbacks novos |
| Manual | /aprender --processar |
| Agendado | Diario (cron) |

## Tratamento de Erros

| Erro | Acao |
|------|------|
| feedback-log.jsonl corrompido | Tentar recuperar ate ultima linha valida |
| Graph invalido | Recuperar de backup (.xforge/learning/graph-backup.json) |
| Sem novos feedbacks | Encerrar ciclo com status=no-op |
| Extracao falhou | Tentar novamente com batch menor |

## Metricas Coletadas

- Total de licoes no graph
- Taxa de aplicacao de licoes
- Taxa de erro antes/depois de aplicar licoes
- Trust score medio por taskType
- Licoes expiradas por mes

## Integracoes

- **B-034 (feedback-capture)**: le feedback-log.jsonl.
- **B-035 (lesson-extractor)**: extrai licoes.
- **B-036 (knowledge graph)**: armazena licoes.
- **B-037 (lesson-applier)**: usa licoes.
- **B-038 (comando /aprender)**: registro manual.
- **B-029 (LDV loop)**: usa licoes antes de executar.
