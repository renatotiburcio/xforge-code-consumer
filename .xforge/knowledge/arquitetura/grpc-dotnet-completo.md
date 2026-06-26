---
id: gRPC-dotnet-completo
type: conhecimento
tags: [grpc, protobuf, grpc-web, load-balancing, streaming, microservices]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre gRPC em .NET - Guia Completo
- **Seções principais**: Conceito, Comparativo, Definição do Serviço (.proto), Server
- **Tags**: grpc, protobuf, grpc-web, load-balancing, streaming, microservices
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `gRPC-dotnet-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# gRPC em .NET - Guia Completo

## Conceito

gRPC é um framework RPC de alta performance baseado em Protocol Buffers (protobuf), ideal para comunicação entre microservices.

## Comparativo

| Aspecto | gRPC | REST/HTTP |
|---------|------|-----------|
| Protocolo | HTTP/2 | HTTP/1.1 ou HTTP/2 |
| Serialização | Protocol Buffers (binário) | JSON (texto) |
| Performance | ~10x mais rápido | Padrão |
| Streaming | Sim (bidirecional) | Limitado |
| Contrato | .proto files | OpenAPI/Swagger |
| Browser | gRPC-Web (limitado) | Nativo |
| Ferramentas | grpcurl, Postman | Qualquer HTTP client |

## Definição do Serviço (.proto)

```protobuf
syntax = "proto3";

option csharp_namespace = "MyApp.Grpc";

package products;

// Serviço
service ProductService {
    // Unary RPC
    rpc GetProduct (GetProductRequest) returns (ProductResponse);
    rpc ListProducts (ListProductsRequest) returns (stream ProductResponse);
    rpc CreateProduct (CreateProductRequest) returns (ProductResponse);
    rpc UpdateProduct (UpdateProductRequest) returns (ProductResponse);
    rpc DeleteProduct (DeleteProductRequest) returns (Empty);
    
    // Server streaming
    rpc SubscribeToProducts (SubscribeRequest) returns (stream ProductEvent);
    
    // Client streaming
    rpc BulkCreateProducts (stream CreateProductRequest) returns (BulkResult);
    
    // Bidirectional streaming
    rpc ProductChat (stream ChatMessage) returns (stream ChatMessage);
}

// Mensagens
message GetProductRequest {
    int32 id = 1;
}

message ListProductsRequest {
    int32 page_size = 1;
    string page_token = 2;
    string filter = 3;
}

message CreateProductRequest {
    string name = 1;
    double price = 2;
    int32 category_id = 3;
}

message UpdateProductRequest {
    int32 id = 1;
    string name = 2;
    double price = 3;
    int32 category_id = 4;
}

message DeleteProductRequest {
    int32 id = 1;
}

message ProductResponse {
    int32 id = 1;
    string name = 2;
    double price = 3;
    int32 category_id = 4;
    string created_at = 5;
}

message ProductEvent {
    string event_type = 1;
    ProductResponse product = 2;
}

message SubscribeRequest {
    repeated string channels = 1;
}

message ChatMessage {
    string user = 1;
    string message = 2;
    string timestamp = 3;
}

message BulkResult {
    int32 created_count = 1;
    repeated int32 created_ids = 2;
}

message Empty {}
```

## Server

### Configuração
```csharp
// Program.cs
builder.Services.AddGrpc();
builder.Services.AddGrpcReflection();

var app = builder.Build();

app.MapGrpcService<ProductGrpcService>();
app.MapGrpcReflectionService();

app.Run();
```

### Implementação do Serviço
```csharp
public class ProductGrpcService : ProductService.ProductServiceBase
{
    private readonly IProductRepository _repo;
    private readonly ILogger<ProductGrpcService> _logger;
    
    public ProductGrpcService(IProductRepository repo, ILogger<ProductGrpcService> logger)
    {
        _repo = repo;
        _logger = logger;
    }
    
    // Unary RPC
    public override async Task<ProductResponse> GetProduct(
        GetProductRequest request, ServerCallContext context)
    {
        var product = await _repo.GetByIdAsync(request.Id);
        if (product == null)
            throw new RpcException(new Status(StatusCode.NotFound, "Product not found"));
        
        return new ProductResponse
        {
            Id = product.Id,
            Name = product.Name,
            Price = (double)product.Price,
            CategoryId = product.CategoryId,
            CreatedAt = product.CreatedAt.ToString("O")
        };
    }
    
    // Server streaming
    public override async Task ListProducts(
        ListProductsRequest request,
        IServerStreamWriter<ProductResponse> responseStream,
        ServerCallContext context)
    {
        var products = await _repo.GetAllAsync();
        foreach (var product in products)
        {
            if (context.CancellationToken.IsCancellationRequested)
                break;
            
            await responseStream.WriteAsync(new ProductResponse
            {
                Id = product.Id,
                Name = product.Name,
                Price = (double)product.Price
            });
        }
    }
    
    // Client streaming
    public override async Task<BulkResult> BulkCreateProducts(
        IAsyncStreamReader<CreateProductRequest> requestStream,
        ServerCallContext context)
    {
        var createdIds = new List<int>();
        
        await foreach (var request in requestStream.ReadAllAsync(context.CancellationToken))
        {
            var product = new Product
            {
                Name = request.Name,
                Price = (decimal)request.Price,
                CategoryId = request.CategoryId
            };
            
            await _repo.AddAsync(product);
            createdIds.Add(product.Id);
        }
        
        return new BulkResult
        {
            CreatedCount = createdIds.Count,
            CreatedIds = { createdIds }
        };
    }
    
    // Bidirectional streaming
    public override async Task ProductChat(
        IAsyncStreamReader<ChatMessage> requestStream,
        IServerStreamWriter<ChatMessage> responseStream,
        ServerCallContext context)
    {
        await foreach (var message in requestStream.ReadAllAsync(context.CancellationToken))
        {
            _logger.LogInformation("Received: {User}: {Message}", message.User, message.Message);
            
            await responseStream.WriteAsync(new ChatMessage
            {
                User = "Server",
                Message = $"Echo: {message.Message}",
                Timestamp = DateTime.UtcNow.ToString("O")
            });
        }
    }
}
```

## Client

### Configuração
```csharp
builder.Services.AddGrpcClient<ProductService.ProductServiceClient>(options =>
{
    options.Address = new Uri("https://localhost:7225");
})
.ConfigureChannel(options =>
{
    options.Credentials = ChannelCredentials.SecureSslTls;
    options.HttpHandler = new SocketsHttpHandler
    {
        ConnectTimeout = TimeSpan.FromSeconds(10),
        KeepAliveDelay = TimeSpan.FromSeconds(30)
    };
});
```

### Uso
```csharp
public class ProductGrpcClient
{
    private readonly ProductService.ProductServiceClient _client;
    
    public ProductGrpcClient(ProductService.ProductServiceClient client)
    {
        _client = client;
    }
    
    // Unary
    public async Task<ProductResponse> GetProductAsync(int id)
    {
        return await _client.GetProductAsync(new GetProductRequest { Id = id });
    }
    
    // Server streaming
    public async IAsyncEnumerable<ProductResponse> ListProductsAsync()
    {
        var call = _client.ListProducts(new ListProductsRequest());
        
        await foreach (var product in call.ResponseStream.ReadAllAsync())
        {
            yield return product;
        }
    }
    
    // Client streaming
    public async Task<BulkResult> BulkCreateAsync(IEnumerable<CreateProductRequest> products)
    {
        using var call = _client.BulkCreateProducts();
        
        foreach (var product in products)
        {
            await call.RequestStream.WriteAsync(product);
        }
        
        await call.RequestStream.CompleteAsync();
        return await call.ResponseAsync;
    }
    
    // Bidirectional streaming
    public async IAsyncEnumerable<ChatMessage> ChatAsync(IAsyncEnumerable<ChatMessage> messages)
    {
        using var call = _client.ProductChat();
        
        // Send messages
        _ = Task.Run(async () =>
        {
            await foreach (var message in messages)
            {
                await call.RequestStream.WriteAsync(message);
            }
            await call.RequestStream.CompleteAsync();
        });
        
        // Receive messages
        await foreach (var message in call.ResponseStream.ReadAllAsync())
        {
            yield return message;
        }
    }
}
```

## gRPC-Web (Browser)

### Configuração
```csharp
// Server
builder.Services.AddGrpcReflection();
app.MapGrpcWebServices();

// Client (JavaScript)
const client = new GrpcWebClient('https://localhost:7225');
const productService = new ProductServiceClient(client);

const product = await productService.getProduct({ id: 1 });
console.log(product.name);
```

## Load Balancing

### Strategies
| Strategy | Descrição |
|----------|-----------|
| Round Robin | Distribui conexões igualmente |
| Pick First | Conecta ao primeiro servidor |
| Custom | Implementação própria |

### Configuração
```csharp
builder.Services.AddGrpcClient<ProductService.ProductServiceClient>(options =>
{
    options.Address = new Uri("https://my-service");
})
.ConfigureChannel(options =>
{
    options.ServiceConfig = new ServiceConfig
    {
        LoadBalancingConfigs = { new RoundRobinConfig() }
    };
});
```

## Interceptors

```csharp
// Logging Interceptor
public class LoggingInterceptor<TRequest, TResponse> : Interceptor
    where TRequest : class
    where TResponse : class
{
    private readonly ILogger<LoggingInterceptor<TRequest, TResponse>> _logger;
    
    public override async Task<TResponse> UnaryServerHandler(
        TRequest request,
        ServerCallContext context,
        UnaryServerMethod<TRequest, TResponse> continuation)
    {
        _logger.LogInformation("Calling {Method} from {Peer}",
            context.Method, context.Peer);
        
        var sw = Stopwatch.StartNew();
        var response = await continuation(request, context);
        sw.Stop();
        
        _logger.LogInformation("Completed {Method} in {Elapsed}ms",
            context.Method, sw.ElapsedMilliseconds);
        
        return response;
    }
}

// Uso
app.MapGrpcService<ProductGrpcService>()
    .Intercept<LoggingInterceptor<GetProductRequest, ProductResponse>>();
```

## Health Checks

```csharp
builder.Services.AddGrpcHealthChecks()
    .AddCheck("products", () => HealthCheckResult.Healthy());

app.MapGrpcHealthService();
```

## Métricas

```csharp
builder.Services.AddGrpcMetrics();

// Métricas disponíveis
// - grpc.server.total.calls
// - grpc.server.active.calls
// - grpc.server.received.messages
// - grpc.server.sent.messages
// - grpc.server.call.duration
```

## Quando Usar gRPC vs REST

| Cenário | gRPC | REST |
|---------|:----:|:----:|
| Microservices internos | ✅ | ✅ |
| Browser clients | ❌ | ✅ |
| Streaming real-time | ✅ | ⚠️ |
| Mobile apps | ✅ | ✅ |
| Contrato forte | ✅ | ✅ |
| Simplicidade | ❌ | ✅ |

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/grpc
- grpc.io/docs/languages/csharp
- github.com/grpc/grpc-dotnet
