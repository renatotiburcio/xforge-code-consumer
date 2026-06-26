---
id: tributos-ipi-iss
type: knowledge
tags: [tributos, ipi, iss, federal, municipal, industrial, servicos]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar o IPI (federal, industrial) e o ISS (municipal, serviços), suas alíquotas, bases de cálculo e obrigações.
- **Principais responsabilidades**: Explicar IPI: alíquotas por NCM, CSTs, não cumulatividade; Explicar ISS: alíquotas por município, lista de serviços, retenção; Cobrir obrigações ac...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, ipi, iss, federal, municipal, industrial, servicos
- **Restrições/Regras**: IPI: alíquotas definidas por decreto federal (TIPI); ISS: cada município define alíquota e regras próprias

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-ipi-iss` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# IPI e ISS — Imposto sobre Produtos Industrializados e Imposto sobre Serviços

## Purpose
Documentar o IPI (federal, industrial) e o ISS (municipal, serviços), suas alíquotas, bases de cálculo e obrigações.

## Responsibilities
- Explicar IPI: alíquotas por NCM, CSTs, não cumulatividade
- Explicar ISS: alíquotas por município, lista de serviços, retenção
- Cobrir obrigações acessórias de ambos

## Dependencies
- `regimes-tributarios.md` — enquadramento por regime
- `icms.md` — tributo estadual correlato
- `reforma-tributaria.md` — IPI→IS, ISS→IBS

## Conteúdo

### IPI — Imposto sobre Produtos Industrializados
**Competência**: Federal (CF, art. 153, IV)

#### Características
- Incide sobre produtos industrializados (nacionais e importados)
- **Não cumulativo**: crédito na entrada, débito na saída
- **Seletividade**: alíquotas variam conforme essencialidade
- Tabela de referência: **TIPI** (Decreto 7.212/2010)

#### Alíquotas
| Categoria | Alíquota |
|---|---|
| Produtos de primeira necessidade | 0-10% |
| Produtos intermediários | 10-20% |
| Produtos supérfluos | 20-30% |
| Cigarros e bebidas | Até 300% |
| Automóveis | 0-35% |

#### Base de Cálculo
```
Base = Valor da operação + Frete + Seguro + Despesas – Descontos incondicionais
```

#### Regimes Especiais
- **Drawback**: Suspensão/isenção na importação para exportação
- **ZFM**: Zona Franca de Manaus
- **REIDI**: Incentivo para infraestrutura
- **RECAP**: Bens de capital para exportadoras

#### Imunidades
Livros, jornais, produtos para exportação, ouro (ativo financeiro), energia elétrica, petróleo.

#### Obrigações
- **EFD ICMS/IPI** — Bloco E (registros E500-E531)
- Apuração mensal

### ISS — Imposto sobre Serviços
**Competência**: Municipal (CF, art. 156, III)

#### Características
- Incide sobre serviços da lista da **LC 116/2003**
- **Cumulativo**: sem crédito
- Alíquotas: **2% a 5%** (definida por cada município)

#### Serviços Típicos (LC 116/2003)
| Código | Serviço |
|---|---|
| 01.01-01.09 | Informática (análise, programação, SaaS, hospedagem) |
| 04.01-04.02 | Medicina, Odontologia |
| 07.01-07.02 | Advocacia, Contabilidade |
| 10.01-10.02 | Engenharia, Arquitetura |
| 17.01 | Assessoria de imprensa |
| 22.01 | Vigilância |

#### Base de Cálculo
```
Base = Preço do serviço – Deduções (materiais, subempreitada)
```

#### Retenção na Fonte
- Tomador responsável pelo recolhimento quando prestador é de outro município
- Alíquota: do município do tomador

#### NFS-e
- Substitui nota fiscal de serviço em papel
- Layout varia por município (padrão nacional em convergência)
- Transmissão via webservice

#### Regimes Especiais
Simples Nacional (ISS no DAS), Fixo (autônomos), Estimativa, Isenção municipal.

## Constraints
- IPI: alíquotas definidas por decreto federal (TIPI)
- ISS: cada município define alíquota e regras próprias
- Reforma Tributária: IPI→IS, ISS→IBS até 2033

## Related Documents
- `icms.md` — ICMS (estadual)
- `regimes-tributarios.md` — Regimes
- `reforma-tributaria.md` — Transição IBS/CBS/IS

