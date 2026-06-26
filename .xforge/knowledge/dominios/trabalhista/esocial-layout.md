---
id: esocial-layout
type: dominio
tags: [esocial, layout, xml, eventos, prazos]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar a estrutura tecnica dos eventos XML do eSocial, incluindo prazos, codigos de retorno e regras de validacao.
- **Principais responsabilidades**: Definir estrutura XML padrao dos eventos; Mapear prazos de envio por evento; Documentar codigos de retorno e erro
- **Seções principais**: Purpose, Responsabilities, Dependencies, Constraints
- **Tags**: esocial, layout, xml, eventos, prazos
- **Restrições/Regras**: Leiaute vigente: S-1.3; Ambiente de producao: v. S-1.3

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `esocial-layout` |
| Tipo | dominio |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 14 |


# eSocial — Layout e Regras Tecnicas

## Purpose
Documentar a estrutura tecnica dos eventos XML do eSocial, incluindo prazos, codigos de retorno e regras de validacao.

## Responsabilities
- Definir estrutura XML padrao dos eventos
- Mapear prazos de envio por evento
- Documentar codigos de retorno e erro
- Garantir conformidade com leiaute vigente

## Dependencies
- `esocial-geral.md` — Visao geral do eSocial
- `esocial-empregadores.md` — Eventos S-1000 a S-1080
- `esocial-trabalhadores.md` — Eventos S-2190 a S-3000
- `esocial-folha.md` — Eventos S-1200 a S-1299

## Constraints
- Leiaute vigente: S-1.3
- Ambiente de producao: v. S-1.3
- Esquemas XSD disponiveis para download no portal eSocial
- Manual de Orientacao (MOS) consolidado

## Estrutura do XML
```xml
<eSocial xmlns="http://www.esocial.gov.br/schema/evt/XXX/v_S_01_03">
  <evtID>
    <Id>XXXXXXXXXXXXXX</Id>
  </evtID>
  <ideEvento>
    <tpAmb>1</tpAmb>        <!-- 1=Producao, 2=Homologacao -->
    <procEmi>1</procEmi>    <!-- 1=Aplicativo do empregador -->
    <verProc>1.0</verProc>
  </ideEvento>
  <ideEmpregador>
    <tpInsc>1</tpInsc>      <!-- 1=CNPJ, 2=CPF -->
    <nrInsc>XXXXXXXXXXXXXX</nrInsc>  <!-- 14 digitos para CNPJ -->
  </ideEmpregador>
  <!-- Dados especificos do evento -->
</eSocial>
```

## Campos Obrigatorios Gerais
| Campo | Descricao | Valores |
|-------|-----------|---------|
| tpAmb | Ambiente | 1=Producao, 2=Homologacao |
| procEmi | Processo de emissao | 1=App empregador, 3=App governo |
| verProc | Versao do processo | Ex: 1.0, 2.1 |
| tpInsc | Tipo inscricao empregador | 1=CNPJ, 2=CPF |
| nrInsc | Numero inscricao | 14 digitos (CNPJ) |

## Eventos de Tabela (S-1000 a S-1080)
| Evento | Descricao | Prazo |
|--------|-----------|-------|
| S-1000 | Informacoes do Empregador | Antes dos demais eventos |
| S-1005 | Tabela de Estabelecimentos | Antes de S-1020 |
| S-1010 | Tabela de Rubricas | Antes da folha |
| S-1020 | Tabela de Lotacoes Tributarias | Antes da folha |
| S-1030 | Tabela de Cargos | Antes da folha |
| S-1040 | Tabela de Funcoes | Antes da folha |
| S-1050 | Tabela de Horarios | Antes da folha |
| S-1060 | Tabela de Ambientes | Antes de S-2240 |
| S-1070 | Tabela de Processos | Antes de retencoes |

## Eventos Cadastrais (S-2190 a S-2420)
| Evento | Descricao | Prazo |
|--------|-----------|-------|
| S-2190 | Admissao — Ativo | Antes da data de inicio |
| S-2200 | Cadastramento Inicial — Vinculo | Antes da data de inicio |
| S-2205 | Alteracao Cadastral | 7 dias |
| S-2206 | Alteracao Contratual | 7 dias |
| S-2210 | CAT — Acidente Trabalho | 1 dia util seguinte |
| S-2220 | Monitoramento da Saude | 7 dias |
| S-2230 | Afastamento Temporario | Imediato |
| S-2240 | Condicoes Ambientais | Apos avaliação |
| S-2299 | Desligamento | 10 dias |

## Eventos de Folha (S-1200 a S-1299)
| Evento | Descricao | Prazo |
|--------|-----------|-------|
| S-1200 | Remuneracao | Ate 5 do mes seguinte |
| S-1202 | Remuneracao RPPS | Ate 5 do mes seguinte |
| S-1210 | Pagamentos | Ate 15 do mes seguinte |
| S-1295 | Fechamento periodos | Ate 5 do mes seguinte |
| S-1298 | Reabertura periodos | Imediato |
| S-1299 | Fechamento eventos | Ate ultimo dia util mes |

## Tabelas de Referencia
| Tabela | Descricao |
|--------|-----------|
| Tabela 1 | Categorias de funcionarios |
| Tabela 2 | Natureza das rubricas |
| Tabela 3 | Codigos de lotacao tributaria |
| Tabela 4 | Cargos/empregos publicos |
| Tabela 5 | Funcoes/comissao |
| Tabela 6 | Horarios/turnos |
| Tabela 7 | Ambientes de trabalho |
| Tabela 8 | Processos administrativos/judiciais |
| Tabela 9 | Operacoes |
| Tabela 10 | Natureza juridica |
| Tabela 11 | Compatibilidade categoria/x |
| Tabela 12 | Compatibilidade lotacao/x |
| Tabela 13 | Compatibilidade categoria/x |
| Tabela 14 | Compatibilidade lotacao/x |
| Tabela 15 | Incidentes S-1200 |
| Tabela 16 | Codigos GPS/GRPS |

## URLs de Webservice (Producao)
| Servico | URL |
|---------|-----|
| Consulta Processamento | https://webservices.producaorestrita.esocial.gov.br/... |
| Recepcao Lote | https://webservices.producaorestrita.esocial.gov.br/... |
| Consulta Lote | https://webservices.producaorestrita.esocial.gov.br/... |

## Codigos de Retorno
| Codigo | Tipo | Descricao |
|--------|------|-----------|
| 100 | Sucesso | Processado com sucesso |
| 201 | Erro | Erro de schema XML |
| 202 | Erro | Erro de obrigatório |
| 203 | Erro | Erro de dominio |
| 301 | Warning | Alerta de validacao |
| 401 | Processando | Lote recebido, aguardando processamento |

## Regras de Validacao
- Todos os campos obrigatorios devem estar preenchidos
- CNPJ/CPF devem ser validos (modulo 11)
- Datas devem ser validas e coerentes
- Valores monetarios com 2 casas decimais
- Codigos de tabelas devem existir na referencia vigente
- Eventos de tabela devem ser enviados antes dos eventos de dados

## Related Documents
- `esocial-geral.md` — Visao geral
- `esocial-empregadores.md` — Eventos do empregador
- `esocial-trabalhadores.md` — Eventos do trabalhador
- `esocial-folha.md` — Eventos de folha
- `obrigacoes-acessorias.md` — Prazos e penalidades
