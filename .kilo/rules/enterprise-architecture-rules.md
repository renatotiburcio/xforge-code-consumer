# enterprise-architecture-rules

Arquitetura enterprise exige disciplina, desacoplamento e rastreabilidade.

## Regras

### Desacoplamento
- Modulos NAO devem depender diretamente um do outro
- Usar eventos (event-bus) para comunicacao cross-module
- Interfaces (abstracoes) entre camadas, nunca implementacoes
- Se precisa de `using` de outro modulo -> possivel violacao

### Bounded Contexts
- Cada dominio tem seu proprio bounded context
- Entidades de um context NAO devem vazar para outro
- Shared kernel apenas para primitivos comuns (Value Objects)
- Context mapping explicito entre bounded contexts

### Integracoes Rastreaveis
- Toda integracao externa DEVE ter:
  - Contrato documentado (OpenAPI/schema)
  - Teste de contrato (WireMock/Pact)
  - Log de chamadas
  - Retry/circuit breaker

### Eventos > Acoplamento Direto
- Comunicacao cross-module -> evento (nao chamada direta)
- Evento DEVE ter: id, type, timestamp, data, correlationId
- Handler DEVE ser idempotente
- Dead letter queue para eventos nao processados

### Impact Analysis Cross-Module
- Antes de mudar interface publica -> impact analysis obrigatorio
- Mudanca em shared kernel -> notificar todos os modulos afetados
- Documentar impacto em `.xforge/decisions/`

### Semantic Entity Map
- Manter mapa de entidades por bounded context
- Atualizar quando entidade e criada/modificada
- Verificar consistencia no pipeline de build

## Verificacao

```powershell
# Verificar dependencias cross-module
dotnet list package --include-transitive | Select-String "ProjectReference"
```

## Proibido

- Dependency injection direta entre modulos (usar interfaces)
- Shared database entre bounded contexts (usar eventos)
- God classes que conhecem todos os modulos
- Mudancas cross-module sem impact analysis
