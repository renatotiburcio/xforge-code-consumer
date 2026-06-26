---
name: cross-project-learning
description: Use when transferring knowledge, patterns, or lessons learned between projects or modules.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# cross-project-learning

## Objetivo

Transferir aprendizados entre projetos para evitar repetição de erros e reaplicar soluções comprovadas.

## O que Transferir

| Tipo | Exemplo | Prioridade |
|------|---------|:----------:|
| Decisões arquiteturais | "XForge.MediatR > MediatR" | Alta |
| Padrões de código | "Extension methods para DI" | Alta |
| Lições de incidentes | "EF Core Include() causa N+1" | Crítica |
| Configurações | "Rate limiting em 100/min" | Média |
| Ferramentas | "TestContainers para integration tests" | Média |

## Procedimento

### 1. Extrair
- Identificar aprendizado significativo
- Verificar se já existe em outro projeto
- Formatar: contexto → decisão → resultado

### 2. Validar
- Verificar se é aplicável a outros projetos
- Verificar se não é específico de contexto
- Avaliar confiança (trust-score)

### 3. Transferir
- Salvar em .xforge/memory/global/
- Atualizar knowledge graph
- Notificar projetos afetados
- Criar PR se aplicável

### 4. Rastrear
- Registrar de onde veio
- Registrar para onde foi
- Monitorar adoção

## Regras

- NUNCA transferir dados sensíveis
- Sempre documentar contexto de origem
- Validar aplicabilidade antes de transferir
- Manter traceabilidade
