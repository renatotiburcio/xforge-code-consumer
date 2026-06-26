---
id: deploy-net
type: knowledge
tags: [deploy, docker, cicd, kubernetes, azure, dotnet, infraestrutura]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Deployment .NET
- **Principais responsabilidades**: Definir Dockerfile otimizado para produção; Configurar pipeline CI/CD com build, teste, segurança e deploy; Gerenciar configurações por ambiente (d...
- **Seções principais**: Propósito, Responsabilidades, Docker Multi-Stage Build, CI/CD Pipeline Stages
- **Tags**: deploy, docker, cicd, kubernetes, azure, dotnet, infraestrutura
- **Tipo**: knowledge | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `deploy-net` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 9 |


# Deployment .NET

## Propósito
Guia de implantação para aplicações .NET em produção, cobrindo Docker multi-stage builds, pipelines CI/CD, configurações por ambiente, health checks e estratégias de rollback.

## Responsabilidades
- Definir Dockerfile otimizado para produção
- Configurar pipeline CI/CD com build, teste, segurança e deploy
- Gerenciar configurações por ambiente (dev/staging/prod)
- Implementar health checks e probes

## Docker Multi-Stage Build

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/ERP.Web/ERP.Web.csproj", "src/ERP.Web/"]
COPY ["src/ERP.Application/ERP.Application.csproj", "src/ERP.Application/"]
COPY ["src/ERP.Domain/ERP.Domain.csproj", "src/ERP.Domain/"]
COPY ["src/ERP.Infrastructure/ERP.Infrastructure.csproj", "src/ERP.Infrastructure/"]
RUN dotnet restore "src/ERP.Web/ERP.Web.csproj"
COPY . .
WORKDIR "/src/src/ERP.Web"
RUN dotnet build "ERP.Web.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "ERP.Web.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN apk add --no-cache icu-libs
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false
COPY --from=publish /app/publish .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
ENTRYPOINT ["dotnet", "ERP.Web.dll"]
```

**Otimizações:** Alpine (~100MB), ReadyToRun, PublishTrimmed, AOT (.NET+8), invariant globalization.

## CI/CD Pipeline Stages

| Stage | Ação | Ferramenta |
|-------|------|------------|
| **Build** | Restore + Build + Test | `dotnet build`, `dotnet test` |
| **Security** | Scan de vulnerabilidades | Trivy, `dotnet list package --vulnerable` |
| **Publish** | Build + Push da imagem Docker | `docker build-push-action` |
| **Deploy Staging** | Deploy em slot de staging | Azure Web Apps / AKS |
| **Smoke Tests** | Verificar health check | `curl /health` |
| **Deploy Production** | Deploy em produção | Azure Web Apps / AKS |

## Configurações por Ambiente

```json
// appsettings.Production.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=prod-sql;Database=ErpDb;Authentication=Active Directory Managed Identity;"
  },
  "Azure": {
    "KeyVaultUrl": "https://erp-prod.vault.azure.net/"
  }
}
```

```csharp
// Program.cs — Key Vault em produção
if (!builder.Environment.IsDevelopment()) {
    var keyVaultUrl = builder.Configuration["Azure:KeyVaultUrl"];
    if (!string.IsNullOrEmpty(keyVaultUrl))
        builder.Configuration.AddAzureKeyVault(new Uri(keyVaultUrl), new DefaultAzureCredential());
}
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddSqlServer(connectionString, name: "database", timeout: TimeSpan.FromSeconds(3))
    .AddRedis(redisConnection, name: "redis", timeout: TimeSpan.FromSeconds(3))
    .AddRabbitMQ(rabbitConnectionString, name: "rabbitmq");

app.MapHealthChecks("/health", new HealthCheckOptions {
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
app.MapHealthChecks("/health/ready", new HealthCheckOptions {
    Predicate = check => check.Tags.Contains("ready")
});
app.MapHealthChecks("/health/live", new HealthCheckOptions {
    Predicate = _ => false
});
```

| Probe | Propósito | Endpoint |
|-------|-----------|----------|
| **Liveness** | App está vivo? Reinicia container | `/health/live` |
| **Readiness** | Pode receber tráfego? Remove do LB | `/health/ready` |
| **Startup** | Iniciou corretamente? | `/health/live` |

## Estratégias de Deploy e Rollback

| Estratégia | Risco | Downtime | Rollback | Uso |
|------------|-------|----------|----------|-----|
| **Rolling** | Médio | Zero | Lento | Atualizações rotineiras |
| **Blue-Green** | Baixo | Zero | Instantâneo | Releases críticos |
| **Canary** | Muito Baixo | Zero | Rápido | Validação gradual |

```bash
# Blue-Green com Azure App Service Slots
az webapp deployment slot swap --resource-group erp-rg --name erp-prod --slot staging --target-slot production

# Rollback no Kubernetes
kubectl rollout undo deployment/erp-api -n erp
kubectl rollout status deployment/erp-api -n erp --timeout=300s
```

## Dependências
- [observabilidade.md](observabilidade.md) — Monitoramento pós-deploy
- [multi-tenancy.md](multi-tenancy.md) — Deploy de migrations multi-tenant

## Restrições
- NUNCA rodar migrations automaticamente em produção — usar pipeline ou job manual
- NUNCA rodar container como root
- Sempre usar Managed Identities em vez de connection strings com senhas
- Migrations devem ser idempotentes (`dotnet ef migrations script --idempotent`)

