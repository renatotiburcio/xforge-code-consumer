# Auto-Retry & Recovery — XForge Engineer

## Visão Geral

Quando o agente encontra um erro durante execução, ele deve tentar se recuperar automaticamente antes de parar. Este sistema define o fluxo de recuperação.

## Fluxo de Recuperação

```
Tarefa em execução
    │
    ─¼
Erro detectado
    │
    ├─→ Tentar fix automático (máx 3 tentativas)
    │       │
    │       ├─→ Sucesso? → Continuar execução
    │       │
    │       └─→ Falhou? → Tentar abordagem alternativa
    │               │
    │               ├─→ Sucesso? → Continuar execução
    │               │
    │               └─→ Falhou? → Salvar checkpoint + parar
    │
    └─→ Erro conhecido? → Usar solução do Error Graph
```

## Regras de Retry

### Quando Auto-Retry

| Tipo de Erro | Auto-Retry? | Máx Tentativas |
|-------------|-------------|----------------|
| Build error (CS*) | ✅ Sim | 3 |
| Null reference | ✅ Sim | 2 |
| Import missing | ✅ Sim | 1 |
| Test failure | ✅ Sim | 2 |
| Timeout | ✅ Sim | 1 |
| API error | ✅ Sim | 2 |
| Disk full | ❌ Não | 0 |
| Auth error | ❌ Não | 0 |
| Network error | ⚠️ Com retry | 3 |

### Padrões de Fix Automático

#### 1. Build Error → Fix
```
Erro: CS0246: tipo não encontrado
→ Verificar imports faltando
→ Adicionar using/referência
→ Rebuild
```

#### 2. Null Reference → Fix
```
Erro: NullReferenceException
→ Identificar variável nula
→ Adicionar null check
→ Rebuild
```

#### 3. Test Failure → Fix
```
Erro: Teste falhou
→ Ler mensagem de erro
→ Corrigir código ou teste
→ Re-run testes
```

#### 4. Timeout → Retry
```
Erro: Timeout
→ Verificar se operação é válida
→ Re-executar com timeout maior
→ Se falhar de novo → checkpoint + parar
```

### Padrões de Abordagem Alternativa

Quando o fix automático não funciona, o agente deve tentar uma abordagem diferente:

| Abordagem Original | Alternativa |
|-------------------|-------------|
| Editar arquivo existente | Criar novo arquivo |
| Usar Entity Framework | Usar SQL direto |
| Implementar feature completa | Criar stub/mocking |
| Rodar todos os testes | Rodar só testes afetados |
| Refatorar tudo | Refatorar incremental |

## Integração com Checkpoint & Resume

Quando o agente não consegue se recuperar após 3 tentativas:

1. Salva checkpoint com:
   - O que foi feito até agora
   - Qual erro ocorreu
   - Quais tentativas foram feitas
   - Qual abordagem alternativa pode funcionar

2. Mostra mensagem:
   ```
   ⚠️ Erro não resolvido após 3 tentativas.
   Progresso salvo em .xforge/checkpoints/<task-id>.json
   Erro: [descrição do erro]
   Última tentativa: [o que foi tentado]
   
   Para continuar, execute: /xforge retomar tarefa
   ```

3. Para automaticamente (espera input do usuário)

## Regras para o Agente

1. **Sempre tentar pelo menos 1 fix** antes de parar
2. **Log do erro** em `.xforge/errors/` para aprendizado futuro
3. ** atualizar error-graph** se o erro é novo
4. **NÃO** tentar fix se o erro é de:
   - Permissão negada
   - Disk space
   - Auth/token
   - Dados corrompidos

## Métricas

| Métrica | Meta |
|---------|------|
| Taxa de auto-fix bem-sucedido | > 60% |
| Tempo médio de retry | < 30s |
| Checkpoints salvos por erros | < 5% das tarefas |
| Erros que precisam de input humano | < 20% |
