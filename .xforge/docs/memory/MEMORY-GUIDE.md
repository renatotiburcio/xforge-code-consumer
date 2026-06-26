# Guia de Memória XForge

## 1. O Que é Memória

Memória é o que o sistema **sabe** sobre o projeto. Não é conhecimento genérico — é **fato específico, decisão tomada, preferência definida, contexto vivo**.

**Conhecimento** = "Como fazer migrations no EF Core" (reutilizável, genérico)
**Memória** = "Decidimos usar PostgreSQL para o módulo fiscal" (específico, persistente)

---

## 2. Estrutura de Memória

```
.xforge/memory/
├── index.json              — Manifest de memória (o que existe e onde)
├── project-preferences.md  — Preferências técnicas e de processo
├── known-decisions.md      — Decisões tomadas com contexto
├── current-context.md      — Contexto vivo do projeto
├── known-errors.md         — Erros conhecidos e soluções
└── business-rules.md       — Regras de negócio do domínio
```

---

## 3. Tipos de Memória

### 3.1 Preferências do Projeto (`project-preferences.md`)

**O que é:** Decisões sobre como o projeto deve funcionar. Padrões, ferramentas, abordagens preferidas.

**Exemplo:**

```markdown
# Memória - Preferências do Projeto

## Preferências Técnicas

- O template deve funcionar sem server externo
- RAG lexical local é obrigatório
- Embeddings são opcionais (futuro)
- Releases devem sair em `dist/`
- Commits em português, código em inglês

## Preferências de Processo

- Toda mudança estrutural roda `doctor.ps1` após
- Toda adição de conhecimento reindexa o RAG
- ADRs para decisões arquiteturais significativas
```

### 3.2 Decisões Conhecidas (`known-decisions.md`)

**O que é:** Registro de decisões tomadas com contexto e data.

**Exemplo:**

```markdown
# Memória - Decisões Conhecidas

## 2026-06-08 — Terminal como produto único

**Contexto:** Múltiplas pastas históricas acumuladas (.xforge/reports, .xforge/backlog, .xforge/testing)

**Decisão:** Focar em `terminal/` como template copiável. Pastas históricas removidas.

**Consequências:**
- Template mais limpo e focado
- Menos confusão sobre o que é template e o que é histórico
- Releases mais enxutas
```

### 3.3 Contexto Atual (`current-context.md`)

**O que é:** O que está acontecendo agora no projeto. Muda frequentemente.

**Exemplo:**

```markdown
# Memória - Contexto Atual

## Fase Atual
Reconhecimento e documentação do template terminal/

## Em Andamento
- Criação de política de conhecimento
- Criação de templates de memória
- Alimentação de conhecimento real
- Criação de backlog/sprints/roadmap

## Próximos Passos
- Implementar script de ingestão automatizada
- Adicionar conhecimento de fontes oficiais
- Criar ADRs para decisões fundamentais
```

### 3.4 Erros Conhecidos (`known-errors.md`)

**O que é:** Erros recorrentes ou difíceis que já foram resolvidos.

**Exemplo:**

```markdown
# Memória - Erros Conhecidos

## EF Core + SQLite em testes

**Sintoma:** Migration falha com "SQLite does not support migrations"

**Causa:** SQLite não suporta todos os operações de migration do EF Core

**Solução:** Usar InMemory database para testes de migration, ou PostgreSQL com Testcontainers

**Fonte:** https://learn.microsoft.com/ef/core/providers/sqlite/limitations
```

### 3.5 Regras de Negócio (`business-rules.md`)

**O que é:** Regras do domínio de negócio que afetam decisões técnicas.

**Exemplo:**

```markdown
# Memória - Regras de Negócio

## Domínio Fiscal

- NFe deve ter schema válido antes de envio
- Cálculo de ICMS segue tabela ICMS-UF vigente
- SPED deve ser gerado com layout vigente

## Domínio Contábil

- Plano de contas segue padrão ECD
- Lançamentos devem ter data dentro do período aberto
```

---

## 4. Como Atualizar Memória

### Regra de Ouro
> **Memória nunca é deletada. É versionada.**

Quando uma informação deixa de ser válida:
1. Mova para seção de histórico
2. Marque como `superseded` ou `deprecated`
3. Registre a nova informação
4. Atualize a data

### Processo

1. Identifique o tipo de memória (preferência, decisão, contexto, erro, regra)
2. Abra o arquivo correspondente em `.xforge/memory/`
3. Adicione a nova informação com data e contexto
4. Se substituindo informação antiga, mova para histórico
5. Reindexe o RAG: `.\.kilo\automation\scripts\rag\index-local.ps1`

---

## 5. Index de Memória

O arquivo `.xforge/memory/index.json` serve como manifest. Deve ser atualizado quando novos arquivos de memória são criados.

---

## 6. Diferença: Memória vs Conhecimento vs Regra

| Aspecto | Memória | Conhecimento | Regra |
|---------|---------|--------------|-------|
| Escopo | Específico do projeto | Reutilizável | Obrigatório |
| Exemplo | "Usamos PostgreSQL" | "Como configurar PostgreSQL" | "Nunca usar connection string hardcoded" |
| Ciclo de vida | Nunca deletada | Versionada | Atualizada/removida |
| Formato | Fato + data + contexto | Como fazer + referências | Lista de restrições |
