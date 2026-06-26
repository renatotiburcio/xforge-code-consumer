---
name: legacy-import
description: Use when importing, migrating, or consolidating legacy systems, old codebases, or external projects into the current architecture.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# legacy-import

## Objetivo

Importar sistemas legados preservando conhecimento e minimizando risco.

## Fases de Importação

### 1. Reconhecimento
- Analisar estrutura do legado
- Identificar dependências
- Mapear funcionalidades
- Classificar: reusar / migrar / descartar

### 2. Extração
- Extrair regras de negócio
- Extrair schemas de banco
- Extrair APIs e contratos
- Extrair testes existentes

### 3. Mapeamento
- Legado → Arquitetura atual
- Dados → Novo schema
- APIs → Novos endpoints
- Configurações → Novo formato

### 4. Migração
- Criar plano de migração passo-a-passo
- Módulo por módulo
- Testar cada módulo antes do próximo
- Manter fallback para legado

### 5. Validação
- Comparar resultados legado vs novo
- Validar performance
- Validar segurança
- Documentar diferenças

## Regras

- NUNCA deletar legado antes de validar novo
- Sempre manter rollback disponível
- Documentar cada decisão de mapeamento
- Testar com dados reais (anonymizados)
