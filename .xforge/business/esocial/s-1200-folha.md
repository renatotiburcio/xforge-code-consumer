---
title: "eSocial S-1200 Remuneracao Mensal"
summary: "S-1200 folha de pagamento, rubricas, INSS/IRRF progressivo, prazos mensais"
keywords: ["esocial", "s-1200", "folha", "inss", "irrf", "rubricas"]
trustScore: 80
lastValidated: 2026-06-13
id: knowledge-esocial-s1200
type: knowledge
---

# eSocial S-1200 Remuneracao do Trabalhador

## S-1200

Evento **periodico mensal** com a remuneracao de cada trabalhador. Obrigatorio para todos os empregadores com celetistas.

## Prazos

| Tipo | Prazo |
|------|-------|
| Mensal | Dia 7 do mes seguinte |
| Adiantamento | Dia 15 do mes de competencia |
| 13o 1a parcela | 30 de novembro |
| 13o 2a parcela | 20 de dezembro |

## Rubricas principais

| Codigo | Descricao | Tipo |
|--------|-----------|------|
| 0001 | Salario Base | Base |
| 0002 | Hora Extra 50% | Base |
| 0003 | Hora Extra 100% | Base |
| 0050 | INSS | Desconto |
| 0051 | IRRF | Desconto |
| 0052 | Vale Transporte | Desconto |
| 0100 | FGTS | Info (8%) |
| 1000 | 13o Salario | Base |
| 1100 | Ferias + 1/3 | Base |
| 2000 | PLR | Base |

## INSS 2024 (progressivo)

| Faixa | Aliquota |
|-------|----------|
| Ate R$ 1.412,00 | 7.5% |
| 1.412,01 a 2.666,68 | 9% |
| 2.666,69 a 4.000,03 | 12% |
| 4.000,04 a 7.786,02 | 14% |

Teto INSS 2024: R$ 908.85

## IRRF 2024

| Faixa | Aliquota | Deducao |
|-------|----------|---------|
| Ate 2.259,20 | isento | - |
| 2.259,21 a 2.826,65 | 7.5% | 169.44 |
| 2.826,66 a 3.751,05 | 15% | 381.44 |
| 3.751,06 a 4.664,68 | 22.5% | 662.77 |
| Acima 4.664,68 | 27.5% | 896.00 |

Deducao por dependente: R$ 189.59

## Layout XML S-1200

```xml
<evtRemun Id="ID1200000000000000000000001">
  <ideEvento>
    <indRetif>1</indRetif>
    <indApuracao>1</indApuracao>
    <perApur>2024-12</perApur>
    <tpAmb>1</tpAmb>
    <procEmi>1</procEmi>
    <verProc>1.0</verProc>
  </ideEvento>
  <ideEmpregador>
    <tpInsc>1</tpInsc>
    <nrInsc>12345678000199</nrInsc>
  </ideEmpregador>
  <ideTrabalhador>
    <cpfTrab>12345678901</cpfTrab>
  </ideTrabalhador>
  <dmDev>
    <ideDmDev>
      <codCateg>101</codCateg>
    </ideDmDev>
    <infoPerApur>
      <ideEstab>
        <tpInsc>1</tpInsc>
        <nrInsc>12345678000199</nrInsc>
        <remunPerApur>
          <matricula>00001</matricula>
          <itensRemun>
            <rubrica>
              <codRubr>0001</codRubr>
              <ideTabRubr>01</ideTabRubr>
              <qtdRubr>30.00</qtdRubr>
              <vrRubr>5500.00</vrRubr>
            </rubrica>
          </itensRemun>
        </remunPerApur>
      </ideEstab>
    </infoPerApur>
  </dmDev>
</evtRemun>
```

## Retificacao

```xml
<indRetif>2</indRetif>
<nrRecibo>{recibo_original}</nrRecibo>
```

## Cuidados

- S-1200 NAO recalcula INSS/IRRF automaticamente, ERP deve fazer
- Validar totalizadores antes de enviar
- Multi-CNPJ precisa de S-1200 por cada estabelecimento
- S-1200 de rescisao: enviar S-2299 antes do S-1200