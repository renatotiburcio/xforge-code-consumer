---
description: Ajuda, orientação e escolha de fluxo
agent: code
---

# /ajuda

## Objetivo

Ajuda, orientação e escolha de fluxo

## Regra REV37

Este é um comando público. O usuário deve preferir este comando em vez de escolher comandos internos.

## Roteamento interno

O Chief Architect deve interpretar a intenção, recuperar memória, selecionar experts e acionar automaticamente os comandos internos necessários.

Comandos internos candidatos:

- `/xforge-ajuda`
- `/xforge-modo-simples`

## Saída obrigatória

- intenção entendida;
- experts selecionados;
- plano de execução;
- comandos internos acionados;
- quality/security gates;
- resultado;
- memória atualizada;
- dashboard/registries atualizados quando aplicável.

## Exemplos

```
/ajuda
/ajuda com parametros especificos do projeto
```
