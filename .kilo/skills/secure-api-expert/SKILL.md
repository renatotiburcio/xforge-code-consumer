---
name: secure-api-expert
description: Expert em segurança de APIs: rate limiting, input validation, CORS, helmet, injection prevention.
metadata:
  version: "37.0.0"
  xforge-category: "continuous-security"
---

# secure-api-expert

## Objetivo

Auditar e implementar segurança em endpoints de API.

## Checklist de Segurança de API

### Input Validation
- [ ] Todas as entradas validadas no boundary
- [ ] Schema validation (FluentValidation/DataAnnotations)
- [ ] Max length em todos os campos string
- [ ] Whitelist de caracteres quando aplicável
- [ ] SQL parameterized queries (NUNCA concatenação)

### Rate Limiting
- [ ] Global rate limit configurado
- [ ] Per-endpoint limits para operações custosas
- [ ] Sliding window ou fixed window
- [ ] Retry-After header na resposta 429

### CORS
- [ ] Origins configuradas explicitamente (NUNCA *)
- [ ] Methods e Headers restrictos
- [ ] Credentials separado de wildcard

### Headers de Segurança
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Strict-Transport-Security
- [ ] Content-Security-Policy
- [ ] X-Request-ID para trace

### Injection Prevention
- [ ] SQL: parameterized queries
- [ ] NoSQL: schema validation
- [ ] Command: no user input em commands
- [ ] Path traversal: sanitize file paths
- [ ] XSS: output encoding

## Procedimento

1. Listar todos os endpoints públicos
2. Aplicar checklist por endpoint
3. Classificar vulnerabilidades (CVSS)
4. Gerar código de correção
5. Bloquear se CRITICAL ou HIGH
