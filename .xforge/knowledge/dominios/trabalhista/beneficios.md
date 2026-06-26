---
id: beneficios
type: knowledge
tags: [trabalhista, beneficios, vt, va, vr, saude, previdencia, pat, esocial]
owner: equipe-juridico-trabalhista
version: "1.0.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar de forma abrangente todos os benefícios trabalhistas — legais (obrigatórios) e espontâneos (opcionais) — c...
- **Seções principais**: Purpose, Responsibilities, Dependencies, 1. Benefícios Legais
- **Tags**: trabalhista, beneficios, vt, va, vr, saude, previdencia, pat, esocial
- **Restrições/Regras**: Este documento é referência genérica e não substitui consulta à legislação vigente; Valores, alíquotas e limites deve...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `beneficios` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | equipe-juridico-trabalhista |
| Total de seções | 10 |


# Benefícios Trabalhistas

Referência completa de benefícios legais e espontâneos, regras de concessão, incidência tributária e eventos de eSocial.

## Purpose

Documentar de forma abrangente todos os benefícios trabalhistas — legais (obrigatórios) e espontâneos (opcionais) — com suas regras de concessão, cálculos, incidência tributária (INSS, IRRF, FGTS) e eventos correspondentes no eSocial, como base para sistemas de RH e folha de pagamento.

## Responsibilities

Este documento cobre: vale-transporte, vale-alimentação/refeição, plano de saúde, plano odontológico, seguro de vida, PLR, auxílio-creche, auxílio-home office, gympass, vale-cultura, auxílio-combustível, previdência privada, bolsa de estudos, incidência tributária consolidada e eventos de eSocial.

## Dependencies

- `clt.md` — referência geral da CLT, remuneração e verbas
- `fgts.md` — FGTS, DIRF, DCTFWeb e EFD-Reinf

---

## 1. Benefícios Legais

### 1.1 Vale-Transporte (VT)

**Legislação:** Lei nº 7.418/1985, Decreto nº 95.247/1987

O vale-transporte é obrigatório para o colaborador que o solicita, destinado ao deslocamento residência-trabalho e vice-versa.

#### Regras

- Desconto limitado a 6% do salário base do empregado
- Se o custo do VT for maior que 6%, o empregado paga a diferença
- Se o custo for menor ou igual a 6%, não há desconto do empregado
- Deve ser utilizado exclusivamente para transporte

#### Cálculo

```
Desconto = Mínimo entre:
  (a) 6% do salário base
  (b) Valor das passagens utilizadas no mês
```

**Exemplo:**
```
Salário base: R$ 4.000,00
Desconto máximo (6%): R$ 240,00
Custo do VT: R$ 600,00
Desconto do empregado: R$ 240,00
Custo da empresa: R$ 360,00
```

#### Incidência Tributária

| Tributo | Incidência |
|---|---|
| INSS | Não |
| IRRF | Não |
| FGTS | Não |

---

### 1.2 Vale-Alimentação (VA) / Vale-Refeição (VR)

**Legislação:** PAT — Programa de Alimentação do Trabalhador (Lei nº 6.321/1976)

#### Diferenças

| Característica | Vale-Refeição (VR) | Vale-Alimentação (VA) |
|---|---|---|
| Uso | Refeições em restaurantes | Compras em supermercados |
| Forma | Cartão aceito em restaurantes | Cartão aceito em mercados |
| Saque | Proibido | Proibido |
| Troca | Permitida (Lei 14.442/2022) | Permitida (Lei 14.442/2022) |

#### Regras Obrigatórias

- Empresas do PAT não podem pagar VA/VR em dinheiro
- Benefício não pode ser negociado por acordo individual
- Desconto do empregado: até 20% do salário (conforme convenção coletiva)
- Proibido cobrança de taxas administrativas sobre o benefício (Lei 14.442/2022)

#### Lei 14.442/2022 — Novidades

- Permite portabilidade e troca entre VA e VR
- Fim da obrigatoriedade de credenciamento de estabelecimentos pelas operadoras
- Mais opções para o trabalhador

#### Incidência Tributária (se inscrito no PAT)

| Tributo | Incidência |
|---|---|
| INSS | Não |
| IRRF | Não |
| FGTS | Não |

Se a empresa não estiver no PAT, o VA/VR integra o salário para todos os fins.

---

### 1.3 FGTS (Fundo de Garantia do Tempo de Serviço)

**Legislação:** Lei nº 8.036/1990

| Item | Valor |
|---|---|
| Alíquota | 8% do salário bruto mensal |
| Prazo | Até o dia 7 do mês seguinte |
| Conta | Conta vinculada na Caixa Econômica Federal |

**Multa rescisória:** 40% sobre o total depositado durante o contrato (demissão sem justa causa).

> Para detalhamento completo, ver [`fgts.md`](./fgts.md).

---

### 1.4 13º Salário (Gratificação Natalina)

**Legislação:** Lei nº 4.090/1962, Lei nº 4.749/1965

| Parcela | Prazo | Valor |
|---|---|---|
| 1ª parcela | Até 30 de novembro | 50% do valor (sem descontos) |
| 2ª parcela | Até 20 de dezembro | 50% − INSS − IRRF |

**Cálculo:** proporcional aos meses trabalhados. Cada 15 dias ou mais conta como mês cheio.

**Incidência:** INSS (sim), IRRF (sim), FGTS (sim).

---

### 1.5 Férias

**Legislação:** Art. 7º, XVIII, CF/88; Arts. 129–142, CLT

| Item | Regra |
|---|---|
| Período | 30 dias corridos após 12 meses de trabalho |
| Remuneração | Salário + 1/3 constitucional |
| Pagamento | Até 2 dias antes do início do gozo |
| Período concessivo | 12 meses seguintes à aquisição |

**Abono pecuniário:** conversão de até 10 dias em pagamento (venda de férias).

**Incidência:** INSS (sim), IRRF (sim, cálculo separado), FGTS (não).

> Para detalhamento completo, ver [`clt.md`](./clt.md).

---

## 2. Benefícios Espontâneos

### 2.1 Plano de Saúde

Benefício opcional, amplamente oferecido no mercado brasileiro.

#### Tipos

| Tipo | Descrição | Característica |
|---|---|---|
| Individual | Contrato pessoal | Caro, reajustado por idade |
| Familiar | Inclui dependentes | Cobertura ampliada |
| Coletivo empresarial | Contrato empresa-operadora | Comodato, mais barato |

#### Estrutura de Custo

| Componente | Descrição |
|---|---|
| Mensalidade | Valor mensal × número de vidas |
| Coparticipação | % paga pelo empregado em cada uso |
| Reajuste anual | Pela ANS (operadoras) ou sinistralidade (coletivos) |

#### Dependentes Elegíveis

- Cônjuge ou companheiro(a)
- Filhos e enteados até 21 anos (ou 24 anos se universitários)
- Pai e mãe (se inválidos ou dependentes)

#### Incidência Tributária

| Tipo | INSS | IRRF | FGTS |
|---|---|---|---|
| Coletivo empresarial | Não | Não | Não |
| Individual | Pode integrar | Pode integrar | Pode integrar |

---

### 2.2 Plano Odontológico

Funciona de forma análoga ao plano de saúde, voltado para procedimentos odontológicos.

**Cobertura típica:** consultas, exames, limpeza, tratamento de canal, extrações, próteses, ortodontia.

**Incidência:** não incide INSS, IRRF nem FGTS (se coletivo empresarial).

---

### 2.3 Seguro de Vida

#### Coberturas Comuns

| Cobertura | Descrição |
|---|---|
| Morte (natural ou acidental) | Indenização ao beneficiário |
| Invalidez por doença | Pagamento por incapacidade |
| Invalidez por acidente | Pagamento por acidente |
| Doenças graves | Antecipação de parte do capital |
| Diária por internamento | Valor por dia de hospitalização |

**Incidência:** em regra, não integra o salário (se coletivo empresarial). Se individual, pode integrar.

---

### 2.4 PLR (Participação nos Lucros e Resultados)

**Legislação:** Lei nº 10.101/2000

#### Regras

- Negociação obrigatória entre empresa, comissão de empregados e sindicato
- Pagamento: até 2 parcelas por ano (intervalo mínimo de 60 dias)
- Não substitui salário
- Não constitui base para encargos (se dentro das regras)

#### Limites de Isenção

Até isento de INSS e IRRF se:
- Valor não exceder o limite por empregado no exercício
- Pago conforme acordo coletivo
- Distribuído para todos os empregados (não seletivo)

Acima desse valor, o excesso integra a base de INSS e IRRF.

---

### 2.5 Auxílio-Creche

- Obrigatório para empresas com mais de 30 mulheres maiores de 16 anos
- Pode ser creche própria ou reembolso de creche particular
- Limite de isenção conforme legislação vigente

---

### 2.6 Auxílio-Home Office

#### Modelos

| Modelo | Descrição |
|---|---|
| Valor fixo | Valor mensal predeterminado |
| Comprovação | Reembolso mediante notas fiscais |
| Híbrido | Valor base + reembolso de itens extras |

#### Despesas Cobertas

Internet, energia elétrica, equipamentos, material de escritório.

#### Incidência Tributária

| Modelo | Incidência |
|---|---|
| Reembolso comprovado | Não integra salário |
| Valor fixo | Pode integrar salário (risco trabalhista) |

---

### 2.7 Gympass / Academia

Convênio com academias e aplicativos de bem-estar.

**Incidência:** não integra salário — isento de INSS, IRRF e FGTS.

---

### 2.8 Vale-Cultura

**Legislação:** Lei nº 8.701/2013 (Programa de Cultura do Trabalhador)

- Valor: até R$ 50,00/mês por empregado
- Uso: cinemas, teatros, museus, livros, shows, cursos
- Isento de INSS, IRRF e FGTS

---

### 2.9 Auxílio-Combustível

Para funcionários que usam veículo próprio a serviço da empresa.

| Modelo | Cálculo |
|---|---|
| Valor fixo | Ex: R$ 500,00/mês |
| Por km rodado | Ex: R$ 0,70/km × km mensal |

**Incidência:** integra o salário — incide INSS, IRRF e FGTS.

---

### 2.10 Previdência Privada

#### Tipos

| Tipo | Característica | Dedução IR |
|---|---|---|
| PGBL | Contribuinte da IR com declaração completa | Deduz até 12% da renda bruta anual |
| VGBL | Contribuinte da IR com declaração simplificada ou isento | Sem dedução |

#### Regras

- Contribuição da empresa: percentual definido sobre o salário
- Contribuição do empregado: opcional (descontada em folha)
- Tributação na tabela regressiva (10 anos = 10% de IR)

**Incidência:** a contribuição da empresa não integra o salário do empregado. No resgate ou aposentadoria, há tributação.

---

### 2.11 Bolsa de Estudos

Auxílio para cursos técnicos, graduação, pós-graduação, MBA e especializações.

#### Modalidades

| Modalidade | Cobertura | Condição |
|---|---|---|
| Integral | 100% do curso | Vínculo de permanência |
| Parcial | 50%–80% do curso | Aprovação da empresa |
| Pós-graduação | Especialização/MBA | Acordo de tempo de serviço |

**Incidência:** em regra, integra o salário (incide INSS, IRRF, FGTS). Se restituído com comprovação de despesa, há discussão jurídica.

---

## 3. Incidência Tributária — Tabela Consolidada

| Benefício | INSS | IRRF | FGTS | Observações |
|---|---|---|---|---|
| Vale-Transporte | Não | Não | Não | Lei 7.418/1985 |
| VR/VA (PAT) | Não | Não | Não | Lei 6.321/1976 |
| Plano de Saúde (coletivo) | Não | Não | Não | Se empresarial |
| Plano Odontológico (coletivo) | Não | Não | Não | Se empresarial |
| Seguro de Vida (coletivo) | Não | Não | Não | Se empresarial |
| PLR | Não | Não | Não | Se Lei 10.101/2000 |
| Vale-Cultura | Não | Não | Não | Até R$ 50/mês |
| Gympass/Academia | Não | Não | Não | Benefício de bem-estar |
| Previdência Privada | Não | Não | Não | Na contribuição |
| Auxílio-Home Office (reembolso) | Não | Não | Não | Se comprovado |
| Salário | Sim | Sim | Sim | Base de cálculo |
| 13º Salário | Sim | Sim | Sim | 1ª parcela sem descontos |
| Férias + 1/3 | Sim | Sim | Não | IRRF separado |
| Abono Pecuniário | Não | Não | Não | Art. 143 CLT |
| Auxílio-Combustível | Sim | Sim | Sim | Integra salário |
| Bolsa de Estudos | Sim | Sim | Sim | Em regra |

---

## 4. eSocial — Eventos de Benefícios

### 4.1 Eventos Principais

| Evento | Descrição | Periodicidade |
|---|---|---|
| S-1200 | Remuneração do trabalhador vinculado ao Regime Geral de Previdência Social | Mensal |
| S-1210 | Pagamentos de rendimentos do trabalho | Mensal |
| S-2299 | Desligamento — término do vínculo trabalhista | Não periódico |
| S-2399 | Trabalhador sem vínculo — término | Não periódico |
| S-1298 | Reabertura dos eventos periódicos | Não periódico |
| S-1299 | Fechamento dos eventos periódicos | Não periódico |

### 4.2 Informações de Benefícios no eSocial

Os benefícios devem ser informados nos eventos de remuneração (S-1200) e pagamentos (S-1210), com discriminação por tipo:

- Rubricas de benefício (código de rubrica)
- Valor do benefício
- Incidência para INSS, IRRF e FGTS
- Identificação do beneficiário (dependentes)

### 4.3 Eventos de Término e Benefícios

No evento S-2299 (desligamento), devem ser informadas:
- Verbas rescisórias com discriminação de benefícios
- Saldo de salário, férias, 13º proporcional
- Multa FGTS e saque

---

## 5. Referências Legais

| Legislação | Tema |
|---|---|
| CLT (Decreto-Lei 5.452/1943) | Regras gerais de direitos trabalhistas |
| Lei nº 4.090/1962 | 13º salário |
| Lei nº 6.321/1976 | PAT — Programa de Alimentação do Trabalhador |
| Lei nº 7.418/1985 | Vale-Transporte |
| Decreto nº 95.247/1987 | Regulamentação do VT |
| Lei nº 8.036/1990 | FGTS |
| Lei nº 8.701/2013 | Vale-Cultura |
| Lei nº 10.101/2000 | PLR |
| Lei nº 14.442/2022 | Novo Marco do PAT — portabilidade VA/VR |
| Constituição Federal, Art. 7º | Direitos fundamentais dos trabalhadores |

---

## Constraints

- Este documento é referência genérica e não substitui consulta à legislação vigente
- Valores, alíquotas e limites devem ser verificados periodicamente
- Normas coletivas podem estabelecer condições mais favoráveis
- A inscrição no PAT é obrigatória para isenção de VA/VR
- O eSocial pode exigir layouts e eventos atualizados periodicamente

## Related Documents

- [`clt.md`](./clt.md) — CLT, remuneração, férias, 13º e verbas rescisórias
- [`fgts.md`](./fgts.md) — FGTS, DIRF, DCTFWeb e EFD-Reinf
