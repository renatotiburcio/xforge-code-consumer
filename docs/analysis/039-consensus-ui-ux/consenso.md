# Consenso Genius Council — UI/UX XForge Code AI

> **Data**: 2026-06-27
> **Tipo**: Decisão formal do Conselho
> **Tema**: Design de UI/UX para o XForge Code AI
> **Participantes**: 8 Gênios + 5 Guardiões + Devil's Advocate

---

## 1. A Questão

**"Qual a melhor experiência de UI/UX para um assistente de código AI que supere todos os 10 concorrentes analisados?"**

---

## 2. Debate do Conselho

### 2.1 AG019 Don Norman — Affordance e Feedback

**Posição**: O chat deve ser uma extensão natural do editor, não uma ferramenta separada.

**Argumentos**:
- Affordance clara: cada botão/comando deve parecer o que é
- Feedback imediato: streaming <50ms, tool calls com status visual
- Mapping natural: @context mostra preview, slash commands mostram opções
- Constraints inteligentes: modos limitados, confirmações para ações destrutivas

**Proposta**: Sidebar integrada ao editor com feedback visual rico.

### 2.2 AG020 Jakob Nielsen — Heurísticas

**Posição**: Recognition > recall. Usuário não deve memorizar comandos.

**Argumentos**:
- Status sempre visível (streaming, tool progress, mode)
- Consistência em todos os painéis
- Prevenção de erros (confirmação, validação, preview)
- Ajuda contextual (tooltips, docs inline)

**Proposta**: Slash commands com autocomplete, tooltips em tudo, ajuda inline.

### 2.3 AG022 Dieter Rams — Minimalismo

**Posição**: Menos mas melhor. Interface invisível.

**Argumentos**:
- Remover tudo que não é essencial
- Máximo 4 cores (primary, success, warning, error)
- Espaço para respirar
- Pixel-perfect nos detalhes

**Proposta**: Sidebar 350px, sem flat extremo, animações sutis <200ms.

### 2.4 AG023 Jony Ive — Premium

**Posição**: Cada interação deve sentir qualidade.

**Argumentos**:
- Micro-interações fluidas
- Tipografia com personalidade (Inter, Geist)
- Dark mode com cores ricas
- Momentos de delight

**Proposta**: Streaming com cursor animado, transições suaves, hover states ricos.

### 2.5 AG025 Brad Frost — Atomic Design

**Posição**: Componentes reutilizáveis e consistentes.

**Argumentos**:
- Hierarquia clara (atoms → organisms → pages)
- Mesmo padrão em tudo
- Design system documentado

**Proposta**: Estrutura atômica de componentes SolidJS.

### 2.6 AG021 Ben Shneiderman — Visualização

**Posição**: Overview first, zoom and filter, details on demand.

**Argumentos**:
- Dashboard de sessões com status geral
- Drill-down em sessões específicas
- Tool calls colapsáveis (expandir para detalhes)
- Histórico pesquisável

**Proposta**: Agent Manager com overview, tool calls colapsáveis, busca.

### 2.7 AG005 Dijkstra — Simplicidade

**Posição**: Eliminar o desnecessário.

**Argumentos**:
- Uma responsabilidade por tela
- Sem modais aninhados
- Tudo acessível em 2 cliques
- Sem estados indefinidos

**Proposta**: Layout simples, sem complexidade desnecessária.

### 2.8 AG016 Steve Jobs — Foco

**Posição**: Foco no que importa para o fluxo de desenvolvimento.

**Argumentos**:
- Streaming (feedback)
- Diff review (confiança)
- Multi-sessão (produtividade)
- Sem distrações (animações, notificações)

**Proposta**: Apenas o essencial para programar.

---

## 3. Devil's Advocate (AG999) — 7 Perguntas

### P1: Por que estamos fazendo isso?
**Resposta**: Porque nenhum concorrente resolveu completamente a experiência de chat. Há lacunas exploráveis que podem ser o diferencial competitivo.

### P2: Existe alternativa melhor?
**Resposta**: Não. A combinação de sidebar + streaming + diff review + multi-sessão + @context é o estado da arte. Faltar qualquer um desses é ficar atrás.

### P3: Existe alternativa mais simples?
**Resposta**: Sim, mas seria inferior. Podemos simplificar removendo desktop app e TUI, mas isso limitaria o alcance. A complexidade é justificada pelo valor.

### P4: Existe alternativa mais barata?
**Resposta**: Sim, focar apenas na extensão VS Code. Mas desktop e web são diferenciais competitivos que justificam o custo.

### P5: Isso é necessidade ou moda?
**Resposta**: Necessidade. Streaming, diff review, e multi-sessão são requisitos mínimos em 2026. @context e worktree isolation são diferenciais.

### P6: Isso ainda fará sentido daqui 5 anos?
**Resposta**: Sim. Os princípios (feedback, confiança, produtividade) são atemporais. A implementação (SolidJS, Electron) pode mudar, mas o design permanece.

### P7: Qual a maior crítica possível?
**Resposta**: "É complexo demais para implementar". Mitigação: implementar em fases (P0: sidebar + streaming, P1: diff review, P2: multi-sessão, P3: desktop/web).

---

## 4. Validação dos 5 Guardiões

### Guardião Architecture — ✅ OK
- Componentes atômicos e reutilizáveis
- Separação clara (UI ↔ Core ↔ Integração)
- API bem definida (Extension ↔ Webview)
- Design system documentado

### Guardião Simplicity — ✅ OK
- Uma responsabilidade por tela
- Sem modais aninhados
- Tudo acessível em 2 cliques
- Estados claros (idle, streaming, tool_call, diff, error, complete)

### Guardião Security — ✅ OK
- Permissions configuráveis
- Secret detection
- Sandbox mode
- Confirmação para ações destrutivas

### Guardião Quality — ✅ OK
- WCAG 2.1 AA compliance
- Performance targets definidos (<50ms streaming, 60fps scroll)
- Acessibilidade completa (keyboard nav, screen reader, reduced motion)
- Testes de UX planejados

### Guardião Documentation — ✅ OK
- Design system documentado
- Fluxos de usuário detalhados
- Especificação de API
- Wireframes descritos

---

## 5. Consenso Final (AG100)

### 5.1 Decisão

**APROVADO** por unanimidade (8/8 Gênios + 5/5 Guardiões).

O XForge Code AI terá a seguinte experiência de UI/UX:

### 5.2 Componentes Aprovados (Prioridade)

| Prioridade | Componente | Justificativa |
|------------|------------|---------------|
| P0 | Sidebar 350px (SolidJS) | Base da experiência |
| P0 | Streaming SSE <50ms | Feedback imediato |
| P0 | Chat com message types | Comunicação rica |
| P0 | Slash commands + autocomplete | Velocidade |
| P0 | Settings panel com busca | Configuração rápida |
| P1 | Diff review inline editável | Confiança |
| P1 | @context system com preview | Precisão |
| P1 | Tool calls colapsáveis | Organização |
| P1 | Error recovery | Resiliência |
| P2 | Multi-sessão + worktree | Produtividade |
| P2 | Agent Manager enhanced | Overview |
| P2 | Inline editing | Edição rápida |
| P3 | Desktop Electron | System tray |
| P3 | TUI Ink | Terminal |
| P3 | Web UI React | Acesso remoto |

### 5.3 Design System Aprovado

| Aspecto | Decisão |
|---------|---------|
| Framework UI | SolidJS (webview) |
| Framework Desktop | Electron |
| Framework TUI | Ink |
| Framework Web | React |
| Cores | 4 principais + neutros dark/light |
| Tipografia | Inter (UI) + JetBrains Mono (código) |
| Ícones | Phosphor Icons |
| Espaçamento | 4/8/16/24/32px |
| Animações | <200ms, ease-in-out |
| Acessibilidade | WCAG 2.1 AA |

### 5.4 Diferenciais Aprovados (vs Concorrentes)

| # | Diferencial | Concorrentes |
|---|-------------|--------------|
| 1 | Diff inline editável | Nenhum |
| 2 | @context com preview | Nenhum |
| 3 | Multi-sessão + worktree | Apenas Kilo Code (sem worktree) |
| 4 | Settings com busca | Nenhum |
| 5 | Desktop + TUI + Web + Extensão | Nenhum (máx 2) |
| 6 | WCAG 2.1 AA | Nenhum |
| 7 | Streaming <50ms | Apenas Kilo Code, Goose, OpenHands |
| 8 | Error recovery integrado | Nenhum |

---

## 6. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Complexidade de implementação | Alta | Alto | Fasear (P0→P3) |
| Performance do webview | Média | Alto | Virtual scroll, lazy load, memoização |
| Bundle size | Média | Médio | Code splitting, tree shaking |
| Acessibilidade incompleta | Baixa | Alto | Auditoria WCAG, testes com screen reader |
| Resistência do usuário | Baixa | Médio | Wizard de setup, tooltips, docs |

---

## 7. Decision Record

```
DR-0XXX-ui-ux-xforge

Status: Aprovado
Data: 2026-06-27
Participantes: AG005, AG016, AG019, AG020, AG021, AG022, AG023, AG025, AG999, AG100
Decisão: Implementar UI/UX em 4 fases (P0-P3) com 18 features diferenciadas
Justificativa: Nenhum concorrente oferece todas as 18 features; combinação é inédita
Riscos: Complexidade (mitigação: fases), Performance (mitigação: otimizações)
```

---

## 8. Next Steps (AG102 — LLM Execution)

### Fase 1: Fundação (P0)
1. Criar projeto SolidJS (webview-ui/)
2. Implementar SidebarLayout com ChatPanel
3. Implementar streaming via SSE
4. Criar design system (tokens.css, global.css)
5. Implementar SlashCommandMenu com autocomplete
6. Criar SettingsPanel com busca

### Fase 2: Confiança (P1)
1. Implementar DiffBlock com syntax highlighting
2. Criar DiffReview com accept/reject/modify
3. Implementar @context system com preview
4. Criar ToolCall colapsável
5. Implementar ErrorRecovery

### Fase 3: Produtividade (P2)
1. Criar AgentManager com overview
2. Implementar worktree isolation
3. Criar multi-sessão navigation
4. Implementar inline editing
5. Criar session export/import

### Fase 4: Alcance (P3)
1. Criar Electron desktop app
2. Implementar system tray + global hotkey
3. Criar TUI com Ink
4. Implementar Web UI com React
5. Criar mobile responsive

---

*Consenso criado em 2026-06-27 — XForge Code AI v1.0.0*
