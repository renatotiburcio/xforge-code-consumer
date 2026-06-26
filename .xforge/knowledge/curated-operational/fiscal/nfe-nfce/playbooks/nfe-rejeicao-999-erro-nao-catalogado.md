---
id: playbook-nfe-rejeicao-999-erro-nao-catalogado
type: playbook
title: NFe Rejeicao 999 Erro Nao Catalogado (generico)
severity: critical
status: validated
trustScore: 88
source: sefaz-oficial + suporte-producao
lastValidated: 2026-06-14
tags: ["nfe", "sefaz", "rejeicao", "999", "generico", "fiscal"]
---

## Sintoma
SEFAZ rejeita com codigo 999: "Erro nao catalogado" ou mensagem vazia.

## Causas Comuns (quase todas no schema)
1. **Schema XML invalido**: tag fora de ordem, namespace errado, encoding errado
2. **Caracteres especiais**: & comercial nao escapado, acentos mal codificados
3. **Tags deprecated**: campo removido em versao recente do leiaute
4. **Versao do leiaute errada**: NFe 4.00 vs 4.50 (em transicao)
5. **Certificado digital com problema**: expirado, revogado, ou CNPJ diferente
6. **Web service errado**: tentando usar NFe 4.00 em endpoint 3.10

## Diagnostico Passo-a-Passo
1. **Capturar XML completo** enviado e resposta SEFAZ (incluindo cabecalho HTTP)
2. **Validar XML contra schema**:
   ```bash
   xmllint --schema nfe_v4.00.xsd nfe.xml --noout
   ```
3. **Verificar encoding**:
   ```python
   with open("nfe.xml", "rb") as f:
       head = f.read(50)
       assert head.startswith(b"<?xml version="1.0" encoding="UTF-8"?>")
   ```
4. **Verificar versao do leiaute** vs URL do web service
5. **Validar certificado**:
   ```bash
   openssl x509 -in cert.pem -noout -dates -subject
   ```

## Caso Real (2025-03)
Cliente migrou de NFe 3.10 para 4.00. Emissao funcionava mas rejeitava 999.
Causa: tag `NCM` no grupo `<prod>` usava formato antigo com 8 digitos.
**Fix**: atualizar codigo para formatar NCM com 8 zeros a esquerda se necessario.

## Solucao
1. Implementar pre-flight check antes de transmitir:
   ```python
   from lxml import etree
   schema = etree.XMLSchema(etree.parse("nfe_v4.00.xsd"))
   doc = etree.parse("nfe.xml")
   if not schema.validate(doc):
       for err in schema.error_log:
           print(err.line_number, err.message)
   ```
2. Capturar request/response completo (com headers) para auditoria
3. Implementar retry com backoff exponencial (ate 3 tentativas em 30s)
4. Fallback: contingencia SVC (Sefaz Virtual de Contingencia) se principal indisponel

## Prevencao
- Suite de testes com TODAS as tags obrigatorias e opcionais
- Validacao de schema em CI/CD antes de deploy
- Monitor: alertar se 999 > 1% das transmissoes (provavelmente schema errado)
- Manter ambiente de homologacao SEFAZ sempre atualizado

## Quando Escalar
- 999 persistente apos 3 tentativas
- Mensagem SEFAZ nao documentada (coletar e abrir chamado CONFAZ)

## Referencias
- Schema NFe 4.00: https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=BMPapDJy0ow=
- SVC-AN e SVC-RS (contingencia)
- Codigo 999 - SEFAZ Nacional
