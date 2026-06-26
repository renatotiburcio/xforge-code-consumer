# Simplicity Criterion — XForge Engineer

## Visão Geral

Inspirado no autoresearch: "All else being equal, simpler is better." Uma melhoria mínima que adiciona complexidade feia não vale a pena. Uma melhoria de ~0 mas código muito mais simples? Vale muito.

## Regra

```
╔══════════════════════════════════════════════════════════════╗
║  AVALIAR CADA MUDANÇA POR:                                  ║
║'  1. Quanto melhorou? (ganho de xfs)                         ║'
║'  2. Quanto complexidade adicionou? (linhas, arquivos, deps)  ║'
║'  3. O ganho justifica a complexidade?                        ║'
╚══════════════════════════════════════════════════════════════╝
```

## Matriz de Decisão

| Ganho xfs | Complexidade | Decisão | Exemplo |
|-----------|-------------|---------|---------|
| > 5% | Baixa | ✅ **KEEP** | Adicionar null check |
| > 5% | Média | ✅ **KEEP** | Adicionar FluentValidation |
| > 5% | Alta | ⚠️ **REVIEW** | Refatorar service inteiro |
| 1-5% | Baixa | ✅ **KEEP** | Remover unused using |
| 1-5% | Média | ⚠️ **REVIEW** | Adicionar cache layer |
| 1-5% | Alta | ❌ **DISCARD** | Migrar framework |
| < 1% | Baixa | ✅ **KEEP** | Melhoria trivial |
| < 1% | Média | ❌ **DISCARD** | Complexidade desnecessária |
| < 1% | Alta | ❌ **DISCARD** | Over-engineering |
| 0% (ou negativo) | Qualquer | ❌ **DISCARD** | Não ajudou |

## Classificação de Complexidade

### Baixa (1 ponto)
- Mudança em 1-2 linhas
- 1 arquivo afetado
- Sem novas dependências
- Sem mudança de API

### Média (2 pontos)
- Mudança em 10-30 linhas
- 2-5 arquivos afetados
- Sem novas dependências
- Mudança interna (não expõe nova API)

### Alta (3 pontos)
- Mudança em 30+ linhas
- 5+ arquivos afetados
- Novas dependências adicionadas
- Nova API ou mudança de contrato
- Mudança de arquitetura

## Fórmula de Vale a Pena

```
vale_a_pena = (ganho_xfs * 100) / (complexidade_pontos * 10)

SE vale_a_pena > 1.0 → KEEP
SE vale_a_pena entre 0.5 e 1.0 → REVIEW (humano decide)
SE vale_a_pena < 0.5 → DISCARD
```

### Exemplos

| Mudança | Ganho xfs | Complexidade | Vale a pena? |
|---------|-----------|-------------|--------------|
| Adicionar null check | +3% | 1 (baixa) | 3.0 → ✅ KEEP |
| Adicionar FluentValidation | +7% | 2 (média) | 3.5 → ✅ KEEP |
| Migrar para Redis | +2% | 3 (alta) | 0.67 → ⚠️ REVIEW |
| Refatorar todo o service | +1% | 3 (alta) | 0.33 → ❌ DISCARD |
| Remover código morto | +0.5% | 1 (baixa) | 0.5 → ⚠️ REVIEW |
| Adicionar feature complexa | +0.2% | 3 (alta) | 0.07 → ❌ DISCARD |

## Regras Adicionais

1. **Deletar código é melhor que adicionar**: Se remove código e mantém funcionalidade, é sempre bom
2. **Consistência > Novidade**: Seguir padrão existente é melhor que criar padrão novo
3. **UmResponsabilidade**: Cada mudança deve ter um objetivo claro
4. **Reversibilidade**: Preferir mudanças que podem ser desfeitas facilmente

## Integração com Scoring

O campo `simplicity` no xfs já reflete parcialmente este critério. Mas o agente deve usar esta matriz ANTES de implementar, não só depois de medir.

```
ANTES de implementar:
1. Estimar ganho de xfs (baseado em experiência)
2. Estimar complexidade (linhas, arquivos, deps)
3. Calcular vale_a_pena
4. SE < 0.5: não implementar, buscar alternativa mais simples

DEPOIS de implementar:
1. Medir xfs real
2. Comparar com estimativa
3. Ajustar estimativas futuras (aprendizado)
```
