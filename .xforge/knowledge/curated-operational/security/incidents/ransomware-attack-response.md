---
id: playbook-security-ransomware-response
type: playbook
title: Ransomware Attack - Contencao e Recuperacao
severity: critical
status: validated
trustScore: 95
source: incident-response-playbook + cisa-nist
lastValidated: 2026-06-14
tags: ["security", "ransomware", "incident", "contencao", "disaster-recovery"]
---

## Sintoma
- Arquivos com extensao estranha (.locked, .encrypted, .crypted)
- Nota de resgate em desktops (README_DECRYPT.txt, HOW_TO_RECOVER.html)
- Usuarios nao conseguem abrir arquivos criticos
- Atividade suspeita: muitos arquivos modificados em pouco tempo
- Antivrus alertando sobre processo desconhecido

## ACAO IMEDIATA (< 5 min) - CONTER

### 1. ISOLAR MAQUINAS AFETADAS
```bash
# Desconectar da rede (cabo + WiFi)
# Windows
netsh interface set interface "Ethernet" admin=disable
# Ou fisicamente

# Linux
sudo ip link set eth0 down

# NAO desligar (precisamos de memoria para forense)
```

### 2. NOTIFICAR EQUIPE
- Ligar para CISO / Security Lead
- Abrir war room (Slack #incident-XXXX, conf call)
- PagerDuty: severity=SEV1

### 3. PRESERVAR EVIDENCIA
- Tirar foto da tela (nota de resgate)
- Capturar processos rodando: `tasklist /v` ou `ps aux`
- NAO deletar nada
- NAO pagar resgate (FBI + maioria dos especialistas recomenda NAO pagar)

## AVALIAR ESCOPO (5-15 min)

### 1. Identificar ransomware variant
- Checar extensao dos arquivos
- Ler nota de resgate
- Buscar hash em https://www.nomoreransom.org/crypto-sheriff
- Identificar variante: LockBit, BlackCat, Conti, Akira, etc.

### 2. Identificar vetor de entrada
- Phishing email (checar mailbox)
- RDP exposto
- Software desatualizado (vulnerability conhecida)
- Credential comprometida (reutilizada, brute force)
- Supply chain (vendor comprometido)
- Insider threat (raro, mas possivel)

### 3. Listar sistemas afetados
- Scan rapido de todos endpoints
- Buscar por IOC (indicators of compromise)
- Identificar patient zero (primeira maquina infectada)

## CONTER PROPAGACAO (15-60 min)

### 1. Isolar segmento de rede
```bash
# Firewall rule: bloquear comunicacao entre segmentos
# Se VLAN disponivel: mover segmento afetado para quarentena

# Iptables (Linux)
sudo iptables -A INPUT -s 10.0.0.0/8 -j DROP
sudo iptables -A OUTPUT -d 10.0.0.0/8 -j DROP
```

### 2. Desabilitar contas comprometidas
- Azure AD / Okta: revoke sessions
- Domain controller: disable account
- VPN: kill active sessions

### 3. Desabilitar servicos nao-essenciais
- RDP, SMB, FTP (vetores comuns)
- Portas nao usadas
- API endpoints publicos (se nao criticos)

### 4. Bloquear C2 (Command & Control)
- Bloquear dominios/IPs conhecidos do ransomware
- Sinkhole DNS para dominios maliciosos
- EDR/XDR: kill processos maliciosos conhecidos

## INVESTIGAR (em paralelo)

### 1. Forense
- Disk image (bit-by-bit copy)
- Memory dump (antes de reiniciar)
- Logs de EDR/antivirus
- Network captures (se PCAP disponivel)

### 2. Identificar dados exfiltrados
- DNS queries anomalas (tunneling)
- HTTP POST para dominios externos
- Cloud storage access logs
- DLP (Data Loss Prevention) alerts

### 3. Cronologia
- Patient zero: quando entrou?
- Tempo ate primeira deteccao
- Tempo ate conter
- Quais dados foram acessados/modificados

## RECUPERAR (RTO 4-24h)

### 1. Decidir: pagar ou nao?
**NAO PAGAR** (recomendacao FBI/CISA):
- Nao ha garantia de recuperacao
- Financia criminosos
- Pode marcar empresa para re-ataque
- Multas regulatórias (LGPD + internacionais)

**EXCECAO**: vida em risco, dados criticos sem backup, custo de downtime > resgate

### 2. Restaurar de backup limpo
```bash
# Verificar backup (CRITICO: backup tambem pode ter sido infectado)
# 1. Restore em ambiente ISOLADO primeiro
# 2. Verificar hashes vs backup anterior
# 3. Scan antivirus do backup
# 4. So entao restaurar em producao
```

Seguir playbook `postgres-pitr-restore` para banco.

### 3. Rebuild do zero (recomendado para servidores)
- **NAO** confiar no OS da maquina afetada
- Format + reinstall OS
- Aplicar patches antes de conectar na rede
- Mudar TODAS senhas
- Re-emitir todos os tokens / API keys / certs

### 4. Validacao pos-restore
- Sistema funciona?
- Dados estao integros?
- Nenhum IOC permanece?
- Monitoring detectaria re-ataque?

## COMUNICAR (LGPD Obrigatorio)

### 1. ANPD (Autoridade Nacional)
- **Prazo**: 72h apos conhecimento (LGPD Art. 48)
- **Conteudo**: natureza do incidente, dados afetados, numero de pessoas, medidas tomadas
- Canal: https://www.gov.br/anpd/

### 2. Titulares (clientes afetados)
- Notificar individualmente se dados pessoais foram expostos
- Informar: quais dados, o que aconteceu, o que fazer
- Oferecer suporte (call center, FAQ)

### 3. Stakeholders
- Board / investidores
- Clientes corporativos (B2B)
- Imprensa (se for grande)
- Seguradoras (acionar apolice cyber)

## POST-MORTEM (ate 7 dias)

### 1. Root cause analysis
- Como entrou?
- Quanto tempo esteve la?
- O que faltou (monitoring, patch, treinamento)?

### 2. Action items
- Imediato: patches, reset credenciais
- 30 dias: implementar deteccao que faltou
- 90 dias: tabletop exercise, melhorar runbook
- Anual: red team engagement

### 3. Melhorias de seguranca
- MFA em TUDO (especialmente admin)
- Principio de menor privilegio
- Network segmentation
- Backup offline (air-gapped, ransomware nao alcança)
- EDR em 100% endpoints
- Treinamento phishing (simulacoes trimestrais)

## Caso Real (2024-08)
Empresa de manufatura, 200 funcionarios. Clique em phishing email.
LockBit ransomware se espalha via SMB em 4h.
150 endpoints criptografados, 3 servidores de arquivos, 1 banco de testes.
**Custo**: $2.3M (downtime, recuperacao, multa LGPD)
**Backup**: tinha, mas estava no mesmo network (tambem criptografado)
**Fix**: backup offline (tape mensal), EDR com deteccao de encrypt massivo, treinamento.

## Prevencao

### 1. 3-2-1 Backup
- 3 copias
- 2 midias diferentes
- 1 off-site AIR-GAPPED (nao na rede)

### 2. EDR (Endpoint Detection Response)
- CrowdStrike, SentinelOne, Microsoft Defender for Endpoint
- Detecta encrypt massivo de arquivos
- Auto-isolamento de endpoint

### 3. MFA + Least Privilege
- TUDO com MFA (nao so VPN)
- Service accounts: managed identities (Azure) ou IAM roles (AWS)
- Domain Admin: so 2-3 pessoas, just-in-time access

### 4. Network Segmentation
- VLANs separados por funcao (RH, Fiscal, Dev, Admin)
- Zero Trust: nenhum segmento confia em outro
- Lateral movement bloqueado

### 5. Patch Management
- Critical patches: 7 dias
- High: 30 dias
- Medium: 90 dias
- Vuln scan trimestral

### 6. Treinamento Phishing
- Simulacoes trimestrais (KnowBe4, GoPhish)
- Treinamento obrigatorio para quem clica
- Bonus/reconhecimento para quem reporta

## Referencias
- NIST Cybersecurity Framework
- CISA Stop Ransomware: https://www.cisa.gov/stopransomware
- No More Ransom: https://www.nomoreransom.org/
- LGPD Art. 48 - Comunicacao de incidente
- NIST SP 800-61 - Computer Security Incident Handling
- SANS PICERL: Preparation, Identification, Containment, Eradication, Recovery, Lessons
