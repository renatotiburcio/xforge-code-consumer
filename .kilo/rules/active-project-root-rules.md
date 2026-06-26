# Active Project Root Rules

> **DR-0180**: Stack-agnostic. O sistema NAO assume stack. Cada novo projeto tem seu proprio stack, detectado por sinais do projeto ativo.

## Regra absoluta

Quando o usuário pedir para gerar um novo app, módulo, pacote, biblioteca, componente, API, Blazor app, worker ou qualquer novo projeto dentro do repositório atual, o Engineer deve gerar **dentro da pasta do projeto ativa**.

## Proibido

Não criar automaticamente uma pasta externa com o nome do app ao lado do projeto atual.

Errado:

```text
D:\dev\
├── ProjetoAtual\
└── NovoApp\
```

## Correto

Criar dentro do root ativo:

```text
D:\dev\ProjetoAtual\
├── src\NovoApp\
```

ou conforme padrão detectado:

```text
D:\dev\ProjetoAtual\
├── src\NovoApp\
```

## Procedimento obrigatório

Antes de criar qualquer app:

1. Detectar o root ativo do workspace.
2. Detectar se existe solution `.sln` ou `.slnx`.
3. Detectar estrutura atual:
   - `src/`
   - `packages/`
   - `modules/`
   - `tests/`
4. Perguntar ou inferir o destino correto.
5. Criar dentro do root ativo.
6. Adicionar à solution existente quando aplicável.
7. Atualizar PROJECT-DNA.
8. Atualizar memória.

## Se houver dúvida

Perguntar:

```text
Deseja criar dentro de src/, modules/ ou packages/?
```