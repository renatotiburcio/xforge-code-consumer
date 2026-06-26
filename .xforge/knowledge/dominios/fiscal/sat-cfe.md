---
id: sat-cfe
type: knowledge
tags: [fiscal, sat, cfe, cupom-fiscal, sao-paulo, sefaz-sp]
owner: fiscal-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar o Sistema de Autenticação e Transmissão de Cupom Fiscal Eletrônico (SAT) do estado de São Paulo, que gera ...
- **Principais responsabilidades**: Definir o layout XML do CF-e (versão 0.07); Documentar equipamento SAT, ativação e estados; Cobrir transmissão, cancelamento e integração com PDV
- **Seções principais**: Purpose, Responsibilities, Dependencies, Constraints
- **Tags**: fiscal, sat, cfe, cupom-fiscal, sao-paulo, sefaz-sp
- **Restrições/Regras**: Uso exclusivo no estado de São Paulo; Transmissão online obrigatória (não funciona offline)

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `sat-cfe` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | fiscal-team |
| Total de seções | 13 |


# SAT/CF-e — Cupom Fiscal Eletrônico (São Paulo)

## Purpose
Documentar o Sistema de Autenticação e Transmissão de Cupom Fiscal Eletrônico (SAT) do estado de São Paulo, que gera o CF-e (Cupom Fiscal Eletrônico, modelo 59) como alternativa ao ECF tradicional.

## Responsibilities
- Definir o layout XML do CF-e (versão 0.07)
- Documentar equipamento SAT, ativação e estados
- Cobrir transmissão, cancelamento e integração com PDV
- Explicar comunicação Aplicativo Comercial ↔ SAT via DLL

## Dependencies
- Equipamento SAT homologado (Bematech, Dimep, Elgin, Tanca, Gertech, Sweda, Nitere)
- Código de ativação (mínimo 8 caracteres)
- DLL do fabricante para comunicação
- Conexão com internet (transmissão em tempo real)

## Constraints
- Uso exclusivo no estado de São Paulo
- Transmissão online obrigatória (não funciona offline)
- Cancelamento: até 30 minutos após emissão
- Assinatura digital pelo equipamento SAT (SHA-1 + RSA 2048 bits)

## Conceito
O SAT substitui os ECFs (Emissores de Cupom Fiscal) baseados em hardware lacrado. O equipamento SAT armazena o certificado digital, assina os XMLs e transmite para a SEFAZ-SP em tempo real. O CF-e é o documento XML resultante.

## Equipamento SAT
- Hardware dedicado com certificado digital embutido
- Ativação via Aplicativo Comercial (CNPJ contribuinte + CNPJ softwarehouse)
- Gera par de chaves RSA 2048 bits
- Estados: 0=DESBLOQUEADO, 1=BLOQUEADO_SEFAZ, 2=BLOQUEADO_CONTRIBUINTE, 3=BLOQUEADO_AUTONOMO, 4=BLOQUEADO_PARA_DESATIVACAO

## Layout XML CF-e
- **ide**: cUF(35), cNF, mod(59), nserieSAT, nCFe, dEmi, hEmi, cDV, tpAmb, CNPJ(softwarehouse), signAC, assinaturaQRCODE, numeroCaixa
- **emit**: CNPJ, xNome, xFant, enderEmit, IE, IM, cRegTribISSQN, indRatISSQN
- **dest**: CPF/CNPJ/idEstrangeiro (opcional), xNome
- **det**: prod(cProd, cEAN, xProd, NCM, CFOP, uCom, qCom, vUnCom, vProd, indRegra), imposto(ICMS, PIS, COFINS)
- **total**: ICMSTot(vICMS, vProd, vDesc, vPIS, vCOFINS, vOutro), vCFe, vCFeLei12741
- **pgto**: MP(cMP, vMP, cAdmC), vTroco
- **infAdic**: infCpl, obsFisco
- **Signature**: assinatura digital SHA-1 + RSA

## Transmissão
1. App Comercial monta XML do CF-e
2. Envia ao SAT via DLL (EnviarDadosVenda)
3. SAT assina digitalmente (SHA-1 + RSA)
4. SAT transmite para SEFAZ-SP via HTTPS
5. SEFAZ valida e retorna autorização
6. SAT retorna XML assinado + número do CF-e
7. App imprime DANFE CF-e

## Cancelamento
- Prazo: até 30 minutos após emissão
- Deve referenciar o CF-e original (chCanc)
- Gera novo XML de cancelamento assinado
- Ambos os XMLs devem ser armazenados por 5 anos

## QR Code
- Contém: chave de acesso (44 dígitos), timestamp, valor total, assinatura
- URL de consulta: `https://www.fazenda.sp.gov.br/sat/consulta?chave=[44-digitos]`

## Integração com PDV
- Arquitetura: PDV → App Comercial → DLL SAT → Equipamento SAT → SEFAZ-SP
- Funções DLL: AtivarSAT, EnviarDadosVenda, CancelarUltimaVenda, ConsultarSAT, ExtrairLogs, TesteFimAFim
- Tratamento de erros: SAT não responde (bloquear venda), SEFAZ não autorizar (exibir rejeição), sem internet (aguardar)

## Diferenças SAT vs NFC-e
| Característica | SAT (CF-e) | NFC-e |
|----------------|------------|-------|
| Estado | São Paulo | Demais estados |
| Modelo | 59 | 65 |
| Equipamento | Hardware dedicado | Software + certificado |
| Offline | Não | Sim |
| Custo | R$ 800-2000 (equipamento) | R$ 200-500/ano (certificado) |

## Related Documents
- [NFC-e](nfce.md) — nota fiscal de consumidor eletrônico (demais estados)
- [NF-e](nfe.md) — nota fiscal eletrônica
- [EFD ICMS/IPI](efd-icms-ipi.md) — escrituração fiscal digital
