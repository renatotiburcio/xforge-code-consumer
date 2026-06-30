const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// Adicionar outLine no topo
const marker = 'import { icon } from';
if (code.includes(marker)) {
  code = code.replace(marker,
    "const xforgeOut = vscode.window.createOutputChannel('XForge', { log: true });\nfunction outLine(s) { xforgeOut.appendLine('[xforge] ' + s); }\n\n" + marker);
}

// Patch resolveWebviewView: outLine + lazy init
code = code.replace(
  'public resolveWebviewView(\n        webviewView: vscode.WebviewView,\n        _ctx: vscode.WebviewViewResolveContext,\n        _token: vscode.CancellationToken\n    ) {',
  'public resolveWebviewView(webviewView, _ctx, _token) {\n        outLine("resolve");'
);

// Patch onDidReceiveMessage callback to use outLine
code = code.replace(
  '            (msg) => {\n                switch (msg.type) {',
  '            (msg) => {\n                outLine("msg=" + msg.type);\n                switch (msg.type) {'
);

// Patch sendMessage case
code = code.replace(
  "case 'sendMessage': this._handleSendMessage(msg.text); break;",
  "case 'sendMessage': outLine(\"send=\" + (msg.text||\"\").substring(0,40)); this._handleSendMessage(msg.text); break;"
);

// Patch _handleSendMessage
code = code.replace(
  'private async _handleSendMessage(text: string) {\n        if (!text.trim() || !this._view) return;',
  'private async _handleSendMessage(text) {\n        outLine("handle: " + (text||\"\").substring(0,60));\n        if (!text.trim() || !this._view) return;'
);

// Patch _persistSession
code = code.replace(
  'private _persistSession(userMessage: string): void {\n        console.log',
  'private _persistSession(userMessage) {\n        outLine("persist: " + (userMessage||\"\").substring(0,40));'
);

// Patch _startNewSession to log
code = code.replace(
  'private _startNewSession(): void {\n        this._activeSessionId = null;',
  'private _startNewSession() {\n        outLine("newSession"); this._activeSessionId = null;'
);

// Patch _refreshSidebar to log
code = code.replace(
  'private _refreshSidebar(): void {\n        if (!this._view) return;\n        const trash = this._icon',
  'private _refreshSidebar() {\n        if (!this._view) return;\n        outLine("refreshSidebar sessions=" + (this._sessions||[]).length);\n        const trash = this._icon'
);

// Patch _callProvider to ALWAYS create session if active doesn't exist
code = code.replace(
  /const assistantId = this\._generateId\(\);[\s\S]*?this\._view\.webview\.postMessage\(\{ type: 'streamStart', id: assistantId \}\);/,
  `// Garantir que existe uma sessao ativa
        if (!this._activeSessionId || !this._sessions.find(s => s.id === this._activeSessionId)) {
            outLine("criando sessao antes do stream");
            const now = new Date().toISOString();
            this._activeSessionId = 'sess_' + Date.now();
            const sel = loadActiveSelection(this._globalState);
            this._sessions.unshift({ id: this._activeSessionId, name: (userMessage || 'Nova conversa').substring(0,40), messages: [], providerId: sel.providerId, model: sel.model, createdAt: now, updatedAt: now });
            saveSessions(this._globalState, this._sessions);
            saveActiveSessionId(this._globalState, this._activeSessionId);
        }
        const assistantId = this._generateId();
        outLine("iniciando stream assistantId=" + assistantId);
        this._view.webview.postMessage({ type: 'streamStart', id: assistantId });`
);

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK patch final aplicado');
