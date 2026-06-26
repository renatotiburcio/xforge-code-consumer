---
id: playbook-nfe-rejeicao-297-cnpj-destinatario
type: playbook
title: NFe Rejeicao 297 CNPJ Destinatario Invalido
severity: high
status: validated
trustScore: 92
source: sefaz-oficial + operacao-real
lastValidated: 2026-06-14
tags: ["nfe", "sefaz", "rejeicao", "297", "cnpj", "fiscal"]
---

## Sintoma
SEFAZ rejeita NFe/NFCe com codigo 297: "CNPJ do destinatario invalido".

## Causas Comuns (em ordem de frequencia)
1. **CNPJ alfanumerico**: a partir de 2026, CNPJ pode ter letras. Validar formato novo (12 chars + 2 digitos + 0001)
2. **Digitos verificadores errados**: CNPJ matematicamente invalido
3. **CNPJ zerado ou com mascara**: `00.000.000/0000-00` ou `00000000000000`
4. **CNPJ de outro pais**: NFCe exige CNPJ/CPF ou `idEstrangeiro` (tag especifica)
5. **Destinatario ISENTO**: precisa tag `indIEDest=9` + dados do endereco completos

## Diagnostico
```sql
-- Validar CNPJ armazenado
SELECT cnpj FROM clientes WHERE id = :id;
-- Verificar tamanho (14 digitos) e digitos verificadores
```

```python
def validar_cnpj(cnpj: str) -> bool:
    cnpj = "".join(c for c in cnpj if c.isalnum())
    if len(cnpj) != 14: return False
    if cnpj == cnpj[0] * 14: return False  # rejeita 00000000000000
    # Validar digitos verificadores
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    d1 = sum(int(c) * p for c, p in zip(cnpj[:12], pesos1)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    d2 = sum(int(c) * p for c, p in zip(cnpj[:13], pesos2)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    return cnpj[12:14] == f"{d1}{d2}"
```

## Solucao
1. Aplicar validacao ANTES de transmitir
2. Atualizar base de clientes (corrigir CNPJ com DV errado)
3. Para estrangeiros: usar tag `idEstrangeiro` + indicador especifico
4. Para isentos: tag `indIEDest=9` + IE vazia

## Prevencao
- Validar CNPJ no momento do cadastro (cliente/fornecedor)
- Atualizar biblioteca de validacao para suportar CNPJ alfanumerico
- Job batch diario: detectar CNPJs invalidos antes de NFe ser emitida

## Referencias
- NT 2025.002 - CNPJ alfanumerico
- Manual de Orientacao do Contribuinte (MOC) 7.0
- SEFAZ - Tabela de Rejeicoes (codigo 297)
