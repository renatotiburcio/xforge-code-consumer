---
id: sprints
type: planejamento
tags: [sprints, planejamento, ldv, ace, smart-routing, v5]
owner: project-team
version: 5.2.0
updated: 2026-06-10
---

# Sprints v5.2.0 — Intelligence Loop

## Visao Geral

| Sprint | Nome | Duracao | Itens | Entregavel |
|--------|------|---------|-------|------------|
| S5 | LDV Core | 14 dias | B-026 a B-033 | Loop de Decomposicao com Validacao funcional |
| S6 | ACE Core | 10 dias | B-034 a B-040 | Aprendizado Continuo Estruturado funcional |
| S7 | Smart Routing | 7 dias | B-041 a B-047 | Auto-selecao de provider por complexidade + fila offline |
| S8 | Cross Validation | 10 dias | B-048 a B-049 | Validacao cruzada multi-agente + release v5.0.0 |
| S9 | Limpeza Estrutural | 5 dias | B-050 a B-054 | 240+ arquivos removidos, 55K+ tokens economizados |
| S10 | Consolidacao | 7 dias | B-055 a B-059 | 43 agentes -> ~20, 35K+ tokens economizados |
| S11 | Reescrita Alta Densidade | 10 dias | B-060 a B-067 | 35-45% reducao total, release v5.1.0 |
| S12 | Qualidade Critica + LDV | 10 dias | B-068 a B-074 | 6 criticos corrigidos, LDV executavel |
| S13 | Qualidade Alta + RAG | 10 dias | B-075 a B-084 | 9 altos corrigidos, RAG semantico |
| S14 | Qualidade Media + Release | 10 dias | B-085 a B-096 | 8 medios corrigidos, release v5.2.0 |

---

## Sprint 5: LDV Core (14 dias)

**Objetivo:** Loop de Decomposicao com Validacao — de solicitacao do usuario a execucao validada de tarefas granuladas.

**Premissa:** Toda solicitacao complexa e decomposta em tarefas atomicas com SDD/harness. O loop so finaliza quando 100% do checklist passa.

### Dia 1-3: Skill deep-request-analyzer (B-026)
- [ ] Criar diretorio .kilo/skills/deep-request-analyzer/
- [ ] Criar SKILL.md com frontmatter (name, description)
- [ ] Implementar prompt de analise estruturada:
  - Resumo da intencao (1 paragrafo)
  - Contexto necessario (projeto, stack, restricoes)
  - Dependencias identificadas (modulos, APIs, banco)
  - Riscos e restricoes (seguranca, LGPD, fiscal)
  - Criterios de aceitacao (o que significa OK)
- [ ] Adicionar ao skill-registry.json
- [ ] Testar com 3 solicitacoes de exemplo

### Dia 4-6: Skill task-decomposer (B-027)
- [ ] Criar diretorio .kilo/skills/task-decomposer/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar prompt de decomposicao:
  - Recebe analise do deep-request-analyzer
  - Produz lista de tarefas atomicas (5-15 por solicitacao)
  - Cada tarefa tem: descricao, entrada, saida, criterio validacao, complexidade (S/M/L), dependencias
  - Gera DAG (grafo aciclico direcionado) de dependencias
- [ ] Validar: nenhuma tarefa ambigua, todas testaveis
- [ ] Adicionar ao skill-registry.json

### Dia 7-10: Skill sdd-generator (B-028)
- [ ] Criar diretorio .kilo/skills/sdd-generator/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar geracao de SDD para cada tarefa:
  - Especificacao funcional (contratos, regras, edge cases)
  - Contratos de interface (DTOs, APIs, eventos)
  - Casos de teste esperados (minimo 3 por tarefa)
  - Regras de negocio aplicaveis
  - Harness de validacao (script Python ou PS1)
- [ ] Criar template de harness Python (.xforge/templates/harness-template.py)
- [ ] Criar template de harness PowerShell (.xforge/templates/harness-template.ps1)
- [ ] Adicionar ao skill-registry.json

### Dia 11-12: Workflow loop-decomposicao-validacao (B-029)
- [ ] Criar .kilo/workflows/loop-decomposicao-validacao.md
- [ ] Definir etapas do workflow:
  1. Receber solicitacao do usuario
  2. Executar deep-request-analyzer
  3. Executar task-decomposer
  4. Executar sdd-generator para cada tarefa
  5. Para cada tarefa (em paralelo quando possivel):
     a. Agente executor-tarefas executa com SDD
     b. Harness de validacao roda
     c. Se PASS -> avancar
     d. Se FAIL -> retry (max 3) com contexto do erro
     e. Se FAIL apos 3 retries -> pausar loop, reportar ao usuario
  6. Rodar checklist loop-decomposicao-checklist
  7. Se 100% OK -> finalizar e reportar
  8. Se nao OK -> identificar falhas, permitir retry seletivo
- [ ] Adicionar ao workflow-registry.json

### Dia 12-13: Comando /decompor + Agente executor (B-030, B-031)
- [ ] Criar .kilo/commands/decompor.md (comando publico)
- [ ] Criar .kilo/agents/executor-tarefas.md (subagent)
  - mode: subagent
  - permission: edit allow, bash allow (execucao controlada)
  - prompt: especialista em executar tarefas granuladas com SDD
- [ ] Adicionar ao command-registry.json e expert-registry.json

### Dia 13-14: Checklist + Testes (B-032, B-033)
- [ ] Criar .kilo/checklists/loop-decomposicao-checklist.md
- [ ] Criar diretorio .xforge/tests/ldv/
- [ ] Testes: test_analyzer.py, test_decomposer.py, test_sdd_generator.py, test_loop_execution.py
- [ ] Validar: 8/8 testes passando

### Definicao de Pronto (Sprint 5)
- [ ] /decompor funciona end-to-end com solicitacao de exemplo
- [ ] Loop executa 5+ tarefas atomicas com SDD/harness
- [ ] Harness de validacao roda e detecta falhas
- [ ] Retry funciona (max 3 tentativas)
- [ ] Checklist 100% OK antes de finalizar
- [ ] 8 testes LDV passando

---

## Sprint 6: ACE Core (10 dias)

**Objetivo:** Aprendizado Continuo Estruturado — cada erro vira licao, cada licao melhora a proxima execucao.

**Premissa:** Feedback e automatico e estruturado. O knowledge graph e populado a cada execucao.

### Dia 1-2: Skill feedback-capture (B-034)
- [ ] Criar diretorio .kilo/skills/feedback-capture/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar captura automatica:
  - tarefa executada (tipo, descricao)
  - resultado (SUCCESS / FAIL / PARTIAL)
  - erro especifico (mensagem, stack trace, contexto)
  - solucao aplicada (se houver)
  - provider e modelo usados
  - complexidade da tarefa
  - timestamp
- [ ] Formato de saida: JSON estruturado
- [ ] Armazenar em .xforge/learning/feedback-log.jsonl

### Dia 3-5: Skill lesson-extractor (B-035)
- [ ] Criar diretorio .kilo/skills/lesson-extractor/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar extracao de licoes:
  - Agrupa feedbacks por tipo de tarefa
  - Identifica padroes de erro recorrentes (minimo 2 ocorrencias)
  - Extrai solucoes validadas (que levaram a SUCCESS)
  - Gera anti-patterns (o que NAO fazer)
  - Gera regras de ouro (best practices derivadas)
  - Calcula trust score por licao (baseado em frequencia e sucesso)

### Dia 5-6: Knowledge Graph de Erros e Solucoes (B-036)
- [ ] Criar .xforge/knowledge/errors-solutions-graph.json
- [ ] Estrutura: erro -> causa_raiz -> solucoes[] -> trust_score -> frequencia -> ultima_ocorrencia
- [ ] Script de atualizacao incremental
- [ ] Script de busca por similaridade (match por tipo de tarefa + erro)

### Dia 7-8: Skill lesson-applier (B-037)
- [ ] Criar diretorio .kilo/skills/lesson-applier/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar aplicacao de licoes:
  - Antes de executar tarefa, busca no knowledge graph
  - Filtra por tipo de tarefa similar
  - Ordena por trust score (maior primeiro)
  - Injeta top-5 licoes no contexto do agente
  - Formato: !! Historico: <erro> (ocorreu Nx) / ** Solucao: <solucao>

### Dia 8-9: Workflow ciclo-aprendizado + Comando /aprender (B-039, B-038)
- [ ] Criar .kilo/workflows/ciclo-aprendizado.md
- [ ] Criar .kilo/commands/aprender.md (registro manual de erro/solucao)
- [ ] Workflow periodico: coleta feedbacks -> extrai licoes -> atualiza graph -> ajusta trust

### Dia 9-10: Testes ACE (B-040)
- [ ] Criar diretorio .xforge/tests/ace/
- [ ] Testes: test_feedback_capture.py, test_lesson_extractor.py, test_lesson_applier.py, test_learning_cycle.py
- [ ] Validar: 6/6 testes passando

### Definicao de Pronto (Sprint 6)
- [ ] Feedback capturado automaticamente em cada execucao
- [ ] Licoes extraidas de feedbacks acumulados
- [ ] Knowledge graph populado e funcional
- [ ] lesson-applier injeta licoes no contexto antes da execucao
- [ ] /aprender permite registro manual
- [ ] 6 testes ACE passando

---

## Sprint 7: Smart Routing + Offline (7 dias)

**Objetivo:** Auto-selecao de provider por complexidade + fila offline com replay.

### Dia 1-2: Skill complexity-classifier (B-041)
- [ ] Criar diretorio .kilo/skills/complexity-classifier/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar classificacao:
  - SIMPLES: resposta direta, sem ferramentas (ex: explicar conceito)
  - MEDIA: 1-2 ferramentas, logica simples (ex: criar 1 endpoint)
  - COMPLEXA: multiplas ferramentas, raciocinio encadeado (ex: CRUD completo)
  - CRITICA: arquitetura, seguranca, fiscal, LGPD (ex: sistema de NFe)
- [ ] Usa heuristicas: numero de ferramentas, profundidade de raciocinio, dominio

### Dia 2-3: Regras de Roteamento (B-042)
- [ ] Criar .kilo/rules/complexity-routing-rules.md
- [ ] Definir mapeamento:
  - SIMPLES -> provider barato/rapido (ex: openrouter/haiku, ollama/local)
  - MEDIA -> provider standard (ex: openrouter/sonnet, openai/gpt-4o-mini)
  - COMPLEXA -> provider premium (ex: anthropic/claude-sonnet, openai/gpt-4o)
  - CRITICA -> provider maximo (ex: anthropic/claude-opus, openai/gpt-4o)
- [ ] Fallback automatico se provider indisponivel

### Dia 3-4: Integracao kilo.jsonc (B-043)
- [ ] Atualizar kilo.jsonc com secao complexityRouting
- [ ] Mapeamento complexidade -> provider/modelo
- [ ] Manter compatibilidade com routing existente

### Dia 4-5: Fila Offline (B-045, B-047)
- [ ] Expandir .xforge/scripts/offline-manager.ps1
- [ ] Capacidade de enfileirar tarefas completas (com SDD/harness)
- [ ] Persistencia em .xforge/queue/offline-queue.json
- [ ] Criar .kilo/commands/fila.md para visualizar fila

### Dia 5-6: Script de Replay (B-046)
- [ ] Criar .xforge/scripts/replay-queue.ps1
- [ ] Processa fila na ordem correta (respeitando dependencias)
- [ ] Injeta contexto ACE antes de cada replay
- [ ] Remove da fila quando executado com sucesso

### Dia 6-7: Testes (B-044)
- [ ] Criar diretorio .xforge/tests/routing/
- [ ] Testes: test_complexity_classifier.py, test_routing_rules.py, test_offline_queue.py, test_replay.py
- [ ] Validar: 4/4 testes passando

### Definicao de Pronto (Sprint 7)
- [ ] Tarefas classificadas corretamente por complexidade
- [ ] Provider selecionado automaticamente por complexidade
- [ ] Fila offline funciona (enfileirar + visualizar)
- [ ] Replay processa fila com contexto ACE
- [ ] 4 testes routing passando

---

## Sprint 8: Cross Validation + Release (10 dias)

**Objetivo:** Validacao cruzada multi-agente para tarefas criticas + release v5.0.0.

### Dia 1-3: Workflow validacao-cruzada (B-048)
- [ ] Criar .kilo/workflows/validacao-cruzada.md
- [ ] Definir fluxo:
  1. Identificar tarefa como CRITICA
  2. Enviar para 2+ agentes diferentes (ex: code + plan)
  3. Cada agente executa independentemente
  4. result-comparator compara saidas
  5. Se consenso -> aprovar
  6. Se divergencia -> solicitar arbitragem (3o agente ou humano)
  7. Registrar resultado no ACE

### Dia 3-5: Skill result-comparator (B-049)
- [ ] Criar diretorio .kilo/skills/result-comparator/
- [ ] Criar SKILL.md com frontmatter
- [ ] Implementar comparacao:
  - Compara saidas de 2+ agentes
  - Identifica consenso (mesmo resultado)
  - Identifica divergencias (resultados diferentes)
  - Avalia qualidade (usando criterios do SDD)
  - Sugere melhor resultado ou arbitragem

### Dia 5-7: Integracao LDV + ACE + Smart Routing
- [ ] Garantir que LDV usa ACE (lesson-applier) antes de cada tarefa
- [ ] Garantir que LDV usa Smart Routing para selecionar provider
- [ ] Garantir que tarefas CRITICAS usam validacao cruzada
- [ ] Teste end-to-end: /decompor solicitacao complexa -> LDV + ACE + Smart Routing + Cross Validation

### Dia 7-9: Documentacao e Polimento
- [ ] Atualizar .xforge/docs/COMO-USAR.md com novos comandos (/decompor, /aprender, /fila)
- [ ] Atualizar .xforge/docs/ARQUITETURA.md com diagramas LDV + ACE
- [ ] Atualizar .xforge/docs/COMO-ESTENDER.md com guia de criacao de skills LDV/ACE
- [ ] Atualizar AGENTS.md com instrucoes do LDV
- [ ] Atualizar README.md com badges v5.0.0

### Dia 9-10: Release v5.0.0
- [ ] Atualizar .xforge/version.json para 5.0.0
- [ ] Atualizar .xforge/backlog/BACKLOG.md — marcar B-026 a B-049 como Concluido
- [ ] Atualizar .xforge/roadmap/ROADMAP.md — marcar Fase 2 como CONCLUIDA
- [ ] Validar doctor.ps1: 0 erros, 0 warnings
- [ ] Validar testes: todos passando
- [ ] Criar tag v5.0.0

### Definicao de Pronto (Sprint 8)
- [ ] Validacao cruzada funciona para tarefas CRITICAS
- [ ] LDV + ACE + Smart Routing integrados e funcionais
- [ ] Documentacao atualizada
- [ ] doctor.ps1: 0 erros, 0 warnings
- [ ] Release v5.0.0 publicado

---

## Riscos e Mitigacoes

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|--------------|---------|-----------|
| Decomposicao gera tarefas ambiguas | Medio | Alto | Validacao humana no SDD antes da execucao; retry com contexto |
| Harness de validacao falso-positivo | Medio | Alto | Harness simples e deterministicos; revisao humana para CRITICO |
| Knowledge graph cresce demais | Baixo | Medio | TTL + decay de trust score; compressao periodica |
| Complexidade classificada errado | Medio | Medio | Fallback para provider premium se duvida; feedback loop |
| Loop LDV nunca termina (retry infinito) | Baixo | Alto | Max 3 retries por tarefa; escalacao para humano |
| Conflito entre agentes na validacao cruzada | Baixo | Medio | Arbitragem por 3o agente; voto majoritario |

---

## Dependencias entre Sprints

`
S5 (LDV Core) ──────────────┐
  │                          │
  │ deep-request-analyzer    │
  │ task-decomposer          │
  │ sdd-generator            │
  │ workflow loop            │
  │                          ▼
S6 (ACE Core) ──────────> S8 (Integration)
  │                          ▲
  │ feedback-capture         │
  │ lesson-extractor         │
  │ lesson-applier ──────────┘
  │                          ▲
S7 (Smart Routing) ─────────┘
  │ complexity-classifier
  │ offline queue
`

**Nota:** S5, S6, S7 podem ser executados em paralelo com Agent Manager (worktree isolado).
S8 depende de S5, S6, S7. S9-S11 sao sequenciais.
