---
id: renda-fixa
type: knowledge
tags: [renda-fixa, cdb, lci, tesouro-direto]
owner: investments-team
version: "1.0"
updated: "2026-06-13"
---
# Renda Fixa

## Indexadores
- **CDI** (Certificado de Deposito Interbancario): taxa over, base para ~90% dos produtos
- **IPCA**: indice de precos, protecao contra inflacao
- **Prefixado**: taxa fixa no momento da aplicacao
- **TR** (Taxa Referencial): praticamente extinta para pessoa fisica
- **IGPM**: indice geral de precos de mercado

## Produtos principais

### CDB (Certificado de Deposito Bancario)
- Emissor: bancos
- Cobertura: FGC ate R$ 250k por CPF por instituicao
- Liquidez: pode ter carencia ou ser diario
- Tributacao IR regressiva: 22.5% (ate 180d) a 15% (>720d)

### LCI / LCA (Letras de Credito Imobiliario / Agronegocio)
- Cobertura: FGC
- **Isencao de IR para pessoa fisica**
- Carencia minima: 90 dias

### Tesouro Direto
- Emissor: Tesouro Nacional
- Custodia: B3
- Opcoes: Selic, IPCA+, Prefixado, Prefixado com Juros Semestrais
- Marcar a mercado: sim (exceto na data de vencimento)
- Tributacao: IR regressivo (mesma tabela CDB)

### Debentures
- Emissor: empresas SA
- Incentivadas (infra): isencao de IR
- Convencionais: IR regressivo
- Risco: credito da empresa (analisar rating)

## Calculo de rentabilidade
```
Bruto = Principal * (1 + Taxa * dias/252)
Liquido = Bruto * (1 - IR)
Liquido Diario = (Liquido / Principal) ^ (252/dias) - 1
Equivalente CDI = Taxa * (252/dias) / CDI_diario
```