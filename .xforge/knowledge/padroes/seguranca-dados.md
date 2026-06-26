---
id: seguranca-dados
type: padrao
tags: [seguranca, criptografia, backup, auditoria, lgpd, dados]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Definir padroes de seguranca de dados para proteger informacoes sensiveis em repouso, em transito e em processamento.
- **Principais responsabilidades**: Criptografar dados sensiveis em repouso e em transito; Hashing seguro de senhas; Backup criptografado e verificavel
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: seguranca, criptografia, backup, auditoria, lgpd, dados
- **Restrições/Regras**: Nunca armazenar senhas em texto claro; Nunca logar dados sensiveis (senhas, tokens, CPF completo)

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `seguranca-dados` |
| Tipo | padrao |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 12 |


# Seguranca de Dados — Criptografia, Backup e Auditoria

## Purpose
Definir padroes de seguranca de dados para proteger informacoes sensiveis em repouso, em transito e em processamento.

## Responsibilities
- Criptografar dados sensiveis em repouso e em transito
- Hashing seguro de senhas
- Backup criptografado e verificavel
- Trilha de auditoria imutavel
- Conformidade com LGPD

## Dependencies
- `compliance/lgpd.md` — Requisitos LGPD
- `padroes/seguranca-api.md` — Seguranca de API
- `padroes/certificacao-digital.md` — Certificacoes digitais

## Constraints
- Nunca armazenar senhas em texto claro
- Nunca logar dados sensiveis (senhas, tokens, CPF completo)
- Dados criptografados devem usar algoritmos padrao (AES-256, Argon2id)
- Backup deve ser testado periodicamente (restore testing)

## Criptografia em Repouso

### Always Encrypted (SQL Server)
Protege dados sensiveis em repouso e em transito entre aplicacao e banco. O SQL Server nunca ve os dados em texto claro.

| Tipo | Descricao | Caso de Uso |
|------|-----------|-------------|
| Deterministico | Mesmo texto plano = mesmo texto cifrado | Buscas exatas (=), JOINs |
| Aleatorio | Mesmo texto plano = texto cifrado diferente | Dados sem busca (senhas, notas) |

```sql
CREATE COLUMN MASTER KEY [CMK_Azure]
WITH (KEY_STORE_PROVIDER_NAME = ''AZURE_KEY_VAULT'',
      KEY_PATH = ''https://<vault>.vault.azure.net/keys/CMK/abc123'');

CREATE COLUMN ENCRYPTION KEY [CEK_Clientes]
WITH VALUES (COLUMN_MASTER_KEY = [CMK_Azure],
             ALGORITHM = ''RSA_OAEP'',
             ENCRYPTED_VALUE = 0x016E000001...);
```

### TDE (Transparent Data Encryption)
Criptografa o banco inteiro em nivel de arquivo. Transparente para a aplicacao.
```sql
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE [TDE_Certificate];
ALTER DATABASE [ErpDb] SET ENCRYPTION ON;
```

### AES-256 para Arquivos
```csharp
public class AesEncryptionService {
    public async Task EncryptFileAsync(string inputPath, string outputPath, byte[] key) {
        using var aes = Aes.Create(); aes.KeySize = 256; aes.Key = key;
        aes.GenerateIV();
        using var output = new FileStream(outputPath, FileMode.Create);
        await output.WriteAsync(aes.IV, 0, aes.IV.Length);
        using var crypto = new CryptoStream(output, aes.CreateEncryptor(), CryptoStreamMode.Write);
        using var input = File.OpenRead(inputPath);
        await input.CopyToAsync(crypto);
    }
}
```

## Hashing de Senhas

### Algoritmos Recomendados (OWASP 2024)
| Algoritmo | Iteracoes | Memory | Uso |
|-----------|-----------|--------|-----|
| Argon2id | 3+ | 64MB+ | Recomendado |
| scrypt | N=32768 | 64MB+ | Alternativa |
| bcrypt | 2^12 rounds | 4KB | Legado |
| PBKDF2 | 600.000+ | — | Minimo OWASP 2024 |

```csharp
// Argon2id
public static string HashPassword(string password) {
    var salt = RandomNumberGenerator.GetBytes(16);
    var argon = new Argon2id(Encoding.UTF8.GetBytes(password)) {
        Salt = salt, Iterations = 3, MemorySize = 65536, DegreeOfParallelism = 4
    };
    return Convert.ToBase64String(argon.GetBytes(32));
}

// PBKDF2 (minimo OWASP 2024)
public static string HashPasswordPbkdf2(string password) {
    var salt = RandomNumberGenerator.GetBytes(16);
    var hash = Rfc2898DeriveBytes.Pbkdf2(password, salt, 600_000, HashAlgorithmName.SHA256, 32);
    return Convert.ToBase64String(salt) + "|" + Convert.ToBase64String(hash);
}
```

### Salt + Pepper
```csharp
private static readonly string Pepper = Configuration["Security:Pepper"];
public static string HashWithPepper(string password) {
    var salt = RandomNumberGenerator.GetBytes(16);
    var combined = Encoding.UTF8.GetBytes(password + Pepper);
    var hash = Rfc2898DeriveBytes.Pbkdf2(combined, salt, 600_000, HashAlgorithmName.SHA256, 32);
    return $"{Convert.ToBase64String(salt)}|{Convert.ToBase64String(hash)}";
}
```

## Data Masking
| Dado | Mascara |
|------|---------|
| CPF | ***.***.456-** |
| CNPJ | **.***.***/0001-** |
| Email | jo**@***.com |
| Salario | R$ ****.** |
| Cartao | ****-****-****-1234 |
| Telefone | (**) 9****-** |

## Backup e Recovery

### Estrategia Full + Differential + Log
| Tipo | Frequencia | Retencao | Descricao |
|------|------------|----------|-----------|
| Full | Semanal (domingo) | 4 semanas | Banco completo |
| Differential | Diaria | 7 dias | Alteracoes desde ultimo Full |
| Log | A cada 15 min | 48h | Transacoes continuas |

### RPO e RTO
| Indicador | Descricao | Meta Tipica |
|-----------|-----------|-------------|
| RPO (Recovery Point Objective) | Quantidade de dados que pode perder | 15 minutos |
| RTO (Recovery Time Objective) | Tempo para restaurar operacao | 1 hora |

### Backup Criptografado
```sql
BACKUP DATABASE [ErpDb]
TO URL = ''https://<storage>.blob.core.windows.net/backups/erp_20260609.bak''
WITH FORMAT, COMPRESSION,
     ENCRYPTION (ALGORITHM = AES_256,
                 SERVER CERTIFICATE = [BackupCert]);
```

### Verificacao de Backup
```csharp
// Job que testa restore semanalmente
public class BackupVerificationJob {
    public async Task VerifyAsync(string backupPath) {
        // 1. Restore para banco temporario
        // 2. DBCC CHECKDB para integridade
        // 3. Consulta de amostra para validar dados
        // 4. Limpa banco temporario
        // 5. Envia relatorio de sucesso/falha
    }
}
```

## Auditoria e Trilha de Auditoria

### Tabela de Auditoria
```sql
CREATE TABLE AuditLog (
    Id BIGINT IDENTITY PRIMARY KEY,
    TableName NVARCHAR(200) NOT NULL,
    Action NVARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
    RecordId NVARCHAR(100) NOT NULL,
    OldValues NVARCHAR(MAX),
    NewValues NVARCHAR(MAX),
    ChangedBy NVARCHAR(200) NOT NULL,
    ChangedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CorrelationId NVARCHAR(100),
    IPAddress NVARCHAR(50),
    TenantId UNIQUEIDENTIFIER
);
```

### Interceptor Pattern (EF Core)
```csharp
public class AuditInterceptor : SaveChangesInterceptor {
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData, InterceptionResult<int> result, CancellationToken ct = default) {
        foreach (var entry in eventData.Context.ChangeTracker.Entries()) {
            if (entry.State == EntityState.Modified || entry.State == EntityState.Added) {
                // Registrar mudanca na tabela de auditoria
            }
        }
        return base.SavingChangesAsync(eventData, result, ct);
    }
}
```

## Secret Management
- **Nunca** hardcodear connection strings, secrets ou chaves
- **Desenvolvimento:** User Secrets (`dotnet user-secrets`)
- **Producao:** Azure Key Vault / AWS Secrets Manager
- **Rotacao:** automatizar rotacao de chaves periodicamente

```csharp
builder.Configuration.AddAzureKeyVault(
    new Uri("https://<vault>.vault.azure.net/"),
    new DefaultAzureCredential());
```

## Incidentes de Seguranca (LGPD)
- Comunicar a ANPD em prazo razoavel (recomendado: 72h)
- Comunicar o titular se risco ou dano relevante
- Documentar incidente e medidas adotadas
- Manter RIPD (Relatorio de Impacto a Protecao de Dados)

## Related Documents
- `compliance/lgpd.md` — Lei Geral de Protecao de Dados
- `padroes/seguranca-api.md` — Seguranca de API
- `padroes/certificacao-digital.md` — Certificacao Digital
