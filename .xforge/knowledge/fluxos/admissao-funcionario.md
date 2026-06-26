---
id: admissao-funcionario
type: fluxo
tags: [admissao, rh, esocial, s-2190, s-2200, contrato, beneficios]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Admissão de Funcionário
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: admissao, rh, esocial, s-2190, s-2200, contrato, beneficios
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `admissao-funcionario` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Admissão de Funcionário

## Propósito
Documentar o fluxo completo de admissão: do cadastro inicial à integração com folha de pagamento e envio dos eventos eSocial obrigatórios.

## Etapas

1. **Cadastro Pessoal**: Nome completo, CPF, RG, data de nascimento, estado civil, nacionalidade, endereço, telefone, e-mail, nome dos pais, grau de instrução, raça/cor, PCD (se aplicável).
2. **Documentos Necessários**: RG, CPF, CTPS (Carteira de Trabalho), título de eleitor, comprovante de residência, certificado de reservista (homens), certidão de casamento/nascimento, foto 3x4, PIS/PASEP, comprovante de escolaridade, certidão de dependentes (para IR).
3. **Exames Admissionais**: ASO (Atestado de Saúde Ocupacional) emitido pelo médico do trabalho. Avaliação clínica, exames complementares conforme riscos da função (audiometria, espirometria, etc.). Prazo: antes do início das atividades.
4. **Contrato de Trabalho**: Registro na CTPS (física ou digital). Definição de: cargo, salário, jornada (diária/semanal), regime (CLT, temporário, intermitente, aprendiz, estágio), local de trabalho, data de início. Período de experiência (até 90 dias, renovável uma vez).
5. **Eventos eSocial**:
   - **S-2190** (Admissão — Prévio): enviado antes do início das atividades. Contém dados cadastrais, vínculo, cargo, salário, jornada. Obrigatório para CLT.
   - **S-2200** (Cadastral): enviado no início das atividades. Dados completos do trabalhador — CPF, NIS, CTPS, escolaridade, raça/cor, PCD, contato. Referencia o S-2190.
   - **S-2205** (Alteração Cadastral): se houver correção nos dados após S-2200.
   - **S-2210** (CAT): se acidente no primeiro dia de trabalho.
6. **Integração com Folha**: Cadastro de rubricas específicas (salário, adicionais, benefícios). Definição de centro de custo, lotação tributária (S-1020), tabela de rubricas (S-1010). Categoria eSocial (101 empregado CLT, 103 aprendiz, 901 estagiário, etc.).
7. **Benefícios**: Vale-transporte (desconto 6%), vale-refeição/alimentação, plano de saúde, plano odontológico, seguro de vida, PLR, auxílio-creche, auxílio-combustível. Registro no sistema de RH e parametrização na folha.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Trabalhador CLT? | Sim | S-2190 + S-2200 obrigatórios |
| Estagiário? | Sim | S-2200 com categoria 901, contrato específico |
| Aprendiz? | Sim | S-2200 com categoria 103, jornada especial |
| PCD? | Sim | S-2200 com indicador, cota de contratação |
| Exame admissional apto? | Não | Reavaliação ou recusa da contratação |

## Integrações

- **eSocial**: S-2190, S-2200, S-2205, S-2210 — envio via webservice com certificado digital
- **Folha de Pagamento**: cadastro de rubricas, centro de custo, lotação, categoria
- **Departamento Pessoal**: registro em CTPS digital, controle de documentos, ASO
- **Fiscal**: DIRF (informe de rendimentos anual), EFD-Reinf
- **Contábil**: rateio de encargos por centro de custo

## Documentos Relacionados

- [Rescisão de Funcionário](rescisao-funcionario.md)
- [Folha de Pagamento](folha-pagamento.md)
- [PDV/Frente de Caixa](pdv-venda.md)

