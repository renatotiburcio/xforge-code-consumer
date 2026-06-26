---
id: fgts-multa-rescisao
type: dominio
title: FGTS e Multa 40% na Rescisao: Calculo Completo e Casos Especiais
domain: trabalhista
trustScore: 90
source: CLT Art. 18 Lei 8.036/90 + Lei 13.932/19
tags: [fgts, rescisao, multa, trabalhista]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# FGTS e Multa 40% na Rescisao

## Contexto Legal

- FGTS: Fundo de Garantia do Tempo de Servico (Lei 8.036/90)
- Multa 40%: Sobre saldo FGTS, rescisao sem justa causa
- Multa 20%: Acordo entre empregado e empregador (Lei 13.932/19)

## Deposito Mensal

| Periodo | Percentual |
|---------|------------|
| Mes regular | 8% |
| Mes de ferias | 8% sobre adicional 1/3 |
| Mes de 13o | 8% sobre 13o |
| Aprendiz (1 ano) | 2% |
| Domestico | 8% (11% com aviso previo) |
| Tempo parcial | 8% proporcional |

## Multa Rescisoria por Tipo

| Tipo | Multa | Codigo eSocial |
|------|-------|----------------|
| Sem justa causa | 40% | S-2299 |
| Acordo Lei 13.932/19 | 20% | S-2299 acordo |
| Justa causa | 0% | S-2299 tipo 2 |
| Pedido demissao | 0% | S-2299 tipo 1 |
| Rescisao indireta | 40% | S-2299 tipo 4 |
| Culpa reciproca | 20% | S-2299 tipo 4 |
| Aposentadoria | 0% | S-2299 |
| Falecimento | 0% | S-2299 tipo 5 |
| Forca maior | 0% | S-2299 tipo 6 |
| Termino prazo determinado | 0% | S-2299 tipo 7 |
| Saida PDV | Conforme acordo | S-2299 tipo 8 |
| Termino experiencia | 0% | S-2299 tipo 9 |

## Calculo da Multa 40%

```
Saldo FGTS = Soma depositos + atualizacao (TR + juros 3% a.a.)
Multa 40% = Saldo FGTS x 0.40
```

### Exemplo

```
Funcionario: 5 anos de empresa
Salario mensal: R$ 3.000
Saldo FGTS atual: R$ 14.500
Multa 40% = R$ 14.500 x 0.40 = R$ 5.800
```

## Multa 20% (Acordo Lei 13.932/19)

```
Multa 20% = Saldo FGTS x 0.20
```

### Outras Consequencias do Acordo

- Aviso previo: 50%
- Saque FGTS: apenas 80% do saldo
- Seguro-desemprego: NAO tem direito

## Saque FGTS na Rescisao

| Situacao | Valor a sacar |
|----------|---------------|
| Demissao sem justa causa | 100% |
| Acordo | 80% |
| Rescisao indireta | 100% |
| Culpa reciproca | 80% |
| Justa causa | 0% |
| Pedido demissao | 0% |
| Aposentadoria | 100% |
| Falecimento | 100% (dependentes) |
| Forca maior | 100% |

## Saque-Aniversario (Lei 13.932/19)

A partir de 2020, opcao de saque anual:

| Saldo (R$) | Aliquota | Adicional |
|------------|----------|-----------|
| 0 - 500 | 50% | 0 |
| 500,01 - 1.000 | 40% | 50 |
| 1.000,01 - 5.000 | 30% | 150 |
| 5.000,01 - 10.000 | 20% | 650 |
| 10.000,01 - 15.000 | 15% | 1.150 |
| 15.000,01 - 20.000 | 10% | 1.900 |
| > 20.000 | 5% | 2.900 |

ATENCAO: Em caso de demissao sem justa causa, nao recebe multa 40%.

## eSocial - Eventos

| Evento | Descricao | Prazo |
|--------|-----------|-------|
| S-2200 | Admissao | Ate 5 dias uteis antes |
| S-2206 | Alteracao contrato | Ate 5 dias uteis antes |
| S-2299 | Desligamento | Ate 10 dias do desligamento |
| S-2399 | TSVE | Mensal |
| S-3000 | Exclusao | Imediato |

## Calculo de Verbas Rescisorias

### Componentes

1. Saldo de salario: dias x salario/dia
2. Aviso previo: 30 dias + 3 dias/ano (max 90)
3. 13o proporcional: meses/12 x salario
4. Ferias vencidas: salario + 1/3
5. Ferias proporcionais: meses/12 + 1/3
6. Saque FGTS (se aplicavel)
7. Multa FGTS (se aplicavel)

### Descontos

- INSS: sobre salario + 13o
- IRRF: sobre total tributavel
- Pensao alimenticia: se houver

## Tabela INSS 2025 (Desligamento)

| Faixa | Aliquota |
|-------|----------|
| Ate R$ 1.518,00 | 7.5% |
| R$ 1.518,01 - R$ 2.793,88 | 9% |
| R$ 2.793,89 - R$ 4.190,83 | 12% |
| R$ 4.190,84 - R$ 8.157,41 | 14% |

Teto INSS 2025: R$ 908.85

## Tabela IRRF 2025 (Rescisao)

| Faixa (R$) | Aliquota | Deducao |
|------------|----------|---------|
| 0 - 2.259,20 | 0% | 0 |
| 2.259,21 - 2.826,65 | 7.5% | 169.44 |
| 2.826,66 - 3.751,05 | 15% | 381.44 |
| 3.751,06 - 4.664,68 | 22.5% | 662.77 |
| > 4.664,68 | 27.5% | 896.00 |

## Implementacao XForge

```csharp
public decimal CalcularMultaFgts(decimal saldoFgts, TipoRescisao tipo)
{
    return tipo switch
    {
        TipoRescisao.SemJustaCausa => saldoFgts * 0.40m,
        TipoRescisao.Acordo => saldoFgts * 0.20m,
        TipoRescisao.CulpaReciproca => saldoFgts * 0.20m,
        TipoRescisao.RescisaoIndireta => saldoFgts * 0.40m,
        _ => 0m
    };
}
```

## Referencias

- CLT Art. 18 e Art. 487
- Lei 8.036/90 (FGTS)
- Lei 13.932/19 (multa acordo)
- LC 110/2001 (multa 10%)
- Manual eSocial S-2299
