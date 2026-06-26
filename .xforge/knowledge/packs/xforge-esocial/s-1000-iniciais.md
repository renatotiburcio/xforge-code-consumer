---
title: "eSocial S-1000 Informacoes do Empregador"
summary: "Evento S-1000 inicial do eSocial, layout XML, classificacao tributaria, validacoes"
keywords: ["esocial", "s-1000", "empregador", "layout", "xml"]
trustScore: 82
lastValidated: 2026-06-13
id: knowledge-esocial-s1000
type: knowledge
---

# eSocial S-1000 Informacoes do Empregador

## O que e

O S-1000 e o **primeiro evento** a ser enviado ao eSocial. Define quem e o empregador/contribuinte. Sem ele, nenhum outro evento pode ser recebido.

## Eventos iniciais obrigatorios

- S-1000: Informacoes do Empregador (sempre)
- S-1005: Tabela de Estabelecimentos
- S-1010: Tabela de Rubricas
- S-1020: Tabela de Lotas
- S-1070: Tabela de Processos (judiciais/admin)

## Classificacao Tributaria (classTrib)

| Codigo | Tipo |
|--------|------|
| 01 | Empresa |
| 02 | Empregador Domestico |
| 03 | Entidade sem fins lucrativos |
| 04 | MEI |
| 06 | Microempresa (Simples) |
| 09 | Lucro Presumido |
| 10 | Lucro Real |
| 21 | Orgao Publico |

## Layout XML S-1000

```xml
<?xml version="1.0" encoding="UTF-8"?>
<eSocial xmlns="http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v02_05_00">
  <evtInfoEmpregador Id="ID1000000000000000000000001">
    <ideEvento>
      <tpAmb>1</tpAmb>
      <procEmi>1</procEmi>
      <verProc>1.0.0</verProc>
    </ideEvento>
    <ideEmpregador>
      <tpInsc>1</tpInsc>
      <nrInsc>12345678000199</nrInsc>
    </ideEmpregador>
    <infoEmpregador>
      <inclusao>
        <idePeriodo>
          <iniValid>2020-01</iniValid>
        </idePeriodo>
        <infoCadastro>
          <nmRazao>Empresa X LTDA</nmRazao>
          <classTrib>01</classTrib>
          <natJurid>2062</natJurid>
          <indConstr>0</indConstr>
          <indDesFolha>0</indDesFolha>
        </infoCadastro>
      </inclusao>
    </infoEmpregador>
  </evtInfoEmpregador>
</eSocial>
```

## Assinatura digital

Todos os XMLs do eSocial devem ser **assinados digitalmente** com certificado ICP-Brasil (A1 ou A3). Envelopados em lote:

```xml
<eSocial xmlns="http://www.esocial.gov.br/schema/lote/eventos/envio/v1.1.1">
  <ideEmpregador><tpInsc>1</tpInsc><nrInsc>12345678000199</nrInsc></ideEmpregador>
  <ideLote><nrLote>00001</nrLote><tpAmb>1</tpAmb></ideLote>
  <eventos>
    <evento Id="ID...">  <!-- XML assinado -->  </evento>
  </eventos>
</eSocial>
```

## Resposta do governo

| Codigo | Significado |
|--------|------------|
| 201 | Sucesso, evento processado |
| 202 | Recebido, em processamento |
| 301 | Erro de schema |
| 401 | Erro de regra de negocio |
| 501 | Certificado invalido |

## Retificacao

Para corrigir, enviar novo S-1000 com:

```xml
<indRetif>2</indRetif>
<nrRecibo>{recibo_original}</nrRecibo>
```

## Cuidados

- XSD atualizado frequentemente, sempre validar
- Manter protocolo para retificacao
- Eventos de tabela (S-10XX) tem prazo diferente de periodicos (S-12XX)
- Backup de XML por 5 anos (regulacao + LGPD)