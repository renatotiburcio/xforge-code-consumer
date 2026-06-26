---
name: sped-fiscal-expert
description: Expert em SPED Fiscal: EFD ICMS/IPI, EFD Contribuicoes, ECD, ECF, layouts, validacoes e prazos.
metadata:
  version: "1.0.0"
  xforge-category: "domain-expert"
---

# sped-fiscal-expert

## Objetivo

Gerar, validar e transmitir arquivos SPED com conformidade total.

## Tipos de SPED

### EFD ICMS/IPI (Escrituração Fiscal Digital)
- **Conteúdo**: Entradas, saídas, estoque, apuração ICMS e IPI
- **Prazo**: Até o dia 15 do mês seguinte
- **Transmissão**: Via portal SEFAZ ou software validador
- **Assinatura**: Certificado digital A1 ou A3

### EFD Contribuições
- **Conteúdo**: PIS/COFINS, contribuições sociales
- **Prazo**: Até o dia 15 do mês seguinte
- **Blocos**: 0 (identificação), A (apuração), C (documentos), M (apuração)

### ECD (Escrituração Contábil Digital)
- **Conteúdo**: Balancete, razão, diary, balanço
- **Prazo**: Até 31 de julho do ano seguinte
- **Transmissão**: Via eCAC

### ECF (Escrituração Contábil Fiscal)
- **Conteúdo**: Lucro real, presumido, LALUR
- **Prazo**: Até 31 de julho do ano seguinte
- **Obrigação**: Empresas com Lucro Real

## Layout EFD ICMS/IPI

### Blocos
| Bloco | Conteúdo |
|-------|----------|
| 0 | Abertura e Identificação |
| C | Documentos Fiscais I - Mercadorias |
| D | Documentos Fiscais II - Serviços |
| E | Apuração do ICMS e do IPI |
| G | Controle do Crédito de ICMS do Ativo Permanente |
| H | Inventário Físico |
| K | Controle da Produção e do Estoque |
| 1 | Complemento da Escrituração |
| 9 | Controle e Encerramento |

### Registros Principais
| Registro | Descrição |
|----------|-----------|
| C100 | Documento - Nota Fiscal |
| C170 | Itens do Documento |
| C190 | Registro Analítico do Documento |
| E100 | Período da Apuração do ICMS |
| E110 | Apuração do ICMS - Operações Próprias |
| E500 | Período de Apuração do IPI |

## Validações

| Erro | Causa | Correção |
|------|-------|----------|
| CFOP inválido | CFOP não existe na tabela | Corrigir CFOP no documento |
| CST inconsistente | CST não compatível com operação | Verificar regime tributário |
| Duplicidade | Mesmo documento registrado 2x | Verificar origem e remover |
| Saldo estoque | Diferença entre sistema e informado | Ajustar inventário |

## Procedimento

1. Fechar período no sistema
2. Gerar arquivo EFD ICMS/IPI
3. Validar com validador SEFAZ
4. Corrigir erros
5. Assinar com certificado digital
6. Transmitir
7. Guardar recibo de entrega
8. Gerar EFD Contribuições (se aplicável)

## Regras

- NUNCA transmitir sem validação prévia
- Backup do arquivo antes de transmitir
- Recibo de entrega保存ado por 5 anos
- Correção via novo arquivo (não exclusão)
- Certificado digital válido e não expirado
