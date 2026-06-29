const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');

let content = fs.readFileSync(fp, 'utf-8');

// Adicionar session ao import
content = content.replace(
  "import { callProvider, resolveApiKey, resolveBaseUrl, loadActiveSelection, StoredProvider, getProviderConfig } from '../services/apiProvider';",
  "import { callProvider, resolveApiKey, resolveBaseUrl, loadActiveSelection, StoredProvider, getProviderConfig, SessionData, loadSessions, saveSessions, loadActiveSessionId, saveActiveSessionId } from '../services/apiProvider';"
);

// Adicionar session state
content = content.replace(
  "    private _activeStreamRequest?: { abort: () => void };",
  "    private _activeStreamRequest?: { abort: () => void };\n    private _sessions: SessionData[] = [];\n    private _activeSessionId: string | null = null;"
);

// Atualizar resolveWebviewMessage para 142:144 (carregar sessions)
content = content.replace(
  "        this._pushSelectionToWebview();",
  "        this._sessions = this._globalState ? loadSessions(this._globalState) : [];\n        this._activeSessionId = this._globalState ? loadActiveSessionId(this._globalState) : null;\n        this._pushSelectionToWebview();"
);

// Adicionar metodo _persistSession antes dispose
content = content.replace(
  "    dispose() {",
  "    private _persistSession(userMessage: string): void {\n        if (!this._globalState) return;\n        const now = new Date().toISOString();\n        if (!this._activeSessionId) {\n            this._activeSessionId = 'sess_' + Date.now();\n            const sel = loadActiveSelection(this._globalState);\n            this._sessions.unshift({\n                id: this._activeSessionId,\n                name: userMessage.substring(0, 40),\n                messages: [],\n                providerId: sel.providerId,\n                model: sel.model,\n                createdAt: now,\n                updatedAt: now\n            });\n        }\n        const session = this._sessions.find(s => s.id === this._activeSessionId);\n        if (session) {\n            session.messages.push({ role: 'user', content: userMessage, timestamp: now });\n            session.updatedAt = now;\n        }\n        saveSessions(this._globalState, this._sessions);\n        saveActiveSessionId(this._globalState, this._activeSessionId);\n    }\n\n    private _appendAssistantMessage(text: string): void {\n        if (!this._globalState || !this._activeSessionId) return;\n        const session = this._sessions.find(s => s.id === this._activeSessionId);\n        if (session) {\n            session.messages.push({ role: 'assistant', content: text, timestamp: new Date().toISOString() });\n            session.updatedAt = new Date().toISOString();\n            saveSessions(this._globalState, this._sessions);\n        }\n    }\n\n    dispose() {"
);

// Atualizar _handleSendMessage para chamar _persistSession e limpar welcome
content = content.replace(
  "        await this._callProvider(text);",
  "        this._persistSession(text);\n        await this._callProvider(text);"
);

// Atualizar _callProvider para capturar session
content = content.replace(
  "                onToken: (token) => {\n                    assistantMessage.content += token;\n                    this._view?.webview.postMessage({ type: 'streamToken', id: assistantId, token });",
  "                onToken: (token) => {\n                    assistantMessage.content += token;\n                    this._appendAssistantMessage(assistantMessage.content);\n                    this._view?.webview.postMessage({ type: 'streamToken', id: assistantId, token });"
);

fs.writeFileSync(fp, content, 'utf-8');
console.log('OK');
