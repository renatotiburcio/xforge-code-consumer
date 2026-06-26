---
id: danfe-dacte
type: knowledge
tags: [fiscal, danfe, dacte, documento-auxiliar, impressao, nfe, cte]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar o layout, regras e impressão do DANFE (Documento Auxiliar da NF-e) e do DACTE (Documento Auxiliar do CT-e)...
- **Principais responsabilidades**: Definir o layout visual do DANFE (NF-e) e DACTE (CT-e); Documentar dados obrigatórios, formato e estrutura; Cobrir DANFE simplificado (NFC-e), cont...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, danfe, dacte, documento-auxiliar, impressao, nfe, cte
- **Restrições/Regras**: DANFE/DACTE não substitui o XML (documento fiscal); Obrigatório para acompanhar a mercadoria/carga

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `danfe-dacte` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 8 |


# DANFE e DACTE — Documentos Auxiliares da NF-e e CT-e

## Purpose
Documentar o layout, regras e impressão do DANFE (Documento Auxiliar da NF-e) e do DACTE (Documento Auxiliar do CT-e), representações gráficas simplificadas dos documentos fiscais eletrônicos que acompanham o trânsito de mercadorias e cargas.

## Responsibilities
- Definir o layout visual do DANFE (NF-e) e DACTE (CT-e)
- Documentar dados obrigatórios, formato e estrutura
- Cobrir DANFE simplificado (NFC-e), contingência e QR Code
- Explicar regras de impressão e armazenamento

## Dependencies
- XML autorizado da NF-e ou CT-e
- Impressora (A4 para DANFE/DACTE, térmica para NFC-e)
- Chave de acesso (44 dígitos) para consulta

## Constraints
- DANFE/DACTE não substitui o XML (documento fiscal)
- Obrigatório para acompanhar a mercadoria/carga
- Sem DANFE, a mercadoria pode ser apreendida
- XML deve ser armazenado por no mínimo 5 anos

## DANFE — Documento Auxiliar da NF-e

### Finalidade
- Acompanhar o trânsito de mercadorias
- Permitir consulta via chave de acesso
- Comprovar a operação fiscal
- Facilitar a fiscalização

### Formato
- Papel: A4 (210mm × 297mm), retrato
- Área útil: 180mm × 260mm
- Margens: 5mm (superior, inferior, esquerda, direita)

### Estrutura do Layout
1. **Emitente**: logotipo, razão social, CNPJ, IE, endereço
2. **Cabeçalho DANFE**: tipo (0=entrada/1=saída), série, número, página
3. **Chave de Acesso**: 44 dígitos em destaque + código de barras Code 128 + protocolo de autorização (15 dígitos)
4. **Natureza da Operação** + IE do substituto
5. **Destinatário/Remetente**: nome, CNPJ/CPF, data emissão, endereço, bairro, CEP, data/hora entrada/saída
6. **Fatura/Duplicatas**: número, vencimento, valor
7. **Cálculo do Imposto**: base ICMS, valor ICMS, base ST, valor ST, total produtos, frete, seguro, desconto, outras despesas, IPI, total NF-e
8. **Transportador**: razão social, frete por conta, ANTT, placa, UF, CNPJ, endereço, quantidade, espécie, peso bruto/líquido
9. **Produtos/Serviços**: código, descrição, NCM, CFOP, unidade, quantidade, valor unitário, valor total (por item)
10. **Dados Adicionais**: informações complementares, reservado ao fisco

### Dados Obrigatórios
Chave de acesso (44 dígitos), código de barras, protocolo, emitente (razão social, CNPJ), destinatário, cálculo do imposto, data/hora, valor total.

### DANFE Simplificado (NFC-e)
- Formato reduzido (80mm ou 58mm)
- Via do consumidor + via do estabelecimento
- QR Code para consulta (obrigatório)
- Chave de acesso no QR Code
- Impresso em impressora térmica

### DANFE de Contingência
- DANFE em formulário de segurança (FS)
- DANFE em formulário de contingência (FS-IA, FS-DA)
- DANFE EPEC (Pré-evento)

## DACTE — Documento Auxiliar do CT-e

### Finalidade
- Acompanhar o trânsito de cargas
- Permitir consulta via chave de acesso
- Comprovar o serviço de transporte
- Facilitar a fiscalização

### Formato
- Papel: A4 (210mm × 297mm)
- Impressão: jato de tinta ou laser
- Via: única (com via do tomador quando necessário)

### Estrutura do Layout
1. **Cabeçalho DACTE**: CT-e número, série
2. **Emitente**: razão social, CNPJ, IE, endereço
3. **Chave de Acesso**: 44 dígitos + código de barras Code 128
4. **Tipo do CT-e** + tipo de serviço + modal + municípios início/fim
5. **Tomador do Serviço**: nome, CNPJ/CPF, IE
6. **Remetente**: nome, CNPJ/CPF
7. **Expedidor**: nome, CNPJ/CPF
8. **Destinatário**: nome, CNPJ/CPF
9. **Informações da Carga**: produto predominante, valor total, quantidades
10. **Componentes do Valor**: frete peso, frete valor, pedágio, outros, BC ICMS, alíquota ICMS, valor ICMS, total serviço, valor a receber
11. **Informações do Fisco**
12. **Veículos**: placa, UF, RNTRC, proprietário
13. **Seguro**: apólice, seguradora
14. **Observações**

### Dados Obrigatórios
Chave de acesso (44 dígitos), código de barras, emitente (razão social, CNPJ, IE), tomador, remetente, expedidor, destinatário, componentes do valor, informações da carga, veículos, protocolo de autorização.

## Regras Gerais
- DANFE/DACTE é obrigatório para acompanhar a mercadoria/carga
- Sem documento auxiliar, a mercadoria pode ser apreendida
- Consulta via chave de acesso no site da SEFAZ ou QR Code
- O documento auxiliar não substitui o XML
- Em contingência: DANFE/DACTE em formulário de segurança

## Related Documents
- [NF-e](nfe.md) — nota fiscal eletrônica
- [CT-e](cte.md) — conhecimento de transporte eletrônico
- [NFC-e](nfce.md) — nota fiscal de consumidor eletrônico
- [MDF-e](mdfe.md) — manifesto de documentos fiscais eletrônico
