---
id: esocial-trabalhadores
type: knowledge
tags: [esocial, trabalhador, cadastro, s2190, s3000, vinculo, tsve, cat, afastamento]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Eventos Cadastrais e Periódicos do Trabalhador no eSocial
- **Principais responsabilidades**: Enviar eventos cadastrais (S-2190 a S-2420) e TSVE (S-2300 a S-2399) dentro dos prazos legais.; Gerenciar eventos de afastamento (S-2230), CAT (S-2...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: esocial, trabalhador, cadastro, s2190, s3000, vinculo, tsve, cat, afastamento
- **Restrições/Regras**: **S-2190 deve ser enviado antes do S-2200** quando o trabalhador já está em atividade.; CPF e data de nascimento são ...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `esocial-trabalhadores` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Eventos Cadastrais e Periódicos do Trabalhador no eSocial

## Propósito
Documentar os eventos do trabalhador no eSocial, cobrindo todo o ciclo de vida: admissão, alterações, afastamentos, acidentes, saúde, condições ambientais e desligamento.

## Responsabilidades
- Enviar eventos cadastrais (S-2190 a S-2420) e TSVE (S-2300 a S-2399) dentro dos prazos legais.
- Gerenciar eventos de afastamento (S-2230), CAT (S-2210), saúde (S-2220), toxicológico (S-2221), condições ambientais (S-2240) e treinamentos (S-2245).
- Garantir a ordem de envio: S-2190 (pré-admissão) → S-2200 (cadastro) → demais eventos.
- Utilizar S-3000 para exclusão de eventos enviados indevidamente.

## Dependências
- Eventos de tabela do empregador (S-1000, S-1005, S-1010) devem estar cadastrados e ativos.
- Certificado digital e-CNPJ para transmissão.
- Leiaute S-1.3 do eSocial.

## Constraints
- **S-2190 deve ser enviado antes do S-2200** quando o trabalhador já está em atividade.
- CPF e data de nascimento são **imutáveis** no S-2205 (requer S-3000 + novo S-2200).
- CAT (S-2210) deve ser enviada até o 1º dia útil seguinte ao acidente (óbito: imediatamente).
- Afastamentos (S-2230) exigem envio de início e retorno.
- Prazo para eventos periódicos: até o dia 15 do mês seguinte.

## Conteúdo

### Grupo: Trabalhador com Vínculo (S-2190 a S-2420)

| Evento | Descrição | Prazo |
|--------|-----------|-------|
| S-2190 | Admissão — Ativo (pré-cadastro) | Antes de S-2200 |
| S-2200 | Cadastramento Inicial — Vínculo | Até 1 dia útil após início |
| S-2205 | Alteração Cadastral | Imediato |
| S-2206 | Alteração Contratual | Imediato |
| S-2210 | CAT — Acidente de Trabalho | 1º dia útil seguinte |
| S-2220 | Monitoramento da Saúde | Imediato |
| S-2221 | Exame Toxicológico (motorista) | Imediato |
| S-2230 | Afastamento Temporário | Imediato |
| S-2231 | Cessão/Exercício em Outro Órgão | Imediato |
| S-2240 | Condições Ambientais — Riscos | 1º dia útil seguinte |
| S-2245 | Treinamentos e Capacitações | 15 do mês seguinte |
| S-2250 | Aviso Prévio Trabalhado | Imediato |
| S-2298 | Reintegração | Imediato |
| S-2299 | Desligamento | 10 dias do desligamento |
| S-2400 a S-2420 | Benefícios Previdenciários (RPPS) | Conforme evento |

### Grupo: Trabalhador Sem Vínculo — TSVE (S-2300 a S-2399)

| Evento | Descrição |
|--------|-----------|
| S-2300 | TSVE — Início (estagiário, autônomo, diretor sem vínculo) |
| S-2305 | TSVE — Alteração Contratual |
| S-2306 | TSVE — Alteração Motória |
| S-2399 | TSVE — Término |

### Grupo: Exclusão (S-3000)
Permite excluir eventos enviados indevidamente. Deve referenciar o evento original pelo número do recibo.

### Eventos Cadastrais vs Periódicos
- **Cadastrais (não periódicos)**: Ocorrem conforme necessidade (admissão, alteração, desligamento, CAT, afastamento).
- **Periódicos**: Folha de pagamento (S-1200 a S-1299) — enviados mensalmente.

### CAT — Comunicação de Acidente de Trabalho (S-2210)
- **Tipos**: Típico (1), Doença ocupacional (2), Doença do trabalho (3), Trajeto (4).
- **Tipos de CAT**: Inicial (1), Reabertura (2), Óbito (3).
- **Iniciativa**: Empregador, sindicato, médico, DRT ou acidentado.
- **Não requer S-2200 prévio** — pode ser enviada independentemente.

### Afastamentos (S-2230)
- Mesmo evento para **início** (`iniAfastamento`) e **retorno** (`fimAfastamento`).
- Motivos principais: acidente/doença trabalho (00000001), doença não relacionada (00000003), licença-maternidade (00000006), licença-paternidade (00000008).
- Pagamento: empregador (1º ao 15º dia) → INSS (a partir do 16º dia para auxílio-doença).

### Categorias de Trabalhadores (codCateg — principais)
- 101: Empregado Geral (CLT)
- 103: Aprendiz
- 106: Trabalhador Temporário
- 111: Empregado Doméstico
- 301: Servidor Público Titular
- 308: Estagiário
- 721: Contribuinte Individual — Diretor
- 901: Bolsista

## Related Documents
- [esocial-empregador](esocial-empregadores.md) — Eventos de tabela do empregador
- [esocial-folha](esocial-folha.md) — Eventos de folha de pagamento
- [afastamentos](afastamentos.md) — Detalhamento de afastamentos e licenças
- [saude-trabalho](saude-trabalho.md) — PCMSO, PGR, LTCAT e SST
