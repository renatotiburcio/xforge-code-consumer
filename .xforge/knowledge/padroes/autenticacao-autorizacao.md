---
id: autenticacao-autorizacao
type: pattern
tags: [auth, jwt, identity, blazor, security, oauth2, oidc]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Autenticação e Autorização
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: auth, jwt, identity, blazor, security, oauth2, oidc
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `autenticacao-autorizacao` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Autenticação e Autorização

## Propósito

Estabelecer padrões de autenticação JWT, refresh tokens, autorização por roles/policies e integração com Blazor Server/WASM para sistemas ERP multi-tenant.

## Descrição do Padrão

### Geração de JWT

```csharp
public TokenPair GenerateTokens(ApplicationUser user, IEnumerable<Claim> claims)
{
    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_settings.Secret));
    var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

    var accessToken = new JwtSecurityToken(
        issuer: _settings.Issuer,
        audience: _settings.Audience,
        claims: claims,
        expires: DateTime.UtcNow.AddMinutes(_settings.AccessTokenExpirationMinutes),
        signingCredentials: credentials
    );

    return new TokenPair {
        AccessToken = new JwtSecurityTokenHandler().WriteToken(accessToken),
        RefreshToken = Convert.ToBase64String(RandomNumberGenerator.GetBytes(64)),
        AccessTokenExpiresAt = DateTime.UtcNow.AddMinutes(15),
        RefreshTokenExpiresAt = DateTime.UtcNow.AddDays(7)
    };
}
```

**Claims padrão:** `sub` (userId), `name`, `email`, `tenant_id`, `empresa_id`, `roles`.

### Refresh Token Flow

1. Cliente recebe Access Token (15 min) + Refresh Token (7 dias).
2. Quando Access Token expira, cliente envia `POST /api/auth/refresh`.
3. Servidor valida Refresh Token, gera novo par e invalida o antigo (rotação).
4. Se Refresh Token for reusado (possível roubo), revoga todos os tokens do usuário.

```csharp
public class TokenRefreshHandler : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken ct)
    {
        var response = await base.SendAsync(request, ct);
        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            var refreshed = await _authService.TryRefreshTokensAsync();
            if (refreshed)
            {
                request.Headers.Authorization = new AuthenticationHeaderValue(
                    "Bearer", await _tokenService.GetAccessTokenAsync());
                response = await base.SendAsync(request, ct);
            }
        }
        return response;
    }
}
```

### Autorização por Políticas

```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("FinanceiroAccess", policy =>
        policy.RequireClaim("modulo", "Financeiro", "Admin"));

    options.AddPolicy("MesmaEmpresa", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim("empresa_id",
                context.Resource?.ToString())));
});
```

### Blazor Auth State

- **Server**: `AuthenticationStateProvider` via `IHttpContextAccessor`.
- **WASM**: `RemoteAuthenticationStateProvider` com OIDC/OAuth2.
- **Proteção de rotas**: `[Authorize(Policy = "Financeiro.Read")]` ou `<AuthorizeRouteView>` em `App.razor`.

### Armazenamento Seguro (WASM)

```csharp
public class TokenService
{
    private readonly IJSRuntime _jsRuntime;
    public async Task SaveTokensAsync(TokenPair tokens) { /* localStorage/sessionStorage */ }
    public async Task<string?> GetAccessTokenAsync() { /* ... */ }
    public async Task ClearTokensAsync() { /* ... */ }
}
```

## Quando Usar

- APIs REST que exigem autenticação stateless (JWT).
- Apps Blazor Server com dados sensíveis (código no servidor).
- Apps Blazor WASM públicos com IdentityServer/Duende.
- Sistemas multi-tenant com isolamento por `tenant_id`.

## Exemplo de Uso

```csharp
[HttpPost("login")]
public async Task<IActionResult> Login([FromBody] LoginRequest request)
{
    var user = await _userManager.FindByEmailAsync(request.Email);
    if (user == null || !await _userManager.CheckPasswordAsync(user, request.Password))
        return Unauthorized(new { message = "Credenciais inválidas" });

    var tokens = await GenerateTokensAsync(user);
    return Ok(tokens);
}

[Authorize(Policy = "FinanceiroAccess")]
[HttpGet("contas-pagar")]
public async Task<IActionResult> ListarContas() { /* ... */ }
```

## Padrões Relacionados

- [[seguranca-api]] — proteção de endpoints, CORS, rate limiting
- [[componentes-blazor]] — Blazor auth state e proteção de rotas
- [[logging.md]] — auditoria de autenticação

