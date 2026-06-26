---
id: ferias
type: knowledge
tags: [ferias, periodo-aquisitivo, periodo-concessivo, abono-pecuniario, calculo, esocial]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Férias — Cálculos e Regras (CLT Art. 129-153)
- **Principais responsabilidades**: Calcular férias (salário/30 × dias + 1/3 constitucional).; Controlar períodos aquisitivo e concessivo de cada empregado.; Gerenciar abono pecuniári...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: ferias, periodo-aquisitivo, periodo-concessivo, abono-pecuniario, calculo, esocial
- **Restrições/Regras**: **Período concessivo**: 12 meses após o aquisitivo. Após o prazo, pagamento em dobro (CLT Art. 137).; **Pagamento**: ...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `ferias` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Férias — Cálculos e Regras (CLT Art. 129-153)

## Propósito
Documentar as regras de férias conforme a CLT: períodos aquisitivo e concessivo, cálculo de remuneração, abono pecuniário, férias coletivas, descontos e integração com eSocial.

## Responsabilidades
- Calcular férias (salário/30 × dias + 1/3 constitucional).
- Controlar períodos aquisitivo e concessivo de cada empregado.
- Gerenciar abono pecuniário (venda de até 10 dias).
- Aplicar tabela de faltas para redução de dias.
- Gerar provisão contábil mensal (salário + 1/3) / 12.
- Enviar eventos S-2230 (afastamento) e S-1200 (remuneração) no eSocial.

## Dependências
- Cadastro de funcionários com data de admissão e histórico de faltas.
- Médias de adicionais (horas extras, noturno, insalubridade) dos últimos 12 meses.
- Tabelas INSS e IRRF vigentes para cálculo de descontos.

## Constraints
- **Período concessivo**: 12 meses após o aquisitivo. Após o prazo, pagamento em dobro (CLT Art. 137).
- **Pagamento**: até 2 dias antes do início das férias (CLT Art. 145).
- **Fracionamento**: até 3 períodos (1 com mínimo 14 dias, demais com mínimo 5 dias).
- **Início proibido**: véspera de feriado ou DSR.
- **Mínimo de gozo**: 5 dias corridos por período.

## Conteúdo

### Períodos
- **Aquisitivo**: 12 meses de trabalho contados da admissão ou término das últimas férias.
- **Concessivo**: 12 meses seguintes ao término do aquisitivo. O empregador deve conceder dentro deste prazo.

### Cálculo de Férias
```
Base de cálculo = Salário + Médias de adicionais (HE, noturno, insalubridade, periculosidade)
Valor diário = Base / 30
Valor férias = Valor diário × dias de férias
1/3 constitucional = Valor férias / 3
Total bruto = Valor férias + 1/3
```

**Exemplo (salário R$ 3.000, médias R$ 200, 30 dias):**
```
Base: R$ 3.200
Diária: R$ 3.200 / 30 = R$ 106,67
Férias: R$ 106,67 × 30 = R$ 3.200
1/3: R$ 3.200 / 3 = R$ 1.066,67
Total bruto: R$ 4.266,67
(-) INSS e IRRF
= Líquido de férias
```

### Férias Proporcionais (Rescisão)
```
Dias proporcionais = (Meses trabalhados no período aquisitivo / 12) × 30
Mês com 15+ dias = mês cheio para cálculo proporcional
Valor = (Base / 30) × dias proporcionais + 1/3
```

### Abono Pecuniário (Venda de Férias)
- **Limite**: até 10 dias (1/3 do período).
- **Prazo para solicitar**: até 15 dias antes do término do período aquisitivo.
- **Valor**: (Base / 30) × dias vendidos + 1/3.
- **IRRF**: isento (jurisprudência STF).
- **INSS**: incide normalmente.

### Férias Coletivas
- Podem ser concedidas a todos, setores ou departamentos.
- **Duração mínima**: 5 dias corridos.
- **Comunicação**: sindicato e MTE com 15 dias de antecedência.
- Empregados com menos de 12 meses: férias proporcionais.

### Descontos em Férias
- **INSS**: incide sobre valor total (férias + 1/3).
- **IRRF**: incide sobre valor total, com dedução de dependentes.
- **Faltas**: reduzem dias de férias conforme tabela.

### Tabela de Faltas × Dias de Férias (Art. 130 CLT)
| Faltas no período aquisitivo | Dias de Férias |
|------------------------------|----------------|
| Até 5 faltas | 30 dias |
| 6 a 14 faltas | 24 dias |
| 15 a 23 faltas | 18 dias |
| 24 a 32 faltas | 12 dias |
| Mais de 32 faltas | Sem direito |

### Provisão Contábil de Férias
```
Provisão mensal = (Salário + 1/3) / 12
Lançamento: D — Despesa de Férias (Provisão) / C — Provisão para Férias
```

### Férias no eSocial
- **S-2230**: Afastamento temporário — início e retorno das férias.
- **S-1200**: Remuneração de férias com rubricas específicas.
- **S-1210**: Pagamento de férias (`tpPgto=6`).
- **S-2299**: Desligamento — inclui férias proporcionais na rescisão.

### Perda do Direito a Férias (Art. 133 CLT)
- Mais de 32 faltas injustificadas no período aquisitivo.
- Licença sem vencimento superior a 30 dias.
- Afastamento previdenciário superior a 6 meses.
- Deixar de trabalhar para outro emprego e não ser readmitido.

## Related Documents
- [clt](clt.md) — Consolidação das Leis do Trabalho
- [folha-pagamento](folha-pagamento.md) — Cálculos de folha
- [esocial-folha](esocial-folha.md) — Eventos de folha no eSocial
- [inss-irrf](inss-irrf.md) — Tabelas INSS e IRRF
