const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// 1) Adiciona outLine global e output channel
const importEnd = code.indexOf("function loadSvg");
const injection = `const xforgeOut = vscode.window.createOutputChannel('XForge', { log: true });
function outLine(s) { xforgeOut.appendLine(s); }

`;
code = code.substring(0, importEnd) + injection + code.substring(importEnd);

// 2) Substitui o bloco resolveWebviewView inicial
code = code.replace(
    /public resolveWebviewView\(\s*webviewView: vscode\.WebviewView,\s*_ctx: vscode\.WebviewViewResolveContext,\s*_token: vscode\.CancellationToken\s*\) \{\s*this\._view = webviewView;[\s\S]*?this\._pushSelectionToWebview\(\);\s*\}/,
    `public resolveWebviewView(webviewView, _ctx, _token) {
        outLine('[xforge] resolveWebviewView called');
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        this._sessions = this._globalState ? loadSessions(this._globalState) : [];
        this._activeSessionId = this._globalState ? loadActiveSessionId(this._globalState) : null;
        outLine('[xforge] sessions loaded: ' + this._sessions.length);
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        outLine('[xforge] html set');
        webviewView.webview.onDidReceiveMessage((msg) => {
            outLine('[xforge] msg received: ' + msg.type);
            switch (msg.type) {
                case 'sendMessage': outLine('[xforge] sendMessage: ' + (msg.text || '').substring(0, 60)); this._handleSendMessage(msg.text); break;
                case 'newSession': outLine('[xforge] newSession'); this._startNewSession(); break;
                case 'selectSession': outLine('[xforge] selectSession: ' + msg.sessionId); this._loadSession(msg.sessionId); break;
                case 'deleteSession': outLine('[xforge] deleteSession: ' + msg.sessionId); this._removeSession(msg.sessionId); break;
                case 'requestSwitch': if (this._globalState) { const m = require('../commands/providerCommands'); m.showProviderQuickPick(this._globalState, this); } break;
                case 'requestNew': if (this._globalState) { const m = require('../commands/providerCommands'); m.configureProviderCommand(this._globalState, () => this.notifySelectionChanged()); } break;
            }
        });
        this._pushSelectionToWebview();
    }`
);

// 3) Logar handleSendMessage e _persistSession
code = code.replace(
    /private async _handleSendMessage\(text: string\) \{\s*if \(!text\.trim\(\) \|\| \!this\._view\) return;/,
    "private async _handleSendMessage(text) {\n        outLine('[xforge] handleSendMessage: ' + text.substring(0, 60));\n        if (!text.trim() || !this._view) return;"
);

code = code.replace(
    /private _persistSession\(userMessage: string\): void \{\s*if \(!this\._globalState\) return;/,
    "private _persistSession(userMessage) {\n        outLine('[xforge] persistSession: ' + userMessage.substring(0, 50));\n        if (!this._globalState) return;"
);

code = code.replace(
    /private _startNewSession\(\): void \{\s*this\._activeSessionId = null;/,
    "private _startNewSession() {\n        outLine('[xforge] startNewSession');\n        this._activeSessionId = null;"
);

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK');
