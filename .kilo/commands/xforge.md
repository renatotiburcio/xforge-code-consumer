---
name: xforge
description: Roteamento inteligente para qualquer solicitacao.
agent: code
---

# /xforge

## Categoria

orquestracao

## Objetivo

Roteamento inteligente para qualquer solicitacao.

## Comandos publicos canonicos

- `/analisar-projeto`
- `/criar-projeto`
- `/desenvolver`
- `/qualidade`
- `/seguranca`
- `/conhecimento`
- `/memoria`
- `/documentacao`
- `/release`

## Aliases e comandos internos

Aliases existem para compatibilidade. A IA deve preferir os comandos publicos canonicos e usar comandos internos apenas como rotas.

## Fluxo obrigatorio

1. Identificar intencao.
2. Recuperar memoria relevante sob demanda.
3. Selecionar agente primario.
4. Selecionar skills minimas.
5. Aplicar policies, RBAC, seguranca e golden rules.
6. Escolher subcomando adequado.
7. Executar com validacao.
8. Atualizar memoria, audit trail, docs e knowledge graph quando aplicavel.


## Exemplos

```
/xforge
/xforge criar uma API de pagamentos
/xforge analisar o projeto atual
```
