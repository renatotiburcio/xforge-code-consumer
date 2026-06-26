---
id: cnab-boletos
type: conhecimento
tags: [financeiro, cnab, boleto, pix, integracao-bancaria]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre CNAB, Boletos e Integração Bancária
- **Seções principais**: CNAB (Comunicação Bancária Padronizada), PIX, Integrações Bancárias, Conciliação Bancária
- **Tags**: financeiro, cnab, boleto, pix, integracao-bancaria
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `cnab-boletos` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 4 |


# CNAB, Boletos e Integração Bancária

## CNAB (Comunicação Bancária Padronizada)

### CNAB 240 (Spefin - FEBRABAN)
- Padrão nacional para remessa e retorno
- Usado para: títulos, folha, DARF, GPS
- Layout: header + detalhes (segmentos A-J) + trailer
- Cada banco pode ter particularidades

### CNAB 400 (Legado)
- Padrão antigo ainda usado por bancos menores
- Layout: header + registro tipo 1 e 2 + trailer
- Menos campos, menos validações

### Fluxo Boleto
1. Emissão → Gerar dados (sacado, valor, vencimento)
2. Nosso número → Sequencial por carteira
3. Linha digitável → Código de barras
4. Remessa → Arquivo CNAB enviado ao banco
5. Retorno → Banco devolve status dos títulos

### Registros CNAB 240 - Título
| Segmento | Função |
|----------|--------|
| A | Dados do título |
| B | Dados do sacado |
| C | Dados do sacador/avalista |
| D | Ocorrências |
| E | Desconto/Deduação |
| F | Juros/Mora |
| G | Desconto por antecipação |
| H | Abatimento |

## PIX

### Tipos de Chave
| Tipo | Formato | Uso |
|------|---------|-----|
| CNPJ | 14 dígitos | Empresas |
| Email | email@domínio | Pessoas/Física |
| Telefone | +55DDEXXXXX | Pessoas/Física |
| Aleatória | UUID | Qualquer |

### Modalidades
| Modo | Descrição | Uso |
|------|-----------|-----|
| Estático | QR Code fixo | Recebimentos recorrentes |
| Dinâmico | QR Code único por transação | E-commerce |

### Vantagens sobre Boleto
- Liquidação instantânea (vs D+1-D+30)
- Sem custo de registro
- Sem protesto necessário
- Confirmação via webhook

## Integrações Bancárias

### Open Banking / Open Finance
- Fase 1: Dados de contas e cartões
- Fase 2: Meios de pagamento
- Fase 3: Crédito
- Fase 4: Seguros
- API REST com OAuth 2.0

### APIs Bancárias Principais
| Banco | Endpoint | Auth |
|-------|----------|------|
| Itaú | api.itau.com.br | OAuth 2.0 |
| Bradesco | api.bradesco.com.br | OAuth 2.0 |
| BB | api.bb.com.br | Certificado |
| Inter | api.inter.co | OAuth 2.0 |
| Sicredi | api.sicredi.com.br | OAuth 2.0 |

## Conciliação Bancária

### Processo
1. Extrair extrato bancário (OFX ou API)
2. Importar lançamentos do ERP
3. Match automático: valor + data + documento
4. Divergências → fila de análise
5. Conciliação manual para não-match

### Critérios de Match
- Valor exato
- Data dentro de tolerância (±2 dias)
- Documento referenciado
- Descrição parcial compatível
