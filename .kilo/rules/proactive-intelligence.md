# Proactive Intelligence — XForge Engineer

## Visão Geral

O agente XForge não é apenas reativo — ele analisa o contexto e sugere ações preventivas antes que problemas aconteçam. Baseado no grafo de erros (errors-solutions-graph.json) e no padrão de trabalho do usuário.

## Tipos de Inteligência Proativa

### 1. Context-Aware Suggestions
O agente analisa o que você está fazendo e sugere ações relacionadas.

**Trigger**: Usuário edita arquivo de domínio específico
**Ação**: Sugerir validações do domínio

```
🔍 Detectei que você está editando FolhaPagamentoService.cs

Sugestões:
1. Validar tabelas INSS/IRRF 2025 antes de commitar
2. Rodar testes de cálculo de folha
3. Verificar se eSocial S-1200 está configurado
```

### 2. Error Prevention
O agente verifica erros conhecidos antes que eles aconteçam.

**Trigger**: Código usa padrão que historicamente causa erro
**Ação**: Alertar e sugerir correção

```
⚠️ Atenção: Este padrão (FirstOrDefault sem null check) causou 3 NullReferenceException nos últimos 30 dias.

Recomendação:
var produto = await _context.Produtos.FirstOrDefaultAsync(x => x.Id == id);
if (produto == null) return NotFound();  // ← Adicionar esta linha
```

### 3. Impact Analysis
Antes de uma mudança significativa, o agente analisa o impacto.

**Trigger**: Edição em arquivo com muitos dependents
**Ação**: Listar arquivos impactados e sugerir testes

```
📊 Impact Analysis para FolhaPagamentoService.cs:

Arquivos dependents (7):
- Controllers/FolhaController.cs
- Tests/FolhaServiceTests.cs
- Handlers/CalcularINSSHandler.cs
- Handlers/CalcularIRRFHandler.cs
- Handlers/CalcularFGTSHandler.cs
- Handlers/CalcularFeriasHandler.cs
- Handlers/CalcularDecimoHandler.cs

Sugestão: Rodar testes antes de commitar
```

### 4. Pattern Recognition
O agente detecta padrões no seu trabalho e sugere melhorias.

**Trigger**: Mesma correção aplicada 3+ vezes
**Ação**: Sugerir automação ou regra

```
🔄 Padrão detectado: Você corrigiu "async sem await" 5 vezes esta semana.

Sugestão: Criar regra self-healing SH-003 para corrigir automaticamente.
```

### 5. Knowledge Gap Detection
O agente detecta quando falta conhecimento para uma tarefa.

**Trigger**: Tarefa requer conhecimento não disponível
**Ação**: Sugerir criação de knowledge file

```
📚 Knowledge gap detectado: Não tenho informações sobre API específica da prefeitura para NFS-e.

Sugestão: Criar knowledge file em .xforge/knowledge/dominitos/fiscal/nfse-[cidade].md
```

## Integração com Split Architecture

### Router Layer (qwen2.5:7b, <2s)
O Router detecta se a tarefa precisa de inteligência proativa:
- `needsProactiveAnalysis: true` → Worker analisa contexto
- `errorPrevention: true` → Verifica grafo de erros
- `impactAnalysis: true` → Lista arquivos dependentes

### Worker Layer (qwen2.5:72b, 10-30s)
O Worker executa a análise proativa completa:
- Lê errors-solutions-graph.json
- Analisa dependências do código
- Verifica padrões históricos
- Gera sugestões contextualizadas

## Comandos de Inteligência Proativa

```
/inteligencia executar análise completa do projeto
/inteligencia verificar padrões de erro nos últimos 30 dias
/inteligencia sugerir melhorias de performance
/inteligencia analisar impacto de mudança em [arquivo]
/inteligencia detectar knowledge gaps
```

## Métricas

| Métrica | Meta |
|---------|------|
| Sugestões aceitas pelo usuário | > 70% |
| Erros prevenidos por mês | > 20 |
| Falsos positivos | < 10% |
| Tempo de análise proativa | < 5s |
| Knowledge gaps detectados | 2-5/mês |
