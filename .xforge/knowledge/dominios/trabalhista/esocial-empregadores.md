---
id: esocial-empregadores
type: knowledge
tags: [esocial, empregador, tabela, s1000, s1080, eventos, obrigacoes]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Eventos do Empregador no eSocial (S-1000 a S-1080)
- **Principais responsabilidades**: Cadastrar informações do empregador (S-1000), estabelecimentos (S-1005), rubricas (S-1010), lotações tributárias (S-1020), cargos (S-1030), carreir...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: esocial, empregador, tabela, s1000, s1080, eventos, obrigacoes
- **Restrições/Regras**: Eventos de tabela devem ser enviados **antes** de qualquer evento de folha ou não periódico.; Retificações exigem pre...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `esocial-empregadores` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Eventos do Empregador no eSocial (S-1000 a S-1080)

## Propósito
Documentar os eventos de tabela do empregador no eSocial, que formam a base cadastral necessária para todos os demais eventos do sistema.

## Responsabilidades
- Cadastrar informações do empregador (S-1000), estabelecimentos (S-1005), rubricas (S-1010), lotações tributárias (S-1020), cargos (S-1030), carreiras (S-1035), funções (S-1040), horários (S-1050), ambientes (S-1060), processos judiciais (S-1070) e operadores portuários (S-1080).
- Garantir a ordem de envio: S-1000 → S-1005 → S-1020 → S-1070 → S-1010 → S-1030/S-1035/S-1040 → S-1050 → S-1060 → S-1080.
- Gerenciar retificações (envio completo do evento) e exclusões (com validade reduzida).
- Manter certificação digital válida (e-CNPJ A1 ou A3) para transmissão.

## Dependências
- Certificado digital e-CNPJ (A1 ou A3) para assinatura dos eventos.
- Sistema ERP/Software de folha para geração dos arquivos XML.
- Leiaute S-1.3 do eSocial (NT 06/2026).
- Tabelas de códigos oficiais: CNAE (IBGE), CBO (MTE), FPAS, classificação tributária.

## Constraints
- Eventos de tabela devem ser enviados **antes** de qualquer evento de folha ou não periódico.
- Retificações exigem preenchimento de **todos** do registro, não apenas dos campos alterados.
- Exclusões são rejeitadas enquanto houver vínculos ativos com outros eventos.
- Períodos de validade (`iniValid`/`fimValid`) não podem se sobrepor para o mesmo registro.
- Ambiente de homologação (tpAmb=2) obrigatório para testes antes de produção (tpAmb=1).

## Conteúdo

### Tabela de Eventos (S-1000 a S-1080)

| Evento | Descrição | Campos Chave |
|--------|-----------|-------------|
| S-1000 | Informações do Empregador | tpInsc, nrInsc, nmRazao, classTrib, natJurid |
| S-1005 | Tabela de Estabelecimentos | tpInsc, nrInsc, cnaePre, aliqRat, fap |
| S-1010 | Tabela de Rubricas | codRubr, ideTabRubr, natRubr, codIncCP, codIncIRRF, codIncFGTS |
| S-1020 | Lotações Tributárias | codLotacao, tpLotacao, fpasLotacao |
| S-1030 | Cargos/Empregos Públicos | codCargo, nmCargo, cargoPublico, sitCargo |
| S-1035 | Carreiras Públicas | codCarreira, nmCarreira |
| S-1040 | Funções/Cargos em Comissão | codFuncao, dscFuncao |
| S-1050 | Horários/Turnos | codHorContratual, hrEntrada, hrSaida, durJornada |
| S-1060 | Ambientes de Trabalho | codAmb, nmAmb, dscAmb, localAmb |
| S-1070 | Processos Adm/Judiciais | tpProc, nrProc, descDecisao, infoSusp |
| S-1080 | Operadores Portuários | cnpjOpPortuario, aliqRat, fap, aliqRatAjust |

### Regras de Retificação e Exclusão
- **Retificação**: Enviar o mesmo evento com operação `alteracao`, preenchendo **todos** os campos (substituição integral).
- **Exclusão**: Enviar o evento com operação `exclusao`, referenciando o período de validade a ser excluído.
- Não é possível retificar dados de período anterior ao evento mais recente.

### Processamento Assíncrono
O eSocial utiliza modelo assíncrono: envio → processamento → resultado. O empregador deve aguardar o retorno de cada lote antes de enviar eventos dependentes. O recibo de entrega (`nrRecibo`) é obrigatório para retificações.

### Certificação Digital
Obrigatória para transmissão. Tipos aceitos: e-CNPJ A1 (arquivo) ou A3 (token/cartão). O certificado deve estar dentro da validade e ser emitido por autoridade certificadora ICP-Brasil.

## Related Documents
- [esocial-trabalhador](esocial-trabalhadores.md) — Eventos cadastrais do trabalhador (S-2190 a S-3000)
- [esocial-folha](esocial-folha.md) — Eventos de folha de pagamento (S-1200 a S-1299)
- [esocial-geral](esocial-geral.md) — Visão geral do eSocial
