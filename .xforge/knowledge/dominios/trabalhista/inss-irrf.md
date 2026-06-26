---
id: inss-irrf
type: knowledge
tags: [inss, irrf, contribuicao-previdenciaria, imposto-renda, tabelas, retencao, dirf, dctfweb]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre INSS e IRRF — Contribuição Previdenciária e Imposto de Renda Retido na Fonte
- **Principais responsabilidades**: Calcular INSS do empregado (tabela progressiva) e contribuição patronal (20%).; Calcular IRRF com deduções legais (dependentes, INSS, pensão alimen...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: inss, irrf, contribuicao-previdenciaria, imposto-renda, tabelas, retencao, dirf, dctfweb
- **Restrições/Regras**: **Teto INSS 2026**: R$ 8.380,75 (contribuição máxima).; **Dedução por dependente**: R$ 189,59 (2026).

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `inss-irrf` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# INSS e IRRF — Contribuição Previdenciária e Imposto de Renda Retido na Fonte

## Propósito
Documentar as regras de cálculo do INSS (contribuição previdenciária) e do IRF (Imposto de Renda Retido na Fonte): tabelas progressivas, deduções, retenção na fonte, DIRF e DCTFWeb.

## Responsabilidades
- Calcular INSS do empregado (tabela progressiva) e contribuição patronal (20%).
- Calcular IRRF com deduções legais (dependentes, INSS, pensão alimentícia).
- Gerar guias GPS (INSS) e DARF (IRRF).
- Informar na DIRF anual os rendimentos e retenções.
- Integrar com DCTFWeb para declaração de tributos federais.

## Dependências
- Tabelas INSS e IRRF atualizadas anualmente pela RFB/INSS.
- Cadastro de funcionários com dependentes declarados.
- Base de cálculo correta (proventos tributáveis).

## Constraints
- **Teto INSS 2026**: R$ 8.380,75 (contribuição máxima).
- **Dedução por dependente**: R$ 189,59 (2026).
- **Pensão alimentícia**: dedução integral (valor judicial).
- **DIRF**: entrega até último dia útil de fevereiro.
- **DCTFWeb**: 15º dia útil do 2º mês seguinte.

## Conteúdo

### INSS — Contribuição Previdenciária

#### Tabela INSS do Empregado (2026)
| Faixa Salarial | Alíquota |
|----------------|----------|
| Até R$ 1.518,00 | 7,50% |
| R$ 1.518,01 a R$ 2.777,65 | 9,00% |
| R$ 2.777,66 a R$ 4.190,38 | 12,00% |
| R$ 4.190,39 a R$ 8.380,75 | 14,00% |

**Teto INSS 2026**: R$ 8.380,75

#### Contribuição Patronal
| Tipo | Alíquota |
|------|----------|
| INSS Patronal | 20% sobre folha |
| RAT (Riscos Ambientais) | 1%, 2% ou 3% (conforme CNAE) |
| FAP (Fator Acidentário) | 0,5 a 2,0 (multiplicador do RAT) |
| Terceiros (SESI, SENAI, etc.) | 5,8% |
| Salário-educação | 2,5% |

#### Cálculo INSS (exemplo: salário R$ 5.000)
```
Faixa 1: R$ 1.518,00 × 7,50% = R$ 113,85
Faixa 2: (R$ 2.777,65 − R$ 1.518,00) × 9% = R$ 113,37
Faixa 3: (R$ 4.190,38 − R$ 2.777,65) × 12% = R$ 169,53
Faixa 4: (R$ 5.000 − R$ 4.190,38) × 14% = R$ 113,35
Total INSS = R$ 510,10
```

### IRRF — Imposto de Renda Retido na Fonte

#### Tabela IRRF 2026 (Mensal)
| Base de Cálculo | Alíquota | Parcela a Deduzir |
|-----------------|----------|-------------------|
| Até R$ 2.427,65 | Isento | R$ 0,00 |
| R$ 2.427,66 a R$ 2.826,65 | 7,50% | R$ 182,07 |
| R$ 2.826,66 a R$ 3.751,05 | 15,00% | R$ 393,23 |
| R$ 3.751,06 a R$ 4.664,68 | 22,50% | R$ 627,32 |
| Acima de R$ 4.664,68 | 27,50% | R$ 861,36 |

#### Deduções Permitidas
| Dedução | Valor |
|---------|-------|
| Dependente | R$ 189,59/mês por dependente |
| INSS | Valor efetivamente pago |
| Pensão alimentícia | Valor judicial (integral) |
| Previdência privada (PGBL) | Até 12% da renda bruta anual |
| Despesas médicas | Sem limite (comprovação) |
| Educação | Até R$ 3.561,50 por pessoa |

#### Cálculo IRRF (exemplo: salário R$ 5.000, 1 dependente)
```
Base = R$ 5.000 − R$ 510,10 (INSS) − R$ 189,59 (1 dependente) = R$ 4.300,31
IRRF = R$ 4.300,31 × 22,50% − R$ 627,32 = R$ 340,25
```


#### Isenção Efetiva (até ~R$ 5.000 com deduções)
Com as deduções legais (INSS + dependentes), um contribuinte com salário bruto de até ~R$ 5.000 pode ter base de cálculo abaixo do limite de isenção (R$ 2.427,65), resultando em IRRF = R$ 0,00.

**Exemplo (salário R$ 5.000, 2 dependentes):**
```
Base = R$ 5.000 − R$ 510,10 (INSS) − R$ 379,18 (2 dependentes) = R$ 4.110,72
Base ainda tributável → IRRF = R$ 4.110,72 × 22,50% − R$ 627,32 = R$ 297,59
```

**Exemplo (salário R$ 3.500, 2 dependentes):**
```
Base = R$ 3.500 − R$ 337,07 (INSS) − R$ 379,18 (2 dependentes) = R$ 2.783,75
Base ainda tributável → IRRF = R$ 2.783,75 × 7,50% − R$ 182,07 = R$ 26,71
```

**Exemplo (salário R$ 2.800, 1 dependente):**
```
Base = R$ 2.800 − R$ 224,80 (INSS) − R$ 189,59 (1 dependente) = R$ 2.385,61
Base < R$ 2.427,65 → ISENTO de IRRF
```

### Retenção na Fonte
| Rendimento | Obrigatoriedade |
|------------|----------------|
| Salário | Obrigatório |
| 13º salário | Obrigatório (2ª parcela) |
| Férias | Obrigatório |
| Rescisão | Obrigatório |
| PLR | Obrigatório |
| Serviços (PF) | Obrigatório |
| Aluguel (PF) | Obrigatório |

### Códigos de Receita IRRF
| Código | Descrição |
|--------|-----------|
| 0473 | Rendimento do trabalho assalariado |
| 0561 | Rendimento do trabalho sem vínculo |
| 0588 | Rendimento do trabalho — 13º salário |
| 3533 | Férias |
| 3562 | Participação nos lucros |

### DIRF — Declaração do IR Retido na Fonte
- **Obrigatoriedade**: Pessoas jurídicas que efetuaram retenção de IR.
- **Prazo**: último dia útil de fevereiro (ano seguinte ao ano-calendário).
- **Conteúdo**: rendimentos pagos, IR retido, deduções (dependentes, INSS, pensão).
- **Cruzamento**: RFB cruza DIRF com DIRPF do contribuinte (malha fina).

### DCTFWeb — Declaração de Débitos e Créditos Tributários Federais Web
- **Obrigatoriedade**: contribuintes de tributos federais.
- **Prazo**: 15º dia útil do 2º mês seguinte ao mês de referência.
- **Créditos declarados**: IRPJ, CSLL, PIS, COFINS, INSS, IPI, IOF, etc.
- **Integração**: importa dados da EFD-Reinf (retenções de IR, PIS, COFINS, CSLL).

### INSS sobre 13º Salário
- Incide exclusivamente na 2ª parcela.
- Alíquota conforme tabela progressiva.
- Teto do INSS se aplica.

### INSS sobre Férias
- Incide sobre valor total (férias + 1/3 constitucional).
- Alíquota conforme tabela progressiva.

### INSS sobre Rescisão
- Incide sobre saldo de salário, férias, 13º proporcional e aviso prévio.
- Alíquota conforme tabela progressiva.

## Related Documents
- [folha-pagamento](folha-pagamento.md) — Cálculos de folha
- [fgts](fgts.md) — FGTS, DIRF e DCTFWeb
- [esocial-folha](esocial-folha.md) — Eventos de folha no eSocial
- [clt](clt.md) — Consolidação das Leis do Trabalho

