---
id: knowledge-fluxos-exame-medico-admissional
type: knowledge
title: Fluxo de Exame Medico Admissional (ASO)
category: fluxos
domain: rh
trustScore: 85
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [rh, aso, exame, admissional, medico, esocial]
---

# Fluxo de Exame Medico Admissional (ASO)

## Contexto

A admissão de funcionario exige exame medico admissional conforme
**NR-7 (PCMSO)** e **Art. 168 da CLT**. O resultado e registrado no
**ASO (Atestado de Saude Ocupacional)**.

## Fluxo

1. RH cadastra funcionario (dados pessoais + funcao + setor + riscos)
2. RH agenda exame com clinica credenciada
3. Funcionario comparece a clinica
4. Medico do trabalho examina:
   - Avaliacao clinica
   - Exames complementares conforme risco (audiometria, hemograma, etc.)
5. Medico emite ASO com:
   - Apto / Inapto / Apto com restricoes
   - Data de validade (max 1 ano para periodicos)
6. Clinica envia ASO digital (PDF + assinatura ICP-Brasil)
7. RH arquiva no prontuario do funcionario
8. Sistema dispara evento S-2220 (eSocial) com informacoes do ASO

## Exames por risco

| Risco | Exame |
|-------|-------|
| Ruido > 85 dB | Audiometria |
| Altura > 2m | Hemograma, glicemia, ECG |
| Produtos quimicos | Hemograma, plaquetas, TGO/TGP |
| Computador (visual) | Acuidade visual |
| Esforco fisico | ECG, ergometria |

## Modelos ASO

- **ASO Admissional**: obrigatorio antes do inicio das atividades
- **ASO Periodico**: anual ou bienal (depende da idade e risco)
- **ASO Retorno**: apos afastamento > 30 dias
- **ASO Mudanca de risco**: troca de funcao/setor
- **ASO Demissional**: ate 10 dias apos termino do contrato

## Responsabilidades

- **Empregador**: arcar com custos, agendar, manter prontuario por 20 anos
- **Medico do trabalho**: realizar exame, emitir ASO, indicar restricoes
- **Funcionario**: submeter-se aos exames
- **SESMT**: acompanhar e supervisionar

## Eventos eSocial

- **S-2220**: ASO (com data, medico, CRM, exames, resultado)
- **S-2240**: Condicoes ambientais do trabalho (risco)
- Vinculacao: S-2200 (admissao) -> S-2220 (aso) -> S-2240 (ambiente)

## Referencias

- NR-7 (PCMSO) - Portaria 24/1994
- Art. 168 CLT
- Lei 8.213/1991 Art. 58 (aposentadoria especial)
- eSocial leiaute S-2220

