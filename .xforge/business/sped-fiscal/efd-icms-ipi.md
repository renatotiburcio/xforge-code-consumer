---
title: "EFD ICMS IPI \u2014 SPED Fiscal"
summary: "EFD ICMS IPI: registros, blocos, prazos, validacoes, layout do arquivo magnetico"
keywords: ["sped", "efd", "icms", "ipi", "sped-fiscal", "bloco-0", "bloco-h"]
trustScore: 83
lastValidated: 2026-06-13
id: knowledge-sped-efd-icms-ipi
type: knowledge
---

# EFD ICMS IPI \u2014 SPED Fiscal

## O que e

A EFD ICMS IPI (Escrituracao Fiscal Digital) e um arquivo digital que substitui varios livros fiscais em papel:
- Registro de Entradas
- Registro de Saidas
- Registro de Inventario
- Apuracao do ICMS
- Apuracao do IPI

## Prazos

| Tipo | Prazo |
|------|-------|
| Mensal | Dia 25 do mes seguinte |
| Anual SPED Contribuicoes | Segundo dia util de marco |

## Blocos do arquivo

| Bloco | Conteudo | Obrigatorio |
|-------|----------|-------------|
| 0 | Abertura, identificacao, referencias | Sim |
| C | Documentos fiscais I (entradas/saidas) | Sim |
| D | Documentos fiscais II (CT-e, NF-e servico) | Condicional |
| E | Apuracao do ICMS e IPI | Sim |
| G | Controle do credito fiscal CIAP | Condicional |
| H | Inventario fisico | Sim (estoque) |
| K | Control de producao e estoque | Industrial |
| 1 | Informacoes complementares | Opcional |
| 9 | Encerramento | Sim |

## Estrutura de registros

Cada bloco tem varios tipos de registros. Exemplos:

### Bloco 0 (Abertura)
- 0000: Abertura do arquivo
- 0001: Abertura do bloco 0
- 0005: Dados do contribuinte
- 0100: Dados do contabilista
- 0150: Tabela de cadastro de participantes
- 0190: Tabela de unidades de medida
- 0200: Tabela de identificacao do item
- 0205: Alteracao do item
- 0220: Conversao de unidades

### Bloco C (Documentos fiscais I)
- C001: Abertura do bloco
- C100: Documento (NF, NFC, etc)
- C101: Informacoes complementares
- C113: DOC Fiscal referenciado
- C170: Itens do documento
- C190: Analise do documento
- C195: Observacoes do lancamento fiscal
- C200: CT-e
- C300: Resumo diario NF
- C400: Equipamento ECF
- C500: Energia eletrica / agua / gas

### Bloco E (Apuracao)
- E001: Abertura
- E100: Periodo da apuracao
- E110: Apuracao do ICMS
- E200: Periodo da apuracao IPI
- E210: Apuracao IPI

### Bloco H (Inventario)
- H001: Abertura
- H005: Totais do inventario
- H010: Item do inventario
- H020: Informacoes complementares

## Validacoes

| Erro | Significado |
|------|-------------|
| Schema invalido | XML nao confere com XSD do PVA |
| Totalizacao errada | Soma dos itens nao bate com total do documento |
| CFOP incompativel | CFOP nao permitido para operacao |
| CEST faltando | Item exige CEST mas nao tem |
| NCM nao existe | Codigo NCM invalido ou revogado |
| Data invalida | Data futura ou muito antiga |

## PVA (Programa Validador e Assinador)

Software disponibilizado pela Receita Federal:
- Valida arquivo contra XSD oficial
- Verifica regras de negocio
- Assina digitalmente
- Gera arquivo .txt pronto para transmissao

Download: https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/downloads

## Cuidados

- Validar **antes** de assinar (PVA mostra erros detalhados)
- Backup do arquivo original (nao retificar, gerar novo)
- Cenarios especificos: transferencia entre filiais, devolucoes, substituicao tributaria
- ECD (Escrituracao Contabil Digital) e **separada** (Bloco J na EFD)