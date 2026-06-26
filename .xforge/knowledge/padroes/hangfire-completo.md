---
id: hangfire-completo
type: conhecimento
tags: [hangfire, background-jobs, recurring, fire-and-forget, delayed, dashboard]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Hangfire - Jobs em Background
- **Seções principais**: Conceito, Tipos de Job, Setup, Fire-and-Forget Jobs
- **Tags**: hangfire, background-jobs, recurring, fire-and-forget, delayed, dashboard
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `hangfire-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 15 |


# Hangfire - Jobs em Background

## Conceito

Hangfire é a biblioteca para processamento de jobs em background no .NET, suportando fire-and-forget, delayed, recurring e continuations.

## Tipos de Job

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| **Fire-and-Forget** | Executa imediatamente | Enviar email |
| **Delayed** | Executa após delay | Lembrete em 1h |
| **Recurring** | Executa em schedule | Backup diário |
| **Continuation** | Executa após outro job | Processar após upload |
| **Failable** | Com retry automático | Chamada API externa |

## Setup

```csharp
// Program.cs
builder.Services.AddHangfire(config => config
    .SetDataCompatibilityLevel(CompatibilityLevel.Version_180)
    .UseSimpleAssemblyNameTypeSerializer()
    .UseRecommendedSerializerSettings()
    .UseSqlServerStorage(builder.Configuration.GetConnectionString("Hangfire")));

builder.Services.AddHangfireServer(options =>
{
    options.WorkerCount = Environment.ProcessorCount * 2;
    options.Queues = new[] { "critical", "default", "low" };
});

// Dashboard (apenas Admin)
app.MapHangfireDashboard("/hangfire", new DashboardOptions
{
    DashboardTitle = "XForge Jobs",
    Authorization = new[] { new HangfireCustomFilter() }
});
```

## Fire-and-Forget Jobs

```csharp
// Simples
BackgroundJob.Enqueue(() => Console.WriteLine("Hello!"));

// Com parâmetros
BackgroundJob.Enqueue<IEmailService>(x => 
    x.SendEmailAsync("user@example.com", "Welcome!", "Hello"));

// Com interface
BackgroundJob.Enqueue<INotificationService>(x => 
    x.SendPushNotificationAsync(userId, "New order created"));
```

## Delayed Jobs

```csharp
// Em 1 hora
BackgroundJob.Schedule(() => Console.WriteLine("Reminder"), TimeSpan.FromHours(1));

// Em 30 minutos
BackgroundJob.Schedule<IReminderService>(x => 
    x.SendReminderAsync(userId, "Your session expires soon"), 
    TimeSpan.FromMinutes(30));

// Em específico
BackgroundJob.Schedule(
    () => Console.WriteLine("Executed"),
    new DateTimeOffset(2024, 1, 15, 9, 0, 0, TimeSpan.Zero));
```

## Recurring Jobs

```csharp
// Configuração
RecurringJob.AddOrUpdate(
    "daily-cleanup",
    () => _cleanupService.CleanupOldRecords(),
    Cron.Daily); // Todo dia à meia-noite

RecurringJob.AddOrUpdate(
    "hourly-sync",
    () => _syncService.SyncDataAsync(),
    Cron.Hourly); // A cada hora

RecurringJob.AddOrUpdate(
    "weekly-report",
    () => _reportService.GenerateWeeklyReport(),
    Cron.Weekly(DayOfWeek.Monday, 9, 0)); // Segunda às 9h

// Com timezone
RecurringJob.AddOrUpdate(
    "monthly-billing",
    () => _billingService.ProcessMonthlyBilling(),
    Cron.Monthly,
    new RecurringJobOptions
    {
        TimeZone = TimeZoneInfo.FindSystemTimeZoneById("America/Sao_Paulo")
    });
```

## Continuations

```csharp
// Executa APÓS outro job
var parentId = BackgroundJob.Enqueue(() => Console.WriteLine("Step 1"));
BackgroundJob.ContinueJobWith(parentId, () => Console.WriteLine("Step 2"));
BackgroundJob.ContinueJobWith(parentId, () => Console.WriteLine("Step 3"));

// Com filtro
BackgroundJob.ContinueJobWith<INotificationService>(
    parentId,
    x => x.SendNotificationAsync("Processing complete"),
    JobContinuationOptions.OnlyOnSucceededState);
```

## Filas e Prioridades

```csharp
// Enfileirar em fila específica
BackgroundJob.Enqueue("critical", () => ProcessPaymentAsync(orderId));
BackgroundJob.Enqueue("default", () => SendEmailAsync(userId));
BackgroundJob.Enqueue("low", () => GenerateReportAsync());

// Worker processa filas por prioridade
builder.Services.AddHangfireServer(options =>
{
    options.Queues = new[] { "critical", "default", "low" };
});
```

## Filtros

```csharp
// Filtro de autenticação
public class HangfireCustomFilter : IDashboardAuthorizationFilter
{
    public bool Authorize(DashboardContext context)
    {
        var httpContext = context.GetHttpContext();
        return httpContext.User.IsInRole("Admin");
    }
}

// Filtro de log
public class LoggingFilter : IElectStateFilter
{
    public void OnStateElection(ElectStateContext context)
    {
        var jobName = context.BackgroundJob?.Job?.Type?.Name;
        var state = context.CandidateState?.Name;
        
        Console.WriteLine($"Job {jobName} → {state}");
    }
}

// Filtro de retry
public class RetryFilter : IElectStateFilter
{
    public void OnStateElection(ElectStateContext context)
    {
        var failedState = context.CandidateState as FailedState;
        if (failedState != null)
        {
            context.CandidateState = new SucceededState();
        }
    }
}
```

## Dashboard

```csharp
// Configuração avançada
app.MapHangfireDashboard("/hangfire", new DashboardOptions
{
    DashboardTitle = "XForge Job Dashboard",
    DashboardName = "XForge",
    IsReadOnlyFunc = context => false,
    DisplayStorageConnectionString = false,
    Authorization = new[]
    {
        new HangfireCustomFilter()
    },
    AppPath = "/admin",
    StatsPollingInterval = 15000
});
```

## Batch Jobs

```csharp
// Criar batch de jobs
using var batch = new BackgroundJobBatch();
batch.Add(() => Console.WriteLine("Job 1"));
batch.Add(() => Console.WriteLine("Job 2"));
batch.Add(() => Console.WriteLine("Job 3"));
await batch.CommitAsync();
```

## State Machine

```csharp
// Estados possíveis
// Enqueued → Processing → Succeeded
//                     └→ Failed → Enqueued (retry)
//                     └→ Deleted

// Forçar estado
BackgroundJob.Enqueue(() => Console.WriteLine("test"));
var jobId = BackgroundJob.Enqueue(() => Console.WriteLine("test"));
BackgroundJob.Delete(jobId); // Deletar
BackgroundJob.Requeue(jobId); // Reenfileirar
```

## Exemplo Completo

```csharp
// Serviço que usa Hangfire
public class OrderProcessingService : IOrderProcessingService
{
    public async Task ProcessOrderAsync(int orderId)
    {
        // 1. Processar pagamento (critical queue)
        BackgroundJob.Enqueue("critical", () => 
            ProcessPaymentAsync(orderId));
        
        // 2. Enviar email de confirmação (default queue, delay 1min)
        BackgroundJob.Schedule(() => 
            SendConfirmationEmailAsync(orderId), 
            TimeSpan.FromMinutes(1));
        
        // 3. Atualizar estoque (após pagamento - continuation)
        var paymentJobId = BackgroundJob.Enqueue(() => 
            ProcessPaymentAsync(orderId));
        
        BackgroundJob.ContinueJobWith(paymentJobId, () => 
            UpdateInventoryAsync(orderId));
        
        // 4. Gerar relatório (recurring)
        if (!RecurringJob.JobExists("order-report"))
        {
            RecurringJob.AddOrUpdate("order-report", 
                () => GenerateOrderReportAsync(),
                Cron.Daily);
        }
    }
}
```

## Health Check

```csharp
builder.Services.AddHealthChecks()
    .AddHangfire(options =>
    {
        options.MaximumDuration = TimeSpan.FromMinutes(2);
        options.ChecksToFail = new[] { "critical" };
    }, name: "hangfire");
```

## Fontes Oficiais
- hangfire.io
- docs.hangfire.io
- github.com/HangfireIO/Hangfire
