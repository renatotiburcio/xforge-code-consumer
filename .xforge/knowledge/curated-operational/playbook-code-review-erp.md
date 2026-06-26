# Playbook: Code Review para ERP Brasileiro

## Checklist de Code Review

### 1. Conformidade Fiscal
- [ ] Cálculos de impostos usam tabelas vigentes (2025)
- [ ] CFOPs mapeados corretamente
- [ ] Regras de Substituição Tributária aplicadas
- [ ] Validar XML contra XSD antes de enviar

### 2. Conformidade Trabalhista
- [ ] INSS progressivo calculado corretamente
- [ ] IRRF com isenção até R$2.259,20
- [ ] FGTS 8% sobre remuneração
- [ ] eSocial layout correto

### 3. Segurança
- [ ] Sem secrets hardcoded
- [ ] Input validation com FluentValidation
- [ ] JWT com expiry ≤ 15 min
- [ ] Rate limiting habilitado
- [ ] CORS com origins explícitas

### 4. Performance
- [ ] Sem N+1 queries
- [ ] Async/await consistente
- [ ] CancellationToken em métodos async
- [ ] Paging em listas grandes

### 5. Código
- [ ] Testes unitários cobrem > 85%
- [ ] Sem warnings no build
- [ ] Formatação consistente (dotnet format)
- [ ] XML comments em endpoints públicos
