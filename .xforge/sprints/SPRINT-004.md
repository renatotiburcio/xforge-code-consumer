---
id: sprint-004
type: sprint
tags: [sprint, p3, grpc, sdk, marketplace, dashboard, multi-tenant, cache, offline]
owner: project-team
version: 1.1.0
updated: 2026-06-09
---

# Sprint 4: P3

## Status: CONCLUIDA — Infrastructure & Extensibility

## Resumo
Quarta sprint do template. Foco em infraestrutura avancada: gRPC headless, SDK Node.js, marketplace, dashboard, multi-tenant, RAG cache incremental e modo offline.

## Periodo
- **Inicio:** 2026-06-09
- **Fim:** 2026-09-30
- **Duracao:** 16 semanas

## Objetivos
1. Preparar submissao ao Kilo Marketplace (B-021)
2. Implementar cache incremental do RAG (B-024)
3. Adicionar suporte multi-tenant (B-023)
4. Implementar modo offline (B-025)
5. Scaffolding para gRPC headless server (B-019)
6. Scaffolding para SDK Node.js (B-020)
7. Scaffolding para dashboard web (B-022)

## Backlog Items
- B-019, B-020, B-021, B-022, B-023, B-024, B-025

---

## B-021: Marketplace Submission

### Escopo
Preparar o template para submissao no Kilo Marketplace:
- Criar `.xforge/marketplace/kilo-template.json` com metadados
- Criar screenshot/preview
- Validar conformidade com requisitos do marketplace

---

## B-024: RAG Incremental Cache

### Escopo
Modificar `rag_local.py` para:
- Calcular hash de cada arquivo antes de indexar
- Comparar com hash anterior para detectar mudancas
- Reindexar apenas arquivos modificados
- Manter manifesto de hashes em `.xforge/rag/manifest.json`

---

## B-023: Multi-Tenant Config

### Escopo
Suportar multiplos tenants em um unico template:
- Arquivo `.xforge/tenants/<tenant-id>/config.json` por tenant
- Variaveis de ambiente `XFORGE_TENANT` para selecionar tenant ativo
- Isolamento de knowledge base por tenant

---

## B-025: Offline Mode

### Escopo
Permitir operacao sem conexao:
- Cache local de respostas do modelo
- Fallback para modelo local (Ollama)
- Queue de operacoes pendentes para sync posterior

---

## B-019: gRPC Headless Server

### Escopo
Scaffolding para servidor gRPC:
- Definir protocol buffers
- Implementar servidor Python
- Suportar operacoes via gRPC (query, index, doctor)

---

## B-020: Node.js SDK

### Escopo
Scaffolding para SDK Node.js:
- Empacotar comandos XForge como funcoes TypeScript
- Publicar como pacote npm
- Documentar API

---

## B-022: Dashboard Web

### Escopo
Scaffolding para dashboard React:
- Pagina de health (doctor results)
- Pagina de RAG stats
- Pagina de agents/skills overview
- Usar React + Tailwind + shadcn/ui

---

## Definition of Done
- [x] Marketplace metadata pronto
- [x] RAG cache incremental funcional (789 tracked files)
- [x] Multi-tenant config suportado (2 tenants: default, acme)
- [x] Modo offline documentado + script
- [x] gRPC scaffolding criado (proto + server.py)
- [x] SDK Node.js scaffolding criado (TypeScript)
- [x] Dashboard scaffolding criado (Next.js + shadcn)

## Metricas
| Indicador | Meta |
|-----------|------|
| doctor.ps1 erros | 0 |
| RAG reindex speedup | 5x+ (arquivos nao modificados) |
| Tenants suportados | 2+ |
