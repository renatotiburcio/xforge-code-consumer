---
id: holerite-v2
type: knowledge
tags: [holerite, contracheque, recibo-pagamento, proventos, descontos, inss, irrf, fgts, folha, esocial]
owner: trabalhista
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura, conteudo obrigatorio, proventos, descontos, bases de calculo e regras de entrega do holerite ...
- **Principais responsabilidades**: Gerar holerites mensais com discriminacao completa de proventos e descontos.; Calcular corretamente INSS, IRRF e FGTS conforme tabelas vigentes.; G...
- **Seções principais**: Proposito, Responsabilidades, Dependencias, Constraints
- **Tags**: holerite, contracheque, recibo-pagamento, proventos, descontos, inss, irrf, fgts, folha, esocial
- **Restrições/Regras**: **Obrigatoriedade**: CLT Art. 464 -- pagamento contra recibo assinado ou mecanismo eletronico valido.; **Prazo de pag...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `holerite-v2` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 7 |


# Holerite / Contracheque -- Recibos de Pagamento

## Proposito

Documentar a estrutura, conteudo obrigatorio, proventos, descontos, bases de calculo e regras de entrega do holerite (recibo de pagamento / contracheque) conforme a CLT, eSocial e jurisprudencia trabalhista, como base para sistemas de folha de pagamento.

## Responsabilidades

- Gerar holerites mensais com discriminacao completa de proventos e descontos.
- Calcular corretamente INSS, IRRF e FGTS conforme tabelas vigentes.
- Garantir entrega do holerite em formato impresso ou digital com aceite.
- Refletir no holerite os dados enviados ao eSocial (eventos S-1200, S-1210).
- Gerar holerites especificos de rescisao, 13o salario e ferias.
- Manter comprovantes de pagamento por 5 anos (prazo prescricional).

## Dependencias

- Tabelas vigentes de INSS e IRRF (atualizadas anualmente).
- Sistema de folha de pagamento (ERP/DP).
- Certificado digital e-CNPJ para eSocial.
- Dados cadastrais do trabalhador (S-2200, S-2206).
- Controle de ponto para apuracao de HE, faltas e atrasos.
- Convenao coletiva de trabalho (pisos, beneficios, adicionais).
- [Saude e Seguranca do Trabalho](./saude-trabalho.md) -- adicionais de insalubridade e periculosidade.
- [Departamento Pessoal](./departamento-pessoal.md) -- rotinas de admissao, folha e desligamento.
- [Obrigações Acessorias Federais](./obrigacoes-acessorias.md) -- eSocial, EFD-Reinf, DCTFWeb.

## Constraints

- **Obrigatoriedade**: CLT Art. 464 -- pagamento contra recibo assinado ou mecanismo eletronico valido.
- **Prazo de pagamento**: ate o 5o dia util do mes seguinte (CLT Art. 459, 1o).
- **Conteudo minimo**: 9 campos obrigatorios (empresa, funcionario, periodo, proventos, descontos, bases, data, totais, assinatura).
- **Rescisao**: prazo de 10 dias corridos para pagamento (CLT Art. 477, 6o).
- **Ferias**: pagamento ate 2 dias antes do inicio do periodo (CLT Art. 145).
- **13o**: 1a parcela ate 30 de novembro; 2a parcela ate 20 de dezembro.
- **eSocial**: evento S-1200 deve ser enviado ate o dia 7 do mes seguinte.

## Conteudo

### 1. Base Legal

**CLT Art. 464**: "O pagamento do salario devera ser efetuado contra recibo, assinado pelo empregado, ou por mecanismo eletronico valido."

**eSocial**: O evento tabelas deve conter as rubricas utilizadas nos holerites. O envio dos eventos periodicos (S-1200) exige a correta individualizacao das remuneracoes.

**Jurisprudencia TST**: A ausencia do holerite pode gerar presuncao de veracidade das alegacoes do empregado quanto aos valores nao comprovados (Sumula 370 -- salario por fora).

### 2. Conteudo Obrigatorio (9 Campos)

| # | Campo | Descricao |
| 1 | **Dados da Empresa** | CNPJ, razao social, endereco |
| 2 | **Dados do Funcionario** | Nome, cargo, CPF, PIS/PASEP, data admissao |
| 3 | **Periodo de Referencia** | Mes/ano de competencia |
| 4 | **Proventos** | Discriminacao completa (rubrica, referencia, valor) |
| 5 | **Descontos** | Discriminacao completa (rubrica, referencia, valor) |
| 6 | **Bases de Calculo** | Base INSS, base IRRF, base FGTS |
| 7 | **Totais** | Valor bruto, total de descontos, valor liquido |
| 8 | **Data de Pagamento** | Local e data efetiva do deposito |
| 9 | **Assinatura** | Fisica ou digital (aceite eletronico) |

### 3. Layout do Holerite

**Estrutura**: cabecalho (dados empresa + dados funcionario) / periodo referencia / tabela de rubricas (codigo, descricao, referencia, proventos | descontos) / totais (bruto, descontos, liquido) / bases (INSS, IRRF, FGTS) / data pagamento + assinatura. Cada rubrica possui:codigo (numerico, 4 digitos recomendado), descricao, referencia (horas, dias, percentual), valor provento e valor desconto.

### 4. Proventos -- Tipos e Calculos

| Provento | Calculo |
| Salario Base | Valor mensal contratual |
| Horas Extras 50% | (Salario/220) x 1,50 x Qtd horas |
| Horas Extras 100% | (Salario/220) x 2,00 x Qtd horas |
| Adicional Noturno 20% | (Salario/jornada) x 0,20 x horas noturnas |
| Insalubridade | Salario Minimo x % grau (10/20/40%) |
| Periculosidade | Salario Base x 30% |
| DSR | (Variaveis / dias uteis) x DSRs no mes |
| Comissoes | Vendas x % comissao (conforme contrato) |
| 13o Salario | Salario x meses trabalhados / 12 |
| Ferias | (Salario/30) x dias + 1/3 constitucional |
| Abono Pecuniario | (Salario/30) x dias vendidos + 1/3 |
| Salario-Familia | Valor por dependente (conforme faixa) |
| PLR | Isento INSS/FGTS (Lei 10.101/2000) |

### 5. Descontos -- Tipos e Calculos

| Desconto | Calculo |
| INSS | Tabela progressiva (7,5% / 9% / 12% / 14%) |
| IRRF | Tabela progressiva sobre base (bruto - INSS - dependentes R$ 189,59 c/um - pensao) |
| Vale-Transporte | Ate 6% do salario base |
| Faltas | (Salario/30) x dias de falta |
| Atrasos | (Salario/220) x horas de atraso |
| Pensao Alimenticia | Base x % definido judicialmente |
| Contribuicao Sindical | Facultativa (apos Reforma 2017) |
| Plano de Saude/ Odontologico | Coparticipacao ou mensalidade |
| Vale-Refeicao | Ate 20% (conforme PAT) |
| Adiantamento | Geralmente 40% descontado integralmente |
| Danos | Somente se dolosos ou previsao em acordo (Art. 462 CLT) |

### 6. Tabela INSS (2025 -- empregado)

| Faixa Salarial | Aliquota | Parcela a Deduzir |
| Ate R$ 1.518,00 | 7,50% | R$ 0,00 |
| R$ 1.518,01 a 2.793,88 | 9,00% | R$ 22,77 |
| R$ 2.793,89 a 4.190,73 | 12,00% | R$ 106,59 |
| R$ 4.190,74 a 8.157,38 | 14,00% | R$ 190,40 |

### 7. Tabela IRRF (2025)

| Base de Calculo | Aliquota | Parcela a Deduzir |
| Ate R$ 2.259,20 | Isento | R$ 0,00 |
| R$ 2.259,21 a 2.826,65 | 7,50% | R$ 169,44 |
| R$ 2.826,66 a 3.751,05 | 15,00% | R$ 381,44 |
| R$ 3.751,06 a 4.664,68 | 22,50% | R$ 662,77 |
| Acima de 4.664,68 | 27,50% | R$ 896,00 |

**Base IRRF** = Salario bruto - INSS - dependentes (R$ 189,59/cada) - pensao alimenticia.

### 8. Bases de Calculo

| Base | Descricao | Incidencia |
| **Base INSS** | Salario + verbas remuneratorias | INSS (GPS) |
| **Base IRRF** | Base INSS - deducoes (dependentes, INSS, pensao) | Imposto de Renda |
| **Base FGTS** | Todas as verbas salariais mensais | FGTS (8%) |

### 9. Holerite de Rescisao

**Verbas**: saldo de salario, ferias vencidas + 1/3, ferias proporcionais + 1/3, 13o proporcional, aviso previo (trabalhado ou indenizado), multa FGTS 40%. **Descontos**: INSS sobre saldo/13o/aviso, IRRF, adiantamentos. **Prazo**: 10 dias corridos (aviso indenizado) ou 1o dia util (aviso trabalhado). **Tabela aviso previo**: 30 dias + 3 dias/ano (maximo 90 dias).

### 10. Holerite de 13o Salario

**1a parcela** (1o/fev a 30/nov): 50% do valor bruto, sem descontos. **2a parcela** (ate 20/dez): 50% restante, menos INSS e IRRF. **Provisao mensal**: Salario / 12. **Incidencias**: FGTS (1a e 2a), INSS (2a apenas), IRRF (2a apenas).

### 11. Holerite de Ferias

**Composicao**: (Salario/30) x dias + 1/3 constitucional. **Abono pecuniario**: (Salario/30) x dias vendidos (max 10) + 1/3. **Prazo**: ate 2 dias antes do inicio. **Media de variaveis**: HE, adicional noturno, comissoes (media dos ultimos 12 meses).

### 12. Entrega Eletronica

**Impresso**: entrega no ato, assinatura, guardar 5 anos. **Digital**: e-mail, portal ou app. **Aceite digital**: confirmacao de leitura ou assinatura ICP-Brasil. **eSocial**: S-1200 (remuneracao) e S-1210 (pagamentos). O holerite deve refletir os dados enviados ao eSocial.

## Documentos Relacionados

- [Saude e Seguranca do Trabalho](./saude-trabalho.md) -- adicionais insalubridade/periculosidade.
- [Departamento Pessoal](./departamento-pessoal.md) -- rotinas de DP e folha.
- [Obrigações Acessorias Federais](./obrigacoes-acessorias.md) -- eSocial, EFD-Reinf, DCTFWeb.
- [Folha de Pagamento](./folha-pagamento.md) -- calculos e encargos patronais.
- [INSS e IRRF](./inss-irrf.md) -- tabelas progressivas e deducoes.
- [FGTS](./fgts.md) -- depositos e multa rescisoria.
- [13o Salario](./decimo-terceiro.md) -- calculo detalhado e parcelas.
- [Ferias](./ferias.md) -- calculo, abono e pagamento.
- [Beneficios](./beneficios.md) -- VT, VR/VA, plano de saude.
- [Ponto Eletronico](./ponto-eletronico.md) -- controle de jornada.

## Referenciais Legais

| Norma | Dispositivo | Assunto |
| CLT | Art. 464 | Obrigatoriedade do recibo de pagamento |
| CLT | Art. 459, 1o | Prazo de pagamento (5o dia util) |
| CLT | Art. 477, 6o | Prazo de pagamento da rescisao (10 dias) |
| CLT | Art. 145 | Pagamento de ferias (2 dias antes) |
| CLT | Art. 462 | Descontos salariais |
| CLT | Art. 59 | Horas extras (maximo 2h/dia) |
| Lei 8.213/91 | -- | Planos de Beneficios da Previdencia Social |
| Lei 10.101/2000 | -- | PLR |
| Lei 13.467/2017 | -- | Reforma Trabalhista |

| Jurisprudencia | Teor |
| Sumula 47 TST | Adicional de insalubridade -- base de calculo |
| Sumula 171 TST | Gratificacao de funcao -- reflexos |
| Sumula 264 TST | Horas extras habituais -- reflexos |
| Sumula 370 TST | Salario por fora -- integracao |

> Valores de tabelas (INSS, IRRF, salario minimo) sao atualizados anualmente -- sempre consultar os valores vigentes.
