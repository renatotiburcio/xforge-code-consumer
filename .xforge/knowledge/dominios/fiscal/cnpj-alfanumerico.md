---
id: cnpj-alfanumerico
type: conhecimento
tags: [fiscal, cnpj, alfanumerico, cadastro, 2026]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre CNPJ Alfanumérico
- **Seções principais**: Base Legal, Visão Geral, Formato, Diferenças
- **Tags**: fiscal, cnpj, alfanumerico, cadastro, 2026
- **Restrições/Regras**: CNPJ alfanumérico é o padrão; Número sequencial é gerado automaticamente

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `cnpj-alfanumerico` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 9 |


# CNPJ Alfanumérico

## Base Legal
- Lei 14.596/2023
- Portaria RFB nº 2.080/2024
- IN RFB nº 2.200/2024

## Visão Geral

O CNPJ alfanumérico é a nova identificação de pessoa jurídica no Brasil, substituindo o CNPJ numérico tradicional.

## Formato

### CNPJ Numérico (Atual/Legado)
```
XX.XXX.XXX/XXXX-XX
12 dígitos numéricos
Ex: 12.345.678/0001-90
```

### CNPJ Alfanumérico (Novo)
```
XX.XXX.XXX/XXXX-XX
12 caracteres alfanuméricos
Ex: 12.ABC.345/0001-9X
```

### Estrutura do CNPJ Alfanumérico
| Posição | Tamanho | Conteúdo |
|---------|:-------:|----------|
| 01-02 | 2 | UF (unidade federativa) |
| 03-05 | 3 | Código municipal |
| 06-08 | 3 | Sequencial |
| 09-12 | 4 | Ordem do estabelecimento |
| 13-14 | 2 | Dígitos verificadores |

### Caracteres Permitidos
- Números: 0-9
- Letras: A-Z (maiúsculas)
- **NÃO aceita:** I, O, Q (evitar confusão com 1, 0)

## Diferenças

| Aspecto | Numérico | Alfanumérico |
|---------|----------|-------------|
| Formato | 12 dígitos | 12 caracteres |
| Espaços | ~3,7 trilhões | ~3,6 quintilhões |
| Compatibilidade | Legado | Novo padrão |
| Validação | Módulo 11 | Módulo adaptado |

## Migração

### Quem pode usar
- Novas empresas: CNPJ alfanumérico obrigatório
- Empresas existentes: podem manter numérico ou migrar
- Órgãos públicos: devem aceitar ambos

### Prazos
| Data | Evento |
|------|--------|
| 15/10/2024 | Publicação da IN RFB 2.229 |
| 25/10/2024 | Entrada em vigor da IN |
| **Julho/2026** | **Implementação do novo modelo CNPJ alfanumérico** |
| 01/07/2026 | eSocial v.S-1.3 com suporte a CNPJ alfanumérico |
| 01/01/2027 | Órgãos públicos devem aceitar alfanumérico |
| 01/01/2028 | Migração facultativa para empresas existentes |
| 01/01/2030 | Migração obrigatória para todos |

### Processo de Migração
1. Acessar portal da Receita Federal
2. Solicitar migração
3. Novo CNPJ é gerado
4. Antigo permanece válido durante transição
5. Atualizar cadastros em todos os sistemas

## Validação

### Algoritmo de Validação
```python
def validate_cnpj_alpha(cnpj):
    # Remove formatação
    cnpj = re.sub(r'[^A-Z0-9]', '', cnpj.upper())
    
    if len(cnpj) != 14:
        return False
    
    # Verificar caracteres inválidos (I, O, Q)
    if any(c in cnpj for c in 'IOQ'):
        return False
    
    # Calcular dígitos verificadores
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Converter letras para valores
    valores = {}
    for i, c in enumerate('0123456789ABCDEFGHJKLMNPRTUVWXYZ'):
        valores[c] = i
    
    # Primeiro dígito verificador
    soma = sum(valores[c] * pesos1[i] for i, c in enumerate(cnpj[:12]))
    resto = soma % 31
    dv1 = 0 if resto < 2 else 31 - resto
    
    # Segundo dígito verificador
    soma = sum(valores[c] * pesos2[i] for i, c in enumerate(cnpj[:13]))
    soma += valores[chr(dv1 + ord('0'))] * 2
    resto = soma % 31
    dv2 = 0 if resto < 2 else 31 - resto
    
    return cnpj[12:] == chr(dv1 + ord('0')) + chr(dv2 + ord('0'))
```

### Validação em .NET
```csharp
public class CnpjAlphaValidator
{
    private const string ValidChars = "0123456789ABCDEFGHJKLMNPRTUVWXYZ";
    
    public bool Validate(string cnpj)
    {
        cnpj = Regex.Replace(cnpj.ToUpper(), @"[^A-Z0-9]", "");
        
        if (cnpj.Length != 14) return false;
        if (cnpj.Any(c => "IOQ".Contains(c))) return false;
        
        // Calcular DV1 e DV2...
        return true;
    }
}
```

## Impactos em Sistemas

### Cadastros
- Tabela de empresas: campo CNPJ deve aceitar 12 chars
- Validação: novo algoritmo
- Busca: índice alfanumérico
- Relatórios: formatação flexível

### NF-e / Documentos Fiscais
- CNPJ emitente: pode ser alfanumérico
- CNPJ destinatário: pode ser alfanumérico
- Validação SEFAZ: aceitar ambos
- XML: campo CNPJ expandido

### eSocial
- CNPJ da empresa: pode ser alfanumérico
- CNPJ do tomador: pode ser alfanumérico
- Validação: adaptada

### SPED
- EFD: campo CNPJ expandido
- ECD: campo CNPJ expandido
- ECF: campo CNPJ expandido

### Integrações Bancárias
- CNAB: campo CNPJ expandido
- PIX: chave CNPJ pode ser alfanumérico
- APIs bancárias: adaptadas

### Banco de Dados
```sql
-- Alteração de coluna
ALTER TABLE empresas 
ALTER COLUMN cnpj VARCHAR(14) NOT NULL;

-- Índice atualizado
CREATE INDEX idx_empresa_cnpj ON empresas(cnpj);
```

## Regras de Negócio

### Para Empresas Novas
- CNPJ alfanumérico é o padrão
- Número sequencial é gerado automaticamente
- UF + município determinam os primeiros dígitos

### Para Empresas Existentes
- CNPJ numérico continua válido até 2030
- Migração é facultativa até 2030
- Depois de migrado, o antigo é desativado

### Para Órgãos Públicos
- Devem aceitar ambos desde 01/01/2027
- Sistemas devem ser adaptados
- Validação flexível

## Fontes Oficiais
- Lei 14.596/2023
- Portaria RFB nº 2.080/2024
- IN RFB nº 2.200/2024
- Portal da Receita Federal
