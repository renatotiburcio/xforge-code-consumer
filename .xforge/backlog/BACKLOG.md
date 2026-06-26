---
id: backlog
type: planejamento
tags: [backlog, priorizacao, tasks, P0, P1, P2, P3, loop-decomposicao, aprendizado-continuo]
owner: project-team
version: 6.0.0
updated: 2026-06-10
---

# Backlog do Template (v6.0.0)

Priorizacao baseada na analise exaustiva de:
- Repositorio OpenClaude (28.5k stars, 796 commits) — gaps em decomposicao, aprendizado, offline
- Documentacao Kilo (kilo.ai/docs) — compatibilidade 100% com agents, skills, commands, workflows, Agent Manager
- Repositorio XForge atual (v4.0.0) — 25 itens concluidos, base solida para evolucao

---

## ✅ Concluido (v4.0.0)

| ID | Item | Esforco | Sprint |
|----|------|---------|--------|
| B-001 | Migrar 132 skills para formato SKILL.md oficial (Agent Skills spec) | 3 dias | S1 |
| B-002 | Adicionar YAML frontmatter nos 36 agentes (.kilo/agents/) | 1 dia | S1 |
| B-003 | Expandir kilo.jsonc com agent, skills, commands, workflows | 1 dia | S1 |
| B-004 | Deletar pasta knowledge/old/ (146 arquivos removidos, 2.64 MB liberados) | 1 hora | S1 |
| B-005 | Script de bootstrap (init-template.sh/ps1) para novos projetos | 2 dias | S1 |
| B-006 | Adicionar .github/workflows/ci.yml (doctor.ps1 + lint) | 1 dia | S1 |
| B-007 | Criar comando /provider para troca de modelo on-the-fly | 2 dias | S2 |
| B-008 | Expandir doctor.ps1 com validacao de conectividade de modelo | 1 dia | S2 |
| B-009 | Adicionar agent routing no kilo.jsonc (model por agente) | 2 dias | S2 |
| B-010 | Unificar nomes de agentes (portugues, consistencia) | 1 dia | S2 |
| B-011 | Adicionar exemplos de uso nos comandos de .kilo/commands/ | 3 dias | S2 |
| B-012 | Criar ~/.xforge/config.json para preferencias persistentes | 2 dias | S2 |
| B-013 | MCP servers pre-configurados (PostgreSQL, Redis, RabbitMQ) | 3 dias | S3 |
| B-014 | Comando /buscar com web search (DuckDuckGo + Firecrawl) | 2 dias | S3 |
| B-015 | Testes unitarios para scripts RAG (Python, chunking, index) | 2 dias | S3 |
| B-016 | Git hooks (pre-commit rodando doctor.ps1, pre-push) | 1 dia | S3 |
| B-017 | Documentacao do template: como usar, como extender | 3 dias | S3 |
| B-018 | Privacy verification script (verify:privacy) | 1 dia | S3 |
| B-019 | gRPC headless server (inspirado openclaude) - implementacao real | 5 dias | S15 |
| B-020 | SDK export para Node.js - implementacao real | 3 dias | S15 |
| B-021 | Template marketplace submission (Kilo Marketplace) | 2 dias | S4 |
| B-022 | Dashboard web para health + metrics - scaffolding | 5 dias | S4 |
| B-023 | Multi-tenant config suporte | 3 dias | S4 |
| B-024 | Cache inteligente do RAG (incremental, diff-based) | 3 dias | S4 |
| B-025 | Modo offline completo | 4 dias | S4 |
| B-019 | gRPC headless server - implementacao real (server.py + xforge.proto) | 5 dias | S15 |
| B-020 | SDK export para Node.js - implementacao real (index.ts com shell-out) | 3 dias | S15 |
| B-034 | Skill de Captura de Feedback - agente feedback-capture.md | 2 dias | S15 |
| B-035 | Skill de Extracao de Licoes - agente lesson-extractor.md | 3 dias | S15 |
| B-036 | Knowledge Graph de Erros e Solucoes - errors-solutions-graph.json | 2 dias | S15 |
| B-037 | Skill de Aplicacao de Licoes - agente lesson-applier.md | 3 dias | S15 |
| B-038 | Comando /aprender - comando para registro manual de licoes | 1 dia | S15 |
| B-039 | Workflow de Ciclo de Aprendizado - ciclo-aprendizado.md | 2 dias | S15 |
| B-040 | Testes do ACE - test_ace.py com 13+ assertions | 2 dias | S15 |
| B-045 | Script de Fila Offline - offline-manager.ps1 com enable/disable/sync/queue | 2 dias | S15 |
| B-046 | Script de Replay - replay-queue.ps1 para processar fila offline | 2 dias | S15 |
| B-047 | Comando /fila - comando para gerenciar fila offline | 1 dia | S15 |
| B-048 | Workflow de Validacao Cruzada - validacao-cruzada.md multi-agente | 2 dias | S15 |
| B-049 | Skill de Comparacao de Resultados - result-comparator/SKILL.md | 2 dias | S15 |
| B-090 | Trigger automatico para ACE - ace-trigger.ps1 pos-comando | 2 dias | S15 |
| B-094 | Type hints em rag_cache.py - Dict, List, Optional, Tuple, Any | 0.5 dia | S15 |
| B-095 | Testes reais de chunking - test_chunking.py testa chunk_file() real | 0.5 dia | S15 |

---

## v6.0.0 - Registry Cleanup and Consolidation (S15)

| ID | Item | Esforco | Sprint |
|----|------|---------|--------|
| B-096 | Registry cleanup: knowledge-registry.json rebuilt from filesystem (9 areas, 126 files) | 0.5 dia | S15 |
| B-097 | Registry cleanup: architecture-registry.json paths corrected to real files | 0.5 dia | S15 |
| B-098 | Engineer consolidation: 129 placeholder dirs deleted, curated-operational preserved | 1 dia | S15 |
| B-099 | Test data cleanup: errors-solutions-graph.json and feedback-log.jsonl purged | 0.5 dia | S15 |



---

## P0 — Loop de Decomposicao com Validacao (LDV)

> **Conceito central:** Usuario faz solicitacao → sistema absorve e analisa profundamente → gera internamente (via engenharia de prompt) tarefas granuladas com SDD/harness → IAs simples executam cada tarefa → loop so finaliza quando TODO o checklist passa com resultado OK.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-026 | **Skill de Analise Profunda de Solicitacao** — Criar skill .kilo/skills/deep-request-analyzer/SKILL.md que recebe qualquer solicitacao do usuario e produz: (1) resumo estruturado da intencao, (2) contexto necessario, (3) dependencias identificadas, (4) riscos e restricoes, (5) criterios de aceitacao | 3 dias | Alto — base do LDV | S5 |
| B-027 | **Skill de Decomposicao em Tarefas Granuladas** — Criar skill .kilo/skills/task-decomposer/SKILL.md que recebe a analise da B-026 e produz lista de tarefas atomicas, cada uma com: (1) descricao clara e nao-ambigua, (2) entrada esperada, (3) saida esperada, (4) criterio de validacao, (5) complexidade estimada (S/M/L), (6) dependencias entre tarefas | 3 dias | Alto — nucleo do LDV | S5 |
| B-028 | **Skill de Geracao de SDD (Spec-Driven Development)** — Criar skill .kilo/skills/sdd-generator/SKILL.md que gera para cada tarefa: (1) especificacao funcional, (2) contratos de interface, (3) casos de teste esperados, (4) regras de negocio aplicaveis, (5) harness de validacao (script Python/PS1 que verifica se a saida atende o criterio) | 4 dias | Alto — garantia de qualidade | S5 |
| B-029 | **Workflow de Execucao do Loop LDV** — Criar workflow .kilo/workflows/loop-decomposicao-validacao.md que orquestra: analise → decomposicao → geracao SDD → execucao por agente → validacao → retry se falhar → so finaliza quando 100% do checklist passa | 3 dias | Alto — orquestracao | S5 |
| B-030 | **Comando /decompor** — Criar comando .kilo/commands/decompor.md que expoe o LDV como comando publico /decompor <solicitacao> com interface simples para o usuario | 1 dia | Alto — usabilidade | S5 |
| B-031 | **Agente Executor de Tarefas** — Criar agente .kilo/agents/executor-tarefas.md (mode: subagent) especializado em executar tarefas granuladas com SDD/harness, reportando resultado estruturado | 2 dias | Alto — execucao | S5 |
| B-032 | **Checklist de Validacao do Loop** — Criar checklist .kilo/checklists/loop-decomposicao-checklist.md com todos os criterios que devem passar antes do loop ser considerado completo | 1 dia | Medio — qualidade | S5 |
| B-033 | **Testes do LDV** — Criar testes em .xforge/tests/ldv/ cobrindo: analise de solicitacao, decomposicao, geracao SDD, execucao do loop, validacao de harness | 3 dias | Alto — confiabilidade | S5 |

---

## P1 — Aprendizado Continuo Estruturado (ACE)

> **Conceito central:** Capturar acertos e erros de cada execucao, armazenar em knowledge graph com trust score, e usar esse conhecimento para errar menos no futuro.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-034 | **Skill de Captura de Feedback** — Criar skill .kilo/skills/feedback-capture/SKILL.md que registra automaticamente: (1) tarefa executada, (2) resultado (sucesso/falha), (3) erro especifico se falhou, (4) solucao aplicada, (5) contexto (provider, modelo, complexidade), (6) timestamp | 2 dias | Alto — base do ACE | S6 |
| B-035 | **Skill de Extracao de Licoes** — Criar skill .kilo/skills/lesson-extractor/SKILL.md que analisa feedbacks acumulados e extrai: (1) padroes de erro recorrentes, (2) solucoes validadas, (3) anti-patterns, (4) melhores practices descobertas, (5) regras de ouro derivadas | 3 dias | Alto — inteligencia | S6 |
| B-036 | **Knowledge Graph de Erros e Solucoes** — Expandir .xforge/knowledge/ com estrutura errors-solutions-graph.json que mapeia: erro → causa raiz → solucao → trust score → frequencia → ultima ocorrencia | 2 dias | Alto — persistencia | S6 |
| B-037 | **Skill de Aplicacao de Licoes** — Criar skill .kilo/skills/lesson-applier/SKILL.md que antes de executar qualquer tarefa: (1) busca no knowledge graph por erros similares, (2) injeta licoes relevantes no contexto do agente, (3) ajusta a abordagem baseado em falhas passadas | 3 dias | Alto — prevencao | S6 |
| B-038 | **Comando /aprender** — Criar comando .kilo/commands/aprender.md que permite ao usuario registrar manualmente um erro + solucao, alimentando o ACE | 1 dia | Medio — usabilidade | S6 |
| B-039 | **Workflow de Ciclo de Aprendizado** — Criar workflow .kilo/workflows/ciclo-aprendizado.md que roda periodicamente: coleta feedbacks → extrai licoes → atualiza knowledge graph → ajusta trust scores → promove/deprecia conhecimento | 2 dias | Alto — automacao | S6 |
| B-040 | **Testes do ACE** — Criar testes em .xforge/tests/ace/ cobrindo: captura de feedback, extracao de licoes, aplicacao de licoes, ciclo de aprendizado | 2 dias | Alto — confiabilidade | S6 |

---

## P2 — Auto-selecao de Provider por Complexidade

> **Conceito central:** Tarefas simples vao para modelos baratos/rapidos, tarefas complexas vao para modelos premium. Inspirado no agentRouting do OpenClaude mas com decisao automatica baseada na complexidade da tarefa.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-041 | **Skill de Classificacao de Complexidade** — Criar skill .kilo/skills/complexity-classifier/SKILL.md que analisa cada tarefa e classifica: (1) SIMPLES (resposta direta, sem ferramentas), (2) MEDIA (1-2 ferramentas, logica simples), (3) COMPLEXA (multiplas ferramentas, raciocinio encadeado), (4) CRITICA (arquitetura, seguranca, fiscal) | 2 dias | Medio — otimizacao | S7 |
| B-042 | **Regras de Roteamento por Complexidade** — Criar regra .kilo/rules/complexity-routing-rules.md que define: qual provider/modelo usar para cada nivel de complexidade, com fallback automatico | 1 dia | Medio — configuracao | S7 |
| B-043 | **Integracao com kilo.jsonc routing** — Atualizar kilo.jsonc com nova secao complexityRouting que mapeia niveis de complexidade para providers/modelos | 1 dia | Medio — integracao | S7 |
| B-044 | **Testes de Roteamento** — Criar testes em .xforge/tests/routing/ validando que tarefas de cada complexidade vao para o provider correto | 1 dia | Medio — qualidade | S7 |

---

## P3 — Fila Offline com Replay

> **Conceito central:** Quando offline, tarefas sao enfileiradas com contexto completo. Quando conectado, sao executadas em ordem com replay do aprendizado acumulado.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-045 | **Script de Fila Offline** — Expandir .xforge/scripts/offline-manager.ps1 com capacidade de enfileirar tarefas completas (com SDD/harness) quando offline | 2 dias | Medio — resiliencia | S7 |
| B-046 | **Script de Replay** — Criar .xforge/scripts/replay-queue.ps1 que processa fila offline na ordem correta, com contexto de aprendizado do ACE | 2 dias | Medio — resiliencia | S7 |
| B-047 | **Comando /fila** — Criar comando .kilo/commands/fila.md para visualizar e gerenciar fila offline | 1 dia | Baixo — usabilidade | S7 |

---

## P3 — Validacao Cruzada Multi-Agente

> **Conceito central:** Para tarefas criticas, 2+ agentes independentes executam e comparam resultados. So e considerado valido quando ha consenso.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-048 | **Workflow de Validacao Cruzada** — Criar workflow .kilo/workflows/validacao-cruzada.md que: (1) envia tarefa para 2+ agentes diferentes, (2) compara resultados, (3) identifica divergencias, (4) solicita arbitragem se necessario, (5) so aprova com consenso | 2 dias | Medio — qualidade | S8 |
| B-049 | **Skill de Comparacao de Resultados** — Criar skill .kilo/skills/result-comparator/SKILL.md que compara saidas de multiplos agentes e identifica: consenso, divergencias, melhor resultado | 2 dias | Medio — inteligencia | S8 |

---

---

## P0 — Otimizacao de Tokens v5.1.0

> **Conceito central:** Reducao de 35-45% no consumo de tokens com melhoria simultanea de qualidade, precisao e consistencia. Baseado em analise exaustiva de 539 arquivos (908 KB, ~232.000 tokens).

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-050 | **Deletar diretorio workflows/** — Remover 106 arquivos redundantes (workflows/ espelha commands/). Manter apenas 12 workflows substanciais como comandos especiais. Economia: ~11.000 tokens | 1 dia | Alto — reducao de tokens | S9 |
| B-051 | **Deletar 134 arquivos xforge-*** — Comandos e workflows com prefixo xforge- sao duplicatas expandidas dos comandos base. Manter apenas versoes nao-prefixed. Economia: ~38.000 tokens | 1 dia | Alto — reducao de tokens | S9 |
| B-052 | **Deletar ROADMAP.md** — Conteudo totalmente derivavel de BACKLOG.md + SPRINTS.md. Economia: ~4.200 tokens + eliminacao de sync burden | 0.5 dia | Alto — manutenibilidade | S9 |
| B-053 | **Deletar smart-routing-rules.md** — Duplica kilo.jsonc. Fonte de verdade e o JSON. Economia: ~750 tokens + sync burden | 0.5 dia | Medio — consistencia | S9 |
| B-054 | **Deletar diretorios vazios e stubs** — 38-curated-operational-knowledge/, 40-brazil-software-market-intelligence/, stubs de 1 linha. Economia: ~500 tokens | 0.5 dia | Baixo — limpeza | S9 |

---

## P1 — Consolidacao de Agentes v5.1.0

> **Conceito central:** Consolidar agentes duplicados, bilíngues e boilerplate em agentes unicos, mais curtos e mais precisos.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-055 | **Extrair boilerplate de agentes** — Criar _agent-base.md com "Procedimento minimo" + "Saida esperada" compartilhado. 9 agentes referenciam em vez de duplicar. Economia: ~8.000 tokens | 2 dias | Alto — reducao + padronizacao | S9 |
| B-056 | **Consolidar agentes bilíngues** — 16+ pares PT/EN com funcionalidade identica. Consolidar para PT unico. Economia: ~11.000 tokens | 3 dias | Alto — reducao + clareza | S9 |
| B-057 | **Consolidar agentes diretor** — 10+ agentes "diretor" quase-identicos -> 2 agentes parametrizados (tecnico + negocio). Economia: ~5.000 tokens | 2 dias | Alto — reducao + extensibilidade | S10 |
| B-058 | **Consolidar comandos de seguranca** — 11 security-*-check.md identicos -> 1 arquivo parametrizado. Economia: ~10.000 tokens | 1 dia | Alto — reducao + manutenibilidade | S10 |
| B-059 | **Consolidar padrao analysis** — 27 comandos + 27 workflows identicos -> 1 arquivo com tabela de parametros. Economia: ~12.000 tokens | 2 dias | Alto — reducao + consistencia | S10 |

---

## P2 — Reescrita de Alta Densidade v5.1.0

> **Conceito central:** Reescrever agentes, comandos e regras com instrucoes mais curtas, especificas e acionaveis. Menos tokens, mais qualidade.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-060 | **Reescrever agentes com alta densidade** — Reescrever 43 agentes com instrucoes 40% mais curtas e 60% mais precisas. Tabelas de decisao em vez de texto livre. Economia: ~14.000 tokens + melhoria de qualidade | 5 dias | Alto — qualidade + eficiencia | S10 |
| B-061 | **Reescrever regras com condicoes executaveis** — 24 regras reescritas com formato IF-THEN acionavel. Economia: ~4.000 tokens + 100% acionabilidade | 3 dias | Alto — acionabilidade | S10 |
| B-062 | **Implementar saida estruturada em comandos** — Todos os comandos definem schema de saida JSON obrigatorio. Economia: ~2.000 tokens + 80% consistencia | 2 dias | Medio — consistencia | S11 |
| B-063 | **Mover frontmatter para registro central** — 200+ arquivos perdem YAML frontmatter inline. _registry.json como fonte de verdade. Economia: ~17.000 tokens | 2 dias | Alto — reducao massiva | S11 |
| B-064 | **Mover exemplos para diretorio separado** — 208 linhas de exemplos em 8 agentes -> diretorio _examples/. Economia: ~4.500 tokens | 1 dia | Medio — separacao de concerns | S11 |
| B-065 | **Consolidar documentacao tripla** — Eliminar hierarquias paralelas em docs/. Manter apenas estrutura numerica canonica. Economia: ~12.000 tokens | 2 dias | Alto — navegabilidade | S11 |
| B-066 | **Consolidar glossario** — 5 arquivos -> 1 arquivo com secao por dominio. Economia: ~500 tokens + 4 file-reads | 0.5 dia | Baixo — limpeza | S11 |
| B-067 | **Implementar indexacao semantica de conhecimento** — knowledge/ carrega apenas index.json inicialmente. Conteudo completo sob demanda. Economia: ~100.000 tokens por carga inicial | 3 dias | Alto — performance | S11 |


---

## P0 - Qualidade Critica v5.1.0

> Objetivo: Corrigir 17 problemas criticos/altos que afetam seguranca, corretude e funcionalidade basica.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-068 | Corrigir encoding dos JSON registries - Re-encodar command-registry.json, expert-registry.json, skill-registry.json, rule-registry.json para UTF-8 limpo. Adicionar verificacao de encoding de JSONs ao doctor.ps1 | 1 dia | Critico - corretude | S12 |
| B-069 | Corrigir caminho duplicado em scripts - Fixar path em generate-release-package.ps1, test-template-copy.ps1, backup-engineer.ps1 (segmento .xforge/docs duplicado) | 0.5 dia | Critico - releases | S12 |
| B-070 | Corrigir backup-engineer-full.ps1 - Mudar referencia de engineer para .xforge/engineer | 0.5 dia | Critico - backups | S12 |
| B-071 | Corrigir CI workflow - Substituir --health flag inexistente em ci.yml por comando valido | 0.5 dia | Critico - CI/CD | S12 |
| B-072 | Criar arquivos de security gate - Criar engineer/security/golden-rules/ e releases-gates/ com checklists reais de seguranca | 2 dias | Critico - seguranca | S12 |
| B-073 | Implementar LGPD enforcement basico - Scan automatizado de dados pessoais em DTOs/entities. Verificacao de criptografia e consentimento | 3 dias | Critico - legal | S12 |

---

## P1 - Qualidade Alta v5.1.0

> Objetivo: Corrigir 15 problemas altos que afetam qualidade de produto, performance e seguranca.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-074 | Implementar LDV como codigo executavel - Criar script que orquestre analise -> decomposicao -> execucao -> validacao -> retry. Estado persistido em JSON | 5 dias | Alto - eficacia | S12 |
| B-075 | Corrigir referencias MediatR para XForge.MediatR - Auditar knowledge/ para substituir todas referencias | 1 dia | Alto - consistencia | S12 |
| B-076 | Consolidar agentes orquestradores - Fundir ceo-orquestrador e chefe-orquestrador em unico agente canonico | 1 dia | Alto - clareza | S12 |
| B-077 | Expandir secret scanner - Adicionar patterns para AWS keys, GitHub tokens, JWT, connection strings ao rag_local.py | 1 dia | Alto - seguranca | S12 |
| B-078 | Corrigir validate-rag.ps1 - Verificar LASTEXITCODE apos validate-no-secrets.ps1 corretamente | 0.5 dia | Alto - corretude | S12 |
| B-079 | Corrigir pre-push hook - Substituir health por status. Bloquear push em problemas criticos reais | 0.5 dia | Alto - CI/CD | S12 |
| B-080 | Implementar testes reais de RAG query - Reescrever test_query.py para invocar rag_local.py real | 2 dias | Alto - qualidade | S13 |
| B-081 | Corrigir complexity score maximo - Reconciliar scoring: max real e 19 nao 22. Remover +1 contexto nao definido | 0.5 dia | Alto - precisao | S13 |
| B-082 | Consolidar comandos de seguranca - Diferenciar security-golden-rule-check, audit, release-gate com checklists distintos | 2 dias | Alto - seguranca | S13 |

---

## P2 - Qualidade Media v5.1.0

> Objetivo: Corrigir 15 problemas medios que afetam manutenibilidade, performance e completude.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-083 | Preencher agentes diretor com conteudo - Adicionar orientacao de dominio especifico a 10+ agentes diretor vazios | 3 dias | Medio - eficacia | S13 |
| B-084 | Implementar busca semantica no RAG - Adicionar embedding-based search com scoring hibrido TF-IDF + cosine | 3 dias | Medio - performance | S13 |
| B-085 | Corrigir validate-kilo-strict.ps1 - Reconciliar allowed keys com doctor.ps1 | 0.5 dia | Medio - consistencia | S13 |
| B-086 | Padronizar encoding em file writes - Usar UTF-8 consistente em todos os scripts PowerShell | 1 dia | Medio - manutenibilidade | S14 |
| B-087 | Usar Push-Location/Pop-Location - Corrigir scripts que mudam working directory sem restaurar | 1 dia | Medio - corretude | S14 |
| B-088 | Cruzar glossario com knowledge - Adicionar referencias ao glossario em agentes e comandos relevantes | 1 dia | Medio - usabilidade | S14 |
| B-089 | Corrigir knowledge index - Atualizar contagem de documentos para numero real | 0.5 dia | Medio - confianca | S14 |
| B-090 | Implementar trigger automatico para ACE - Hook pos-comando que invoca feedback-capture automaticamente | 2 dias | Medio - autonomia | S15 |

---

## P3 - Qualidade Baixa v5.1.0

> Objetivo: Melhorias continuas de code quality e manutenibilidade.

| ID | Item | Esforco | Impacto | Sprint |
|----|------|---------|---------|--------|
| B-091 | Remover dead code - Remover linhas 144-146 de rag_cache.py e outros codigos mortos | 0.5 dia | Baixo - limpeza | S14 |
| B-092 | Padronizar nomenclatura de comandos - Usar hifen consistentemente, remover underscore variants | 1 dia | Baixo - consistencia | S14 |
| B-093 | Expandir .kilocodeignore - Adicionar *.crt, *.jks, *.p12, *.ovpn, credentials*, appsettings.json | 0.5 dia | Baixo - seguranca | S14 |
| B-094 | Adicionar type hints em rag_cache.py - Type hints em todas as funcoes | 0.5 dia | Baixo - type safety | S15 |
| B-095 | Corrigir test_chunking.py - Testar chunk_file() real em vez de metodo local | 0.5 dia | Baixo - testes | S15 |
| B-096 | Padronizar version numbering - Definir fonte unica de verdade para versao do projeto | 1 dia | Baixo - manutenibilidade | S14 |

## Referencias

- **OpenClaude:** https://github.com/Gitlawb/openclaude — inspiracao para agent routing, gRPC, diagnostics, MCP, hardening
- **Kilo Docs:** https://kilo.ai/docs/customize — compatibilidade com agents, skills, commands, workflows, Agent Manager
- **Agent Skills:** https://agentskills.io/specification — formato SKILL.md padrao
- **Kilo Repo:** https://github.com/Kilo-Org/kilocode — implementacao de referencia
- **Analise v4.0.0:** .xforge/backlog/BACKLOG.md (v4.0.0) — 25 itens concluidos como base
