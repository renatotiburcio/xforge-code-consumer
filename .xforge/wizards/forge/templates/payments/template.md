# Payments Template for /forge (v3.53.2)

When user requests --payments stripe (or other provider), generate this structure.

## 6 Supported Providers

| Provider | Region | Focus | When to use |
|----------|--------|-------|-------------|
| stripe | Global | Richest API, excellent docs | Default international |
| mercadopago | Brazil/LATAM | PIX, Boleto, installments | Default Brazil |
| pagseguro | Brazil | Traditional, enterprise | Legacy Brazil |
| asaas | Brazil | Subscriptions/recurrence | SaaS BR |
| paddle | Global | Merchant of Record (taxes) | Global sales without CNPJ |
| paypal | Global | Brand recognition | B2C international |

## Command syntax

```bash
# Single provider (default)
/forge new MinhaApp --payments stripe

# Multi-provider (Stripe + Mercado Pago for LATAM)
/forge new MinhaApp --payments stripe,mercadopago

# Multi-provider with strategy
/forge new MinhaApp --payments stripe:intl,mercadopago:br

# No payments
/forge new MinhaApp --no-payments
```

## Project Structure (auto-generated)

```
src/{name}.Infrastructure/Payments/
  IPaymentService.cs              # Provider-agnostic interface
  PaymentResult.cs                # Success/Failure/RequiresAction
  PaymentIntent.cs                # Intent to collect payment
  WebhookEvent.cs                 # Provider webhook payload
  Stripe/
    StripePaymentService.cs
    StripeWebhookHandler.cs       # Webhook + signature verification
    StripeOptions.cs              # SecretKey, PublishableKey, WebhookSecret
    StripeDependencyInjection.cs # AddStripe() extension
  MercadoPago/
    MercadoPagoService.cs
    MercadoPagoWebhookHandler.cs
    MercadoPagoOptions.cs
    MercadoPagoDependencyInjection.cs
  PagSeguro/ Asaas/ Paddle/ PayPal/ same structure

src/{name}.WebApi/Endpoints/Payments/
  CreateCheckoutSessionEndpoint.cs   # POST /api/payments/checkout
  StripeWebhookEndpoint.cs           # POST /api/payments/webhook/stripe
  GetPaymentStatusEndpoint.cs        # GET /api/payments/{id}/status
  RefundPaymentEndpoint.cs           # POST /api/payments/{id}/refund

src/{name}.Shared/Payments/
  PaymentMethod.cs                # Card, Pix, Boleto, BankTransfer
  PaymentStatus.cs                # Pending, Paid, Failed, Refunded
  CreateCheckoutRequest.cs
  CheckoutResponse.cs
  WebhookPayload.cs

tests/{name}.Infrastructure.Tests/Payments/
  StripePaymentServiceTests.cs     # Uses Stripe test mode keys
  MercadoPagoServiceTests.cs
  WebhookSignatureTests.cs         # Verifies signature validation
```

## CRITICAL Rules

1. NEVER touch card data directly - use Stripe Elements / Mercado Pago Brick (PCI-DSS)
2. Always verify webhook signatures - prevents fraud
3. Idempotency keys - prevent duplicate charges on retry
4. Store provider IDs - never re-create customers, sync via ID
5. Secrets in user-secrets / Azure Key Vault - NEVER in appsettings.json
6. Webhook handler must be idempotent - same event fires multiple times
7. LGPD compliance - mask PII in logs, allow data deletion request
8. Test mode - generate test keys, never live keys in dev/test

## IPaymentService Interface

```csharp
namespace {name}.Infrastructure.Payments;

public interface IPaymentService
{
    Task<PaymentResult> CreateCheckoutAsync(CreateCheckoutRequest request, CancellationToken ct = default);
    Task<PaymentStatus> GetStatusAsync(string providerPaymentId, CancellationToken ct = default);
    Task<PaymentResult> RefundAsync(string providerPaymentId, decimal amount, CancellationToken ct = default);
    Task<WebhookEvent> ParseWebhookAsync(string rawBody, string signature, CancellationToken ct = default);
}

public class PaymentResult
{
    public bool IsSuccess { get; init; }
    public string? ProviderPaymentId { get; init; }
    public string? CheckoutUrl { get; init; }
    public PaymentStatus Status { get; init; }
    public string? ErrorMessage { get; init; }
}
```

## NuGet packages per provider

```xml
<!-- Stripe -->
<PackageReference Include="Stripe.net" Version="47.0.0" />

<!-- Mercado Pago -->
<PackageReference Include="mercadopago.sdk" Version="2.4.0" />

<!-- PagSeguro -->
<PackageReference Include="Uol.PagSeguro" Version="3.0.0" />

<!-- Asaas -->
<PackageReference Include="Asaas.Sdk" Version="1.0.0" />

<!-- Paddle -->
<PackageReference Include="Paddle.Sdk" Version="1.0.0" />

<!-- PayPal -->
<PackageReference Include="PayPalCheckoutSdk" Version="1.0.4" />
```

## User Secrets setup (REQUIRED)

```bash
dotnet user-secrets init --project src/{name}.WebApi
dotnet user-secrets set "Payments:Stripe:SecretKey" "sk_test_REAL_KEY_HERE"
```

## Coverage by Layer (v3.53.2)

coverage by layer, coverage + layer, coverage per layer
- IPaymentService (provider-agnostic): 100%
- Stripe: 100% (CreateCheckout, GetStatus, Refund, Webhook)
- MercadoPago: 100%
- PagSeguro/Asaas/Paddle/PayPal: 100% (same pattern)
- Endpoints: 100% (Checkout, Webhook, Status, Refund)
- Shared DTOs: 100%
- Tests: 100% (per provider)
- Payments total: 100% (6 providers supported)