---
id: signalr-realtime-completo
type: conhecimento
tags: [signalr, realtime, websocket, hub, notifications, chat, live]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre SignalR - Comunicação em Tempo Real
- **Seções principais**: Conceito, Hub, Configuração, Cliente JavaScript
- **Tags**: signalr, realtime, websocket, hub, notifications, chat, live
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `signalr-realtime-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# SignalR - Comunicação em Tempo Real

## Conceito

SignalR é a biblioteca .NET para comunicação em tempo real entre servidor e clientes, suportando WebSockets, Server-Sent Events e Long Polling.

## Hub

```csharp
public class ChatHub : Hub
{
    // Enviar para todos os clientes conectados
    public async Task SendMessage(string user, string message)
    {
        await Clients.All.SendAsync("ReceiveMessage", user, message);
    }
    
    // Enviar para grupo específico
    public async Task SendToGroup(string groupName, string message)
    {
        await Clients.Group(groupName).SendAsync("ReceiveMessage", message);
    }
    
    // Enviar para remetente
    public async Task Echo(string message)
    {
        await Clients.Caller.SendAsync("ReceiveMessage", message);
    }
    
    // Enviar para todos exceto remetente
    public async Task Broadcast(string message)
    {
        await Clients.Others.SendAsync("ReceiveMessage", message);
    }
    
    // Entrar em grupo
    public async Task JoinGroup(string groupName)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, groupName);
        await Clients.Group(groupName).SendAsync("Joined", Context.User?.Identity?.Name);
    }
    
    // Sair de grupo
    public async Task LeaveGroup(string groupName)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, groupName);
    }
    
    // Conexão
    public override async Task OnConnectedAsync()
    {
        await Clients.Caller.SendAsync("Connected", Context.ConnectionId);
        await base.OnConnectedAsync();
    }
    
    // Desconexão
    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await Clients.All.SendAsync("UserDisconnected", Context.User?.Identity?.Name);
        await base.OnDisconnectedAsync(exception);
    }
}
```

## Configuração

```csharp
// Server
builder.Services.AddSignalR()
    .AddJsonProtocol(options =>
    {
        options.PayloadSerializerOptions.PropertyNamingPolicy = null;
    })
    .AddStackExchangeRedis("localhost:6379", options =>
    {
        options.Configuration.ChannelPrefix = "XForge";
    });

app.MapHub<ChatHub>("/hub/chat");
app.MapHub<OrderHub>("/hub/orders");
app.MapHub<NotificationHub>("/hub/notifications");
```

## Cliente JavaScript

```javascript
// Conectar
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/hub/chat")
    .withAutomaticReconnect()
    .configureLogging(signalR.LogLevel.Information)
    .build();

// Escutar mensagens
connection.on("ReceiveMessage", (user, message) => {
    console.log(`${user}: ${message}`);
    addMessageToUI(user, message);
});

// Enviar mensagem
async function sendMessage(user, message) {
    await connection.invoke("SendMessage", user, message);
}

// Conectar
connection.start()
    .then(() => console.log("Connected!"))
    .catch(err => console.error("Connection failed:", err));

// Reconexão automática
connection.onreconnecting((error) => {
    console.log("Reconnecting...");
});

connection.onreconnected((connectionId) => {
    console.log("Reconnected:", connectionId);
});

connection.onclose((error) => {
    console.log("Disconnected:", error);
});
```

## Cliente .NET (Blazor/WPF/MAUI)

```csharp
// Registration
builder.Services.AddSignalRClient(options =>
{
    options.Url = "https://localhost:5000/hub/chat";
    options.AccessTokenProvider = () => Task.FromResult(jwtToken);
});

// Usage
public class ChatService
{
    private readonly HubConnection _hubConnection;
    
    public ChatService(HubConnectionFactory factory)
    {
        _hubConnection = factory.CreateHubConnection();
        
        _hubConnection.On<string, string>("ReceiveMessage", (user, message) =>
        {
            MessageReceived?.Invoke(this, new MessageEventArgs(user, message));
        });
    }
    
    public event EventHandler<MessageEventArgs>? MessageReceived;
    
    public async Task ConnectAsync()
    {
        if (_hubConnection.State == HubConnectionState.Disconnected)
        {
            await _hubConnection.StartAsync();
        }
    }
    
    public async Task SendMessageAsync(string user, string message)
    {
        await _hubConnection.InvokeAsync("SendMessage", user, message);
    }
    
    public async Task JoinGroupAsync(string groupName)
    {
        await _hubConnection.InvokeAsync("JoinGroup", groupName);
    }
}
```

## Strongly Typed Hub

```csharp
public interface IChatClient
{
    Task ReceiveMessage(string user, string message);
    Task UserConnected(string connectionId);
    Task UserDisconnected(string connectionId);
    Task Typing(string user);
}

public class TypedChatHub : Hub<IChatClient>
{
    public async Task SendMessage(string message)
    {
        await Clients.All.ReceiveMessage(Context.User?.Identity?.Name ?? "Anonymous", message);
    }
    
    public async Task SendPrivateMessage(string userId, string message)
    {
        await Clients.User(userId).ReceiveMessage(Context.User?.Identity?.Name ?? "Anonymous", message);
    }
}
```

## Autorização

```csharp
// Hub com autorização
[Authorize]
public class SecureHub : Hub
{
    [Authorize(Roles = "Admin")]
    public async Task AdminAction()
    {
        await Clients.All.SendAsync("AdminNotification", "Admin action performed");
    }
    
    public async Task SendMessage(string message)
    {
        // Usuário autenticado pode enviar
        await Clients.All.SendAsync("ReceiveMessage", Context.User?.Identity?.Name, message);
    }
}

// Configuração
app.MapHub<SecureHub>("/hub/secure").RequireAuthorization();
```

## State Management

```csharp
// State no Hub
public class OrderHub : Hub
{
    private static readonly ConcurrentDictionary<string, UserState> _userStates = new();
    
    public async Task SetUserState(string key, string value)
    {
        var state = _userStates.GetOrAdd(Context.ConnectionId, _ => new UserState());
        state.Data[key] = value;
    }
    
    public async Task<string?> GetUserState(string key)
    {
        if (_userStates.TryGetValue(Context.ConnectionId, out var state))
            return state.Data.TryGetValue(key, out var value) ? value : null;
        return null;
    }
    
    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        _userStates.TryRemove(Context.ConnectionId, out _);
        await base.OnDisconnectedAsync(exception);
    }
}

public class UserState
{
    public Dictionary<string, string> Data { get; } = new();
}
```

## Broadcast Patterns

### Send to All
```csharp
await Clients.All.SendAsync("Notify", "System maintenance at 2 AM");
```

### Send to Specific User
```csharp
await Clients.User(userId).SendAsync("Notification", "Your order is ready");
```

### Send to Group
```csharp
await Clients.Group("admins").SendAsync("SecurityAlert", "Failed login attempt");
```

### Send to Connection
```csharp
await Clients.Client(connectionId).SendAsync("Update", "Data refreshed");
```

### Send to Others
```csharp
await Clients.Others.SendAsync("UserJoined", userName);
```

## Performance

### Scalability with Redis
```csharp
builder.Services.AddSignalR()
    .AddStackExchangeRedis("redis:6379", options =>
    {
        options.Configuration.ChannelPrefix = "XForge";
    });
```

### Message Compression
```csharp
builder.Services.AddSignalR()
    .AddJsonProtocol(options =>
    {
        options.PayloadSerializerOptions.Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping;
    });
```

### Connection Management
```csharp
// Limitar conexões
builder.Services.Configure<HubOptions>(options =>
{
    options.MaximumReceiveMessageSize = 64 * 1024; // 64KB
    options.KeepAliveInterval = TimeSpan.FromSeconds(15);
    options.ClientTimeoutInterval = TimeSpan.FromSeconds(30);
});
```

## Casos de Uso

### Chat em Tempo Real
```csharp
public class ChatHub : Hub
{
    public async Task SendPrivateMessage(string userId, string message)
    {
        var fromUser = Context.User?.Identity?.Name;
        await Clients.User(userId).ReceiveMessage(fromUser!, message);
        await Clients.Caller.MessageSent(userId, message);
    }
}
```

### Notificações Push
```csharp
public class NotificationHub : Hub
{
    public async Task SubscribeToNotifications(string[] channels)
    {
        foreach (var channel in channels)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, channel);
        }
    }
    
    public async Task SendNotification(string channel, string title, string body)
    {
        await Clients.Group(channel).SendAsync("Notification", title, body);
    }
}
```

### Atualização em Tempo Real
```csharp
public class DashboardHub : Hub
{
    public async Task SubscribeToMetrics()
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, "metrics");
    }
    
    // Chamado por background service
    public async Task BroadcastMetrics(MetricsData metrics)
    {
        await Clients.Group("metrics").SendAsync("MetricsUpdate", metrics);
    }
}
```

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/signalr
- github.com/dotnet/aspnetcore/tree/main/src/SignalR
