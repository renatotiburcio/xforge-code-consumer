---
id: azure-services-completo
type: conhecimento
tags: [azure, app-service, functions, cosmos-db, key-vault, devops, pipeline, monitoring]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Azure - Serviços Completos
- **Seções principais**: Serviços Principais, App Service, Azure Functions, Cosmos DB
- **Tags**: azure, app-service, functions, cosmos-db, key-vault, devops, pipeline, monitoring
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `azure-services-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 10 |


# Azure - Serviços Completos

## Serviços Principais

### Compute

| Serviço | Descrição | Uso |
|---------|-----------|-----|
| **App Service** | Web apps gerenciadas | APIs, web apps |
| **Azure Functions** | Serverless | Jobs, webhooks, APIs leves |
| **Container Instances** | Containers simples | Tasks, batch |
| **AKS** | Kubernetes gerenciado | Microservices, escala |
| **Virtual Machines** | VMs completas | Legacy, customizações |

### Databases

| Serviço | Tipo | Uso |
|---------|------|-----|
| **Azure SQL** | Relacional | Apps .NET tradicionais |
| **Cosmos DB** | NoSQL | Dados globais, baixa latência |
| **Azure Database for PostgreSQL** | Relacional | Apps Open Source |
| **Azure Database for MySQL** | Relacional | Apps Open Source |
| **Azure Cache for Redis** | Cache | Cache, sessões, filas |

### Storage

| Serviço | Uso |
|---------|-----|
| **Blob Storage** | Arquivos, imagens, backups |
| **File Storage** | Shares SMB/NFS |
| **Queue Storage** | Filas simples |
| **Table Storage** | Dados estruturados simples |

### Messaging

| Serviço | Uso |
|---------|-----|
| **Service Bus** | Filas e tópicos enterprise |
| **Event Grid** | Eventos reativos |
| **Event Hubs** | Streaming de dados |

### Security

| Serviço | Uso |
|---------|-----|
| **Key Vault** | Segredos, chaves, certificados |
| **Azure AD / Entra ID** | Identidade e acesso |
| **Managed Identity** | Identidade sem credenciais |
| **Private Link** | Acesso privado a serviços |

## App Service

### Configuração
```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddAzureSqlStorage(builder.Configuration.GetConnectionString("AzureSQL"))
    .AddRedis(redisConnection);

// appsettings.json
{
  "ConnectionStrings": {
    "AzureSQL": "Server=tcp:myserver.database.windows.net,1433;Database=mydb;User Id=...;Password=...;Encrypt=True"
  }
}
```

### Deployment Slot
```bash
# Criar slot de staging
az webapp deployment slot create --name myapp --resource-group myRG --slot staging

# Deploy para staging
az webapp deployment source config --name myapp --resource-group myRG --slot staging --src ./publish

# Swap staging → production
az webapp deployment slot swap --name myapp --resource-group myRG --slot staging
```

## Azure Functions

### HTTP Trigger
```csharp
[Function("GetProduct")]
public async Task<IActionResult> GetProduct(
    [HttpTrigger(AuthorizationLevel.Function, "get", Route = "products/{id}")] HttpRequest req,
    int id)
{
    var product = await _service.GetByIdAsync(id);
    return product == null ? new NotFoundResult() : new OkObjectResult(product);
}
```

### Timer Trigger
```csharp
[Function("DailyCleanup")]
public async Task Run(
    [TimerTrigger("0 0 2 * * *")] TimerInfo timer)
{
    await _cleanupService.CleanupOldRecords();
}
```

### Queue Trigger
```csharp
[Function("ProcessOrder")]
public async Task ProcessOrder(
    [QueueTrigger("orders", Connection = "AzureWebJobsStorage")] string message)
{
    var order = JsonSerializer.Deserialize<Order>(message);
    await _orderService.ProcessAsync(order);
}
```

### Configuração
```json
{
  "ConnectionStrings": {
    "AzureSQL": "Server=...",
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=...",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated"
  }
}
```

## Cosmos DB

### Configuração
```csharp
builder.Services.AddCosmosClient(
    connectionString,
    new CosmosClientOptions
    {
        SerializerOptions = new CosmosSerializationOptions
        {
            PropertyNamingPolicy = CosmosPropertyNamingPolicy.CamelCase
        }
    });

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseCosmos(
        connectionString,
        databaseName: "mydb"));
```

### Query
```csharp
var container = _client.GetContainer("mydb", "products");

var query = container.GetItemQueryIterator<Product>(
    new QueryDefinition("SELECT * FROM c WHERE c.categoryId = @categoryId")
        .WithParameter("@categoryId", categoryId));

var products = new List<Product>();
while (query.HasMoreResults)
{
    var response = await query.ReadNextAsync();
    products.AddRange(response);
}
```

## Key Vault

### Managed Identity
```csharp
builder.Configuration.AddAzureKeyVault(
    new Uri("https://myvault.vault.azure.net/"),
    new DefaultAzureCredential());

// Uso
var secret = await _keyVaultClient.GetSecretAsync("database-password");
```

### Configuration
```csharp
builder.Configuration.AddAzureKeyVault(
    new Uri("https://myvault.vault.azure.net/"),
    new DefaultAzureCredential(),
    new AzureKeyVaultConfigurationOptions
    {
        ReloadInterval = TimeSpan.FromMinutes(5)
    });
```

## Azure DevOps

### Pipeline YAML
```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UseDotNet@2
  inputs:
    version: '10.0.x'

- script: dotnet restore
  displayName: 'Restore'

- script: dotnet build --no-restore
  displayName: 'Build'

- script: dotnet test --no-build --verbosity normal
  displayName: 'Test'

- script: dotnet publish -c Release -o $(Build.ArtifactStagingDirectory)
  displayName: 'Publish'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)'
```

## App Configuration

```csharp
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(new Uri("https://myconfig.azure.com"), new DefaultAzureCredential())
        .Select("MyApp:*", LabelFilter.Null)
        .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()));
});

// Uso
var value = builder.Configuration["MyApp:Setting1"];
```

## Monitoramento

### Application Insights
```csharp
builder.Services.AddApplicationInsightsTelemetry();
builder.Services.AddApplicationInsightsTelemetryWorkerService();

// Custom telemetry
telemetry.TrackEvent("OrderCreated", new Dictionary<string, string>
{
    { "OrderId", order.Id.ToString() },
    { "Amount", order.Total.ToString() }
});
```

### Alerts
```csharp
// Configurar alertas via Azure CLI
az monitor metrics alert create \
    --name "High Response Time" \
    --resource-group myRG \
    --scopes "/subscriptions/.../webapps/myapp" \
    --condition "avg responseTime > 2000" \
    --action email admin@example.com
```

## CI/CD com GitHub Actions

```yaml
- name: Deploy to Azure
  uses: azure/webapps-deploy@v2
  with:
    app-name: 'myapp'
    publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
    package: './publish'
```

## Fontes Oficiais
- docs.microsoft.com/azure
- docs.microsoft.com/azure/app-service
- docs.microsoft.com/azure/azure-functions
- docs.microsoft.com/azure/cosmos-db
