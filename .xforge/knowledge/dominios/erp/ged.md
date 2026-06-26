---
id: erp-ged
type: knowledge
tags: [erp, ged, gestao-documentos, nfe, ct-e, contratos, rh, indexacao, retencao, lgpd]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre GED — Gestão Eletrônica de Documentos
- **Principais responsabilidades**: Armazenar documentos fiscais: XML NF-e/NFC-e/NFS-e, CT-e, MDF-e, SPED, DANFE, guias de recolhimento, certidões negativas.; Armazenar documentos con...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, ged, gestao-documentos, nfe, ct-e, contratos, rh, indexacao, retencao, lgpd
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-ged` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# GED — Gestão Eletrônica de Documentos

## Propósito

Documentar o módulo de GED do ERP, cobrindo armazenamento digital de documentos (NF-e XML, CT-e XML, contratos, documentos RH), indexação por metadados, busca, versionamento, workflow de aprovação, retenção e descarte, e conformidade com LGPD.

## Responsabilidades

- Armazenar documentos fiscais: XML NF-e/NFC-e/NFS-e, CT-e, MDF-e, SPED, DANFE, guias de recolhimento, certidões negativas.
- Armazenar documentos contratuais: contratos comerciais, aditivos, rescisões, procurações, NDA.
- Armazenar documentos trabalhistas: PPP, ASO, CAT, fichas de registro, guias FGTS/INSS, recibos de férias/rescisão.
- Armazenar documentos contábeis: livros contábeis, balancetes, DRE, notas explicativas.
- Armazenar documentos administratos: atas, alvarás, certidões, documentos societários.
- Indexar documentos por metadados: tipo, número, data, emitente, CNPJ, valor, CFOP, chave de acesso, status.
- Extrair metadados automaticamente de XML (NF-e, CT-e) via parser.
- Aplicar OCR a documentos digitalizados para busca full-text.
- Gerenciar ciclo de vida: criação/captura → classificação → indexação → armazenamento → distribuição → uso → retenção/descarte.
- Controlar retenção por tabela de temporalidade: NF-e (5 anos), trabalhistas (20 anos), FGTS (30 anos), contratos (vigência + 5 anos).
- Gerenciar segurança: controle de acesso por usuário/grupo/documento, criptografia (TLS 1.2+, AES-256), auditoria de ações.
- Garantir conformidade LGPD: direito de acesso/exclusão, anonimização, base legal para tratamento.

## Dependências

- **faturamento.md** — XML de NF-e/NFC-e/CT-e gerados pelo módulo fiscal.
- **fluxo-compras.md** — Contratos de compra, documentos de fornecedores.
- **fluxo-vendas.md** — Contratos de venda, propostas comerciais.

## Restrições

- XML de NF-e: armazenamento obrigatório por 5 anos (art. 202 do CTN).
- Documentos trabalhistas: retenção de 20 anos (CLT).
- FGTS: retenção de 30 anos (Lei 8.036/1990).
- Eliminação digital: exclusão criptográfica com registro formal.
- Eliminação física: trituração cross-cut nível P-4 ou superior com certificado de destruição.
- LGPD: dados pessoais em documentos (CPF, RG, dados de saúde em ASO/CAT) requerem controle de acesso rigoroso.
- Backup: regra 3-2-1 (3 cópias, 2 mídias, 1 offsite); RPO ≤ 24h, RTO ≤ 4h.

## Relacionados

- [faturamento.md](faturamento.md) — Documentos fiscais eletrônicos.
- [fluxo-compras.md](fluxo-compras.md) — Compras e contratos.
- [fluxo-vendas.md](fluxo-vendas.md) — Vendas e documentos comerciais.

