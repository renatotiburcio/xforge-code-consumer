# Multi-Agent Orchestration — XForge Engineer

## Visão Geral

Quando uma tarefa é complexa o suficiente, o sistema coordena múltiplos agentes trabalhando em paralelo. Um **Orchestrator** coordena, e agentes especializados executam suas partes.

## Quando Usar Multi-Agent

| Cenário | Agentes Necessários | Ganho |
|---------|---------------------|-------|
| Criar módulo fiscal completo | Fiscal + Code + Tests + Docs | 4x mais rápido |
| Refatorar grande escala | Analysis + Code + Tests + Review | 3x mais rápido |
| Audit de segurança completo | Security + Code + Docs | 3x mais rápido |
| Criar feature com testes | Code + Tests + Coverage | 2x mais rápido |
| Migrar banco de dados | Analysis + Migration + Tests | 3x mais rápido |

## Arquitetura

```
                    ┌─────────────────┐
                    │   Orchestrator   │
                    │   (Router 7B)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ─¼              ─¼              ─¼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Agent A  │  │ Agent B  │  │ Agent C  │
        │ (Worker) │  │ (Worker) │  │ (Worker) │
        │ 72B      │  │ 72B      │  │ 72B      │
        └──────────┘  └──────────┘  └──────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────┴────────┐
                    │  Merge & Validate│
                    └─────────────────┘
```

## Agentes Disponíveis

### Agent: Fiscal Specialist
- **Modelo**: qwen2.5:72b
- **Especialidade**: Tabelas fiscais, ICMS, PIS, COFINS, eSocial, SPED
- **Entrada**: Requisito fiscal + contexto do projeto
- **Saída**: Services, validações, configurações fiscais

### Agent: Code Builder
- **Modelo**: qwen2.5:72b
- **Especialidade**: Geração de código C#, Clean Architecture, patterns
- **Entrada**: Spec + padrões do projeto
- **Saída**: Controllers, Services, DTOs, Configurações

### Agent: Test Creator
- **Modelo**: qwen2.5:14b
- **Especialidade**: xUnit, FluentAssertions, Moq, Testcontainers
- **Entrada**: Código gerado + domain rules
- **Saída**: Testes unitários + integração

### Agent: Documentation Writer
- **Modelo**: qwen2.5:7b
- **Especialidade**: XML comments, Swagger docs, README
- **Entrada**: Código + API endpoints
- **Saída**: Documentação completa

### Agent: Security Reviewer
- **Modelo**: qwen2.5:72b
- **Especialidade**: OWASP, LGPD, JWT, encryption
- **Entrada**: Código + configurações
- **Saída**: Lista de vulnerabilidades + fixes

### Agent: Performance Analyst
- **Modelo**: qwen2.5:14b
- **Especialidade**: N+1 queries, memory leaks, async issues
- **Entrada**: Código + queries
- **Saída**: Otimizações sugeridas

## Workflow de Orchestração

### Exemplo: "Criar módulo de pagamento com testes e docs"

```
1. Orchestrator analisa o pedido
   → Detecta: complexidade L, 4 domínios (code, tests, docs, fiscal)

2. Orchestrator delega em paralelo:
   → Agent A (Code Builder): Criar PaymentService, PaymentController, DTOs
   → Agent B (Fiscal Specialist): Validar regras de pagamento (NFC-e, SAT)
   → Agent C (Test Creator): Criar testes unitários para PaymentService
   → Agent D (Documentation): Criar Swagger docs e XML comments

3. Agentes trabalham em paralelo (cada um com seu contexto otimizado)

4. Orchestrator recebe resultados:
   → Agent A: 3 arquivos criados
   → Agent B: 1 configuração fiscal validada
   → Agent C: 12 testes criados
   → Agent D: Documentação completa

5. Orchestrator valida:
   → Todos os testes passam? ✅
   → Conflitos entre agentes? ❌ Nenhum
   → Padrões consistentes? ✅

6. Merge final + relatório
```

## Comando

```
/multi-agent criar módulo fiscal completo com testes e docs
/multi-agent refatorar módulo de pagamentos (code + tests + security)
/multi-agent audit completo (security + performance + tests)
```

## Limitações

1. **VRAM**: Com 16GB VRAM, máximo 2 Workers simultâneos (cada um ~10GB)
2. **Contexto**: Cada agente recebe apenas o contexto necessário (não o projeto inteiro)
3. **Conflitos**: Orchestrator detecta e resolve conflitos entre agentes
4. **Sequencial quando necessário**: Agentes com dependência rodam em sequência

## Métricas

| Métrica | Meta |
|---------|------|
| Speedup vs. agente único | 2-4x |
| Conflitos entre agentes | < 5% |
| Qualidade mantida | > 95% (mesmo resultado) |
| Uso de VRAM | < 14GB (2 Workers) |
