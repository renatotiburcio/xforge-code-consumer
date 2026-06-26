# Playbook: Deploy de API .NET em Produção

## Checklist Pré-Deploy

### 1. Build e Testes
```bash
dotnet restore
dotnet build --no-restore -c Release
dotnet test --no-build -c Release
```

### 2. Análise de Código
```bash
dotnet format --verify-no-changes
dotnet list package --vulnerable
```

### 3. Configurações
- [ ] Connection strings em variáveis de ambiente (NUNCA no código)
- [ ] JWT secrets configurados
- [ ] CORS origins configuradas
- [ ] Rate limiting habilitado
- [ ] Logging configurado (Nível: Warning em produção)

### 4. Banco de Dados
```bash
dotnet ef database update --context XForgeDbContext
```

### 5. Docker
```bash
docker build -t xforge-api .
docker run -p 5000:8080 xforge-api
```

## Checklist Pós-Deploy

- [ ] Health check respondendo (`/health`)
- [ ] Swagger desabilitado em produção
- [ ] Logs aparecendo no observability tool
- [ ] Métricas de performance OK
- [ ] Erros < 0.1%

## Rollback

```bash
# Se algo der errado
docker stop xforge-api
docker run -p 5000:8080 xforge-api:previous-tag
```

## Métricas de Sucesso

| Métrica | Meta |
|---------|------|
| Uptime | > 99.9% |
| Latência P95 | < 200ms |
| Erros 5xx | < 0.1% |
| Build time | < 5 min |
