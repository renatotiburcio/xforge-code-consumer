---
title: "Conciliacao Bancaria Automatica"
id: knowledge-conciliacao
type: knowledge
summary: "Algoritmo de conciliacao: matching exato, fuzzy, valor parcial, OFX/CSV/CNAB"
keywords: ["conciliacao", "ofx", "cnab", "extrato-bancario", "matching"]
trustScore: 80
lastValidated: 2026-06-13
---

# Conciliacao Bancaria Automatica

## Fluxo

```
Extrato (OFX/CSV/CNAB retorno)
    -> Parser
    -> Lancamentos normalizados
    -> Matching engine (3 estrategias)
    -> Conciliados / Pendentes / Divergentes
```

## Estrategias de matching

### 1. Exato (confianca 100%)

- valor == AND data == AND documento ==
- 60-80% dos casos

### 2. Fuzzy valor+data (confianca 90%)

- valor == AND data in [-2, +2] days AND tipo compativel
- 15-25% adicionais

### 3. Valor parcial (confianca 70%)

- Lancamento no extrato e menor que titulo
- Requer confirmacao manual

## Parsers

| Formato | Fonte | Dificuldade |
|---------|-------|-------------|
| OFX | Santander, Itau, Bradesco | media |
| CSV | bancos menores, fintechs | baixa |
| CNAB retorno | integracao oficial | alta |
| API | Open Finance, fintechs | baixa |

## Algoritmo

```python
def conciliar(extrato, titulos):
    conciliados, pendentes = [], []
    for lanc in extrato:
        match = next((t for t in titulos
                      if t.valor == lanc.valor
                      and t.data_vencimento == lanc.data
                      and t.documento == lanc.documento
                      and t.status == "aberto"), None)
        if not match:
            match = next((t for t in titulos
                          if t.valor == lanc.valor
                          and abs((t.data_vencimento - lanc.data).days) <= 2
                          and t.status == "aberto"), None)
        if not match:
            match = next((t for t in titulos
                          if lanc.valor < t.valor
                          and lanc.valor > t.valor * Decimal("0.5")
                          and abs((t.data_vencimento - lanc.data).days) <= 5
                          and t.status == "aberto"), None)
        if match:
            conciliados.append((lanc, match))
            match.status = "conciliado"
        else:
            pendentes.append(lanc)
    return Resultado(conciliados, pendentes)
```

## Divergencias

| Caso | Acao |
|------|------|
| Valor a maior | Valor real + diferenca como despesa bancaria |
| Valor a menor | Lancamento parcial + titulo aberto com saldo |
| Data diferente | Aceitar (juros) ou rejeitar (erro) |
| Titulo desconhecido | Criar generico ou "a identificar" |
| Multiplos matches | Apresentar para usuario escolher |

## CNAB 240/400

- Header do arquivo
- Header de lote
- Registros de detalhe
- Trailler de lote
- Trailler de arquivo

Cada campo tem tamanho fixo.

## Boas praticas

- Idempotencia (nao conciliar 2x)
- Audit log (quem/quando/confianca)
- Reversao com motivo
- Reconciliacao diaria
- SLA para pendencias (5 dias uteis)