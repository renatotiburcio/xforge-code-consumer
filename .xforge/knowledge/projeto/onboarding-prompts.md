---
id: onboarding-prompts
type: conhecimento
tags: [onboarding, prompts, getting-started, quickstart, examples]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Prompts de Onboarding — Prontos para Usar
- **Seções principais**: Como Usar, 1. SETUP INICIAL, 2. ANÁLISE DE PROJETO, 3. CRIAÇÃO DE PROJETO
- **Tags**: onboarding, prompts, getting-started, quickstart, examples
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `onboarding-prompts` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 13 |


# Prompts de Onboarding — Prontos para Usar

## Como Usar

Copie e cole qualquer prompt no KiloCode. O sistema vai automaticamente selecionar o agent, skills e regras adequados.

---

## 1. SETUP INICIAL

### Configurar Provider de IA
```
/configurar-ia configurar OpenRouter com minha API key
```

### Verificar Setup
```
/doctor rodar validação completa do sistema
```

### Primeiro Contato
```
/xforge olá! sou novo aqui. me explique o que você pode fazer e como funciona este projeto
```

---

## 2. ANÁLISE DE PROJETO

### Análise Completa
```
/analisar-projeto analisar completamente este projeto: estrutura, arquitetura, padrões, testes, segurança, gaps, e me dar um score de maturidade
```

### Análise Rápida
```
/xforge analisar rapidamente a estrutura deste projeto e me dizer os 5 pontos mais importantes
```

### Análise de Segurança
```
/seguranca audit completo da API incluindo: JWT, rate limiting, CORS, input validation, secrets, dependências vulneráveis
```

### Análise de Performance
```
/xforge analisar performance do projeto: queries N+1, memory leaks, cached queries, async issues
```

---

## 3. CRIAÇÃO DE PROJETO

### API .NET Clean Architecture
```
/criar-projeto API REST com Clean Architecture, .NET 10, PostgreSQL, EF Core, xUnit para testes. Usar XForge.MediatR para CQRS, AutoMapper para mapping, FluentValidation para validação, Swagger para documentação. Incluir autenticação JWT com refresh token.
```

### API com Autenticação
```
/criar-projeto API de gestão de usuários com ASP.NET Core Identity, JWT, roles, policies, MFA, e refresh tokens. PostgreSQL + EF Core.
```

### Projeto com Blazor
```
/criar-projeto Blazor Server para dashboard administrativo com Tailwind CSS, gráficos, tabelas paginadas, e autenticação. PostgreSQL + EF Core.
```

### Worker Service
```
/criar-projeto .NET Worker Service para processamento de filas com Hangfire, RabbitMQ, e logging estruturado
```

---

## 4. DESENVOLVIMENTO

### Criar Feature
```
/desenvolver feature endpoint de CRUD de produtos com: model, DTO, handler (XForge.MediatR), repository, validação (FluentValidation), unit tests, e integration tests
```

### Criar Feature Completa
```
/desenvolver feature módulo de pagamentos com: Stripe integration, webhooks, retry policy, idempotency, logging, e testes unitários + de integração
```

### Criar Componente Blazor
```
/criar-componente-blazor tabela paginada de produtos com: busca, filtros, ordenação, paginação, e ações (editar, excluir). Usar Tailwind CSS.
```

### Corrigir Bug
```
/desenvolver bugfix o cálculo de ICMS para CST 60 está retornando R$ 0 quando deveria calcular o diferencial de alíquota para SP
```

### Refatorar Código
```
/desenvolver refactor separar o UserService em: UserValidator, UserRepository, UserMapper, e NotificationService. Manter todos os testes passando.
```

### Criar Handler CQRS
```
/desenvolver handler para CreateOrderCommand com: validação, regras de negócio, persistência, evento de domínio, e unit test
```

---

## 5. QUALIDADE E SEGURANÇA

### Quality Gates
```
/qualidade rodar todos os quality gates: build, testes, coverage, SOLID, segurança, e documentação
```

### Aumentar Coverage
```
/xforge identificar arquivos com coverage abaixo de 85% e criar testes unitários para eles
```

### Auditoria de Segurança
```
/seguranca audit completo da API incluindo: OWASP Top 10, JWT config, rate limiting, CORS, input validation, secrets scan, e dependências vulneráveis
```

### Conformidade LGPD
```
/seguranca verificar conformidade LGPD: consentimento, criptografia, direitos do titular, mapeamento de dados pessoais
```

---

## 6. DOCUMENTAÇÃO

### Gerar Docs
```
/documentacao gerar documentação completa da API: Swagger com exemplos, README com setup, e ADR para a escolha de Minimal APIs
```

### Gerar CHANGELOG
```
/release changelog das mudanças dos últimos 14 dias
```

### Criar ADR
```
/documentacao criar ADR para a decisão de usar PostgreSQL ao invés de SQL Server
```

### Atualizar README
```
/documentacao atualizar README.md com instruções de setup, dependências, e exemplos de uso
```

---

## 7. RELEASE E DEPLOY

### Preparar Release
```
/release preparar v2.1.0 com: 3 features novas, 2 bugs corrigidos, e breaking change no endpoint /api/v1/users
```

### Criar PR
```
/xforge criar PR com título descritivo, descrição das mudanças, e checklist de quality gates
```

### Deploy
```
/deploy preparar deploy para staging com validação completa
```

---

## 8. MEMÓRIA E CONHECIMENTO

### Salvar Decisão
```
/memoria salvar: decidimos usar PostgreSQL ao invés de SQL Server por suporte a JSONB e custo
```

### Buscar Contexto
```
/memoria buscar todas as decisões sobre autenticação e segurança
```

### Auditar Memória
```
/memoria auditar integridade da memória e verificar se há entradas obsoletas
```

### Ingerir Conhecimento
```
/conhecimento ingerir a documentação da API externa https://docs.example.com/api
```

---

## 9. ERP E NEGÓCIO

### Criar Módulo ERP
```
/xforge criar módulo de estoque com: entrada por NF-e, saída por pedido, curva ABC, inventário físico, relatório Kardex, e integração fiscal
```

### Calcular Folha
```
/xforge calcular folha de pagamento: INSS progressivo 2025, IRRF com dependentes, FGTS, horas extras com adicional 50%, e gerar holerite
```

### Escrituração Fiscal
```
/xforge gerar EFD ICMS/IPI do mês com apuração de ICMS, IPI, e validação de CFOP/CST
```

### Contabilidade
```
/xforge gerar DRE e Balanço Patrimonial do período com centro de custo e rateio de despesas fixas
```

---

## 10. DEBUGGING E TROUBLESHOOTING

### Diagnosticar Erro
```
/xforge diagnosticar por que o build está falhando e corrigir o problema
```

### Investigar Performance
```
/xforge investigar por que a API está lenta: verificar queries, cache, conexões, e memory usage
```

### Resolver Conflito
```
/xforge resolver o conflito de merge na branch main e garantir que todos os testes passam
```

---

## 11. TECNOLOGIAS ESPECÍFICAS

### Blazor
```
/criar-componente-blazor formulário de pagamento com validação, máscara de cartão, loading spinner, e feedback de sucesso/erro. Tailwind CSS.
```

### MAUI
```
/xforge criar app .NET MAUI para consulta de estoque com SQLite local, sincronização com API REST, e modo offline
```

### Tauri
```
/xforge criar app Tauri desktop para gestão de estoque com React frontend e Rust backend
```

### SignalR
```
/xforge adicionar SignalR hub para notificações em tempo real: pedidos atualizados, alertas de estoque, e mensagens do sistema
```

### gRPC
```
/xforge criar serviço gRPC para comunicação entre microservices com streaming e interceptors
```

---

## 12. DOMÍNIOS BRASILEIROS

### NF-e
```
/xforge implementar emissão de NF-e com: validação de CFOP, CST, cálculo de ICMS, geração de XML, e envio para SEFAZ
```

### eSocial
```
/xforge implementar envio de eventos eSocial: admissão (S-2200), remuneração (S-1200), e fechamento (S-1299)
```

### SPED
```
/xforge gerar EFD ICMS/IPI com: bloco C (documentos), bloco E (apuração), e validação com validador SEFAZ
```

### PIX
```
/xforge integrar pagamento via PIX: geração de QR Code estático/dinâmico, webhook de confirmação, e conciliação automática
```

### CNAB
```
/xforge implementar geração de CNAB 240 para remessa de boletos e processamento de retorno
```
