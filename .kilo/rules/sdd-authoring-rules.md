# SDD Authoring Rules

## 12 Secoes Obrigatorias
1. Metadata
2. Context
3. Personas & Cenarios
4. Requisitos
5. Arquitetura
6. Modelo de Dados
7. API Contract
8. UI/UX
9. Testes
10. Observabilidade
11. Seguranca & LGPD
12. Plano de Entrega

## Checklist por Secao

### Metadata
- [ ] ID do SDD
- [ ] Autor
- [ ] Data criacao/atualizacao
- [ ] Versao (SemVer)
- [ ] Status (Draft/Review/Approved)
- [ ] Aprovadores

### Context
- [ ] Problema (1 paragrafo)
- [ ] Objetivo (1 paragrafo)
- [ ] Fora de escopo (lista)

### Personas & Cenarios
- [ ] 1+ personas
- [ ] 1+ cenario por persona
- [ ] Cenarios com passo-a-passo

### Requisitos
- [ ] RF com ID, prioridade, dependencia
- [ ] RNF com metrica
- [ ] RN com exemplo
- [ ] US com criterios Given-When-Then

### Arquitetura
- [ ] C4 L1
- [ ] C4 L2
- [ ] C4 L3 (se aplicavel)
- [ ] Decisoes com tradeoffs

### Dados
- [ ] ER com cardinalidade
- [ ] Dicionario de dados
- [ ] Migrations em ordem

### API
- [ ] OpenAPI 3.1
- [ ] Exemplos happy + error
- [ ] Erros canonicos documentados

### UI/UX
- [ ] Wireframe por tela
- [ ] Estados (idle/loading/empty/error/success)
- [ ] Fluxo de UX
- [ ] Acessibilidade

### Testes
- [ ] Unit (cobertura > 80%)
- [ ] Integration
- [ ] E2E
- [ ] Contract (se aplicavel)

### Observabilidade
- [ ] Logs estruturados
- [ ] Metricas (RED/USE)
- [ ] Traces (OpenTelemetry)
- [ ] Alertas (SLO)

### Seguranca
- [ ] STRIDE basico
- [ ] Dados sensiveis (LGPD)
- [ ] Retencao
- [ ] Criptografia at-rest/in-transit

### Entrega
- [ ] Fases (1, 2, 3...)
- [ ] Criterios de done por fase
- [ ] Plano de rollback
- [ ] Riscos identificados

## Regra
SDD sem 12 secoes completas NAO pode ser aprovado.
