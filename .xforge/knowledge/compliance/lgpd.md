---
id: compliance-lgpd
type: compliance
tags: [lgpd, compliance, dados-pessoais, privacidade, anpd, brasil]
owner: compliance-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Referência completa e genérica sobre a Lei nº 13.709/2018 (LGPD), Lei nº 13.853/2019 (ANPD) e deveres de tratamento d...
- **Principais responsabilidades**: Fornecer referência normativa para decisões de tratamento de dados; Guiar arquitetos, desenvolvedores e times de produto na conformidade; Apoiar o ...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: lgpd, compliance, dados-pessoais, privacidade, anpd, brasil
- **Restrições/Regras**: Conteúdo genérico — sem referências a projetos específicos; Deve ser revisado quando houver atualização normativa da ...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `compliance-lgpd` |
| Tipo | compliance |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | compliance-team |
| Total de seções | 17 |


# LGPD — Lei Geral de Proteção de Dados Pessoais

## Purpose

Referência completa e genérica sobre a Lei nº 13.709/2018 (LGPD), Lei nº 13.853/2019 (ANPD) e deveres de tratamento de dados pessoais no Brasil.

## Responsibilities

- Fornecer referência normativa para decisões de tratamento de dados
- Guiar arquitetos, desenvolvedores e times de produto na conformidade
- Apoiar o Programa de Conformidade e a elaboração de RIPDs

## Dependencies

- Disponível para todos os módulos que tratam dados pessoais de pessoas físicas
- Deve estar alinhado com políticas internas de privacidade e segurança

## Constraints

- Conteúdo genérico — sem referências a projetos específicos
- Deve ser revisado quando houver atualização normativa da ANPD
- Não substitui assessoria jurídica especializada

## Related Documents

- `compliance/gdpr.md` — referência GDPR
- `policy/privacy-policy.md` — política de privacidade
- `security/data-classification.md` — classificação de dados
- `architecture/data-flow.md` — diagrama de fluxo de dados

---

## 1. Visão Geral

A LGPD regulamenta o tratamento de dados pessoais de pessoas naturais (físicas), em meio digital ou físico, por pessoa natural ou jurídica de direito público ou privado, no território nacional ou quando o tratamento tenha por objetivo oferecer bens ou serviços a indivíduos localizados no Brasil.

- **Lei principal:** Lei nº 13.709/2018
- **Autoridade fiscalizadora:** Autoridade Nacional de Proteção de Dados (ANPD) — Lei nº 13.853/2019
- **Aplicabilidade:** Qualquer operação realizada no Brasil ou que envolva dados de titulares no Brasil

## 2. Princípios — Art. 6º

| # | Princípio | Descrição |
|---|-----------|-----------|
| 1 | **Finalidade** | Tratamento para propósitos legítimos, específicos, explícitos e informados ao titular |
| 2 | **Adequação** | Compatibilidade do tratamento com as finalidades informadas |
| 3 | **Necessidade** | Limitação ao mínimo necessário para realizar suas finalidades |
| 4 | **Livre acesso** | Garantia aos titulares de consulta facilitada e gratuita sobre forma e duração do tratamento |
| 5 | **Qualidade** | Garantia de exatidão, clareza, relevância e atualização dos dados |
| 6 | **Transparência** | Informações claras, precisas e facilmente acessíveis sobre o tratamento |
| 7 | **Segurança** | Utilização de medidas técnicas e administrativas aptas a proteger os dados |
| 8 | **Prevenção** | Adoção de medidas para prevenir a ocorrência de danos aos titulares |
| 9 | **Não discriminação** | Impossibilidade de tratamento para fins discriminatórios, ilícitos ou abusivos |
| 10 | **Responsabilização** | Demonstração de medidas eficazes de conformidade e segurança |

## 3. Bases Legais — Art. 7º

| # | Base Legal | Descrição |
|---|------------|-----------|
| I | Consentimento | Manifestação livre, informada e inequívoca do titular |
| II | Obrigação legal | Cumprimento de obrigação legal ou regulatória pelo controlador |
| III | Política pública | Administração pública para políticas públicas em leis/contratos |
| IV | Pesquisa | Estudos por órgão de pesquisa (anonimização sempre que possível) |
| V | Contrato | Execução de contrato ou procedimentos pré-contratuais |
| VI | Exercício de direitos | Exercício regular de direitos em processo judicial, administrativo ou arbitral |
| VII | Proteção da vida | Proteção da vida ou da incolumidade física do titular ou terceiro |
| VIII | Tutela da saúde | Realização por profissionais de saúde ou sanitárias |
| IX | Legítimo interesse | Interesse legítimo do controlador ou de terceiro (exceto direitos do titular) |
| X | Crédito | Proteção do crédito |

## 4. Dados Sensíveis — Art. 5º, II

Dado pessoal sobre:

1. Origem racial ou étnica
2. Convicção religiosa
3. Opinião política
4. Filiação a sindicato ou a organização de caráter religioso, filosófico ou político
5. Dado referente à saúde ou à vida sexual
6. Dado genético ou biométrico, quando vinculado a uma pessoa natural

> Base legal para dados sensíveis: consentimento específico ou uma das hipóteses dos incisos II, V, VI, VII, VIII ou X do Art. 11.

## 5. Direitos do Titular — Art. 18

1. **Confirmação** — existência de tratamento
2. **Acesso** — aos dados pessoais tratados
3. **Correção** — de dados incompletos, inexatos ou desatualizados
4. **Anonimização, bloqueio ou eliminação** — de dados desnecessários, excessivos ou tratados em desconformidade
5. **Portabilidade** — dos dados a outro fornecedor de serviço ou produto
6. **Eliminação** — de dados tratados com consentimento (exceto hipóteses de retenção)
7. **Informação** — sobre entidades públicas e privadas com as quais os dados foram compartilhados
8. **Informação sobre consentimento** — possibilidade de não fornecer consentimento e consequências
9. **Revogação** — do consentimento a qualquer momento

## 6. Agentes de Tratamento — Art. 4º, VI–VIII

| Agente | Papel |
|--------|-------|
| **Controlador** | Toma as decisões sobre o tratamento de dados pessoais |
| **Operador** | Realiza o tratamento em nome do controlador, seguindo suas instruções |
| **Encarregado (DPO)** | Canal de comunicação entre controlador, titulares e ANPD; orientação e execução de práticas de conformidade |

## 7. Penalidades — Art. 52

| Sanção | Detalhes |
|--------|----------|
| **Advertência** | Com prazo para adoção de medidas corretivas |
| **Multa simples** | Até 2% do faturamento (limitada a R$ 50 milhões por infração) |
| **Multa diária** | Limitada ao teto de R$ 50 milhões |
| **Publicização** | Da infração após apuração e confirmação |
| **Bloqueio** | Dos dados pessoais referentes à infração |
| **Eliminação** | Dos dados pessoais referentes à infração |
| **Suspensão parcial ou total** | Do funcionamento do banco de dados |
| **Proibição parcial ou total** | Da atividade de tratamento de dados |

## 8. Programa de Conformidade — Art. 50

1. Política de privacidade e segurança da informação (papel e digital)
2. Mapeamento completo de dados (Data Mapping)
3. Relatório de Impacto à Proteção de Dados (RIPD)
4. Plano de resposta a incidentes de segurança
5. Treinamento periódico de colaboradores
6. Nomeação do Encarregado (DPO) — obrigatório
7. Contratos com operadores (DPA — Data Processing Agreement)
8. Canal de atendimento ao titular em todas as interfaces
9. RIPD obrigatório para tratamentos de alto risco

## 9. Incidentes de Segurança

- **Comunicação à ANPD** em prazo razoável (boa prática: 72 horas)
- **Comunicação ao titular** quando risco ou dano relevante
- **Documentação completa** do incidente, impacto e medidas adotadas
- **RIPD** deve conter medidas preventivas e mitigatórias
- Manter **registro de todos os incidentes** para auditoria

## 10. LGPD vs GDPR — Comparativo

| Aspecto | LGPD | GDPR |
|---------|------|------|
| Abrangência territorial | Brasil | União Europeia |
| Quantidade de bases legais | 10 (Art. 7º) | 6 (Art. 6º) |
| Valor máximo da multa | R$ 50 milhões por infração | € 20 milhões ou 4% do faturamento global |
| DPO | Obrigatório | Obrigatório em casos específicos |
| Autoridade nacional | ANPD (única) | Autoridade por Estado-membro |
| Regulamentação setorial | Em desenvolvimento | Diretiva ePrivacy consolidada |

## 11. Regras para Sistemas e ERPs

1. Mapear todos os dados pessoais e sensíveis tratados
2. Definir base legal específica para cada finalidade
3. Implementar mecanismo para todos os 9 direitos do titular
4. Criptografar dados sensíveis em repouso e em trânsito
5. Aplicar controle de acesso baseado em função (RBAC)
6. Manter logs de auditoria imutáveis e com retenção mínima
7. Estabelecer política de retenção e eliminação por categoria de dado
8. Firmar DPA com todos os operadores e terceiros processadores
9. Disponibilizar canal de atendimento ao titular (digital prioritário)
10. Elaborar RIPD para tratamentos de alto risco
11. Realizar Privacy by Design em todo ciclo de desenvolvimento
12. Revisar conformidade periodicamente (mínimo anual)

## 12. Referências

- [Lei nº 13.709/2018 — LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Lei nº 13.853/2019 — ANPD](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13853.htm)
- [Autoridade Nacional de Proteção de Dados](https://www.gov.br/anpd/pt-br)
- [Guia Orientativo de Segurança da Informação — ANPD](https://www.gov.br/anpd/pt-br/assuntos/publicacoes)
