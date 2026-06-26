---
id: decimo-terceiro
type: knowledge
tags: [decimo-terceiro, gratificacao-natalina, 13-salario, calculo, parcelas, esocial]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre 13º Salário (Gratificação Natalina) — Cálculos e Regras
- **Principais responsabilidades**: Calcular o 13º salário (salário/12 × meses trabalhados).; Gerenciar 1ª parcela (até 30/11) e 2ª parcela (até 20/12).; Constituir provisão contábil ...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: decimo-terceiro, gratificacao-natalina, 13-salario, calculo, parcelas, esocial
- **Restrições/Regras**: **1ª parcela**: até 30 de novembro (50% sem descontos).; **2ª parcela**: até 20 de dezembro (50% − INSS − IRRF).

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `decimo-terceiro` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# 13º Salário (Gratificação Natalina) — Cálculos e Regras

## Propósito
Documentar as regras do 13º salário conforme a Lei 4.090/1962: cálculo, parcelas, descontos, provisão contábil e integração com eSocial.

## Responsabilidades
- Calcular o 13º salário (salário/12 × meses trabalhados).
- Gerenciar 1ª parcela (até 30/11) e 2ª parcela (até 20/12).
- Constituir provisão contábil mensal (1/12 do salário).
- Calcular 13º proporcional na rescisão.
- Enviar eventos S-1200 e S-1210 no eSocial.

## Dependências
- Cadastro de funcionários com data de admissão e remuneração.
- Médias de adicionais (horas extras, noturno, insalubridade) dos últimos 12 meses.
- Tabelas INSS e IRRF vigentes.

## Constraints
- **1ª parcela**: até 30 de novembro (50% sem descontos).
- **2ª parcela**: até 20 de dezembro (50% − INSS − IRRF).
- **Mês trabalhado**: 15 ou mais dias = mês cheio (avo).
- **Adiantamento**: pode ser pago nas férias (solicitação até janeiro).
- **Justa causa**: perde o direito ao 13º proporcional.

## Conteúdo

### Regras Fundamentais
- **Base legal**: Lei 4.090/1962, Lei 4.749/1965, CF Art. 7º, VIII.
- **Base de cálculo**: salário + adicionais (HE, noturno, insalubridade, periculosidade, comissões).
- **Mês considerado**: 15 ou mais dias trabalhados = avo integral.

### Cálculo do 13º Salário
```
Base = Salário + Médias de adicionais
13º bruto = (Base / 12) × número de avos

1ª parcela = 13º bruto / 2 (sem descontos)
2ª parcela = 13º bruto − 1ª parcela − INSS − IRRF
```

**Exemplo (salário R$ 4.000, médias R$ 300, 12 avos):**
```
Base: R$ 4.300
13º bruto: R$ 4.300 / 12 × 12 = R$ 4.300
1ª parcela: R$ 4.300 / 2 = R$ 2.150 (sem desconto)
2ª parcela: R$ 2.150 − INSS − IRRF
```

### Descontos no 13º Salário
| Desconto | 1ª Parcela | 2ª Parcela |
|----------|------------|------------|
| INSS | Não | Sim |
| IRRF | Não | Sim |
| FGTS | Sim (sobre 1ª parcela) | Sim (sobre 2ª parcela) |
| Pensão alimentícia | Não | Sim (se judicial) |

### INSS sobre 13º Salário
- Incide exclusivamente na 2ª parcela.
- Alíquota conforme tabela progressiva vigente.
- Teto do INSS se aplica.

### IRRF sobre 13º Salário
- Incide exclusivamente na 2ª parcela.
- Base = 2ª parcela − INSS − dependentes (R$ 189,59 cada).
- Alíquota conforme tabela progressiva vigente.

### 13º Proporcional na Rescisão
```
13º proporcional = (Remuneração / 12) × avos trabalhados
```
- **Demissão sem justa causa**: integral (avos trabalhados).
- **Pedido de demissão**: integral.
- **Justa causa**: perde o direito.
- **Término de contrato**: proporcional.

### Adiantamento do 13º
- Pode ser pago por ocasião das férias (solicitação até 31 de janeiro).
- Valor: até 50% do 13º estimado.
- Descontado da 1ª parcela (ou da 2ª, se a 1ª for insuficiente).

### Provisão Contábil Mensal
```
Provisão mensal = Salário / 12
Lançamento: D — Despesa de 13º (Provisão) / C — Provisão para 13º
```
A provisão deve ser constituída mensalmente para atender ao regime de competência.

### 13º no eSocial
- **S-1200**: Remuneração do 13º (`indApuracao=2` — Anual).
- **S-1210**: Pagamento do 13º (`tpPgto=5`).
- Rubricas específicas para 1ª e 2ª parcela cadastradas na S-1010.
- Prazo de envio: até o dia 15 do mês seguinte ao pagamento.

### Incidência de Adicionais
Os adicionais integram a base de cálculo do 13º pela média dos últimos 12 meses:
```
Média HE = Total de HE no ano / 12
Média noturno = Total de adicional noturno no ano / 12
Base 13º = Salário + Média HE + Média noturno + Média insalubridade + ...
```

## Related Documents
- [clt](clt.md) — Consolidação das Leis do Trabalho
- [folha-pagamento](folha-pagamento.md) — Cálculos de folha
- [inss-irrf](inss-irrf.md) — Tabelas INSS e IRRF
- [esocial-folha](esocial-folha.md) — Eventos de folha no eSocial
