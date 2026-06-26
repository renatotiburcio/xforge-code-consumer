---
id: esocial-geral
type: knowledge
tags: [esocial, escrituracao, obrigacoes, fiscais, previdenciarias, trabalhistas, layout]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre eSocial — Escrituração Digital das Obrigações Fiscais, Previdenciárias e Trabalhistas
- **Principais responsabilidades**: Unificar o envio de informações trabalhistas, previdenciárias e fiscais em um único sistema digital.; Substituir obrigações acessórias como GFIP, C...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: esocial, escrituracao, obrigacoes, fiscais, previdenciarias, trabalhistas, layout
- **Restrições/Regras**: **Prazo eventos periódicos**: até o dia 15 do mês seguinte.; **Prazo eventos não periódicos**: conforme Tabela 6 do l...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `esocial-geral` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# eSocial — Escrituração Digital das Obrigações Fiscais, Previdenciárias e Trabalhistas

## Propósito
Visão geral do eSocial: conceito, objetivos, estrutura de eventos, leiaute vigente, certificação digital, penalidades e integração com demais obrigações acessórias.

## Responsabilidades
- Unificar o envio de informações trabalhistas, previdenciárias e fiscais em um único sistema digital.
- Substituir obrigações acessórias como GFIP, CAGED, RAIS, DIRF (parcialmente), CAT, LRE, PPP.
- Garantir conformidade com os prazos e leiautes vigentes.

## Dependências
- Certificado digital e-CNPJ (A1 ou A3) para transmissão.
- Leiaute S-1.3 (NT 06/2026) — Manual de Orientação do eSocial (MOS).
- Acesso via gov.br (nível ouro ou prata) ou webservice.
- Integração com EFD-Reinf e DCTFWeb para tributos federais.

## Constraints
- **Prazo eventos periódicos**: até o dia 15 do mês seguinte.
- **Prazo eventos não periódicos**: conforme Tabela 6 do leiaute (ex.: admissão antes do início, desligamento em 10 dias).
- **Multa por atraso**: mínimo de R$ 1.818,25 por evento.
- **Multa por omissão**: mínimo de R$ 1.818,25 por evento.
- **Guarda documental**: 20 anos.

## Conteúdo

### Conceito e Objetivos
O eSocial é o sistema de escrituração digital que unifica o envio de informações trabalhistas, previdenciárias e fiscais ao governo federal. Instituído pelo Decreto 8.373/2015, simplifica o cumprimento de obrigações acessórias, reduzindo redundâncias e automatizando validações.

### Versão Atual
- **Leiaute**: S-1.3 (NT 06/2026)
- **Esquemas XSD**: disponíveis para download no portal oficial
- **Manual de Orientação (MOS)**: consolidado até NO 11/2026

### Grupos de Eventos

| Grupo | Eventos | Descrição |
|-------|---------|-----------|
| **Tabela** | S-1000 a S-1080 | Cadastros do empregador (empresa, estabelecimentos, rubricas, lotações, cargos, etc.) |
| **Não Periódicos** | S-2190 a S-3000 | Admissão, alterações, afastamentos, CAT, desligamento, exclusão |
| **Periódicos** | S-1200 a S-1299 | Remuneração, pagamentos, fechamento da folha |

### Tabela Resumo de Eventos

| Evento | Descrição | Tipo |
|--------|-----------|------|
| S-1000 | Informações do Empregador | Tabela |
| S-1010 | Tabela de Rubricas | Tabela |
| S-1020 | Tabela de Lotações Tributárias | Tabela |
| S-1200 | Remuneração do Trabalhador | Periódico |
| S-1210 | Pagamentos de Rendimentos | Periódico |
| S-1299 | Fechamento dos Eventos Periódicos | Periódico |
| S-2200 | Cadastramento Inicial — Vínculo | Não periódico |
| S-2210 | CAT | Não periódico |
| S-2230 | Afastamento Temporário | Não periódico |
| S-2299 | Desligamento | Não periódico |
| S-3000 | Exclusão de Eventos | Não periódico |

### Obrigações Substituídas pelo eSocial
| Obrigação Substituída | Descrição |
|----------------------|-----------|
| GFIP | Guia de Recolhimento do FGTS |
| CAGED | Cadastro Geral de Empregados e Desempregados |
| RAIS | Relação Anual de Informações Sociais |
| CAT | Comunicação de Acidente de Trabalho |
| LRE | Livro de Registro de Empregados |
| PPP | Perfil Profissiográfico Previdenciário |
| GRRF | Guia de Recolhimento Rescisório do FGTS |
| DIRF | Declaração do IR Retido na Fonte (parcial) |

### Certificação Digital
Obrigatória para transmissão dos eventos. Tipos aceitos:
- **e-CNPJ A1**: arquivo digital (validade 1 ano)
- **e-CNPJ A3**: token ou cartão (validade 1-3 anos)
- Deve ser emitido por autoridade certificadora ICP-Brasil.

### Penalidades
- **Atraso no envio**: multa mínima de R$ 1.818,25 por evento.
- **Omissão de informações**: multa mínima de R$ 1.818,25 por evento.
- **Infrações específicas**: valores variam conforme a gravidade e o número de empregados afetados.

### Integração com EFD-Reinf e DCTFWeb
- **EFD-Reinf**: Escrituração Fiscal Digital de Retenções — complementa o eSocial para retenções de IR, PIS, COFINS, CSLL e ISS.
- **DCTFWeb**: Declaração de Débitos e Créditos Tributários Federais Web — apura tributos federais (IRPJ, CSLL, PIS, COFINS, IPI, etc.) com base nos dados do eSocial e EFD-Reinf.
- Os três sistemas (eSocial, EFD-Reinf, DCTFWeb) compartilham dados, reduzindo redundâncias.

### Grupos de Obrigatoriedade
| Grupo | Empresas | Início |
|-------|----------|--------|
| 1 | Faturamento > R$ 78 milhões | Mar/2018 |
| 2 | Faturamento ≤ R$ 78 milhões (não optantes Simples) | Jul/2018 |
| 3 | Optantes Simples Nacional, PF, produtores rurais | Jan/2019 |
| 4 | Entes públicos e organizações internacionais | Jul/2021 |

### Acesso
- Via **gov.br** (nível ouro ou prata obrigatório a partir de jun/2023)
- **Acesso via código de descontinuado a partir de 12/06/2026** — apenas nível ouro ou prata
- Via **webservice** para integração com sistemas ERP
- Via **módulo web** simplificado para pequenos empregadores

### Atualizações 2026
- **Layout v. S-1.3**: implantado em produção em 01/07/2026
- **CNPJ Alfanumérico**: suporte incluído no layout S-1.3
- **Certificado digital**: novo padrão de segurança a partir de 24/06/2026
- **FGTS Digital**: obrigatório para recolhimentos judiciais a partir de maio/2026
- **CAT Doméstico**: disponível no eSocial Doméstico
- **Naturezas de rubrica**: novas para Crédito do Trabalhador e assistência médica/odontológica

## Related Documents
- [esocial-empregador](esocial-empregadores.md) — Eventos S-1000 a S-1080
- [esocial-trabalhador](esocial-trabalhadores.md) — Eventos S-2190 a S-3000
- [esocial-folha](esocial-folha.md) — Eventos S-1200 a S-1299
- [obrigacoes-acessorias-federais](obrigacoes-acessorias-federais.md) — DIRF, DCTFWeb, EFD-Reinf
