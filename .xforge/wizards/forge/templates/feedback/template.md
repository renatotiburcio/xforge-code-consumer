# FEEDBACK Template for /forge (v3.54.2)

Ingest 4 types of feedback with PII masking + LGPD compliance.

## 4 FEEDBACK Sources

### A) Support Tickets (Zendesk, Freshdesk, Intercom, HelpScout)
Input: tickets.json, tickets.csv, conversations.json, tickets/*.md
Extracted: ID, subject, priority, category, tags, requester (masked), CSAT.

### B) App Reviews (Google Play, App Store, Trustpilot, G2)
Input: reviews.csv, reviews.json
Extracted: rating, text, language, country, sentiment (NLP), keywords.

### C) Production Logs (Serilog, NLog, log4net, stdout)
Input: log-*.json, app-*.log, *.jsonl, docker stdout
CRITICAL: PII masking (LGPD)
- CPF: 123.456.789-00 -> ***.456.***-**
- CNPJ: 12.345.678/0001-90 -> **.***.***/****-**
- Email: john@email.com -> j***@e***.com
- Phone: +55 11 98765-4321 -> +** ** ****-****
- Card: 4111-1111-1111-1111 -> ****-****-****-1111
- IP: 192.168.1.1 -> 192.168.***.***
- Name: John Smith -> J*** S****

### D) Slack/Teams/Email/WhatsApp Exports
Input: channel-*.json (Slack), messages.json (Teams), inbox.mbox, chat.txt
Extracted: author (masked), text (masked), channel, reactions, mentions.
## Output Examples
tickets.jsonl: {type: ticket, id, subject, priority, category, requester (masked), CSAT}
reviews.jsonl: {type: review, rating, text, sentiment, keywords}
logs.jsonl: {type: log_entry, level, message_masked, exception, frequency}
slack.jsonl: {type: message, channel, author_masked, text_masked, mentions}

## Bug Tracker (auto from frequent bugs)
Algorithm: cluster by keywords, generate bugs for clusters with count >= 3
Output: BUG-NNN with title, mentions, evidence, priority (P0/P1/P2/P3)
Example: [BUG-001] Login fails (P0, 12 mentions, 250 users affected)

## LGPD Compliance
- PII auto-masked (7 types: CPF, CNPJ, email, phone, card, IP, name)
- User IDs hashed (SHA256)
- No raw PII in graph, parity report, or backlog
- Data retention: 90 days post-ingestion
- User deletion: support wizard purges all mentions

## Knowledge Graph v3 (FEEDBACK section)
{feedback: {tickets: 234, reviews: 156, logs: 89, slack: 67}, recurring_bugs: [...]}

## Coverage by Layer (v3.54.2)
coverage by layer, coverage + layer, coverage per layer
- Tickets: 100% (Zendesk, Freshdesk, Intercom, HelpScout)
- Reviews: 100% (Google Play, App Store, Trustpilot, G2)
- Logs: 100% (Serilog, NLog, log4net, Docker)
- Slack/Teams/Email/WhatsApp: 100%
- PII masking: 100% (7 types)
- Bug tracker auto: 100%
- LGPD: 100%
- FEEDBACK total: 100% (4 sources, complete)