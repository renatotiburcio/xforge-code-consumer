---
id: tributos-cnpj-alfanumerico
type: knowledge
tags: [tributos, cnpj, alfanumerico, receita-federal, identificacao]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar a nova estrutura alfanumérica do CNPJ, seu formato, regras de validação e impacto em sistemas.
- **Principais responsabilidades**: Explicar o novo formato alfanumérico do CNPJ; Detalhar regras de validação e algoritmo de dígito verificador; Cobrir cronograma de migração e impac...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, cnpj, alfanumerico, receita-federal, identificacao
- **Restrições/Regras**: Algoritmo exato definido pela IN RFB 2.259/2025; Coexistência de formatos durante transição (2026-2028)

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-cnpj-alfanumerico` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# CNPJ Alfanumérico — Nova Estrutura a partir de 2026

## Purpose
Documentar a nova estrutura alfanumérica do CNPJ, seu formato, regras de validação e impacto em sistemas.

## Responsibilities
- Explicar o novo formato alfanumérico do CNPJ
- Detalhar regras de validação e algoritmo de dígito verificador
- Cobrir cronograma de migração e impacto em sistemas

## Dependencies
- `regimes-tributarios.md` — identificação de empresas por regime
- Nenhuma dependência externa obrigatória

## Conteúdo

### Conceito
O CNPJ Alfanumérico é a nova estrutura de identificação de pessoas jurídicas, implementada pela Receita Federal (IN RFB 2.259/2025). Substitui o formato puramente numérico por um formato alfanumérico de 14 caracteres.

### Formato Atual vs. Novo
```
Atual:  XX.XXX.XXX/XXXX-XX  (14 dígitos numéricos)
Novo:   XX.XXX.XXX/XXXX-XX  (14 caracteres alfanuméricos)
Exemplo: 1A.234.567/0001-8B
```

### Estrutura
| Posição | Tipo | Descrição |
|---|---|---|
| 1-2 | Alfanumérico | Raiz |
| 3-5 | Numérico | Estabelecimento |
| 6-8 | Numérico | Estabelecimento |
| 9-12 | Numérico | Filial |
| 13-14 | Alfanumérico | Dígito verificador |

### Regras de Validação
- Caracteres permitidos: 0-9 e A-Z (exceto I, O, Q para evitar confusão)
- Case insensitive: maiúsculas e minúsculas equivalentes
- Dígitos verificadores calculados com algoritmo específico (módulo 11)
- Letras convertidas para valores numéricos (A=10, B=11, ..., Z=35)

### Cronograma
| Fase | Período | Descrição |
|---|---|---|
| Publicação IN | 15/10/2024 | IN RFB 2.229 publicada |
| Vigência IN | 25/10/2024 | IN entra em vigor |
| **1** | **Julho/2026** | **Implementação do novo modelo (novo CNPJ)** |
| eSocial | 01/07/2026 | eSocial v.S-1.3 com suporte alfanumérico |
| 2 | 2026-2028 | Coexistência de formatos |
| 3 | 2028+ | CNPJ alfanumérico como padrão |

### Impacto para ERPs
1. **Validação**: Atualizar validadores para aceitar letras
2. **Banco de Dados**: Usar VARCHAR (nunca INTEGER)
3. **Formatação**: Máscaras de input devem aceitar letras
4. **APIs**: Validar CNPJ alfanumérico em integrações
5. **Integração**: NF-e, NFS-e, eSocial, SPED — todos devem aceitar o novo formato
6. **Migração**: CNPJs existentes continuam válidos (não precisam ser alterados)

### Regras para Desenvolvedores
- Nunca assumir que CNPJ é apenas numérico
- Usar VARCHAR para armazenar CNPJ
- Validar com algoritmo alfanumérico
- Aceitar ambos os formatos durante transição
- Atualizar máscaras de input

### Consulta e Dados Públicos
- **Comprovante**: servicos.receita.fazenda.gov.br/Servicos/cnpjreva
- **Dados abertos**: dados.gov.br (CSV/JSON)
- **API**: Disponível via dados abertos

## Constraints
- Algoritmo exato definido pela IN RFB 2.259/2025
- Coexistência de formatos durante transição (2026-2028)

## Related Documents
- `regimes-tributarios.md` — Identificação de empresas por regime

