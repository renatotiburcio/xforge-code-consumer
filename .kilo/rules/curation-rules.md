# curation-rules

Curadoria de memória e conhecimento é obrigatória e contínua.

## Ações de Curadoria

### Detectar Duplicidade
- Buscar entradas similares antes de criar nova
- Se similaridade > 80% → merge, não duplicar
- Manter a versão mais completa e atualizada

### Comprimir Memória
- Entradas > 500 palavras → resumir para 100-200
- Manter: decisão, motivo, resultado, fonte
- Remover: exemplos óbvios, redundâncias

### Mover para Cold Storage
- Entradas > 30 dias sem uso → `.xforge/memory/archive/`
- Entradas > 90 dias sem uso → compressão automática
- Nunca deletar, sempre arquivar

### Depreciar Conteúdo
- Contradito por informação mais recente → deprecated
- Fonte original desatualizada → deprecated
- Não utilizado em 6+ meses → candidato a deprecated

### Promover Padrões
- Trust score > 80 + usado 3+ vezes → candidato a padrão
- Validado por 2+ projetos → padrão confirmado
- Documentar como golden standard

### Remover Lixo
- Entradas sem fonte e sem confiança → remover
- Entradas duplicadas após merge → remover original
- TODOs sem issue associada → remover ou criar issue

## Frequência

| Ação | Frequência |
|------|:----------:|
| Deduplicação | Semanal |
| Compressão | Mensal |
| Cold storage | Mensal |
| Depreciação | Trimestral |
| Promoção | Sob demanda |
| Limpeza | Mensal |

## Regras

- NUNCA deletar decisões permanentes
- Sempre manter traceabilidade
- Curadoria deve ser auditável
- Resultado da curadoria → audit trail
