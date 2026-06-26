# Feature Mode Template for /forge (v3.55.0)

Add a new feature to an existing project. Uses Knowledge Context to align with existing patterns.

## Command syntax
```bash
/forge feature <name> --entity <EntityName> --endpoint <METHOD> <path>
/forge feature integracao-whatsapp --entity Pedido --endpoint POST /api/pedidos/{id}/whatsapp
/forge feature crud-clientes --entity Cliente
```

## Flow (5 steps)
1. Detect existing project (auto-scan for .sln, .csproj)
2. Load Knowledge Context (auto, from .xforge/knowledge/projects/<name>/ if exists)
3. Ingest IDEAS (check IDEAS.md for related features)
4. Question (5-10 questions about the feature)
5. Generate (CQRS commands/queries + endpoint + tests + docs)

## Questions (10 max)
1. Feature description? (from IDEAS.md or user input)
2. Which entity does it touch? (auto-detect)
3. CQRS split? (command, query, both)
4. Endpoint type? (REST, gRPC, internal, signalr)
5. External integration? (payment, email, SMS, WhatsApp, etc)
6. Validation rules? (from existing business rules)
7. Permission required? (from existing policies)
8. Test coverage target? (default 85%)
9. Migration needed? (if DB schema changes)
10. Backward compatibility? (breaking change warning)

## Generated artifacts
- Command: Application/Features/<Feature>/Commands/<Name>/<Name>Command.cs
- CommandHandler: Application/Features/<Feature>/Commands/<Name>/<Name>Handler.cs
- Validator: Application/Features/<Feature>/Commands/<Name>/<Name>Validator.cs
- Query (if needed): Application/Features/<Feature>/Queries/<Name>/<Name>Query.cs
- Endpoint: WebApi/Endpoints/<Feature>/<Name>Endpoint.cs
- Tests: Application.Tests/Features/<Feature>/<Name>HandlerTests.cs + WebApi.Tests/<Name>EndpointTests.cs
- Docs: updates README + OpenAPI examples

## Coverage by Layer (v3.55.0)
coverage by layer, coverage + layer, coverage per layer
- Feature detection: 100%
- Knowledge Context integration: 100%
- Question flow: 100% (10 questions max)
- Code generation: 100% (CQRS + endpoint + tests)
- Feature mode total: 100%