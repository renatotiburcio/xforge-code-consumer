---
id: knowledge-compliance-data-classification
type: knowledge
title: Classificacao de Dados (LGPD)
category: compliance
domain: compliance
trustScore: 88
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [lgpd, classification, data, sensitive, pii]
---

# Classificacao de Dados (LGPD)

## Categorias (LGPD)

### 1. Dados pessoais comuns

Informacoes que identificam ou tornam identificavel uma pessoa natural.

Exemplos: nome, CPF, RG, endereco, telefone, email, data de nascimento, estado civil.

### 2. Dados pessoais sensiveis (Art. 5 II)

Informacoes sobre origem racial/etnica, conviccao religiosa, opiniao politica,
filiacao a sindicato, dados referentes a saude ou vida sexual, dados biometricos
ou geneticos.

Exemplos: tipo sanguineo, prontuario medico, orientacao sexual, biometria facial.

### 3. Dados de criancas e adolescentes (Art. 14)

Tratamento sempre com consentimento especifico dos pais ou responsaveis.

## Classificacao interna XForge (5 niveis)

| Nivel | Tipo | Exemplos | Criptografia | Acesso |
|-------|------|----------|--------------|--------|
| L1 - Publico | Nenhuma | Marketing, termos | N/A | Todos |
| L2 - Interno | Nao-pessoal | Metricas, logs tecnicos | Em transito | Funcionarios |
| L3 - Pessoal | Dado pessoal comum | Nome, CPF, endereco | At rest + in transit | RBAC + audit |
| L4 - Sensivel | Dado pessoal sensivel | Saude, biometria | At rest + in transit + colunar | RBAC + MFA + audit |
| L5 - Regulamentado | Dados sob regulacao especifica | Dados bancarios, cripto, fiscais | HSM + FIPS 140-2 | Dual control + audit |

## Regras por nivel

### L1 - Publico

- Sem restricao
- Pode ser cacheado em CDN

### L2 - Interno

- Sem criptografia em repouso (mas em transito)
- Acesso por IP da empresa
- Retencao 1 ano

### L3 - Pessoal (LGPD)

- Criptografia AES-256 at rest
- TLS 1.3 in transit
- Audit trail de todo acesso
- Retencao conforme tabela de retencao
- Direito titular: acesso, correcao, exclusao

### L4 - Sensivel (LGPD Art. 5 II)

- Criptografia AES-256 + colunar encryption
- TLS 1.3 in transit
- Audit trail com justification
- MFA obrigatorio para acesso
- Retencao minima necessaria
- Direito titular: bloqueio, eliminacao

### L5 - Regulamentado

- HSM para chaves criticas
- FIPS 140-2 compliant
- Dual control (2 pessoas) para acesso
- Audit trail imutavel (WORM)
- Retencao 5-30 anos conforme legislacao
- Compliance especifico: BACEN, CVM, ANPD

## Implementacao tecnica

### Criptografia em colunas (PostgreSQL)

```sql
CREATE TABLE patient_record (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    blood_type BYTEA NOT NULL,
    diagnosis TEXT
);

-- Insert com criptografia
INSERT INTO patient_record (name, blood_type, diagnosis)
VALUES (
    $1,
    pgp_sym_encrypt($2, current_setting("app.l4_key")),
    pgp_sym_encrypt($3, current_setting("app.l4_key"))
);
```

## Mapeamento de campos comuns

| Campo | Classificacao | Justificativa |
|-------|---------------|---------------|
| Nome completo | L3 | Identifica pessoa |
| CPF/CNPJ | L3 | Identifica pessoa |
| Email | L3 | Identifica pessoa |
| Telefone | L3 | Identifica pessoa |
| Endereco | L3 | Localizacao |
| Data nascimento | L3 | Identifica pessoa |
| Salario | L3 (se vinculado) | Dado pessoal |
| Tipo sanguineo | L4 | Saude |
| Diagnostico | L4 | Saude |
| Biometria | L4 | Biometrico |
| Religiao | L4 | Conviccao religiosa |
| Opiniao politica | L4 | Opiniao politica |
| Dados bancarios | L5 | Financeiro regulado |
| Chave PIX | L5 | Financeiro regulado |

## Referencias

- LGPD Art. 5, 11, 14
- GDPR Art. 4, 9, 22
- BACEN Circular 3.909/2018 (dados financeiros)
- ISO 27001 A.8 (asset classification)
- NIST SP 800-60 (security categorization)

