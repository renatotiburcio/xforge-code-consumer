---
id: session-management-lessons
priority: high
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-30
updated: 2026-06-30
---

# Licoes Aprendidas — Session Management

## O que tentamos e FALHOU

1. **Dynamic refresh via postMessage**: _refreshSidebar() envia innerHTML atualizado, mas o webview não aplica porque outro plugin (Copilot/Cline) está interceptando innerHTML. Solução: usar framework reativo (Solid.js/React)
2. **Persist no provider**: dados salvos no globalState do extension host são perdidos entre sessões de EDH se retainContextWhenHidden nao estiver ativo. Solução: persistir em arquivo JSON local
3. **Sidebar HTML dinâmica**: reconstruir HTML via innerHTML é inconfiável. Solução: framework reativo com Virtual DOM

## O que funciona nas REFERENCIAS

### Twinny (ref/twinny):
- Persiste sessões em arquivo local JSON, nao em MemOria
- Sessões sao identificadas por timestamp
- Interface usa VanillaJS com timeline por data
- Com child_process para Ollama

### Roo-Code (ref/Roo-Code):
- Sessoes persistem em `.roo/sessions/` como arquivos individuais
- IndexedDB no webview para cache local
- Comunicacao via postMessage tipado (Request/Response pattern)
- `retainContextWhenHidden: true`

### Kilocode (ref/kilocode):
- CLI separado roda como child process
- Sessões gerenciadas pelo CLI (nao pelo extension host)
- Webview usa Solid.js reativo com Provider pattern
- Provider comunica via HTTP SSE, nao via postMessage do vscode diretamente

## Arquitetura Nova Baseada em Referencias

### Padrao de Persistencia (Twinny + Kilocode)
1. Estado atual: JSON em `.xforge/sessions/index.json`
2.Prefixo `.xforge/` eh pasta de config (similar a `.roo/`, `.kilo/`, `.cline/`)
3. Cada sessao: `.xforge/sessions/{timestamp}.json` com array de mensagens
4. Sessão ativa: referenciada no index.json com ponteiro
5. UI mostra timeline (parecido com o Git history do VS Code)

### Padrao de Estado Reativo (Kilocode + Roo)
1. Webview: Solid.js ou React (nao Vanilla) para re-render automatico
2. Extension Side: Mantem estado em memoria + disco
3. Comunicacao: `vscode.postMessage` tipado com Request/Response

### Padrao de Comunicacao (Roo-Code)
```typescript
// Extension -> Webview
interface ExtensionMessage {
  type: 'sessionsLoaded';
  sessions: SessionInfo[];
}

// Webview -> Extension
interface WebviewMessage {
  type: 'loadSessions' | 'selectSession' | 'deleteSession' | 'sendMessage';
  sessionId?: string;
  text?: string;
}
```

## Decisao de Design

Usar Roo-Code como referencia primaria para Session Management porque:
- Similar ao nosso webview-only setup
- Usa postMessage tipado
- Persiste em disco, nao perde estado
- Multiplas sessoes em paralelo
- UI timeline por data
