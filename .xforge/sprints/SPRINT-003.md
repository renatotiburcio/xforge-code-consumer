---
id: sprint-003
type: sprint
tags: [sprint, p2, mcp, search, tests, hooks, docs, privacy]
owner: project-team
version: 1.1.0
updated: 2026-06-09
---

# Sprint 3: P2

## Status: CONCLUIDA — MCP, Search, Tests, Hooks, Docs, Privacy

## Resumo
Terceira sprint do template. Foco em infraestrutura: MCP servers pre-configurados, busca web, testes unitarios RAG, git hooks, documentacao do template, e verificacao de privacidade.

## Periodo
- **Inicio:** 2026-06-09
- **Fim:** 2026-07-20
- **Duracao:** 6 semanas

## Objetivos
1. Configurar MCP servers (PostgreSQL, Redis, RabbitMQ) (B-013)
2. Criar comando /buscar com web search (B-014)
3. Escrever testes unitarios para scripts RAG (B-015)
4. Implementar git hooks (pre-commit doctor, pre-push) (B-016)
5. Documentar template: como usar, como extender (B-017)
6. Criar script de verificacao de privacidade (B-018)

## Backlog Items
- B-013, B-014, B-015, B-016, B-017, B-018

---

## B-016: Git Hooks

### Escopo
Criar hooks no `.githooks/`:
- `pre-commit`: roda doctor.ps1 (quick mode) e impede commit se houver erros
- `pre-push`: roda RAG health check e impede push se houver erros

### Instalacao
```powershell
# Configurar git para usar hooks do projeto
git config core.hooksPath .githooks
```

---

## B-015: Testes Unitarios RAG

### Escopo
Criar `tests/rag/` com testes para:
- `test_chunking.py`: testa chunking de documentos
- `test_index.py`: testa criacao de indice
- `test_query.py`: testa queries no indice
- `test_config.py`: testa validacao de config RAG

---

## B-018: Privacy Verification

### Escopo
Criar `.xforge/scripts/verify-privacy.ps1` que:
- Scanna arquivos por padroes de dados sensiveis (CPF, CNPJ, email, telefone, API keys)
- Verifica .gitignore para arquivos sensiveis
- Gera relatorio de risco

---

## B-013: MCP Servers

### Escopo
Configurar MCP servers em `.kilo/mcp/`:
- `postgresql.json`: conexao com PostgreSQL
- `redis.json`: conexao com Redis
- `rabbitmq.json`: conexao com RabbitMQ

---

## B-014: Comando /buscar

### Escopo
Criar comando `.kilo/commands/buscar.md` com:
- Web search via DuckDuckGo API
- Scraping via Firecrawl
- Integracao com knowledge base local

---

## B-017: Documentacao

### Escopo
Criar documentacao em `.xforge/docs/`:
- `COMO-USAR.md`: guia de inicio rapido
- `COMO-ESTENDER.md`: guia para extender o template
- `ARQUITETURA.md`: visao arquitetural

---

## Definition of Done
- [x] Git hooks instalados e funcionando
- [x] Testes unitarios RAG passando (14/14)
- [x] Privacy verification script funcional
- [x] MCP servers configurados (3: PostgreSQL, Redis, RabbitMQ)
- [x] /buscar command criado
- [x] Documentacao do template criada (3 docs)

## Metricas
| Indicador | Meta |
|-----------|------|
| doctor.ps1 erros | 0 |
| RAG testes passando | 100% |
| Git hooks ativos | 2 (pre-commit, pre-push) |
| MCP servers | 3 configurados |
| Comandos com exemplos | 30+ |
