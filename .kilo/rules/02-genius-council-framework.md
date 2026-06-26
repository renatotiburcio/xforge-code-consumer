# Genius Council Framework (GCF) - A Regra de Ouro Suprema

> **Precedencia**: esta regra tem prioridade sobre todas as outras regras, comandos, agentes, skills, workflows e decisoes. Qualquer excecao deve ser registrada como ADR especial com prazo de validade.

## 1. Mandato

Nenhuma implementacao, refatoracao, correcao, melhoria, decisao arquitetural, nova funcionalidade, skill, agent, command, rule, ADR, SDD, documento, conteudo, recurso, opcao, nome, padrao, processo, workflow ou fluxo de trabalho podera avancar sem que o conhecimento tenha passado por:

1. **Descoberto** - o que existe, o que esta implicito, o que pode ser inferido
2. **Analisado** - por multiplas perspectivas tecnicas
3. **Debatido** - incluindo posicoes divergentes explicitas
4. **Validado** - pelos 5 Guardioes especializados
5. **Documentado** - em formato executavel (Decision Record)
6. **Consolidado** - com a fonte oficial da verdade atualizada

**A documentacao e a fonte oficial da verdade.** Qualquer divergencia entre codigo e documentacao e tratada assim: a documentacao tem prioridade; se a documentacao estiver errada, ela e corrigida via Decision Record antes do codigo mudar.

## 2. Por que existe

Sistemas complexos falham nao por falta de codigo, mas por:
- Conhecimento implicito que se perde entre sessoes
- Decisoes sem rastreabilidade (por que fizemos assim?)
- Conflitos entre especialistas nao resolvidos
- Acumulo de debito tecnico **e** documental
- Ausencia de perspectiva multi-disciplinar

O GCF resolve isso institucionalizando um conselho permanente de especialistas virtuais + guardioes + processo de decisao formal.

## 3. Os 8 Dominios e os 38 Genios

### 3.1 Fundamentos da Computacao (AG001-AG003)
- **AG001 - Alan Turing**: Descobrir. O que esta implicito? O que pode ser inferido? O problema e computavel?
- **AG002 - John von Neumann**: Pensar sistemico. A arquitetura e sustentavel? Como escala?
- **AG003 - Claude Shannon**: Analisar informacao. Como dados fluem? Existem gargalos?
### 3.2 Engenharia de Software (AG004-AG007)
- **AG004 - Donald Knuth**: Excelencia algoritmica. O algoritmo e elegante? O custo e justificavel?
- **AG005 - Edsger Dijkstra**: Eliminar complexidade. Pode ser simplificado? Existem estados desnecessarios?
- **AG006 - Barbara Liskov**: Abstracoes corretas. A abstracao representa a realidade? O contrato e consistente?
- **AG007 - Robert C. Martin**: Codigo sustentavel. SOLID, Clean Code, Clean Architecture.

### 3.3 Linguagens e Plataformas (AG008-AG010)
- **AG008 - Dennis Ritchie**: Eficiencia e simplicidade. Recursos, memoria, desempenho.
- **AG009 - Bjarne Stroustrup**: Design para evolucao. APIs e frameworks duraveis.
- **AG010 - Anders Hejlsberg**: Plataformas modernas. .NET, C#, TypeScript, Blazor, tooling.

### 3.4 Web e Infraestrutura (AG011-AG012)
- **AG011 - Tim Berners-Lee**: Integracao. HTTP, URI, Web Semantica, interoperabilidade.
- **AG012 - Linus Torvalds**: Realidade operacional. Funciona em producao? Quem vai manter?

### 3.5 Inteligencia Artificial (AG013-AG015)
- **AG013 - Geoffrey Hinton**: Aplicabilidade de IA. Deep learning, modelos fundacionais.
- **AG014 - Yann LeCun**: Modelagem de IA. CNN, self-supervised, visao.
- **AG015 - Demis Hassabis**: Estrategia de automacao. AGI, multi-agentes, reinforcement learning.

### 3.6 Produto e Negocio (AG016-AG018)
- **AG016 - Steve Jobs**: Foco no valor. O usuario realmente precisa? Podemos remover?
- **AG017 - Bill Gates**: Escalabilidade de negocio. Ecossistemas, plataforma, escala.
- **AG018 - Steve Wozniak**: Praticidade. Solucao mais elegante tecnicamente?
### 3.7 UX, UI e Design System (AG019-AG026)
- **AG019 - Don Norman**: UX, psicologia cognitiva, affordance.
- **AG020 - Jakob Nielsen**: Heuristicas de usabilidade, research.
- **AG021 - Ben Shneiderman**: HCI, dashboards, visualizacao.
- **AG022 - Dieter Rams**: Design minimalista, menos-mas-melhor.
- **AG023 - Jony Ive**: Design premium, refinamento visual.
- **AG024 - Susan Kare**: Iconografia, comunicacao visual.
- **AG025 - Brad Frost**: Atomic Design, componentizacao, design systems escalaveis.
- **AG026 - Nathan Curtis**: Governanca de Design System, tokens, catalogos.

### 3.8 Seguranca, Criptografia e Privacidade (AG027-AG038)
- **AG027 - Whitfield Diffie**: Criptografia moderna, PKI, TLS, identidade digital.
- **AG028 - Martin Hellman**: Protocolos seguros, autenticacao.
- **AG029 - Ron Rivest**: RSA, assinaturas digitais, integridade.
- **AG030 - Adi Shamir**: Criptoanalise, modelagem de ameacas.
- **AG031 - Leonard Adleman**: Complexidade computacional aplicada a criptografia.
- **AG032 - Bruce Schneier**: Engenharia de seguranca, threat modeling, gestao de riscos.
- **AG033 - Ross Anderson**: Seguranca de sistemas distribuidos, sistemas criticos.
- **AG034 - Dan Geer**: Risco cibermetico, governanca, resiliencia.
- **AG035 - Kevin Mitnick**: Engenharia social, pentest, vetores de ataque.
- **AG036 - Charlie Miller**: Exploracao de vulnerabilidades, exploit development.
- **AG037 - Ann Cavoukian**: Privacy by Design, LGPD, GDPR, governanca de dados.
- **AG038 - OWASP Collective**: Top 10, secure coding, SQLi/XSS/CSRF/SSRF.
## 4. Os 5 Guardioes (Validacao Automatica)

Toda decisao passa pelos 5 guardioes antes de ser aprovada:

| Guardiao | Valida |
|----------|--------|
| **Guardian Architecture** | DDD, SOLID, Clean Architecture, Modularizacao |
| **Guardian Simplicity** | KISS, DRY, YAGNI |
| **Guardian Security** | Autenticacao, Autorizacao, Privacidade, Protecao de Dados |
| **Guardian Quality** | Cobertura de testes por camada (min 50% por projeto de teste), Observabilidade, Telemetria. **Desde FB-001 (v3.26.0): exige tabela cobertura-por-camada no DR, nao apenas contagem absoluta.** |
| **Guardian Documentation** | Consistencia, Completude, Rastreabilidade |

## 5. AG999 - Devil''s Advocate (Obrigatorio)

Obrigatoriamente participa de **toda** decisao. Antes de aprovar qualquer coisa, responde:

- Por que estamos fazendo isso?
- Existe alternativa melhor?
- Existe alternativa mais simples?
- Existe alternativa mais barata?
- Isso e necessidade ou moda?
- Isso ainda fara sentido daqui 5 anos?
- Qual a maior critica possivel contra essa decisao?

**Nenhuma decisao e aprovada sem responder todas as objecoes** ou registrar risco aceito.

## 6. AG100 - Consensus Engine

Recebe pareceres, criticas e divergencias. Executa:

1. **Debate** (paralelo, com posicoes explicitas)
2. **Consolidacao** (encontrar terreno comum)
3. **Decisao** (com Decision Record canonico)
## 7. AG101 - Documentation Governor

Atualiza automaticamente (via hooks pos-decisao):

- `backlog`, `roadmap`, `SDD`, `SAD`, `ADR`
- Requisitos, casos de uso, testes
- Manual, glossario, indice
- RAG (reindexar quando novos arquivos surgem)

**Regra**: nada e implementado sem estar documentado. Se foi documentado, esta sob controle de versao.

## 8. AG102 - LLM Execution Specialist

Missao critica: converter conhecimento produzido para execucao por **modelos menores** (Qwen 2.5 7B, DeepSeek Lite, Gemma, Phi, Mistral Small, Llama Small, etc.).

**Proibido nas specs para LLMs menores**:
- Ambiguidades
- Conhecimento implicito
- Decisoes sem justificativa
- Requisitos vagos

**Obrigatorio**:
- Passo a passo numerado
- Criterios de aceite verificaveis
- Dependencias explicitas
- Exemplos positivos e negativos
- Pseudocodigo
- Fluxos textuais
- Excecoes documentadas
- Tabelas de decisao

## 9. Formato Obrigatorio de Decisao (Decision Record)

Toda decisao e registrada em `.xforge/decisions/DR-XXXX-titulo.md` com a estrutura canonica: PROBLEMA, CONTEXTO, ALTERNATIVAS, ARGUMENTOS, DECISAO, JUSTIFICATIVA, RISCOS, MITIGACOES, IMPACTOS, IMPLEMENTACAO, TESTES, CRITERIOS DE ACEITE, RASTREABILIDADE.

Ver `.kilo/skills/genius-council/SKILL.mddecision-record-format.md` para template completo.
## 10. Comando CREATE_GENIUS (Adicionar Novo Genio)

```
CREATE_GENIUS

Nome:
Inspiracao (figura historica real):
Missao (1 frase):
Especialidade (3-5 bullets):
Perguntas Caracteristicas (3-5):
Responsabilidades (3-5):
Artefatos (1-3 entregaveis):
Criterios de Qualidade (3-5):
Participa em (selecionar):
  - [ ] Arquitetura
  - [ ] Backend
  - [ ] Frontend
  - [ ] UX
  - [ ] UI
  - [ ] Dados
  - [ ] IA
  - [ ] Seguranca
  - [ ] Infraestrutura
  - [ ] Documentacao
  - [ ] Negocio
  - [ ] Outro: ____
```

Resultado: cria `agents/genius-council/<dominio>/<codigo>-<nome>.md` + atualiza `.kilo/skills/genius-council/SKILL.mdcouncil-members.md` + gera Decision Record.

## 11. Resultado Esperado (de toda analise GCF)

Toda analise GCF deve gerar 15 entregaveis:

1. **Inventario** - o que existe
2. **Descoberta** - o que estava implicito
3. **Engenharia Reversa** - como funciona hoje
4. **Arquitetura Atual** - diagrama C4 L1/L2/L3
5. **Arquitetura Recomendada** - alvo
6. **Regras de Negocio** - RNs explicitas
7. **Mapa de Dependencias** - entre modulos/servicos
8. **Gap Analysis** - atual vs. alvo
9. **Debito Tecnico** - priorizado
10. **Debito Documental** - priorizado
11. **Roadmap** - visao
12. **Backlog** - execucao
13. **ADRs** - decisoes formais
14. **Plano de Implementacao** - operacional
15. **Versao Executavel para LLMs Menores** - spec final
## 12. Integracao com Regras Existentes

Esta regra **AMPLIA** (nao substitui) as regras existentes:

- **Regra 0 (Stack-Agnostic)** -> validada por Guardian Architecture
- **Regras 1-4 (SOLID, Pacotes Estaveis, Padroes por Stack, Documentacao)** -> validadas pelos Guardioes
- **Regras de auto-retry, memory, quality gates** -> continuam aplicando-se
- **Regra de Ouro (stack-agnostic)** -> rebaixada para Regra 0 sob o GCF

## 13. Excecoes

Excecoes a esta regra devem:

1. Ser registradas como ADR especial (`DR-XXXX-exception-...`)
2. Ter prazo de validade (ex: "valido ate 2026-09-30")
3. Ser revisadas na proxima oportunidade (sprint review)
4. Ser aprovadas explicitamente por humano + Devil''s Advocate

## 14. Enforcement (Aplicacao)

| Momento | Verificacao | Ferramenta |
|---------|-------------|------------|
| **Pre-commit** | Decisao tem Decision Record? | `doctor.ps1` |
| **Pre-push** | Consensus Engine validou? | `pre-push` hook |
| **Pre-merge** | Documentation Governor atualizou indice? | PR check |
| **Pos-merge** | RAG reindexou? Backlog atualizado? | `rag_local.py index` + Backlog sync |
| **Sprint Review** | ADRs revisados? Excecoes expiradas? | Manual |

## 15. Politica de Nao Repeticao

- Toda decisao ja tomada em ADR/Decision Record **NAO** e re-debatida do zero.
- Novas informacoes podem reabrir decisao (via Devil''s Advocate + ADR de revisao).
- Historico de debates preservado em `.xforge/decisions/archive/`.

## 16. Politica 100% Documentacao

Apos 2026-06-17:

- Toda decisao e **documentada antes** de ser implementada.
- Toda implementacao e **referenciada** por Decision Record.
- Se algo novo aparecer mid-execucao, ele **para o fluxo** e vira nova decisao documentada.
- Excecoes a parada (ex: hotfix de producao) sao registradas retroativamente em ate 24h.
## 17. Politica Nada Passa Sem Decisao

- Mudanca em `rules/`, `agents/`, `commands/`, `skills/` -> DR obrigatorio.
- Mudanca em `docs/` (manual) -> DR obrigatorio.
- Mudanca em codigo de producao -> DR + criterios de aceite + testes.
- Mudanca em config/provedor -> DR.
- Mudanca em ADR existente -> novo DR referenciando o anterior.

## 18. Aplicacao Imediata

Esta regra aplica-se **retroativamente** ao backlog ativo de XForge v1.5.0. Decisoes futuras seguirao o processo GCF. Decisoes passadas permanecem validas (sao baseline), mas novas decisoes sobre o mesmo tema exigem DR.

## 19. Resumo Operacional (TL;DR)

| Quando | O que fazer |
|--------|-------------|
| Recebeu pedido | Acionar Conselho (38 genios) |
| Decisao nao-trivial | Aplicar 5 Guardioes |
| Antes de aprovar | Devil''s Advocate ataca |
| Conflitos | Consensus Engine resolve |
| Aprovado | Decision Record em `.xforge/decisions/` |
| Implementado | Documentation Governor atualiza docs |
| Excecao | ADR especial com prazo de validade |
| Sprint Review | Revisar ADRs e excecoes expiradas |

## 20. Historico

- **2026-06-17**: GCF instituido como Regra de Ouro Suprema (v1.5.0+).
- Inspiracao: 38 genios historicos + 5 guardioes + 5 agentes especiais propostos pelo usuario Renato Tiburcio.
- Aplicacao inicial: consolidacao do estado v1.5.0 + plano de expansao do manual modular.
- Status: **ATIVO** desde 2026-06-17.

## 21. Referencias Cruzadas

- Skill: `.kilo/skills/genius-council/SKILL.md`
- Agente orquestrador: `.kilo/agents/genius-council-orchestrator.md`
- Agentes especiais: `.kilo/agents/devils-advocate.md`, `consensus-engine.md`, `documentation-governor.md`, `llm-execution-specialist.md`
- Documentacao: `.kilo/skills/genius-council/SKILL.mdREADME.md`
- Indice de decisoes: `.xforge/decisions/ADR-INDEX.md`
- Indice de regras: `.kilo/rules/00-xforge-rule-index.md`

## 22. Template Simplificado (v3.10.0)

Per DR-0087, GCF template reduzido de 7 fases para **3 fases** (default).

### Template 3-fases (90% das decisoes)

1. **Discovery** (AG001 Turing): o que existe + o que esta implicito + inferencia
2. **Decision** (AG100): opcao escolhida + justificativa + risco + mitigacao
3. **Risks** (5 Guardians + AG999): Guardian status + Devil Advocate 7 perguntas respondidas

### Template 7-fases (APENAS para alto impacto)

Manter template completo para:
- Decisoes arquiteturais multi-modulo/multi-stack
- Breaking changes
- Incident response
- Sprint planning / roadmap changes
- Anything with multi-team impact

### Regra de Ouro

MAIS valor, MENOS ceremony. Documentar para **rastreabilidade**, nao para **impressionar**.
Se o DR canonico tem 12 secoes (per formato canonico), audit doc NAO precisa duplicar.

### Cleanup Policy

- Audit docs legados: DELETADOS, NAO arquivados
- 1 STATUS.md master, sem refresh loop
- CHANGELOG: 1 entry por release, sem duplicatas
- Releases: 1 por sprint (NAO 1 por hora)

---

## 23. Historico (atualizado)

- **2026-06-17**: GCF instituido como Regra de Ouro Suprema (v1.5.0+).
- **2026-06-18**: Template 7-fases aplicado a 6 releases consecutivas (v3.7.2 a v3.9.4).
- **2026-06-18**: v3.10.0 Simplification (DR-0087): template reduzido para 3-fases (default).
  - 6 audit docs (36KB) -> 1 XX-GCF-INDEX.md (~4KB)
  - 15 arquivos de auditoria legada -> DELETADOS
  - STATUS.md: 1 master version, sem refresh loop
  - Ratio doc:código target: 3:1 (era 15:1)
