---
id: afastamentos
type: knowledge
tags: [afastamento, auxilio-doenca, licenca-maternidade, cat, estabilidade, inss, esocial]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Afastamentos — Tipos, Cálculos e Regras
- **Principais responsabilidades**: Controlar afastamentos por doença, acidente, licença-maternidade e outros.; Calcular pagamento dos primeiros 15 dias (empregador) e encaminhar ao I...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: afastamento, auxilio-doenca, licenca-maternidade, cat, estabilidade, inss, esocial
- **Restrições/Regras**: **Auxílio-doença**: empregador paga 15 primeiros dias; INSS assume a partir do 16º dia.; **Estabilidade**: 12 meses a...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `afastamentos` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Afastamentos — Tipos, Cálculos e Regras

## Propósito
Documentar os tipos de afastamento do trabalhador: previdenciários (INSS), remunerados pelo empregador, não remunerados, estabilidade provisória e integração com eSocial.

## Responsabilidades
- Controlar afastamentos por doença, acidente, licença-maternidade e outros.
- Calcular pagamento dos primeiros 15 dias (empregador) e encaminhar ao INSS.
- Garantir estabilidade provisória após retorno de afastamento.
- Emitir CAT (Comunicação de Acidente de Trabalho) quando aplicável.
- Enviar eventos S-2230 (afastamento) e S-2210 (CAT) no eSocial.

## Dependências
- Cadastro de funcionários com dados de vínculo e remuneração.
- Integração com INSS para concessão de benefícios previdenciários.
- PCMSO para monitoramento de saúde e emissão de ASO.

## Constraints
- **Auxílio-doença**: empregador paga 15 primeiros dias; INSS assume a partir do 16º dia.
- **Estabilidade**: 12 meses após retorno de auxílio-doença acidentário (B91).
- **CAT**: envio até 1º dia útil seguinte ao acidente (óbito: imediatamente).
- **Licença-maternidade**: 120 dias (180 para Empresa Cidadã).
- **Suspensão disciplinar**: máximo 30 dias.

## Conteúdo

### Afastamentos Previdenciários (INSS)

| Tipo | Código | Duração | Pagamento | Estabilidade |
|------|--------|---------|-----------|--------------|
| Auxílio-doença | B31 | Conforme perícia | INSS (16º dia+) | Não |
| Auxílio-doença acidentário | B91 | Conforme perícia | INSS (16º dia+) | 12 meses |
| Aposentadoria por invalidez | B42 | Indeterminado | INSS | Não |
| Auxílio-acidente | B94 | Vitalício (sequela) | INSS | Não |
| Salário-maternidade | B93 | 120 dias (180 adotante) | INSS | 5 meses pós-parto |
| Auxílio-reclusão | B95 | Enquanto recluso | INSS | Não |

### Afastamentos Remunerados pelo Empregador
| Tipo | Prazo |
|------|-------|
| Luto (falecimento familiar) | 2 dias |
| Casamento | 3 dias |
| Doação de sangue | 1 dia/ano |
| Alistamento eleitoral | 2 dias |
| Serviço militar | Conforme necessidade |
| Vestibular | Dia da prova |
| Acompanhamento de filho (médico) | 1 dia/ano |
| Acompanhamento de cônjuge (pré-natal) | 3 dias |

### Afastamentos Não Remunerados
| Tipo | Prazo | Observação |
|------|-------|------------|
| Suspensão disciplinar | Até 30 dias | Sem remuneração |
| Licença não remunerada | Conforme acordo | Sem remuneração |
| Greve | Conforme duração | Sem remuneração |

### Licença-Maternidade
- **Duração**: 120 dias (4 meses) sem prejuízo do emprego e salário.
- **Empresa Cidadã**: 180 dias (6 meses) com reembolso tributário.
- **Adoção**: 120 dias (criança até 1 ano), 60 dias (1-4 anos), 30 dias (4-8 anos).
- **Natimorto**: 120 dias.
- **Estabilidade**: da confirmação da gravidez até 5 meses pós-parto.
- **Salário-maternidade**: pago pelo INSS (empresa antecipa e desconta do INSS patronal).

### Licença-Paternidade
- **Padrão**: 5 dias.
- **Empresa Cidadã**: 20 dias (+15).

### Afastamento por Acidente de Trabalho
- **CAT obrigatória**: emitir em até 1º dia útil.
- **Auxílio-doença acidentário (B91)**: INSS paga a partir do 16º dia.
- **Estabilidade**: 12 meses após alta médica.
- **FGTS**: depósito obrigatório durante o afastamento.

### Estabilidade Provisória
| Situação | Período de Estabilidade |
|----------|------------------------|
| Gestante | Confirmação da gravidez até 5 meses pós-parto |
| CIPA | Candidatura até 1 ano após mandato |
| Acidente de trabalho (B91) | 12 meses após alta |
| Dirigente sindical | Candidatura até 1 ano após mandato |

### Afastamentos no eSocial
- **S-2230**: Afastamento temporário — início (`iniAfastamento`) e retorno (`fimAfastamento`).
- **S-2210**: CAT — Comunicação de Acidente de Trabalho.
- **S-2220**: Monitoramento da saúde — exames ocupacionais.
- **S-2299**: Desligamento — inclui informações de SST.

**Códigos de motivo de afastamento (principais):**
| Código | Descrição |
|--------|-----------|
| 00000001 | Acidente / Doença do trabalho |
| 00000003 | Doença (não relacionada ao trabalho) |
| 00000006 | Licença-maternidade |
| 00000008 | Licença-paternidade |
| 00000011 | Licença sem vencimento |

### Retorno ao Trabalho
- **Exame de retorno**: obrigatório após afastamento > 30 dias (S-2220).
- **Reintegração**: empregado estável deve ser readmitido na mesma função.
- **Novo período aquisitivo**: inicia-se após retorno de afastamento > 6 meses.

## Related Documents
- [esocial-trabalhador](esocial-trabalhadores.md) — Eventos cadastrais do trabalhador
- [saude-trabalho](saude-trabalho.md) — PCMSO, PGR, LTCAT e SST
- [clt](clt.md) — Consolidação das Leis do Trabalho
- [inss-irrf](inss-irrf.md) — Contribuições previdenciárias
