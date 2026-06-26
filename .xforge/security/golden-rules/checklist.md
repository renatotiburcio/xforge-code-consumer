# Security Golden Rules Checklist

## Pre-Commit

- [ ] No secrets hardcoded (API keys, passwords, tokens)
- [ ] No SQL injection vulnerabilities
- [ ] Input validation on all user inputs
- [ ] Output encoding for XSS prevention
- [ ] Authentication required for protected routes
- [ ] Authorization checks in place

## Pre-Deploy

- [ ] All tests passing
- [ ] No critical CVEs in dependencies
- [ ] Security headers configured (CORS, CSP, HSTS)
- [ ] Rate limiting enabled
- [ ] Logging configured (no sensitive data)
- [ ] Database migrations reviewed
- [ ] Environment variables set (no defaults in code)

## LGPD Compliance

- [ ] Personal data encrypted at rest
- [ ] Personal data encrypted in transit (TLS)
- [ ] Consent mechanism in place
- [ ] Data retention policy defined
- [ ] Right to deletion implemented
- [ ] Data processing records maintained
