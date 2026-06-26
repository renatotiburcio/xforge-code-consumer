---
id: erp-faturamento
type: knowledge
tags: [erp, faturamento, nfe, nfce, cte, mdfe, nfs-e, fiscal, sefaz, impostos]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Módulo de Faturamento / Notas Fiscais Eletrônicas
- **Principais responsabilidades**: Emitir NF-e (modelo 55) para circulação de mercadorias com cálculo automático de ICMS, IPI, PIS, COFINS.; Emitir NFC-e (modelo 65) para venda ao co...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: erp, faturamento, nfe, nfce, cte, mdfe, nfs-e, fiscal, sefaz, impostos
- **Tipo**: knowledge | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `erp-faturamento` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Módulo de Faturamento / Notas Fiscais Eletrônicas

## Propósito

Documentar o processo de emissão de documentos fiscais eletrônicos no ERP, cobrindo NF-e (modelo 55), NFC-e (modelo 65), CT-e (modelo 57), MDF-e (modelo 58) e NFS-e, além de cancelamento, carta de correção, contingência e integração com estoque, financeiro e SPED.

## Responsabilidades

- Emitir NF-e (modelo 55) para circulação de mercadorias com cálculo automático de ICMS, IPI, PIS, COFINS.
- Emitir NFC-e (modelo 65) para venda ao consumidor final com QR Code e DANFE simplificado.
- Emitir CT-e (modelo 57) para prestação de serviço de transporte de cargas.
- Emitir MDF-e (modelo 58) para consolidação de múltiplas NF-e/CT-e em uma mesma viagem.
- Emitir NFS-e para prestação de serviços sujeitos ao ISS (alíquota municipal de 2% a 5%).
- Calcular tributos automaticamente: ICMS (próprio, ST, DIFAL), IPI, PIS (cumulativo/não-cumulativo), COFINS.
- Transmitir documentos via WebService da SEFAZ com assinatura digital (certificado A1/A3).
- Gerenciar cancelamento (prazo por estado), carta de correção (CC-e, até 720h) e inutilização de numeração.
- Gerar contingência: FS-DA, DPEC, SVC quando SEFAZ indisponível.
- Integrar com estoque (baixa automática), financeiro (geração de contas a receber) e SPED (bloco C).

## Dependências

- **fluxo-vendas.md** — Pedido de venda como origem do faturamento.
- **estoque.md** — Baixa automática de estoque na autorização da NF-e.
- **trocas-devolucoes.md** — NF-e de devolução, estorno de impostos.

## Restrições

- Chave de NF-e: 44 dígitos (cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF + DV).
- Cancelamento NF-e: 24h (maioria), 72h (alguns), 7 dias (AM/AP/BA/CE/DF/ES/GO/MA/PA/PB/PE/PI/RN/RO/RR/SE/TO).
- CC-e: até 720h (30 dias), não pode alterar valores fiscais nem destinatário.
- Inutilização: até o 10º dia do mês seguinte.
- MDF-e deve ser encerrado após conclusão do transporte (multa por omissão).
- Ambiente de homologação obrigatório antes de produção.

## Relacionados

- [fluxo-vendas.md](fluxo-vendas.md) — Pipeline de vendas e pedidos.
- [estoque.md](estoque.md) — Baixa de estoque e movimentações.
- [trocas-devolucoes.md](trocas-devolucoes.md) — Devoluções e documentos fiscais de retorno.

