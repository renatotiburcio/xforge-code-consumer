# Auto-Discover Macros Rule (v3.38.0)

> Regra institucional: o template aprende com uso. Detecta chains recorrentes e SUGERE criar macros. Nunca cria sem consentimento explícito do usuário.

## 1. Conceito

O template observa padrões de uso (chains de comandos). Quando detecta recorrência:

1. Sugere macro (nome + rationale + preview)
2. Explica o motivo (por quê vale criar)
3. Mostra como funcionaria (exemplo de uso)
4. Pede consentimento explícito
5. Se autorizado, cria o macro + atualiza docs

## 2. Tracking (gitignored)

Os dados de uso ficam em .usage/ (gitignored):

`
.usage/                    # gitignored (runtime data)
  commands.log             # cada invocação: timestamp, command, args
  patterns.json            # clusters de chains detectadas
  rejected-macros.json     # sugestões rejeitadas (cooldown 30 dias)
`

Nenhuma informação pessoal é coletada. Apenas: qual comando, quando, com quais flags.

## 3. Heurística de detecção

Um padrão é considerado para sugestão QUANDO:

1. Mesma chain (mesma sequência de comandos com mesmos args) >= 3 vezes
2. Em janela de 7 dias
3. Chain tem >= 2 comandos
4. Nenhuma macro existente cobre essa chain
5. Não foi rejeitada nos últimos 30 dias

## 4. Fluxo de sugestão

`
macro-discovery triggered
  ->
  1. Ler .usage/commands.log
  2. Agrupar chains similares (Jaccard similarity > 0.7)
  3. Filtrar por >= 3 ocorrências em 7 dias
  4. Para cada padrão encontrado:
     a. Propor nome canônico (kebab-case en, alias pt-BR)
     b. Calcular rationale (economia de tempo estimada)
     c. Mostrar preview do comando composto
  5. Apresentar ao usuário:
     >> Detectei que você usou [chain] 5 vezes esta semana. <<
     >> Posso criar a macro /[nome] que faz isso em 1 linha? <<
     >> Responder com: Y / n / edit <<
  6. Se Y: criar .kilo/commands/<nome>.md + atualizar docs
  7. Se n: marcar rejected-macros.json com timestamp
  8. Se edit: usuário personaliza antes de criar
`

## 5. Trigger

A sugestão é disparada:

1. Automaticamente: após N=20 invocações OU semanalmente (whichever vem antes)
2. Manualmente: /macro-suggest (comando canônico)
3. Via Genius Council: /genius-council (com argumento: criar macro para [padrão])

## 6. Criação do macro quando autorizado

1. Nome canônico em kebab-case en (prototype, ship, discover)
2. Alias pt-BR (/prototipar, /entregar, /descobrir)
3. Arquivo: .kilo/commands/<nome>.md com template canônico
4. Frontmatter: name, description, agent=code, category=xforge-core
5. Body: O que faz, sintaxe, exemplos, quando usar, quando NÃO usar
6. Atualizar: docs/SUMMARY.md (tabela de macros)
7. Atualizar: docs/manual/06-commands.html (adicionar ao exemplo)
8. Criar DR: DR-XXXX-novo-macro-<nome>.md (registro da decisão)
9. Atualizar: CHANGELOG.md (entrada da release)
10. Memory entry: .xforge/memory/learning.jsonl (registro do aprendizado)

## 7. Quando NÃO aplicar

- Chain envolve comandos com side-effect destrutivo (--destrutivo, --no-confirm)
- Chain é específica de um único projeto (não generaliza)
- Chain existe mas é trivial (1-2 comandos, já é macro)
- Usuário desabilitou discovery explicitamente (kilo.jsonc: auto_discover: false)

## 8. Configuração

Adicionar a kilo.jsonc:

`jsonc
{
  auto_discover_macros: {
    enabled: true             // default: true
    threshold: 3                // ocorrências mínimas
    window_days: 7             // janela de tempo
    cooldown_days: 30          // após rejeitar, esperar
    auto_suggest: true         // notificar proativamente
    auto_create: false          // NUNCA criar sem consent (safety)
  }
}
`

## 9. Integração com Genius Council

Quando macro-discovery detecta um padrão em timestamp:

1. Sugere nome canônico (consistente com naming-convention.md)
2. Aplica GCF 3-phase mini:
   - Discovery: o que a chain faz
   - Decisão: macro faz sentido pós gasta o tempo?
   - Risks: 5 Guardians + AG999 7 perguntas
3. Só então apresenta ao usuário para consentimento

## 10. Referências

- .kilo/skills/macro-discovery/SKILL.md (análise)
- .kilo/commands/macro-suggest.md (trigger manual)
- .kilo/rules/naming-convention.md (padrão de nmes)
- .kilo/rules/loop-discipline.md (qualidade)
- docs/manual/06-commands.html (manual)
- DR-0127 (este design)
- DR-0126 (composable commands)
- DR-0124 (sequências + naming)
- .xforge/feedback/errors-solutions-graph.json (padrões de uso)
- STATUS.md (evolução das macros)
