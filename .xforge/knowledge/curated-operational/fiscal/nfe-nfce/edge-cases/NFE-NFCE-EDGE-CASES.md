# Edge Cases NF-e/NFC-e

## Resumo Executivo

- **Tema**: Edge Cases NF-e/NFC-e
- **Itens principais**: playbook;; teste;; validação preventiva;
- **Seções**: Casos iniciais, Saída esperada
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Edge Cases NF-e/NFC-e |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 2 |


## Casos iniciais

1. Timeout após envio e reenvio sem consulta.
2. Migração de emissor e numeração já usada.
3. Nota emitida fora do ERP pelo portal do governo.
4. Contingência com diferença na chave.
5. Homologação aceita e produção rejeita.
6. Regra opcional por UF vira obrigatória.
7. Instabilidade SEFAZ confundida com rejeição definitiva.
8. Certificado A1/A3 vencido, bloqueado ou mal instalado.
9. XML assinado com canonicalização incorreta.
10. Responsável técnico obrigatório por UF.

## Saída esperada

Cada edge case deve virar:

- playbook;
- teste;
- validação preventiva;
- known error;
- memory update.
