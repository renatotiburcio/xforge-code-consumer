---
id: owasp-security-deep-dive
type: conhecimento
tags: [seguranca, owasp, jwt, oauth2, criptografia, lgpd, pentest]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre OWASP Top 10 e Segurança Profunda
- **Seções principais**: OWASP Top 10 (2021), JWT - Implementação Completa, OAuth2 / OpenID Connect, Criptografia
- **Tags**: seguranca, owasp, jwt, oauth2, criptografia, lgpd, pentest
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `owasp-security-deep-dive` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 8 |


# OWASP Top 10 e Segurança Profunda

## OWASP Top 10 (2021)

| # | Vulnerabilidade | Prevenção |
|---|----------------|-----------|
| A01 | Broken Access Control | RBAC, deny by default, validação server-side |
| A02 | Cryptographic Failures | TLS 1.3, AES-256, key rotation |
| A03 | Injection | Parameterized queries, input validation |
| A04 | Insecure Design | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Hardening, least privilege |
| A06 | Vulnerable Components | Dependency scanning, SCA |
| A07 | Auth Failures | MFA, rate limiting, secure passwords |
| A08 | Data Integrity Failures | CI/CD security, signed commits |
| A09 | Logging Failures | Audit logs, SIEM, alerting |
| A10 | SSRF | Allowlist URLs, network segmentation |

## JWT - Implementação Completa

### Geração
```csharp
public string GenerateToken(User user, IList<string> roles)
{
    var key = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

    var claims = new List<Claim>
    {
        new(ClaimTypes.NameIdentifier, user.Id),
        new(ClaimTypes.Email, user.Email!),
        new(ClaimTypes.Name, user.UserName!),
        new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
    };
    claims.AddRange(roles.Select(r => new Claim(ClaimTypes.Role, r)));

    var token = new JwtSecurityToken(
        issuer: _config["Jwt:Issuer"],
        audience: _config["Jwt:Audience"],
        claims: claims,
        expires: DateTime.UtcNow.AddMinutes(15),
        signingCredentials: creds);

    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

### Refresh Token
```csharp
public class RefreshToken
{
    public int Id { get; set; }
    public string Token { get; set; } = Guid.NewGuid().ToString();
    public DateTime Expires { get; set; } = DateTime.UtcNow.AddDays(7);
    public bool IsExpired => DateTime.UtcNow >= Expires;
    public DateTime? Revoked { get; set; }
    public bool IsActive => Revoked == null && !IsExpired;
}
```

### Validação
```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = config["Jwt:Issuer"],
            ValidAudience = config["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(config["Jwt:Key"]!)),
            ClockSkew = TimeSpan.Zero
        };
    });
```

## OAuth2 / OpenID Connect

### Fluxo Authorization Code + PKCE
```
1. Client → Auth Server: /authorize?response_type=code&code_challenge=...
2. Auth Server → User: Login page
3. User → Auth Server: Credentials
4. Auth Server → Client: code
5. Client → Auth Server: /token (code + code_verifier)
6. Auth Server → Client: access_token + refresh_token
```

### Implementation
```csharp
builder.Services.AddAuthentication()
    .AddOpenIdConnect("oidc", options =>
    {
        options.Authority = "https://auth.example.com";
        options.ClientId = "erp-client";
        options.ClientSecret = "secret";
        options.ResponseType = "code";
        options.UsePkce = true;
        options.Scope.Add("openid");
        options.Scope.Add("profile");
        options.Scope.Add("api");
        options.SaveTokens = true;
    });
```

## Criptografia

### At Rest
```csharp
// AES-256
using var aes = Aes.Create();
aes.Key = key; // 256 bits
aes.IV = iv;   // 128 bits
aes.Mode = CipherMode.CBC;
aes.Padding = PaddingMode.PKCS7;

using var encryptor = aes.CreateEncryptor();
var encrypted = encryptor.TransformFinalBlock(plainBytes, 0, plainBytes.Length);
```

### In Transit
```csharp
// TLS 1.3 forçado
AppContext.SetSwitch("System.Net.Security.SslProtocols", 
    (int)SslProtocols.Tls13);
```

### Hashing
```csharp
// BCrypt para senhas
var hash = BCrypt.Net.BCrypt.HashPassword(password, BCrypt.Net.BCrypt.GenerateSalt(12));
var isValid = BCrypt.Net.BCrypt.Verify(password, hash);
```

## Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    
    options.AddPolicy("auth", context =>
    {
        var ip = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        return RateLimitPartition.GetFixedWindowLimiter(ip, _ =>
            new FixedWindowRateLimiterOptions
            {
                PermitLimit = 5,
                Window = TimeSpan.FromMinutes(1)
            });
    });
});

app.MapPost("/auth/login", ...).RequireRateLimiting("auth");
```

## Headers de Segurança

```csharp
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");
    context.Response.Headers.Append("Content-Security-Policy", "default-src 'self'");
    context.Response.Headers.Append("Strict-Transport-Security", 
        "max-age=31536000; includeSubDomains");
    await next();
});
```

## LGPD - Implementação

### Consentimento
```csharp
public class ConsentRecord
{
    public int Id { get; set; }
    public string UserId { get; set; }
    public string Purpose { get; set; }
    public bool Granted { get; set; }
    public DateTime Timestamp { get; set; }
    public string IpAddress { get; set; }
}
```

### Direitos do Titular
```csharp
// Art. 18 LGPD
app.MapGet("/user/data", async (ClaimsPrincipal user, IUserService svc) =>
{
    var data = await svc.GetUserDataAsync(user.GetUserId());
    return Results.Ok(data);
});

app.MapDelete("/user/data", async (ClaimsPrincipal user, IUserService svc) =>
{
    await svc.DeleteUserDataAsync(user.GetUserId());
    return Results.Ok();
});
```

## Fontes Oficiais
- owasp.org/Top10
- auth0.com/docs
- docs.microsoft.com/aspnet/core/security
