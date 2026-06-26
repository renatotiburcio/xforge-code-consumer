---
id: reinf-completo
type: conhecimento
tags: [reinf, contribuicao-previdenciaria, servicos-tomados, servicos-prestados, produtor-rural]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre REINF - Regime Especial de Tributação
- **Seções principais**: Base Legal, Conceito, Eventos, Serviços Tomados (R-2010)
- **Tags**: reinf, contribuicao-previdenciaria, servicos-tomados, servicos-prestados, produtor-rural
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `reinf-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# REINF - Regime Especial de Tributação

## Base Legal
- Lei 12.546/2011
- Lei 13.846/2019
- Portaria Conjunta RFB/ME nº 10/2020

## Conceito

O REINF é o sistema que substitui a GFIP para declarar contribuições previdenciárias sobre receitas de prestação de serviços, retenções na fonte e produção rural.

## Eventos

### Eventos Não Periódicos

| Evento | Descrição | Prazo |
|--------|-----------|-------|
| R-1000 | Informações do Contribuinte | Antes do 1º evento |
| R-1070 | Tabelas de Processos Administrativos | Antes do 1º evento |

### Eventos Periódicos

| Evento | Descrição | Prazo |
|--------|-----------|-------|
| R-2010 | Serviços Tomados | Dia 15 do mês seguinte |
| R-2020 | Serviços Prestados | Dia 15 do mês seguinte |
| R-2030 | Produção Rural | Dia 15 do mês seguinte |
| R-2040 | Associação Desportiva | Dia 15 do mês seguinte |
| R-2060 | Contribuição Previdenciária sobre Receita Bruta | Dia 15 do mês seguinte |
| R-2098 | Ajuste Anual | Até dia 15 de janeiro |
| R-2099 | Fechamento dos Eventos Periódicos | Dia 15 do mês seguinte |
| R-3000 | Comunicação de Falecimento | Até 1 dia útil |
| R-5001 | Informações Consolidadas | Dia 15 do mês seguinte |

## Serviços Tomados (R-2010)

### Quando Declarar
- Retenção de INSS em serviços tomados
- Serviços com incidência de CPB (Contribuição Previdenciária sobre Receita Bruta)
- Tomadores de serviços de Pessoas Jurídicas

### Dados Declarados
| Campo | Descrição |
|-------|-----------|
| CNPJ Tomador | CNPJ do tomador |
| CNPJ Prestador | CNPJ do prestador |
| Valor Serviços | Valor total dos serviços |
| Base Cálculo | Base para incidência |
| Alíquota | Alíquota aplicável |
| Valor Retido | Valor retido na fonte |

## Serviços Prestados (R-2020)

### Quando Declarar
- Prestadores de serviços com retenção de INSS
- Serviços com incidência de CPB

### Dados Declarados
| Campo | Descrição |
|-------|-----------|
| CNPJ Prestador | CNPJ do prestador |
| CNPJ Tomador | CNPJ do tomador |
| Valor Serviços | Valor total dos serviços |
| Valor Retido | Valor retido pelo tomador |

## Contribuição Previdenciária sobre Receita Bruta (R-2060)

### Alíquotas por Atividade

| Atividade | Alíquota |
|-----------|:--------:|
| Comércio | 0,45% |
| Indústria | 0,45% |
| Serviços em geral | 0,45% |
| Construção civil | 1,5% |
| Extração de petróleo | 1,5% |

### Cálculo
```
CPB = Receita Bruta × Alíquota
```

### Exemplo
- Receita bruta mensal: R$ 500.000 (comércio)
- Alíquota: 0,45%
- CPB: R$ 500.000 × 0,45% = **R$ 2.250,00**

## Produção Rural (R-2030)

### Quando Declarar
- Produtores rurais com receita bruta
- Cooperativas rurais

### Dados Declarados
| Campo | Descrição |
|-------|-----------|
| CNPJ Produtor | CNPJ do produtor rural |
| Receita Bruta | Receita bruta da produção |
| Alíquota | Alíquota aplicável (1,2% ou 2,25%) |

## Fechamento

### R-2099 (Fechamento Periódico)
- Deve ser transmitido após todos os eventos periódicos do mês
- Confirma que todos os dados foram informados
- Necessário para apuração da contribuição

### R-2098 (Ajuste Anual)
- Transmitido em janeiro
- Ajusta diferenças do ano anterior
- Permite complementar informações

## Transmissão

### Certificado Digital
- Obrigatório certificado A1 ou A3
- e-CNPJ para empresas
- e-CPF para PF

### Web Services
| Ambiente | URL |
|----------|-----|
| Produção | https://www3.esocial.gov.br/servicos/employer |
| Homologação | https://homologacao.esocial.gov.br/servicos/employer |

### Processo
1. Gerar arquivo do evento
2. Assinar com certificado digital
3. Transmitir via web service
4. Aguardar retorno
5. Processar erros se houver

## Integração com Folha

### Dados Necessários
- Retenções de INSS sobre serviços
- Receita bruta por atividade
- Alíquotas aplicáveis

### Cálculo Mensal
```
1. Apurar retenções de INSS
2. Calcular CPB sobre receita bruta
3. Gerar eventos R-2010, R-2020, R-2060
4. Fechar período (R-2099)
5. Transmitir
```

## Penalidades

| Infração | Multa |
|----------|-------|
| Atraso na entrega | R$ 20,00 por dia |
| Omissão de informações | 2% sobre o valor da operação |
| Informações incorretas | Multa variável |
| Não entrega | Multa mínima de R$ 200,00 |

## Fontes Oficiais
- Lei 12.546/2011
- Lei 13.846/2019
- Portal eSocial (esocial.gov.br)
- RFB (receita.fazenda.gov.br)
