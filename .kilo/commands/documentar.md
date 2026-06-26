---
name: documentar
description: Criar, atualizar e sincronizar documentacao tecnica, manuais, changelog e exemplos.
agent: code
category: xforge-public
---

# /documentar

## Objetivo
Criar, atualizar e sincronizar toda a documentacao do projeto: manuais, docs tecnicas, changelog, exemplos.

## Sub-comandos

| Sub-comando | Acao |
|-------------|------|
| `/documentar gerar` | Gerar documentacao a partir do codigo |
| `/documentar atualizar` | Atualizar documentacao existente |
| `/documentar validar` | Validar consistencia da documentacao |
| `/documentar sync` | Sincronizar manual HTML com markdown |

## Procedimento

### Gerar
1. Analisar estrutura do projeto
2. Gerar README, API docs, changelog
3. Criar diagramas C4 se necessario

### Atualizar
1. Identificar documentacao desatualizada
2. Atualizar com mudancas recentes
3. Validar consistencia

### Validar
1. Verificar referencias cruzadas
2. Verificar exemplos funcionais
3. Verificar formatacao

### Sync
1. Ler markdown fonte
2. Atualizar HTML canônico
3. Verificar cache-busting

## Uso
```
/documentar gerar
/documentar atualizar
/documentar validar
/documentar sync
```
