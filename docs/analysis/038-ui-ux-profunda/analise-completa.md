# Análise Profunda de UI/UX — XForge Code AI

> **Data**: 2026-06-27
> **Tipo**: Análise exaustiva com Genius Council
> **Foco**: Chat, Configurações, Extensão, CLI, TUI, Desktop
> **Objetivo**: Criar a melhor experiência de chat/UI entre todos os concorrentes

---

## 1. Discovery (AG001 Turing) — O que está implícito?

### 1.1 O problema real

Nenhum dos 10 concorrentes resolveu completamente a experiência de chat para desenvolvedores. Cada um fez tradeoffs que deixam lacunas exploráveis:

| Concorrente | Tradeoff | Lacuna |
|-------------|----------|--------|
| Kilo Code | Sidebar rica + Agent Manager | Sem diff review inline, sem preview de código ao vivo |
| Cline | Diff review + Plan/Act | Sem streaming, sem multi-sessão, sem system tray |
| Continue | @context system | Read-only, sem tools avançadas, sem streaming |
| Goose | Desktop + TUI | Sem diff review, sem inline editing, sem per-directory rules |
| Aider | Terminal puro | Sem GUI, sem preview, sem autocomplete visual |
| OpenHands | Web UI + WebSocket | Latência do sandbox, sem diff review, sem offline |
| Twinny | Local-first | Sem streaming, sem MCP, sem tools |
| MiMo-Code | Leve | Funcionalidades mínimas |
| OpenCode | TUI | Sem GUI rica, sem streaming |

### 1.2 O que está implícito nas reclamações dos usuários

1. **Context switching** — Usuários alternam entre terminal, editor, browser, e chat constantemente
2. **Cognitive load** — Muita informação espalhada em múltiplos painéis
3. **Trust gap** — Usuários não confiam cegamente no AI; querem ver antes de aplicar
4. **Flow interruption** — Streaming lento ou ausente quebra o fluxo de trabalho
5. **Configuração fragmentada** — Settings espalhados em JSON, UI, env vars, e arquivos
6. **Multi-tarefa impossível** — Não dá para trabalhar em 2+ tarefas simultâneas
7. **Feedback invisível** — Não sabe o que o AI está fazendo em background
8. **Histórico perdido** — Sessões anteriores são inacessíveis ou difíceis de encontrar

### 1.3 O que pode ser inferido

- O vencedor será quem **unificar** todos os contextos em uma experiência fluida
- **Streaming + diff preview + inline editing** é o mínimo esperado
- **Multi-sessão com worktree isolation** é diferencial competitivo
- **Configuração unificada** (UI + CLI + arquivo) reduz fricção
- **Offline-first com sync opcional** é requisito para enterprise

---

## 2. Análise Multi-Perspectiva (8 Gênios)

### 2.1 AG019 Don Norman — UX e Psicologia Cognitiva

**Princípios aplicados ao chat:**

1. **Affordance** — Cada elemento deve comunicar sua função sem texto
   - Botão de enviar deve parecer clicável
   - Diff deve parecer editável
   - Status deve ser óbvio (cor + ícone + animação)

2. **Feedback** — Toda ação deve ter resposta imediata
   - Streaming: cada token aparece em <50ms
   - Tool call: spinner + nome da tool + progresso
   - Erro: mensagem clara + ação sugerida

3. **Mapping** — Relação clara entre controle e efeito
   - Slash commands: lista aparece conforme digita
   - @context: preview do arquivo ao mencionar
   - Mode selector: ícone + cor + descrição

4. **Constraints** — Limitar opções para reduzir erros
   - Modos limitados (Code, Plan, Ask, Debug, Review, Architect)
   - Confirmação para ações destrutivas
   - Validação antes de enviar

**Veredicto**: O chat deve ter **feedback imediato**, **affordance clara**, e **constraints inteligentes**.

### 2.2 AG020 Jakob Nielsen — Heurísticas de Usabilidade

**10 heurísticas aplicadas:**

| # | Heurística | Aplicação no XForge |
|---|------------|---------------------|
| 1 | Status visibility | Streaming, tool progress, mode indicator |
| 2 | Match real world | Linguagem natural, não técnica |
| 3 | User control | Cancel, undo, retry, edit |
| 4 | Consistency | Mesmo padrão em todos os painéis |
| 5 | Error prevention | Confirmação, validação, preview |
| 6 | Recognition > recall | Slash commands com autocomplete |
| 7 | Flexibility | Atalhos, comandos, config |
| 8 | Aesthetic design | Minimalista, foco no conteúdo |
| 9 | Error recovery | Mensagens claras + sugestões |
| 10 | Help | Tooltips, docs inline, exemplos |

**Veredicto**: Recognition > recall é crítico. Slash commands com autocomplete e preview são obrigatórios.

### 2.3 AG022 Dieter Rams — Design Minimalista

**Princípios "menos mas melhor":**

1. **Essencial** — Remover tudo que não é necessário
2. **Claro** — Hierarquia visual óbvia
3. **Neutro** — Não competir com o código
4. **Detalhado** — Pixel-perfect nos detalhes
5. **Atemporal** — Não seguir modas passageiras

**Aplicação:**
- Sidebar com largura fixa (350px) — não distrai do editor
- Cores: máximo 4 (primary, success, warning, error)
- Tipografia: monospace para código, sans para UI
- Espaçamento: consistente (4px, 8px, 16px, 24px)
- Animações: sutis, <200ms, apenas para feedback

**Veredicto**: Interface deve ser **invisível** — o usuário foca no código, não na UI.

### 2.4 AG023 Jony Ive — Design Premium

**Elementos premium para o chat:**

1. **Micro-interações** — Cada transição é fluida
2. **Tipografia** — Fonte com personalidade (Inter, Geist, ou similar)
3. **Espaço** — Respiração entre elementos
4. **Profundidade** — Sombras sutis, não flat extremo
5. **Delight** — Momentos de surpresa positiva

**Aplicação:**
- Streaming com cursor animado
- Tool calls com ícones animados
- Transições suaves entre modos
- Dark mode com cores ricas (não apenas cinza)
- Hover states informativos

**Veredicto**: Cada interação deve sentir **resposta e qualidade**.

### 2.5 AG025 Brad Frost — Atomic Design

**Hierarquia de componentes:**

```
Atoms:        Button, Icon, Input, Badge, Spinner
Molecules:    ChatInput, MessageBubble, ToolCall, DiffLine
Organisms:    ChatPanel, AgentManager, SettingsPanel, SlashCommandMenu
Templates:    SidebarLayout, FullscreenLayout, PopupLayout
Pages:        ChatView, ConfigView, AgentView, HistoryView
```

**Veredicto**: Componentes devem ser **reutilizáveis e consistentes**.

### 2.6 AG021 Ben Shneiderman — HCI e Visualização

**Princípios para ferramentas complexas:**

1. **Overview first** — Dashboard com status geral
2. **Zoom and filter** — Drill-down em sessões
3. **Details on demand** — Expandir tool calls
4. **Relate** — Conectar mensagens relacionadas
5. **History** — Log de ações para replay
6. **Extract** — Exportar sessões

**Veredicto**: Dashboard de sessões com drill-down é essencial.

### 2.7 AG005 Edsger Dijkstra — Simplicidade

**Aplicado ao chat:**

- Cada tela tem **uma responsabilidade**
- Sem modais aninhados (max 1 nível)
- Sem configurações escondidas (tudo acessível em 2 cliques)
- Sem estados indefinidos (sempre sabe o que está acontecendo)

**Veredicto**: Simplicidade é **eliminar o desnecessário**, não adicionar o mínimo.

### 2.8 AG016 Steve Jobs — Foco no Valor

**Pergunta**: "O usuário realmente precisa disso?"

**Funcionalidades que passam no teste:**
- ✅ Streaming (feedback imediato)
- ✅ Diff review (confiança)
- ✅ Multi-sessão (produtividade)
- ✅ Slash commands (velocidade)
- ✅ @context (precisão)
- ✅ Worktree isolation (segurança)

**Funcionalidades que não passam:**
- ❌ Animações elaboradas (distrai)
- ❌ Múltiplos temas (complexidade)
- ❌ Customização extrema (paralisia)
- ❌ Notificações push (interrompe)

**Veredicto**: Foco no que **importa para o fluxo de desenvolvimento**.

---

## 3. Análise Exaustiva por Componente

### 3.1 Chat Interface (Sidebar)

#### 3.1.1 Layout

```
┌─────────────────────────────────────┐
│ [Mode: Code ▼] [Session: main ▼]   │  ← Header (40px)
├─────────────────────────────────────┤
│                                     │
│  ┌─ User ─────────────────────────┐ │
│  │ Crie uma API de pagamentos     │ │
│  └────────────────────────────────┘ │
│                                     │
│  ┌─ Assistant ────────────────────┐ │
│  │ Vou criar a API...             │ │
│  │                                │ │
│  │ 🔧 read_file src/Program.cs   │ │  ← Tool call (colapsável)
│  │ ✅ Encontrado                  │ │
│  │                                │ │
│  │ 🔧 write_file src/Payment.cs  │ │
│  │ ┌─ Diff ─────────────────────┐ │ │
│  │ │ + public class Payment     │ │ │
│  │ │ + {                       │ │ │
│  │ │ +   public int Id { get; } │ │ │
│  │ │ + }                       │ │ │
│  │ └───────────────────────────┘ │ │
│  │ [Accept] [Reject] [Modify]    │ │
│  └────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [📎] [Digite...          ] [➤]     │  ← Input (60px)
└─────────────────────────────────────┘
```

#### 3.1.2 Especificações de UX

| Elemento | Especificação | Razão |
|----------|---------------|-------|
| Largura da sidebar | 350px (fixo) | Legível sem distrair |
| Fonte do chat | 14px, line-height 1.6 | Legibilidade |
| Fonte do código | 13px, monospace | Diferenciação |
| Cores de mensagem | User: azul, Assistant: cinza | Identificação visual |
| Tool calls | Colapsável, ícone animado | Não polui |
| Diff | Syntax highlighted, inline | Contexto imediato |
| Input | Auto-resize, max 200px | Multiline natural |
| Scroll | Smooth, auto-scroll para final | Fluidez |

#### 3.1.3 Estados do Chat

| Estado | Visual | Ação |
|--------|--------|------|
| Idle | Input habilitado | Digitar |
| Streaming | Cursor animado + texto aparecendo | Aguardar |
| Tool call | Spinner + nome da tool | Aguardar |
| Diff pending | Diff destacado + botões | Aceitar/Rejeitar |
| Error | Vermelho + mensagem | Retry/Edit |
| Complete | Check verde | Continuar |

#### 3.1.4 Streaming Spec

- **Latência**: <50ms por chunk
- **Cursor**: Animação suave (blink 1s)
- **Chunk size**: Variável (provider-dependent)
- **Cancelamento**: Esc ou botão stop
- **Reconexão**: Automática com retry (3x)

### 3.2 Message Types (Detalhado)

#### 3.2.1 User Message

```typescript
interface UserMessage {
  id: string;
  type: "user";
  content: string;
  attachments: Attachment[];
  timestamp: Date;
}

interface Attachment {
  type: "file" | "folder" | "codebase" | "url" | "image";
  path?: string;
  name: string;
  preview?: string;
}
```

**UX:**
- Avatar: ícone do usuário ou inicial
- Background: sutilmente diferente do assistant
- Attachments: chips removíveis acima do texto
- Timestamp: hover para ver hora exata

#### 3.2.2 Assistant Message

```typescript
interface AssistantMessage {
  id: string;
  type: "assistant";
  content: string;
  toolCalls: ToolCall[];
  diffs: DiffBlock[];
  streaming: boolean;
  timestamp: Date;
}
```

**UX:**
- Avatar: logo do XForge ou inicial "X"
- Background: neutro, sem distrações
- Tool calls: colapsáveis, ordenados
- Diffs: inline com syntax highlighting
- Code blocks: copy button, language label

#### 3.2.3 Tool Call

```typescript
interface ToolCall {
  id: string;
  name: string;
  status: "pending" | "running" | "success" | "error";
  args: Record<string, unknown>;
  result?: string;
  duration?: number;
}
```

**UX:**
- Ícone: específico por tool (📂 read, ✏️ write, 🔧 bash, 🔍 search)
- Status: spinner (running), ✅ (success), ❌ (error)
- Args: colapsável, mostrado como key=value
- Result: preview com max 10 linhas, expandir para ver tudo
- Duração: mostrada em ms (útil para debug)

#### 3.2.4 Diff Block

```typescript
interface DiffBlock {
  filePath: string;
  language: string;
  additions: number;
  deletions: number;
  hunks: DiffHunk[];
  status: "pending" | "accepted" | "rejected" | "modified";
}
```

**UX:**
- Header: filepath + additions/deletions (+12 -3)
- Syntax highlighting: por linguagem
- Line numbers: visíveis
- Actions: [Accept] [Reject] [Modify] [View File]
- Inline editing: clicar para modificar antes de aceitar

### 3.3 Slash Commands System

#### 3.3.1 Arquitetura

```
Usuário digita "/"
    ↓
Aparece menu com comandos
    ↓
Filtra conforme digita
    ↓
Seleciona com Enter/Tab
    ↓
Mostra parâmetros necessários
    ↓
Executa
```

#### 3.3.2 Comandos Detalhados

| Comando | Ícone | Descrição | Parâmetros |
|---------|-------|-----------|------------|
| `/xforge` | ⚡ | Menu principal | subcommand |
| `/analisar-projeto` | 🔍 | Analisa projeto atual | --depth, --format |
| `/criar-projeto` | ➕ | Cria novo projeto | --template, --name |
| `/desenvolver` | 💻 | Inicia desenvolvimento | feature description |
| `/qualidade` | ✅ | Quality gates | --strict, --fix |
| `/seguranca` | 🔒 | Auditoria segurança | --level |
| `/conhecimento` | 🧠 | Gerencia conhecimento | action, query |
| `/memoria` | 💾 | Gerencia memória | action, scope |
| `/documentacao` | 📄 | Gera documentação | --format, --output |
| `/release` | 🚀 | Gerencia releases | --version, --type |
| `/genius-council` | 🎓 | Inicia debate | topic, --geniuses |
| `/checkpoint` | 💾 | Salva checkpoint | --name |
| `/retomar` | ▶️ | Retoma checkpoint | checkpoint-id |
| `/config` | ⚙️ | Abre configurações | --section |
| `/help` | ❓ | Ajuda | topic |

#### 3.3.3 UX do Menu Slash

- **Trigger**: `/` no início do input
- **Posição**: Flutuante acima do input
- **Filtro**: Fuzzy match no nome e descrição
- **Navegação**: ↑↓ para mover, Enter para selecionar, Esc para fechar
- **Preview**: Mostra descrição + parâmetros ao selecionar
- **Atalho**: `Ctrl+/` abre menu diretamente

### 3.4 @Context System

#### 3.4.1 Tipos de Contexto

| Prefixo | Tipo | Preview | Ação |
|---------|------|---------|------|
| `@file` | Arquivo | Conteúdo (primeiras 5 linhas) | Inclui no contexto |
| `@folder` | Pasta | Lista de arquivos | Inclui todos os arquivos |
| `@codebase` | Projeto inteiro | Resumo (file tree) | Indexa e inclui |
| `@url` | URL | Título da página | Fetch e inclui |
| `@docs` | Documentação | Resumo | Inclui documentação |
| `@git` | Git (diff/log) | Últimos commits | Inclui info git |
| `@search` | Busca | Resultados | Busca e inclui |
| `@knowledge` | Knowledge graph | Entrada relevante | Inclui conhecimento |

#### 3.4.2 UX do @context

- **Trigger:** `@` no meio do texto
- **Autocomplete:** Lista de arquivos/pastas conforme digita
- **Preview:** Hover mostra conteúdo (file) ou lista (folder)
- **Multi-select:** Pode mencionar múltiplos em uma mensagem
- **Visual:** Chip colorido com ícone + nome + remover (x)
- **Limite:** Máximo 20 contextos por mensagem (configurável)

### 3.5 Agent Manager Panel

#### 3.5.1 Layout

```
┌─ Agent Manager ──────────────────────┐
│ [+ New Session] [🔄 Refresh]         │
├──────────────────────────────────────┤
│ ● main (Code)            12:34    ⋮  │
│ ├─ 📝 "Crie API pagamentos"        │
│ └─ ✅ 3 tasks completed             │
│                                      │
│ ● feature/auth (Plan)    12:30    ⋮  │
│ ├─ 📝 "Implementar JWT"            │
│ └─ ⏳ 1 task pending                │
│                                      │
│ ○ bugfix/login (Ask)     12:25    ⋮  │
│ ├─ 📝 "Debug login error"          │
│ └─ ✅ Completed                     │
├──────────────────────────────────────┤
│ 📊 3 sessions | 2 active | 1 done   │
└──────────────────────────────────────┘
```

#### 3.5.2 Funcionalidades

| Funcionalidade | Descrição | Atalho |
|----------------|-----------|--------|
| New Session | Cria sessão nova | Ctrl+Shift+N |
| Switch Session | Troca sessão ativa | Ctrl+Tab |
| Delete Session | Remove sessão | Del |
| Isolate Worktree | Isola em git worktree | — |
| Rename Session | Renomeia sessão | F2 |
| Export Session | Exporta como JSON/MD | — |
| Search Sessions | Busca no histórico | Ctrl+F |

#### 3.5.3 Worktree Isolation

- **Criação:** Automática ao isolar sessão
- **Branch:** `xforge/session-<id>`
- **Status:** Indicador visual (ícone de branch)
- **Merge:** Botão para mergear de volta
- **Cleanup:** Automático ao deletar sessão

### 3.6 Settings/Config Panel

#### 3.6.1 Arquitetura de Configuração

```
Configuração (3 camadas):
  1. Default (built-in)
  2. User (~/.config/kilo/)
  3. Project (.kilo/kilo.jsonc)

UI Settings (acessível por painel):
  - Provider
  - Model
  - Mode
  - Streaming
  - Theme
  - Font Size
  - Language
  - Shortcuts
  - Permissions
  - MCP Servers
  - Skills
```

#### 3.6.2 Layout do Painel de Configuração

```
┌─ Settings ───────────────────────────┐
│ 🔍 Buscar configuração...            │
├──────────────────────────────────────┤
│ ▼ Provider                           │
│   Provider: [OpenRouter ▼]           │
│   Model: [Claude Sonnet ▼]           │
│   API Key: [••••••••] [Show]         │
│                                      │
│ ▼ Behavior                           │
│   Default Mode: [Code ▼]             │
│   Streaming: [✓]                     │
│   Auto-accept: [ ]                   │
│   Confirm destructive: [✓]           │
│                                      │
│ ▼ Appearance                         │
│   Theme: [Dark ▼]                    │
│   Font Size: [14px]                  │
│   Font Family: [Inter ▼]             │
│                                      │
│ ▼ Security                           │
│   Permissions: [Ask ▼]               │
│   Secret detection: [✓]              │
│   Sandbox mode: [✓]                  │
│                                      │
│ ▼ MCP Servers                        │
│   [+ Add Server]                     │
│   ● GitHub (connected)               │
│   ○ Linear (disconnected)            │
│                                      │
│ ▼ Skills                             │
│   [+ Install Skill]                  │
│   ● code-generation (active)         │
│   ● architecture-enterprise (active) │
│   ○ react-modern (inactive)          │
└──────────────────────────────────────┘
```

#### 3.6.3 UX de Configuração

| Aspecto | Especificação |
|---------|---------------|
| Busca | Fuzzy search em todas as configs |
| Validação | Inline, em tempo real |
| Feedback | Toast de sucesso/erro |
| Reset | Botão "Reset to default" por seção |
| Export/Import | JSON export/import |
| Hot reload | Mudanças aplicadas sem reload |
| Preview | Preview de mudanças antes de aplicar |

### 3.7 Inline Editing (Editor Integration)

#### 3.7.1 Funcionalidades

| Funcionalidade | Descrição | Atalho |
|----------------|-----------|--------|
| Inline Suggest | Sugestão inline no código | Tab aceita |
| Quick Fix | Correção rápida | Ctrl+. |
| Refactor | Refatoração inline | Ctrl+Shift+R |
| Explain | Explicar código selecionado | Ctrl+Shift+E |
| Generate | Gerar código a partir de comentário | Ctrl+Shift+G |

#### 3.7.2 UX Inline

- **Suggest:** Texto fantasma (cinza claro) após o cursor
- **Diff inline:** Mudanças mostradas como diff no editor
- **Accept:** Tab aceita, Esc rejeita
- **Partial:** Ctrl+Right aceita palavra por palavra
- **Preview:** Hover mostra diff completo

### 3.8 Terminal Integration (TUI)

#### 3.8.1 Layout

```
┌─ Terminal ───────────────────────────┐
│ $ xforge desenvolver "API pagamentos" │
│                                       │
│ ⚡ XForge Code AI v1.0.0              │
│ ─────────────────────────────────     │
│ Mode: Code                            │
│ Provider: OpenRouter/Claude Sonnet    │
│                                       │
│ Pensando...                           │
│                                       │
│ Vou criar a API de pagamentos...      │
│                                       │
│ 🔧 Lendo src/Program.cs...           │
│ ✅ Encontrado                         │
│                                       │
│ 🔧 Criando src/Payment.cs...         │
│ ┌─ Diff ─────────────────────────┐   │
│ │ + public class Payment         │   │
│ │ + {                           │   │
│ │ +   public int Id { get; }    │   │
│ │ + }                           │   │
│ └─────────────────────────────────┘   │
│ [Accept] [Reject] [Modify]            │
│                                       │
│ ✅ Concluído em 12.3s                 │
└───────────────────────────────────────┘
```

#### 3.8.2 Especificações TUI

| Aspecto | Especificação |
|---------|---------------|
| Cores | 256 colors, true color support |
| Unicode | Suporte completo (emojis, box drawing) |
| Responsivo | Adapta ao tamanho do terminal |
| Scroll | Scroll com mouse/keyboard |
| Copy | Seleção + Ctrl+Shift+C |
| Search | Ctrl+F para buscar no histórico |

### 3.9 Desktop App (Electron)

#### 3.9.1 Layout

```
┌─────────────────────────────────────────────────────┐
│ XForge Code AI                          _ □ ×       │
├────────┬────────────────────────────────────────────┤
│ 📁     │                                            │
│ Files  │  ┌─ Chat ──────────────────────────────┐   │
│        │  │                                      │   │
│ 📄 src │  │  (conteúdo do chat)                 │   │
│  📄 cs │  │                                      │   │
│        │  └──────────────────────────────────────┘   │
│ 📁 docs│                                            │
│        │  ┌─ Terminal ─────────────────────────┐    │
│        │  │ $ dotnet build                     │    │
│        │  │ Build succeeded                    │    │
│        │  └────────────────────────────────────┘    │
│        │                                            │
│        │  ┌─ Preview ──────────────────────────┐    │
│        │  │ (preview de arquivo/diff)          │    │
│        │  └────────────────────────────────────┘    │
├────────┴────────────────────────────────────────────┤
│ ● Ready | Mode: Code | Provider: Claude              │
└─────────────────────────────────────────────────────┘
```

#### 3.9.2 Funcionalidades Desktop

| Funcionalidade | Descrição |
|----------------|-----------|
| System Tray | Ícone na bandeja com quick actions |
| Global Hotkey | Ctrl+Shift+X abre de qualquer lugar |
| Multi-window | Múltiplas janelas para múltiplos projetos |
| Notifications | Notificações nativas |
| File Watcher | Detecta mudanças no projeto |
| Auto-update | Atualização automática |

### 3.10 Web UI (Browser)

#### 3.10.1 Layout

```
┌─────────────────────────────────────────────────────┐
│ [Logo] XForge Code AI    [Search] [Settings] [👤]   │
├────────┬────────────────────────────────────────────┤
│        │                                            │
│ 📁     │  ┌─ Project ──────────────────────────┐    │
│ Files  │  │ src/                               │    │
│        │  │  ├─ Program.cs                     │    │
│        │  │  ├─ Payment.cs                     │    │
│        │  │  └─ ...                            │    │
│        │  └────────────────────────────────────┘    │
│        │                                            │
│        │  ┌─ Chat ──────────────────────────────┐   │
│        │  │ (conteúdo do chat)                  │   │
│        │  └──────────────────────────────────────┘   │
│        │                                            │
├────────┴────────────────────────────────────────────┤
│ Status: Ready | Provider: Claude | 12:34:56         │
└─────────────────────────────────────────────────────┘
```

#### 3.10.2 Funcionalidades Web

| Funcionalidade | Descrição |
|----------------|-----------|
| Real-time sync | WebSocket para streaming |
| File explorer | Navegação no projeto |
| Code viewer | Syntax highlighted |
| Session management | Múltiplas sessões |
| Share | Compartilhar sessão via URL |
| Mobile | Responsive para mobile |

---

## 4. Fluxos de Usuário Detalhados

### 4.1 Fluxo: Primeira Conversação

```
1. Usuário abre VS Code
   → Extensão XForge ativa automaticamente
   → Sidebar aparece com mensagem de boas-vindas

2. Usuário clica na sidebar
   → Input focado
   → Placeholder: "Como posso ajudar?"

3. Usuário digita: "Crie uma API de pagamentos"
   → Mensagem aparece na lista
   → Status muda para "Pensando..."

4. AI responde com streaming
   → Texto aparece gradualmente
   → Tool calls aparecem conforme executadas

5. AI sugere criação de arquivo
   → Diff aparece inline
   → Botões [Accept] [Reject] [Modify]

6. Usuário clica [Accept]
   → Arquivo criado
   → Diff some
   → AI continua

7. AI termina
   → Status: "Completo"
   → Resumo: "Criados 3 arquivos, 2 tools executadas"
```

### 4.2 Fluxo: Multi-sessão

```
1. Usuário tem sessão "main" ativa
   → Quer trabalhar em feature paralela

2. Usuário clica [+ New Session]
   → Modal: "Nome da sessão"
   → Digita: "feature/auth"

3. Nova sessão criada
   → Worktree isolado automaticamente
   → Branch: xforge/feature-auth

4. Usuário trabalha na feature
   → Mudanças isoladas do main

5. Usuário volta para main
   → Ctrl+Tab ou clique na sessão
   → Contexto restaurado

6. Usuário mergeia feature
   → Botão [Merge] no Agent Manager
   → Conflitos mostrados se houver
```

### 4.3 Fluxo: Configuração Inicial

```
1. Usuário instala extensão
   → Wizard de setup aparece

2. Step 1: Provider
   → Escolhe: OpenRouter / Ollama / Azure / etc.
   → Insere API key (se necessário)
   → Teste de conexão automático

3. Step 2: Model
   → Lista de modelos disponíveis
   → Recomendado destacado
   → Preview de capabilities

4. Step 3: Behavior
   → Modo padrão: Code / Plan / Ask
   → Streaming: on/off
   → Auto-accept: on/off

5. Step 4: Security
   → Permissions: Ask / Allow-list / Full
   → Secret detection: on/off
   → Sandbox: on/off

6. Step 5: Skills
   → Lista de skills recomendados
   → Instala com um clique

7. Setup completo
   → Mensagem: "Tudo pronto! Digite /help para começar"
```

### 4.4 Fluxo: Diff Review

```
1. AI sugere mudança
   → Diff aparece inline na mensagem

2. Usuário revisa
   → Syntax highlighting
   → Line numbers
   → Contexto (3 linhas antes/depois)

3. Usuário decide:
   a) [Accept] → Aplica mudança
   b) [Reject] → Descarta mudança
   c) [Modify] → Abre editor inline
   d) [View File] → Abre arquivo completo

4. Se [Modify]:
   → Editor inline abre com diff
   → Usuário edita
   → [Save] aplica, [Cancel] descarta

5. Feedback:
   → Toast: "Mudança aplicada com sucesso"
   → Status atualizado
```

### 4.5 Fluxo: Error Recovery

```
1. AI encontra erro
   → Mensagem vermelha: "Erro ao executar tool X"
   → Detalhes colapsáveis

2. Opções:
   a) [Retry] → Tenta novamente
   b) [Edit] → Edita a mensagem
   c) [Skip] → Pula essa ação
   d) [Debug] → Mostra stack trace

3. Se [Retry]:
   → Spinner + "Tentando novamente (1/3)"
   → Se falhar de novo, mostra opções

4. Se [Edit]:
   → Mensagem editável
   → [Send] reenvia

5. Se [Debug]:
   → Painel com stack trace
   → Sugestão de correção
```

---

## 5. Especificações de Design System

### 5.1 Cores

#### 5.1.1 Paleta Principal

| Nome | Hex | Uso |
|------|-----|-----|
| Primary | #4dabf7 | Ações, links, focus |
| Primary Dark | #339af0 | Hover |
| Success | #51cf66 | Sucesso, accept |
| Warning | #ffd43b | Avisos, pending |
| Error | #ff6b6b | Erros, reject |
| Info | #339af0 | Informação |

#### 5.1.2 Neutros (Dark Mode)

| Nome | Hex | Uso |
|------|-----|-----|
| Background | #1e1e1e | Fundo principal |
| Surface | #252526 | Cards, panels |
| Border | #3c3c3c | Bordas |
| Text Primary | #cccccc | Texto principal |
| Text Secondary | #858585 | Texto secundário |
| Text Disabled | #5a5a5a | Texto desabilitado |

#### 5.1.3 Neutros (Light Mode)

| Nome | Hex | Uso |
|------|-----|-----|
| Background | #ffffff | Fundo principal |
| Surface | #f3f3f3 | Cards, panels |
| Border | #e0e0e0 | Bordas |
| Text Primary | #333333 | Texto principal |
| Text Secondary | #666666 | Texto secundário |
| Text Disabled | #999999 | Texto desabilitado |

### 5.2 Tipografia

| Elemento | Fonte | Size | Weight |
|----------|-------|------|--------|
| H1 | Inter | 24px | 600 |
| H2 | Inter | 18px | 600 |
| H3 | Inter | 16px | 500 |
| Body | Inter | 14px | 400 |
| Code | JetBrains Mono | 13px | 400 |
| Small | Inter | 12px | 400 |
| Tiny | Inter | 10px | 400 |

### 5.3 Espaçamento

| Token | Valor | Uso |
|-------|-------|-----|
| xs | 4px | Ícones, badges |
| sm | 8px | Padding interno |
| md | 16px | Entre elementos |
| lg | 24px | Entre seções |
| xl | 32px | Entre painéis |

### 5.4 Bordas

| Token | Valor | Uso |
|-------|-------|-----|
| radius-sm | 4px | Botões, inputs |
| radius-md | 8px | Cards |
| radius-lg | 12px | Modais |
| radius-full | 50% | Avatares |

### 5.5 Sombras

| Token | Valor | Uso |
|-------|-------|-----|
| shadow-sm | 0 1px 2px rgba(0,0,0,0.1) | Botões |
| shadow-md | 0 4px 8px rgba(0,0,0,0.15) | Cards |
| shadow-lg | 0 8px 16px rgba(0,0,0,0.2) | Modais |

### 5.6 Animações

| Token | Valor | Uso |
|-------|-------|-----|
| duration-fast | 100ms | Hover, focus |
| duration-normal | 200ms | Transições |
| duration-slow | 300ms | Modais |
| easing | ease-in-out | Padrão |

### 5.7 Ícones

- **Set**: Phosphor Icons (leve, consistente)
- **Tamanho**: 16px (small), 20px (medium), 24px (large)
- **Estilo**: Regular (outlined), Fill (ativo)

### 5.8 Breakpoints (Web/Responsive)

| Nome | Largura | Layout |
|------|---------|--------|
| mobile | < 768px | Single column |
| tablet | 768-1024px | Collapsible sidebar |
| desktop | > 1024px | Full layout |

---

## 6. Acessibilidade (WCAG 2.1 AA)

### 6.1 Requisitos

| Requisito | Implementação |
|-----------|---------------|
| Contraste | Mínimo 4.5:1 para texto |
| Keyboard nav | Todos os controles via teclado |
| Screen reader | ARIA labels em tudo |
| Focus indicator | Ring visível (2px) |
| Reduced motion | Respeitar prefers-reduced-motion |
| Color blind | Não usar cor como único indicador |
| Font size | Mínimo 12px, escalável |
| Zoom | Funciona até 200% |

### 6.2 Atalhos de Teclado

| Atalho | Ação | Contexto |
|--------|------|----------|
| Ctrl+K | Abrir chat | Global |
| Ctrl+Shift+K | Abrir Agent Manager | Global |
| Ctrl+/ | Abrir slash commands | Chat focused |
| Ctrl+Enter | Enviar mensagem | Chat focused |
| Ctrl+Tab | Trocar sessão | Chat focused |
| Esc | Cancelar/Fechar | Global |
| Tab | Aceitar sugestão | Inline |
| Ctrl+Z | Desfazer | Global |
| Ctrl+Shift+Z | Refazer | Global |
| Ctrl+F | Buscar | Chat/Manager |
| Ctrl+N | Nova sessão | Manager |
| Del | Deletar sessão | Manager |
| F2 | Renomear sessão | Manager |

---

## 7. Performance de UI

### 7.1 Métricas

| Métrica | Target | Máximo |
|---------|--------|--------|
| First paint | < 100ms | 200ms |
| Time to interactive | < 500ms | 1s |
| Streaming latency | < 50ms | 100ms |
| Scroll FPS | 60fps | 30fps |
| Input latency | < 16ms | 32ms |
| Memory usage | < 100MB | 200MB |

### 7.2 Otimizações

- **Virtual scrolling** para listas longas
- **Lazy loading** de mensagens antigas
- **Memoization** de componentes
- **Debounce** de input (100ms)
- **Throttle** de scroll (16ms)
- **Web Workers** para parsing de diff
- **Code splitting** por rota

---

## 8. Comparação com Concorrentes (UI/UX)

| Feature | Kilo Code | Cline | Goose | OpenHands | XForge (proposto) |
|---------|-----------|-------|-------|-----------|-------------------|
| Sidebar | ✅ SolidJS | ✅ React | ✅ Electron | ❌ | ✅ SolidJS |
| Streaming | ✅ SSE | ❌ | ✅ | ✅ WS | ✅ SSE + WS |
| Diff review | ❌ | ✅ | ❌ | ❌ | ✅ Inline |
| Multi-sessão | ✅ | ❌ | ❌ | ❌ | ✅ Worktree |
| Slash commands | ✅ | ✅ | ❌ | ❌ | ✅ + autocomplete |
| @context | ❌ | ❌ | ❌ | ❌ | ✅ Full |
| Settings UI | ✅ | ✅ | ✅ | ✅ | ✅ + busca |
| Inline edit | ✅ | ✅ | ❌ | ❌ | ✅ + preview |
| Desktop app | ❌ | ❌ | ✅ | ❌ | ✅ Electron |
| TUI | ❌ | ❌ | ✅ | ❌ | ✅ Ink |
| Web UI | ❌ | ❌ | ❌ | ✅ | ✅ |
| Agent Manager | ✅ | ❌ | ❌ | ❌ | ✅ Enhanced |
| Dark mode | ✅ | ✅ | ✅ | ✅ | ✅ + custom |
| Acessibilidade | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ WCAG AA |

**Resultado**: XForge propõe **18/18** features vs melhor concorrente **8/18**.

---

## 9. Componentes SolidJS Propostos

### 9.1 Estrutura

```
webview-ui/
  src/
    components/
      atoms/
        Button.tsx
        Icon.tsx
        Input.tsx
        Badge.tsx
        Spinner.tsx
        Avatar.tsx
        Tooltip.tsx
      molecules/
        ChatInput.tsx
        MessageBubble.tsx
        ToolCall.tsx
        DiffBlock.tsx
        SlashCommandMenu.tsx
        ContextChip.tsx
      organisms/
        ChatPanel.tsx
        AgentManager.tsx
        SettingsPanel.tsx
        SlashCommandMenu.tsx
        DiffReview.tsx
      templates/
        SidebarLayout.tsx
        FullscreenLayout.tsx
      pages/
        ChatView.tsx
        ConfigView.tsx
        AgentView.tsx
        HistoryView.tsx
    hooks/
      useStreaming.ts
      useToolCalls.ts
      useSlashCommands.ts
      useTheme.ts
      useSettings.ts
    stores/
      chatStore.ts
      sessionStore.ts
      settingsStore.ts
      uiStore.ts
    styles/
      tokens.css
      global.css
      dark.css
      light.css
    App.tsx
    index.tsx
```

### 9.2 Signals (Estado Reativo)

```typescript
// chatStore.ts
import { createSignal } from "solid-js";

export const [messages, setMessages] = createSignal<Message[]>([]);
export const [streaming, setStreaming] = createSignal(false);
export const [currentSession, setCurrentSession] = createSignal<Session>(null);
export const [mode, setMode] = createSignal<Mode>("code");

// settingsStore.ts
export const [settings, setSettings] = createSignal<Settings>(defaultSettings);
export const [theme, setTheme] = createSignal<Theme>("dark");
```

---

## 10. Especificação de API (Extension ↔ Webview)

### 10.1 Mensagens

```typescript
// Extension → Webview
interface ExtensionMessage {
  type: "stream" | "tool_call" | "diff" | "error" | "session";
  payload: unknown;
}

// Webview → Extension
interface WebviewMessage {
  type: "send_message" | "cancel" | "accept_diff" | "reject_diff" | "switch_session" | "update_settings";
  payload: unknown;
}
```

### 10.2 Streaming Protocol

```typescript
// Server-Sent Events
event: stream
data: { "token": "Pensando", "messageId": "msg_123" }

event: stream
data: { "token": "...", "messageId": "msg_123" }

event: stream_end
data: { "messageId": "msg_123", "duration": 1234 }
```

---

## 11. Resumo de Decisões de UI/UX

| # | Decisão | Justificativa |
|---|---------|---------------|
| 1 | SolidJS para webview | Performance, reatividade, bundle pequeno |
| 2 | Sidebar 350px fixo | Legível sem distrair |
| 3 | Streaming SSE | Latência <50ms, reconexão automática |
| 4 | Diff inline editável | Confiança + controle |
| 5 | Slash commands + autocomplete | Velocidade + discovery |
| 6 | @context com preview | Precisão + contexto |
| 7 | Multi-sessão + worktree | Produtividade + isolamento |
| 8 | Settings com busca | Configuração rápida |
| 9 | Desktop Electron | System tray + global hotkey |
| 10 | TUI com Ink | Terminal experience |
| 11 | Web UI React | Acesso remoto |
| 12 | WCAG 2.1 AA | Inclusão |
| 13 | Dark/Light + custom | Preferência do usuário |
| 14 | Phosphor Icons | Consistente + leve |
| 15 | Inter + JetBrains Mono | Legibilidade |

---

## 12. Próximos Passos

1. **Validar** esta análise com o Genius Council completo
2. **Criar** wireframes de cada tela
3. **Implementar** protótipo do webview
4. **Testar** com usuários reais
5. **Iterar** baseado em feedback

---

*Análise criada em 2026-06-27 — XForge Code AI v1.0.0*
