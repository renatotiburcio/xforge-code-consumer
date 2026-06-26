# Webhooks PIX + Idempotencia

Padroes para receber e processar webhooks PIX com seguranca.

## Fluxo do webhook

```
PSP/BCB --> POST /webhooks/pix --> API XForge
                                         |
                                         v
                                    [Validar signature]
                                         |
                                         v
                                    [Verificar idempotencia]
                                         |
                                         v
                                    [Processar evento]
                                         |
                                         v
                                    [Atualizar pagamento]
                                         |
                                         v
                                    [Retornar 200]
```

## Validacao de assinatura

```csharp
public class WebhookSignatureValidator {
    public bool Validate(string payload, string signature, string publicKeyPem) {
        using var rsa = RSA.Create();
        rsa.ImportFromPem(publicKeyPem);
        var sig = Convert.FromBase64String(signature);
        var data = Encoding.UTF8.GetBytes(payload);
        return rsa.VerifyData(data, sig, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
    }
}
```

## Idempotencia

```csharp
public class WebhookProcessor {
    private readonly IIdempotencyStore _store;
    private readonly IPagamentoRepository _repo;

    public async Task<WebhookResult> ProcessarAsync(WebhookEvent evento, CancellationToken ct) {
        // 1. Verificar se ja foi processado
        if (await _store.ExistAsync(evento.EventId, ct)) {
            return WebhookResult.AlreadyProcessed();
        }

        // 2. Marcar como em processamento
        await _store.RegisterAsync(evento.EventId, ct);

        // 3. Buscar pagamento
        var pagamento = await _repo.ObterPorTxidAsync(evento.Txid, ct);
        if (pagamento is null) {
            return WebhookResult.NotFound();
        }

        // 4. Atualizar status
        pagamento.Status = MapearStatus(evento.Status);
        pagamento.PagoEm = evento.Horario;
        await _repo.SalvarAsync(pagamento, ct);

        // 5. Marcar como completo
        await _store.CompleteAsync(evento.EventId, ct);
        return WebhookResult.Ok();
    }
}
```

## Retry do PSP

- PSPs reenviam webhooks por ate 72h se nao receberem 2xx
- Sempre retorne 200 rapido (processar async se necessario)
- Para processamentos longos, use fila (Hangfire)

## Tags

pix, webhook, idempotencia, signature, mTLS, br
