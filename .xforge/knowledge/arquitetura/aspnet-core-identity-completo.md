---
id: aspnet-core-identity-completo
type: conhecimento
tags: [identity, auth, jwt, cookie, oauth2, oidc, mfa, claims, roles, policies]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre ASP.NET Core Identity - Guia Completo
- **Seções principais**: Conceito, Configuração, Autenticação, Autorização
- **Tags**: identity, auth, jwt, cookie, oauth2, oidc, mfa, claims, roles, policies
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `aspnet-core-identity-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 13 |


# ASP.NET Core Identity - Guia Completo

## Conceito

ASP.NET Core Identity é o sistema de autenticação e autorização integrado, suportando autenticação baseada em cookie, JWT, OAuth2, OpenID Connect e MFA.

## Configuração

### Setup Básico
```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    options.Password.RequireDigit = true;
    options.Password.RequiredLength = 8;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequireUppercase = true;
    options.Password.RequireLowercase = true;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.User.RequireUniqueEmail = true;
    options.SignIn.RequireConfirmedEmail = false;
})
.AddEntityFrameworkStores<AppDbContext>()
.AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/account/login";
    options.LogoutPath = "/account/logout";
    options.AccessDeniedPath = "/account/access-denied";
    options.ExpireTimeSpan = TimeSpan.FromMinutes(60);
    options.SlidingExpiration = true;
});
```

### Entity Configuration
```csharp
public class ApplicationUser : IdentityUser
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public bool IsActive { get; set; } = true;
}

public class AppDbContext : IdentityDbContext<ApplicationUser, IdentityRole, string>
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    
    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        
        builder.Entity<ApplicationUser>(e =>
        {
            e.Property(u => u.FirstName).HasMaxLength(100).IsRequired();
            e.Property(u => u.LastName).HasMaxLength(100).IsRequired();
            e.HasIndex(u => u.Email).IsUnique();
        });
    }
}
```

## Autenticação

### Cookie Authentication
```csharp
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        options.LoginPath = "/Account/Login";
        options.LogoutPath = "/Account/Logout";
        options.AccessDeniedPath = "/Account/AccessDenied";
        options.Cookie.Name = "XForge.Auth";
        options.Cookie.HttpOnly = true;
        options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
        options.Cookie.SameSite = SameSiteMode.Strict;
        options.ExpireTimeSpan = TimeSpan.FromHours(1);
        options.SlidingExpiration = true;
    });
```

### JWT Authentication
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
        
        options.Events = new JwtBearerEvents
        {
            OnTokenValidated = async context =>
            {
                var userManager = context.HttpContext.RequestServices
                    .GetRequiredService<UserManager<ApplicationUser>>();
                var user = await userManager.GetUserAsync(context.Principal!);
                if (user == null || !user.IsActive)
                    context.Fail("User inactive or not found");
            }
        };
    });
```

### OAuth2 / OpenID Connect
```csharp
builder.Services.AddAuthentication()
    .AddGoogle(options =>
    {
        options.ClientId = config["Google:ClientId"]!;
        options.ClientSecret = config["Google:ClientSecret"]!;
        options.SaveTokens = true;
    })
    .AddMicrosoftAccount(options =>
    {
        options.ClientId = config["Microsoft:ClientId"]!;
        options.ClientSecret = config["Microsoft:ClientSecret"]!;
        options.SaveTokens = true;
    })
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

## Autorização

### Roles
```csharp
// Criar roles
await roleManager.CreateAsync(new IdentityRole("Admin"));
await roleManager.CreateAsync(new IdentityRole("Manager"));
await roleManager.CreateAsync(new IdentityRole("User"));

// Atribuir role
await userManager.AddToRoleAsync(user, "Admin");

// Verificar role
if (User.IsInRole("Admin"))
{
    // Acesso admin
}
```

### Policies
```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));
    
    options.AddPolicy("MinimumAge", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
    
    options.AddPolicy("ApiKey", policy =>
        policy.RequireClaim("api_key"));
    
    options.AddPolicy("SameCompany", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim("company_id", "same")));
});

// Custom Requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }
    
    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var birthDate = context.User.FindFirst("birth_date");
        if (birthDate == null)
        {
            context.Fail();
            return Task.CompletedTask;
        }
        
        var age = DateTime.Today - DateTime.Parse(birthDate.Value);
        if (age.Days >= requirement.MinimumAge * 365)
            context.Succeed(requirement);
        else
            context.Fail();
        
        return Task.CompletedTask;
    }
}
```

### Resource-Based Authorization
```csharp
public class DocumentAuthorizationHandler : 
    AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        if (context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }
        
        if (resource.OwnerId == context.User.FindFirst("sub")?.Value)
        {
            context.Succeed(requirement);
        }
        
        return Task.CompletedTask;
    }
}
```

## Multi-Factor Authentication (MFA)

### Configuração
```csharp
builder.Services.Configure<IdentityOptions>(options =>
{
    options.SignIn.RequireConfirmedAccount = true;
});

// TOTP (Google Authenticator, etc.)
builder.Services.AddDefaultIdentity<ApplicationUser>(options =>
{
    options.SignIn.RequireConfirmedAccount = true;
})
.AddEntityFrameworkStores<AppDbContext>()
.AddDefaultTokenProviders()
.AddTokenProvider<TotpSecurityStampValidator<ApplicationUser>>("TOTP");
```

### Setup MFA
```csharp
[HttpPost]
public async Task<IActionResult> EnableTwoFactor()
{
    var user = await _userManager.GetUserAsync(User);
    var token = await _userManager.GenerateTwoFactorTokenAsync(user, "TOTP");
    
    // QR Code para Google Authenticator
    var qrCodeUrl = $"otpauth://totp/{Uri.EscapeDataString("XForge")}:{Uri.EscapeDataString(user.Email)}?secret={token}&issuer=XForge";
    
    return View(new TwoFactorSetupViewModel { QrCodeUrl = qrCodeUrl });
}
```

## Claims

### Adicionar Claims
```csharp
var claims = new List<Claim>
{
    new(ClaimTypes.Name, user.UserName),
    new(ClaimTypes.Email, user.Email!),
    new("company_id", user.CompanyId.ToString()),
    new("department", user.Department),
    new("permissions", string.Join(",", user.Permissions))
};

var claimsIdentity = new ClaimsIdentity(
    claims, CookieAuthenticationDefaults.AuthenticationScheme);

await HttpContext.SignInAsync(
    CookieAuthenticationDefaults.AuthenticationScheme,
    new ClaimsPrincipal(claimsIdentity));
```

### Usar Claims
```csharp
// Em controller
var companyId = User.FindFirst("company_id")?.Value;
var permissions = User.FindFirst("permissions")?.Value?.Split(',');

// Em policy
options.AddPolicy("CanEditDocuments", policy =>
    policy.RequireClaim("permissions", "documents.edit"));
```

## Refresh Tokens

```csharp
public class RefreshToken
{
    public int Id { get; set; }
    public string UserId { get; set; }
    public string Token { get; set; } = Guid.NewGuid().ToString("N");
    public DateTime Expires { get; set; } = DateTime.UtcNow.AddDays(7);
    public DateTime? Revoked { get; set; }
    public string CreatedByIp { get; set; }
    public string? ReplacedByToken { get; set; }
    
    public bool IsExpired => DateTime.UtcNow >= Expires;
    public bool IsActive => Revoked == null && !IsExpired;
}

public async Task<TokenResponse> GenerateTokensAsync(ApplicationUser user)
{
    var accessToken = GenerateJwtToken(user);
    var refreshToken = new RefreshToken
    {
        UserId = user.Id,
        Expires = DateTime.UtcNow.AddDays(7),
        CreatedByIp = "127.0.0.1"
    };
    
    _context.RefreshTokens.Add(refreshToken);
    await _context.SaveChangesAsync();
    
    return new TokenResponse(accessToken, refreshToken.Token);
}

public async Task<TokenResponse> RefreshTokenAsync(string token, string ipAddress)
{
    var refreshToken = await _context.RefreshTokens
        .FirstOrDefaultAsync(r => r.Token == token);
    
    if (refreshToken == null || !refreshToken.IsActive)
        throw new UnauthorizedAccessException("Invalid refresh token");
    
    // Revoke old token
    refreshToken.Revoked = DateTime.UtcNow;
    refreshToken.ReplacedByToken = newRefreshToken.Token;
    
    // Generate new tokens
    var user = await _userManager.FindByIdAsync(refreshToken.UserId);
    return await GenerateTokensAsync(user);
}
```

## External Logins

```csharp
// Listar logins externos
var logins = await _userManager.GetLoginsAsync(user);

// Adicionar login externo
var result = await _userManager.AddLoginAsync(user, info);

// Remover login externo
await _userManager.RemoveLoginAsync(user, loginProvider, providerKey);

// Verificar se tem login externo
var hasExternalLogins = (await _userManager.GetLoginsAsync(user)).Any();
```

## Password Reset

```csharp
// Gerar token de reset
var token = await _userManager.GeneratePasswordResetTokenAsync(user);

// Resetar senha
var result = await _userManager.ResetPasswordAsync(user, token, newPassword);

// Email de reset
var callbackUrl = Url.Action("ResetPassword", "Account",
    new { token, email = user.Email }, protocol: Request.Scheme);

await _emailSender.SendAsync(user.Email, "Reset Password",
    $"Please reset your password by <a href='{callbackUrl}'>clicking here</a>.");
```

## Confirmação de Email

```csharp
// Gerar token de confirmação
var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);

// Confirmar email
var result = await _userManager.ConfirmEmailAsync(user, token);

// Verificar se confirmado
var isConfirmed = await _userManager.IsEmailConfirmedAsync(user);
```

## Endpoints (Minimal APIs)

```csharp
app.MapPost("/auth/register", async (RegisterRequest req, UserManager<ApplicationUser> userManager) =>
{
    var user = new ApplicationUser
    {
        UserName = req.Email,
        Email = req.Email,
        FirstName = req.FirstName,
        LastName = req.Results.LastName
    };
    
    var result = await userManager.CreateAsync(user, req.Password);
    if (!result.Succeeded)
        return Results.BadRequest(result.Errors);
    
    return Results.Ok(new { message = "User created" });
});

app.MapPost("/auth/login", async (LoginRequest req, SignInManager<ApplicationUser> signInManager) =>
{
    var result = await signInManager.PasswordSignInAsync(
        req.Email, req.Password, req.RememberMe, lockoutOnFailure: true);
    
    if (result.Succeeded)
        return Results.Ok(new { message = "Logged in" });
    
    if (result.IsLockedOut)
        return Results.BadRequest(new { error = "Account locked" });
    
    return Results.BadRequest(new { error = "Invalid credentials" });
});

app.MapPost("/auth/logout", async (SignInManager<ApplicationUser> signInManager) =>
{
    await signInManager.SignOutAsync();
    return Results.Ok(new { message = "Logged out" });
}).RequireAuthorization();
```

## Segurança

### Best Practices
```csharp
// Forçar HTTPS
app.UseHsts();
app.UseHttpsRedirection();

// Anti-forgery
app.MapControllers().RequireAntiforgeryToken();

// Content Security Policy
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("Content-Security-Policy", 
        "default-src 'self'; script-src 'self'");
    await next();
});

// Rate limiting em login
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("login", opt =>
    {
        opt.PermitLimit = 5;
        opt.Window = TimeSpan.FromMinutes(1);
    });
});
```

## Fontes Oficiais
- docs.microsoft.com/aspnet/core/security/authentication
- docs.microsoft.com/aspnet/core/security/authorization
- github.com/dotnet/aspnetcore/tree/main/src/Identity
