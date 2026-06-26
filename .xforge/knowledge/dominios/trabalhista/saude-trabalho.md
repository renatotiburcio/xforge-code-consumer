---
id: saude-trabalho-v2
type: knowledge
tags: [saude-trabalho, pcmso, pgr, ltcat, ppp, cipa, epi, sesmt, aposentadoria-especial, nr, sst, esocial, cat]
owner: trabalhista
version: "2.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar as obrigacoes de Saude e Seguranca do Trabalho: PCMSO, PGR, LTCAT, PPP, SESMT, CIPA, EPI e aposentadoria e...
- **Principais responsabilidades**: Elaborar PCMSO com exames obrigatorios (admissional, periodico, retorno, mudanca funcao, demissional).; Elaborar PGR com inventario de riscos e pla...
- **Seções principais**: Proposito, Responsabilidades, Dependencias, Constraints
- **Tags**: saude-trabalho, pcmso, pgr, ltcat, ppp, cipa, epi, sesmt, aposentadoria-especial, nr, sst, esocial, cat
- **Restrições/Regras**: PCMSO obrigatorio para todos os empregadores com empregados CLT.; PGR substituiu o PPRA a partir de 02/01/2022 (Porta...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `saude-trabalho-v2` |
| Tipo | knowledge |
| Versão | 2.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Saude e Seguranca do Trabalho (SST) -- PCMSO, PGR, LTCAT, PPP

## Proposito

Documentar as obrigacoes de Saude e Seguranca do Trabalho: PCMSO, PGR, LTCAT, PPP, SESMT, CIPA, EPI e aposentadoria especial, com checklists de compliance por NR.

## Responsabilidades

- Elaborar PCMSO com exames obrigatorios (admissional, periodico, retorno, mudanca funcao, demissional).
- Elaborar PGR com inventario de riscos e plano de acao conforme hierarquia de controles.
- Emitir LTCAT para documentar exposicao a agentes nocivos e fundamentar aposentadoria especial.
- Gerar PPP na rescisao e mante-lo atualizado por 20 anos.
- Dimensionar SESMT (NR-4), constituir CIPA (NR-5) e fornecer EPIs com CA valido (NR-6).
- Enviar eventos de SST no eSocial (S-2210, S-2220, S-2240, S-2245).

## Dependencias

- Medico do Trabalho (coordenador do PCMSO).
- Engenheiro de Seguranca do Trabalho (PGR, LTCAT).
- Certificado digital e-CNPJ para transmissao no eSocial.
- NRs vigentes (NR-4, NR-5, NR-6, NR-7, NR-9, NR-15, NR-16, NR-17).
- [Departamento Pessoal](./departamento-pessoal.md) -- exames admissionais e registro.
- [Obrigações Acessorias Federais](./obrigacoes-acessorias.md) -- eventos eSocial de SST.

## Constraints

- PCMSO obrigatorio para todos os empregadores com empregados CLT.
- PGR substituiu o PPRA a partir de 02/01/2022 (Portaria MTP 8.066/2022).
- CAT envio ate 1o dia util seguinte ao acidente (obito: imediatamente).
- EPI fornecimento gratuito, CA valido (5 anos), ficha de controle individual.
- PPP obrigatorio na rescisao; manter arquivado por 20 anos.

## Conteudo

### NR-7 -- PCMSO

#### Exames Obrigatorios

| Tipo de Exame | Momento | Prazo |
| Admissional | Antes de iniciar atividades | Ate 1o dia de trabalho |
| Periodico | Conforme idade/risco | Ver tabela abaixo |
| Retorno ao trabalho | Retorno apos afastamento >= 30 dias | 1o dia de retorno |
| Mudanca de funcao | Antes da mudanca | Ate 1o dia na nova funcao |
| Demissial | Ate 10 dias da rescisao | Dentro do prazo de homologacao |

#### Periodicidade dos Exames Periodicos

| Faixa Etaria | Risco Baixo (Grau 1-2) | Risco Alto (Grau 3-4) |
| < 18 anos | Anual | Anual |
| 18 a 45 anos | Bienal | Anual |
| > 45 anos | Anual | Anual |

#### ASO -- Atestado de Saude Ocupacional

Contem: identificacao do trabalhador, riscos ocupacionais, procedimentos medicos, parecer de aptidao, carimbo/CRM. **Classificacoes:** APTO, INAPTO, APTO COM RESTRICOES.

### NR-9 -- PGR (Programa de Gerenciamento de Riscos)

#### Inventario de Riscos

| Categoria | Agentes Principais | Referencia |
| Fisicos | Ruido, calor, vibracao, radiacao, pressao | NR-15 |
| Quimicos | Poeiras, fumos, gases, vapores, solventes | NR-15 |
| Biologicos | Bacterias, virus, fungos, parasitas | NR-32 |
| Ergonomicos | Esforco fisico, postura, repetitividade,estresse | NR-17 |
| Mecanicos/Acidentes | Maquinas, altura, eletricidade, confinamento | NR-12,35,10,33 |

#### Hierarquia de Controle

1. Eliminacao do risco (mais eficaz)
2. Reducao / substituicao
3. Protecao coletiva (EPC)
4. Medidas administrativas
5. Protecao individual (EPI) (menos eficaz)

#### Planos de Acao por Prioridade

| Nivel de Risco | Prazo |
| Critico | Imediato |
| Alto | Ate 30 dias |
| Medio | Ate 90 dias |
| Baixo | Ate 180 dias |
| Muito baixo | Continuo |

### LTCAT -- Laudo Tecnico de Condicoes Ambientais do Trabalho

**Base legal:** Lei 8.213/91 (arts. 57-58), IN INSS 128/2022. **Agentes nocivos:** fisicos (ruido, calor, vibracao), quimicos (poeiras, gases, solventes), biologicos (bacterias, virus). Documenta condicoes ambientais para fundamentar **aposentadoria especial**.

### PPP -- Perfil Profissiografico Previdenciario

Substitui SB-40, DISES-BRE, DSS-8030 e DIRBEN 8030. **Conteudo:** dados da empresa e trabalhador, atividades, registros ambientais, exposicao a agentes nocivos, exames medicos, responsaveis. **Obrigacoes:** emitir na rescisao, atualizar, manter 20 anos.

### NR-4 -- SESMT

#### Dimensionamento (resumo)

| N Empregados | Grau 2 | Grau 3 | Grau 4 |
| 26 a 50 | Eng. Seg. (parcial) | Eng. Seg. + Med. Trab. | + Enf. Trab. |
| 51 a 250 | Eng. Seg. (parcial) | Eng. Seg. + Med. Trab. | + Enf. Trab. |
| 251 a 1.000 | Eng. Seg. (parcial) | Eng. Seg. + Med. Trab. | + Enf. Trab. + Tec. Seg. |

"Parcial" = minimo 3h/dia. Grau 4 com >= 501 exige jornada integral. **Profissionais:** Eng. Seg. Trab. (CREA), Med. Trab. (CRM), Enf. Trab. (COREN), Tec. Seg. (DRT/MTE).

### NR-5 -- CIPA

#### Dimensionamento (resumo)

| N Empregados | Grau 2 (Ef+Supl) | Grau 3 (Ef+Supl) | Grau 4 (Ef+Supl) |
| 20-29 | 1+1 | 1+1 | 1+1 |
| 30-50 | 1+1 | 2+1 | 2+2 |
| 51-80 | 2+1 | 3+2 | 3+3 |
| 81-120 | 3+1 | 4+2 | 4+3 |
| Acima 10.000 | +1/+1 por grupo 5.000 | +1/+1 por grupo 5.000 | +1/+1 por grupo 5.000 |

**Atribuicoes:** identificar riscos, mapa de riscos, inspecoes, SIPAT, reunioes mensais, atas. **Estabilidade:** mandato 1 ano + 1 ano pos-mandato.

### NR-6 -- EPI/EPC

**CA (Certificado de Aprovação):** validade 5 anos, obrigatorio. **EPI por parte do corpo:** cabeca (capacete), olhos/face (oculos), ouvidos (protetor auditivo), maos (luvas), pes (calçado), corpo (avental/colete), respiratoria (respirador), queda (cinto/talabarte). **Controle:** ficha individual, termo de responsabilidade, devolucao na rescisao.

### Aposentadoria Especial (pos-Reforma EC 103/2019)

| Tempo | Idade Minima |
| 15 anos (mina subterranea) | 55 anos |
| 20 anos | 58 anos |
| 25 anos (demais agentes) | 60 anos |

**Conversao:** 15 anos = fator 2,0 (H) / 1,67 (M); 20 anos = 1,5 / 1,25; 25 anos = 1,4 / 1,20. **Documentos:** PPP, LTCAT, CAT, laudos, exames PCMSO.

### Checklist de Compliance por NR

#### NR-7 (PCMSO)

- [ ] PCMSO elaborado e medico coordenador designado.
- [ ] Exames admissionais, periodicos, retorno, mudanca e demissional realizados.
- [ ] ASOs emitidos para todos os exames.
- [ ] Dados mantidos por 20 anos.

#### NR-9 (PGR)

- [ ] PGR e inventario de riscos elaborados.
- [ ] Riscos fisicos, quimicos, biologicos, ergonomicos e mecanicos avaliados.
- [ ] Hierarquia de controle aplicada e plano de acao elaborado.

#### NR-4 (SESMT)

- [ ] SESMT dimensionado (CNAE + N empregados).
- [ ] Profissionais contratados com registro no conselho.

#### NR-5 (CIPA)

- [ ] CIPA dimensionada, eleicao anual, estabilidade garantida.
- [ ] Reunioes mensais, atas, SIPAT, mapa de riscos.

#### NR-6 (EPI/EPC)

- [ ] EPI com CA valido, ficha preenchida, termo assinado.
- [ ] Substituicao quando danificado, EPC instalado.

#### LTCAT / PPP

- [ ] LTCAT elaborado e atualizado.
- [ ] PPP emitido na rescisao, atualizado, mantido 20 anos.

## Documentos Relacionados

- [Holerite / Contracheque](./holerite.md) -- adicionais de insalubridade/periculosidade.
- [Departamento Pessoal](./departamento-pessoal.md) -- exames, admissao, desligamento.
- [Obrigações Acessorias Federais](./obrigacoes-acessorias.md) -- eSocial SST.
- [Afastamentos](./afastamentos.md) -- CAT, auxilio-doenca, estabilidade acidentaria.
- [CLT](./clt.md) -- artigos SST (154-201).
- [eSocial Trabalhadores](./esocial-trabalhadores.md) -- S-2200, S-2210, S-2220, S-2240.
