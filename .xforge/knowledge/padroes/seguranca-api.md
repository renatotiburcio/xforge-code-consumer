---
id: seguranca-api
type: pattern
tags: [security, api, cors, rate-limiting, https, headers, xss, csrf, sql-injection]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Segurança de API
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: security, api, cors, rate-limiting, https, headers, xss, csrf, sql-injection
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `seguranca-api` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Segurança de API

## Propósito

Estabelecer padrões de segurança para APIs REST em sistemas ERP, cobrindo CORS, rate limiting, HTTPS, headers de segurança, prevenção de SQL injection, XSS, CSRF e validação de entrada.

## Descrição do Padrão

### CORS

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("ErpWebPolicy", policy =>
    {
        policy.WithOrigins("https://erp.meuerp.com.br", "https://app.meuerp.com.br")
              .WithMethods("GET", "POST", "PUT", "DELETE", "PATCH")
              .WithHeaders("Authorization", "Content-Type", "X-Correlation-Id")
              .AllowCredentials()
              .SetPreflightMaxAge(TimeSpan.FromHours(24));
    });
});

app.UseCors("ErpWebPolicy");
app.UseAuthentication();
app.UseAuthorization();
```

### Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;

    options.AddFixedWindowLimiter("PorIp", opt =>
    {
        opt.PermitLimit = 100;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 10;
    });

    options.AddSlidingWindowLimiter("PorUsuario", opt =>
    {
        opt.PermitLimit = 60;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.SegmentsPerWindow = 6;
    });

    options.AddTokenBucketLimiter("Pesado", opt =>
    {
        opt.TokenLimit = 20;
        opt.ReplenishmentPeriod = TimeSpan.FromSeconds(10);
        opt.TokensPerPeriod = 5;
    });
});
```

### HTTPS e HSTS

```csharp
builder.Services.AddHsts(options =>
{
    options.Preload = true;
    options.IncludeSubDomains = true;
    options.MaxAge = TimeSpan.FromDays(365);
});

if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
}
app.UseHttpsRedirection();
```

### Headers de Segurança

```csharp
context.Response.Headers.Append("Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'");
context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
context.Response.Headers.Append("X-Frame-Options", "DENY");
context.Response.Headers.Append("X-XSS-Protection", "1; mode=block");
context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");
context.Response.Headers.Append("Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload");
context.Response.Headers.Remove("Server");
context.Response.Headers.Remove("X-Powered-By");
```

### Prevenção de SQL Injection

```csharp
// CORRETO — EF Core usa parameterized queries automaticamente
var cliente = await _context.Clientes
    .FirstOrDefaultAsync(c => c.Cnpj == cnpj);

// CORRETO — Dapper com parâmetros
var result = await connection.QueryFirstOrDefaultAsync<Cliente>(
    "SELECT * FROM Clientes WHERE Id = @Id", new { Id = id });

// ERRADO — Nunca concatene strings em SQL
// .FromSqlRaw($"SELECT * FROM Clientes WHERE Nome LIKE '%{nome}%'")
```

### Prevenção de XSS

- Codificação de output automática no Razor.
- CSP header restringe scripts.
- Sanitização de input: `Regex.Replace(input, "<.*?>", "")`.

### Prevenção de CSRF

```csharp
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-XSRF-TOKEN";
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    options.Cookie.SameSite = SameSiteMode.Strict;
});

// Para APIs com JWT, CSRF geralmente não é necessário.
// Se usar cookies para auth, é obrigatório:
[HttpPost("transferencia")]
[ValidateAntiForgeryToken]
[Authorize]
public async Task<IActionResult> Transferencia(TransferenciaDto dto) { }
```

### Proteção contra Mass Assignment

```csharp
// ERRADO — aceita qualquer campo
[HttpPost] public IActionResult Create(Cliente cliente)

// CORRETO — DTO com apenas campos permitidos
[HttpPost] public IActionResult Create(ClienteCreateDto dto)
```

### Nunca Logar Dados Sensíveis

```csharp
// ERRADO
_logger.LogInformation("Login: {Email}, Senha: {Senha}", email, senha);

// CORRETO
_logger.LogInformation("Login attempt: {Email}", LogMasker.MaskEmail(email));
```

## Quando Usar

- Toda API REST deve ter CORS, rate limiting e HTTPS.
- Headers de segurança em produção.
- Validação de entrada em todos os endpoints.
- Anti-forgery quando usar cookies de autenticação.

## Exemplo de Uso

```csharp
[ApiController]
[Route("api/[controller]")]
[EnableRateLimiting("PorUsuario")]
public class ClientesController : ControllerBase
{
    [HttpPost]
    [Authorize(Roles = "Admin,Fiscal")]
    [EnableRateLimiting("PorIp")]
    public async Task<IActionResult> Criar(ClienteCreateDto dto)
    {
        // Validação automática via FluentValidation + sanitização
        // Log de auditoria
        // Resposta com headers de segurança
    }
}
```

## Padrões Relacionados

- [[autenticacao-autorizacao.md]] — JWT, Identity, policies
- [[validacao.md]] — validação de entrada com FluentValidation
- [[logging.md]] — log de segurança e auditoria

