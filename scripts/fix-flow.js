const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// 1) Carregar sessions ANTES de gerar HTML
code = code.replace(
  "        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);\n        webviewView.webview.onDidReceiveMessage(",
  "        this._sessions = this._globalState ? loadSessions(this._globalState) : [];\n        this._activeSessionId = this._globalState ? loadActiveSessionId(this._globalState) : null;\n        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);\n        webviewView.webview.onDidReceiveMessage(",
);

// 2) Remover linhas duplicadas do final de resolveWebviewView
code = code.replace(
  /        this\._sessions = this\._globalState \? loadSessions\(this\._globalState\) : \[\];\s*this\._activeSessionId = this\._globalState \? loadActiveSessionId\(this\._globalState\) : null;\s*this\._pushSelectionToWebview\(\);\s*\}/,
  "        this._pushSelectionToWebview();\n    }"
);

// 3) Adicionar logs em handleSendMessage
code = code.replace(
  /private async _handleSendMessage\(text: string\) \{\s*if \(!text\.trim\(\) \|\| \!this\._view\) return;/,
  "private async _handleSendMessage(text: string) {\n        console.log('[xforge] handleSendMessage:', text.substring(0, 80));\n        if (!text.trim() || !this._view) return;"
);

// 4) Corrigir _persistSession para logar
code = code.replace(
  /private _persistSession\(userMessage: string\): void \{\s*if \(!this\._globalState\) return;/,
  "private _persistSession(userMessage: string): void {\n        console.log('[xforge] persistSession called:', userMessage.substring(0, 50));\n        if (!this._globalState) return;"
);

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK');
