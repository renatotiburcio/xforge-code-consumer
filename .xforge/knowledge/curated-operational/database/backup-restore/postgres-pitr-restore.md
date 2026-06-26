---
id: playbook-db-restore-point-in-time
type: playbook
title: PostgreSQL Point-in-Time Recovery (PITR)
severity: critical
status: validated
trustScore: 92
source: operacao-real + postgresql-docs
lastValidated: 2026-06-14
tags: ["database", "postgresql", "backup", "pitr", "restore", "disaster-recovery"]
---

## Quando Usar
- DELETE/UPDATE acidental sem WHERE
- DROP TABLE acidental
- Corruption de dados
- Ransomware (restaurar de backup pre-ataque)
- Teste de DR

## Pre-requisitos
1. **WAL archiving ativo** (escrito continuamente para storage duravel)
   ```ini
   # postgresql.conf
   wal_level = replica
   archive_mode = on
   archive_command = "cp %p /mnt/wal_archive/%f"
   ```
2. **Base backup periodico** (pg_basebackup diario)
3. **Conhecimento do timestamp alvo** do restore

## Procedimento (PostgreSQL)

### 1. Parar aplicacao
```bash
systemctl stop xforge-app
```

### 2. Mover data directory atual
```bash
mv /var/lib/postgresql/data /var/lib/postgresql/data_corrupted_$(date +%Y%m%d_%H%M)
```

### 3. Restaurar base backup
```bash
# Init novo cluster
mkdir -p /var/lib/postgresql/data
chown postgres:postgres /var/lib/postgresql/data
sudo -u postgres /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/data

# Restore base backup
sudo -u postgres /usr/lib/postgresql/15/bin/pg_basebackup     -h backup-server -D /var/lib/postgresql/data -Fp -Xs -P
```

### 4. Configurar recovery
```ini
# postgresql.conf (no novo cluster)
restore_command = "cp /mnt/wal_archive/%f %p"
recovery_target_time = "2026-06-14 10:30:00"  # timestamp alvo
recovery_target_action = "promote"  # apos restaurar, virar primary
```

### 5. Criar recovery.signal
```bash
touch /var/lib/postgresql/data/recovery.signal
chown postgres:postgres /var/lib/postgresql/data/recovery.signal
```

### 6. Iniciar PostgreSQL (modo recovery)
```bash
sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data start
```

### 7. Acompanhar restore
```bash
# Logs do PostgreSQL devem mostrar:
# "restored log file ..."
# "recovery in progress"
# "database system is ready to accept read only connections" (durante recovery)
# "database system is ready to accept connections" (apos promote)
```

### 8. Validar dados
```sql
-- Verificar se dados estao corretos
SELECT COUNT(*) FROM clientes;
SELECT MAX(data_emissao) FROM nfe_cabecalho;

-- Conferir tabelas criticas
SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'public';
```

### 9. Re-aplicar transacoes perdidas (se necessario)
Se dados foram perdidos entre o PITR e o momento do incidente:
- Extrair do backup corrompido (que ainda esta em data_corrupted_*)
- Ou do log de aplicacao (audit trail)

### 10. Subir aplicacao
```bash
systemctl start xforge-app
```

## Validacao
1. Smoke tests da aplicacao
2. Conferir inventario (deve bater com timestamp alvo)
3. Verificar NFe autorizadas recentemente
4. Conferir saldo de estoque
5. Validar fluxo de caixa

## Caso Real (2024-11)
Dev rodou `DELETE FROM clientes WHERE id > 1000` em prod por engano.
Perdeu 2500 clientes (nao tinha backup mais recente).
**Com PITR** (que existia): restaurou em 35min, perdeu 0 clientes.
**Licao**: PITR + WAL archiving vale cada byte de storage.

## Backup Strategy Recomendada

| Tipo | Frequencia | Retencao | Storage |
|------|:----------:|:--------:|---------|
| **Base backup full** | diario | 30 dias | S3 standard |
| **WAL archive** | continuo | 7 dias | S3 standard |
| **Weekly full** | semanal | 12 semanas | S3 IA |
| **Monthly full** | mensal | 7 anos (fiscal) | S3 Glacier |
| **Annual snapshot** | anual | permanente | S3 Glacier Deep Archive |

## Custo Estimado
- DB 100GB: $10/mes S3 + $1/mes Glacier
- DB 1TB: $80/mes S3 + $8/mes Glacier
- DB 10TB: $800/mes S3 + $80/mes Glacier

## Testes Obrigatorios
- **Mensal**: restore de base backup + WAL replay (validar logs)
- **Trimestral**: PITR completo em staging
- **Anual**: DR drill (perda total simulada)

## Prevencao
- **Separacao de papeis**: DBA nao tem acesso SSH em prod (usa bastion)
- **Confirmacao dupla**: operacoes destrutivas exigem 2 pessoas
- **Read-only user por padrao**: app usa user com permissoes minimas
- **Audit log**: registrar todas DDL/DML
- **Soft delete**: nunca DELETE direto, sempre marcar deleted_at
- **Snapshots automaticos** antes de migrations

## Referencias
- PostgreSQL docs: Continuous Archiving and Point-in-Time Recovery
- AWS RDS: Automated Backups and Point-in-Time Restore
- pgBackRest: https://pgbackrest.org/
- WAL-G: https://github.com/wal-g/wal-g
- ADR-0024 XForge: Disaster Recovery Strategy
