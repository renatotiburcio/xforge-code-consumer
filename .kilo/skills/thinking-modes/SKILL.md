---
name: thinking-modes
description: Use when selecting FAST, CHEAP, SAFE, DEEP, ENTERPRISE, OFFLINE, or RESEARCH execution mode.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# thinking-modes

## Objetivo

Selecionar o modo de execução adequado para cada tarefa, equilibrando velocidade, custo e qualidade.

## Modos Disponíveis

| Modo | Quando Usar | Modelo Recomendado | Custo |
|------|-------------|-------------------|-------|
| **FAST** | Edições simples, typos, formatação | ollama/llama3 | Grátis |
| **CHEAP** | Refactors pequenos, CRUD simples | openrouter/auto | Baixo |
| **SAFE** | Features novas, código com testes | claude-sonnet-4 | Médio |
| **DEEP** | Arquitetura, multi-file, patterns | claude-sonnet-4 | Médio |
| **ENTERPRISE** | ERP, domínio complexo, compliance | claude-opus-4 | Alto |
| **OFFLINE** | Sem internet, dados sensíveis | ollama/llama3 | Grátis |
| **RESEARCH** | POC, spike, exploração técnica | claude-sonnet-4 | Médio |

## Procedimento de Seleção

1. Avaliar complexidade da tarefa (score 0-19)
2. Verificar se há restrição de dados (LGPD → ENTERPRISE ou OFFLINE)
3. Verificar conectividade (offline → OFFLINE)
4. Verificar orçamento (custo disponível)
5. Selecionar modo com melhor custo-benefício
6. Registrar escolha no audit trail

## Regras

- Dados sensíveis NUNCA saem do ambiente local
- Tarefas com score > 15 → sempre ENTERPRISE
- Tarefas com score < 4 → sempre FAST ou CHEAP
- Em dúvida → SAFE (padrão seguro)
