# knowledge-rules

Todo conhecimento deve ter origem, confiança e rastreabilidade.

## Regras

### Origem
- Toda entrada de conhecimento DEVE ter campo `source` (URL, arquivo, PR, conversa)
- Sem fonte = não usar como referência
- Fonte primária > fonte secundária > inferência

### Confiança
- Trust score mínimo para uso: 50
- Trust score para promoção: 80
- Fonte oficial = 100, Blog = 60, AI-generated = 40
- Revalidar trimestralmente

### Rastreabilidade
- Cada entrada DEVE ter: id, type, domain, source, trustScore, createdAt
- **Aplicabilidade por stack (DR-0180)**: cada entry DEVE ter campo `applicabilityScope` em INDEX.json
  - `["*"]` = universal
  - `["dotnet"]`, `["python"]`, `["node"]`, etc = especifico por stack
  - Router filtra entries incompativeis com o projeto ativo
- Atualizar `lastValidated` ao usar
- Manter histórico de mudanças

### Armazenamento
- Decisões → `.xforge/decisions/`
- Aprendizados → `.xforge/learning/`
- Conhecimento → `.xforge/knowledge/`
- Global → `.xforge/memory/global/`

### Lifecycle
- Create → Active (confiança ≥ 50)
- Active → Deprecated (contradito ou obsoleto)
- Nunca deletar decisões permanentes
- Arquivar entradas > 90 dias sem uso

## Proibido

- Usar conhecimento sem fonte
- Confiar em AI-generated sem validação
- Deletar decisões arquiteturais
- Misturar dados sensíveis com conhecimento público
