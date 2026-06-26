---
id: sprint-002
type: sprint
tags: [sprint, p1, provider, doctor, routing, naming, examples, config]
owner: project-team
version: 1.1.0
updated: 2026-06-09
---

# Sprint 2: P1 — Provider, Routing, Naming, Config

## Status: ✅ CONCLUIDA

## Resumo
Segunda sprint do template. Foco em experiencia do desenvolvedor: comando /provider para troca de modelo, validacao de conectividade no doctor, routing de modelos por agente, unificacao de nomes em portugues, exemplos de uso nos comandos, e config persistente.

## Periodo
- **Inicio:** 2026-06-09
- **Fim:** 2026-06-22
- **Duracao:** 14 dias corridos

## Objetivos
1. Criar comando /provider para troca de modelo on-the-fly (B-007)
2. Expandir doctor.ps1 com validacao de conectividade (B-008)
3. Adicionar agent routing no kilo.jsonc (B-009)
4. Unificar nomes de agentes em portugues (B-010)
5. Adicionar exemplos de uso nos comandos (B-011)
6. Criar ~/.xforge/config.json para preferencias persistentes (B-012)

## Backlog Items
- B-007, B-008, B-009, B-010, B-011, B-012

---

## B-007: Comando /provider

### Escopo
Criar comando .kilo/commands/provider.md que permite ao usuario:
- Listar modelos disponiveis
- Trocar modelo ativo on-the-fly
- Persistir escolha em ~/.xforge/config.json

### Estructura
`powershell
# provider.md define:
# /provider list          → lista modelos disponiveis
# /provider set <model>   → troca modelo ativo
# /provider status        → mostra modelo atual
# /provider reset         → volta ao padrao do kilo.jsonc
`

### Modelos Suportados
| Provider | Modelos |
|----------|---------|
| Anthropic | claude-sonnet-4-20250514, claude-opus-4-20250514 |
| OpenAI | gpt-4o, gpt-4o-mini, o1-preview |
| Google | gemini-2.5-pro, gemini-2.5-flash |
| xAI | grok-3 |

---

## B-008: Doctor Connectivity

### Escopo
Expandir doctor.ps1 com:
- Connectivity check: ping no provider ativo
- Model availability check: verificar se modelo existe no provider
- Latency report: tempo de resposta do modelo
- Auth validation: verificar API key configurada

### Novas Validacoes
`
kilo.jsonc
[OK]    Modelo ativo responde em <5s
[OK]    API key configurada
[WARN]  Latencia alta (>3s)
[ERR]   Modelo nao encontrado no provider
`

---

## B-009: Agent Routing

### Escopo
Adicionar "routing" section no kilo.jsonc para mapear modelos por agente:

`jsonc
{
  "agent": {
    "code": { "model": "anthropic/claude-sonnet-4-20250514" },
    "plan": { "model": "anthropic/claude-sonnet-4-20250514" },
    "debug": { "model": "openai/gpt-4o" },
    "docs-writer": { "model": "openai/gpt-4o", "temperature": 0.2 }
  },
  "routing": {
    "defaultProvider": "openrouter",
    "providers": {
      "openrouter": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "apiKey": "env:OPENROUTER_API_KEY"
      },
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "apiKey": "env:OPENAI_API_KEY"
      },
      "anthropic": {
        "baseUrl": "https://api.anthropic.com",
        "apiKey": "env:ANTHROPIC_API_KEY"
      },
      "google": {
        "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
        "apiKey": "env:GOOGLE_API_KEY"
      }
    }
  }
}
`

---

## B-010: Unificar Nomes de Agentes

### Escopo
Renomear agentes para portugues com padrao 
ome-funcionalidade.md:

| Atual | Novo nome |
|-------|-----------|
| i-provider-router.md | provedor-ia-router.md |
| rchitect-solution.md | rquiteto-solucao.md |
| code-reviewer.md | 
evisor-codigo.md |
| code-simplicity-reviewer.md | 
evisor-simplicidade.md |
| devops-observability.md | devops-observabilidade.md |
| devops-pipeline.md | devops-pipeline.md |
| engineer-dotnet-api.md | engenheiro-dotnet-api.md |
| engineer-dotnet-researcher.md | engenheiro-dotnet-pesquisador.md |
| engineer-frontend.md | engenheiro-frontend.md |
| engineer-software.md | engenheiro-software.md |
| engineer-software-researcher.md | engenheiro-software-pesquisador.md |
| git-manager.md | gerenciador-git.md |
| knowledge-ingestion-engineer.md | engenheiro-ingestao-conhecimento.md |
| memory-curator-engineer.md | engenheiro-curador-memoria.md |
| multi-agent-conductor.md | condutor-multi-agente.md |
| performance-profiler.md | perfilador-performance.md |
| quality-gates-engineer.md | engenheiro-portoes-qualidade.md |
| specialist-benchmark.md | especialista-benchmark.md |
| specialist-knowledge-curation.md | especialista-curadoria-conhecimento.md |
| specialist-policy-engine.md | especialista-motor-politica.md |
| specialist-rbac.md | especialista-rbac.md |
| rchitecture-visual-designer.md | designer-visual-arquitetura.md |
| manager-event-bus.md | gerenciador-barramento-eventos.md |
| manager-memory.md | gerenciador-memoria.md |
| manager-state-machine.md | gerenciador-maquina-estados.md |
| security-threat-modeler.md | modelador-ameacas-seguranca.md |
| 	ech-debt-manager.md | gerenciador-divida-tecnica.md |
| 	ech-lead-orchestrator.md | orquestrador-tech-lead.md |
| 	ester-unit.md | 	estador-unitario.md |
| 	ester-e2e.md | 	estador-e2e.md |
| pi-designer.md | designer-api.md |
| database-architect.md | rquiteto-banco-dados.md |
| infrastructure-engineer.md | engenheiro-infraestrutura.md |
| ml-engineer.md | engenheiro-ml.md |
| data-engineer.md | engenheiro-dados.md |
| cloud-architect.md | rquiteto-nuvem.md |

---

## B-011: Exemplos de Uso nos Comandos

### Escopo
Adicionar secao "Exemplos" em cada comando existente em .kilo/commands/:
- Mostrar 2-3 exemplos de uso real
- Incluir parametros comuns
- Documentar output esperado

---

## B-012: Config Persistente

### Escopo
Criar ~/.xforge/config.json template:
`json
{
  "version": "1.0.0",
  "provider": {
    "active": "openrouter",
    "model": "anthropic/claude-sonnet-4-20250514",
    "fallbackProviders": ["openai", "anthropic"]
  },
  "preferences": {
    "language": "portugues",
    "doctorOnStartup": false,
    "autoReindex": true
  },
  "paths": {
    "globalSkills": "~/.xforge/skills",
    "globalCommands": "~/.xforge/commands"
  }
}
`

---

## Definition of Done
- [x] /provider command criado e funcional
- [x] doctor.ps1 com connectivity check
- [x] kilo.jsonc com routing section
- [x] 36 agentes renomeados em portugues
- [x] Exemplos em 8 comandos publicos (26+ total com exemplos)
- [x] ~/.xforge/config.json template criado

## Metricas
| Indicador | Meta |
|-----------|------|
| Comandos com exemplos | 100% |
| Agentes renomeados | 100% (36) |
| doctor connectivity check | Sim |
| doctor.ps1 erros | 0 |