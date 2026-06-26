---
id: ponto-eletronico
type: knowledge
tags: [ponto-eletronico, rep, jornada, horas-extras, banco-horas, esocial, portaria-671]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar as registro de ponto eletronico: tipos de registro, requisitos do sistema (Portaria 671/2021), jornada de ...
- **Principais responsabilidades**: Registrar entrada, saida e intervalos dos empregados.; Calcular horas extras, faltas, atrasos e DSR automaticamente.; Controlar banco de horas e co...
- **Seções principais**: Proposito, Responsabilidades, Dependencias, Constraints
- **Tags**: ponto-eletronico, rep, jornada, horas-extras, banco-horas, esocial, portaria-671
- **Restrições/Regras**: **Obrigatoriedade**: estabelecimentos com mais de 20 empregados (CLT Art. 74).; **Tolerancia**: 5 minutos (maximo 10 ...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `ponto-eletronico` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Ponto Eletronico - Regras e Legislacao

## Proposito
Documentar as registro de ponto eletronico: tipos de registro, requisitos do sistema (Portaria 671/2021), jornada de trabalho, horas extras, banco de horas, tratamento de ponto e integracao com eSocial.

## Responsabilidades
- Registrar entrada, saida e intervalos dos empregados.
- Calcular horas extras, faltas, atrasos e DSR automaticamente.
- Controlar banco de horas e compensacao de jornada.
- Gerar espelho de ponto e arquivo AFD para eSocial.
- Garantir conformidade com a Portaria MTP 671/2021.

## Dependencias
- Sistema de ponto eletronico (REP-P, REP-A ou REP-C) homologado.
- Certificado digital para transmissao de arquivos.
- Cadastro de funcionarios com jornada contratual definida.

## Constraints
- **Obrigatoriedade**: estabelecimentos com mais de 20 empregados (CLT Art. 74).
- **Tolerancia**: 5 minutos (maximo 10 minutos) para atraso/saida antecipada.
- **Horas extras**: maximo 2h por dia (CLT Art. 59).
- **Interjornada**: minimo 11 horas entre jornadas (CLT Art. 66).
- **Intrajornada**: 1h (jornada >6h) ou 15 min (4-6h).

## Conteudo

### Tipos de Registro de Ponto
| Tipo | Descricao | Obrigadorio |
|------|-----------|-------------|
| REP-P | Registrador Eletronico de Ponto - Programa | Sim (Portaria 671) |
| REP-A | Registrador Eletronico de Ponto - Alternativo | Sim (acordo coletivo) |
| REP-C | Registrador Eletronico de Ponto - Convencional | Sim (Portaria 671) |

### Requisitos do Sistema de Ponto (Portaria 671/2021)
- Registrar entrada, saida e intervalos.
- Nao permitir alteracao de registros.
- Nao permitir bloqueio de marcacao.
- Gerar arquivo AFD (Arquivo Fonte de Dados).
- Gerar arquivo CF (Controle de Frequencia).
- Gerar espelho de ponto.
- Armazenar registros por pelo menos 5 anos.
- Permitir consulta pelo empregado.
- Interface amigavel.

### Jornada de Trabalho
| Tipo | Duracao | Observacao |
|------|---------|------------|
| Normal | 8h diarias / 44h semanais | Padrao |
| 6h diarias | 6h diarias / 30h semanais | Turnos ininterruptos |
| 12x36 | 12h trabalho / 36h descanso | Acordo ou convencao |
| 24x48 | 24h trabalho / 48h descanso | Bombeiros, saude |
| Parcial | Ate 25h ou 30h semanais | Reforma Trabalhista |

### Horas Extras
\\\
Valor da hora normal = Salario / 220h
Hora extra 50% = Hora normal x 1,5
Hora extra 100% = Hora normal x 2,0
Limite: 2 horas extras por dia
\\\

### Banco de Horas
- Pode ser estabelecido por acordo individual (Reforma Trabalhista).
- Compensacao em ate 6 meses (acordo individual) ou 1 ano (coletivo).
- Horas nao compensadas: pagamento como hora extra.

### Intervalos
| Tipo | Duracao | Observacao |
|------|---------|------------|
| Intrajornada (refeicao) | 1-2h | Jornada > 6h |
| Intrajornada (descanso) | 15 min | Jornada 4-6h |
| Interjornada | 11h | Entre duas jornadas |
| Descanso semanal | 24h | Preferencialmente domingo |

### Regime 12x36
- 12 horas de trabalho seguidas de 36 horas de descanso.
- Pode ser estabelecido por acordo individual.
- Horas extras: apenas se ultrapassar 12h.
- Intervalo: 1h para refeicao.
- DSR: incluido nas 36h de descanso.

### Trabalho Noturno
- **Periodo**: 22h as 5h (urbano).
- **Adicional**: 20% sobre a hora diurna.
- **Hora noturna**: 52min30s (1h = 52min30s).
- **Calculo**: Hora normal x 1,2.

### Tratamento de Ponto
Rotina diaria:
1. Coletar marcacoes (REP, manual, app).
2. Identificar omissoes, marcacoes duplas.
3. Aplicar escalas/jornadas.
4. Calcular horas extras, faltas, atrasos.
5. Tratar sobreaviso, interjornada.
6. Gerar espelho de ponto (assinatura do empregado).

### Ponto no eSocial
- **S-2200**: Admissao - com jornada.
- **S-2206**: Alteracao contratual - com jornada.
- **S-1200**: Remuneracao - com horas extras.
- O registro de ponto nao e enviado diretamente ao eSocial, mas os dados de jornada sao informados nos eventos cadastrais e de remuneracao.

### Penalidades
| Infracao | Multa |
|----------|-------|
| Falta de registro | R$ 4.000-8.000 por empregado |
| Registro falso | R$ 2.000-4.000 por empregado |
| Jornada excessiva | R$ 1.000-2.000 por empregado |
| Falta de intervalo | R$ 500-1.000 por empregado |

## Related Documents
- [clt](clt.md) - Consolidacao das Leis do Trabalho
- [folha-pagamento](folha-pagamento.md) - Calculos de folha
- [esocial-trabalhador](esocial-trabalhadores.md) - Eventos cadastrais do trabalhador
