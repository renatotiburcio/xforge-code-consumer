---
name: validacao-cruzada
description: Workflow de validacao cruzada multi-agente. Envia tarefa para 2+ agentes independentes, compara resultados e so aprova com consenso.
type: workflow
version: 1.0.0
agent: code
---

# Validacao Cruzada Multi-Agente

## Visao Geral

Para tarefas criticas (seguranca, LGPD, arquitetura, fiscais), o XForge envia a mesma tarefa para 2+ agentes independentes, compara os resultados usando o result-comparator (B-049), e so considera validado quando ha consenso.

## Quando Usar

- Tarefas de seguranca (autenticacao, autorizacao, criptografia)
- Tarefas LGPD (dados pessoais, consentimento, portabilidade)
- Tarefas fiscais (NFe, NFSe, SPED, eSocial)
- Tarefas de arquitetura (decisoes estruturais)
- Tarefas com complexidade CRITICA

## Diagrama de Fluxo

```
Tarefa Critica identificada
        |
        v
[1] Selecionar 2+ agentes independentes
        |
        v
[2] Enviar tarefa para cada agente (paralelo)
        |
        v
[3] Aguardar resultados de todos
        |
        v
[4] result-comparator (B-049) compara resultados
        |
        +-- Consenso --> [5] Aprovar resultado
        |
        +-- Divergencia --> [6] Arbitragem
        |
        +-- Conflito --> [7] Escalacao humana
```

## Passo 1: Selecao de Agentes

**Criterios**:
- Agentes devem ter expertise complementar (ex: security + architecture)
- Nao podem ser o mesmo agente com modelos diferentes
- Minimo 2, maximo 5 agentes

**Pares recomendados**:

| Dominio | Agente 1 | Agente 2 | Arbitro |
|---------|----------|----------|---------|
| Seguranca | security-lgpd-expert | continuous-security-architect | human-review |
| Arquitetura | architecture-enterprise-expert | dotnet-enterprise-expert | human-review |
| Fiscal | fiscal-tax-expert | compliance | human-review |
| Qualidade | quality-gates | testing-qa-expert | human-review |

## Passo 2: Envio Paralelo

Cada agente recebe:
- A tarefa original (contexto completo)
- O mesmo nivel de complexidade
- Output esperado (formato JSON estruturado)
- Timeout: 10 minutos por agente

## Passo 3: Coleta de Resultados

Aguardar todos os agentes terminarem.
Se algum agente timeout: usar resultado parcial + marcar como "incompleto".

## Passo 4: Comparacao (result-comparator)

Usar o skill result-comparator (B-049) para:
1. Comparar outputs estruturados
2. Identificar consenso (campos iguais em todos)
3. Identificar divergencias (campos diferentes)
4. Calcular score de consenso (0-100%)

### Niveis de Consenso

| Score | Classificacao | Acao |
|-------|---------------|------|
| 90-100% | Consenso total | Aprovar automaticamente |
| 70-89% | Consenso parcial | Aprovar com revisao |
| 50-69% | Divergencia moderada | Arbitragem por 3o agente |
| 0-49% | Conflito | Escalacao para humano |

## Passo 5: Aprovacao

Se consenso >= 70%:
- Usar resultado majoritario
- Registrar decisao no knowledge graph
- Prosseguir com execucao

## Passo 6: Arbitragem

Se consenso < 70%:
- Selecionar agente arbitro (da tabela de pares)
- Enviar resultados divergentes + contexto
- Arbitro decide ou solicita informacoes adicionais

## Passo 7: Escalacao Humana

Se arbitragem falhar:
- Apresentar todos os resultados ao usuario
- Incluir analise de divergencias
- Solicitar decisao manual
- Registrar decisao para aprendizado futuro

## Tratamento de Erros

| Erro | Acao |
|------|------|
| Agente indisponivel | Usar agente alternativo da lista |
| Timeout | Usar resultado parcial + marcar |
| Todos divergem | Escalacao humana imediata |
| Resultado vazio | Retry com agente diferente |

## Metricas

- Taxa de consenso por dominio
- Tempo medio de validacao
- Taxa de escalacao humana
- Divergencias mais comuns

## Integracoes

- **B-049 (result-comparator)**: compara resultados
- **B-029 (LDV loop)**: usa validacao cruzada para tarefas CRITICAS
- **B-034 (feedback-capture)**: registra resultado da validacao
