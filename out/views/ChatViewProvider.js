"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModesViewProvider = exports.SettingsViewProvider = exports.AgentManagerViewProvider = exports.WelcomeViewProvider = exports.ChatViewProvider = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const apiProvider_1 = require("../services/apiProvider");
const icons_1 = require("../webview/icons");
class ChatViewProvider {
    constructor(_extensionUri, viewContext = 'chat', _globalState) {
        this._extensionUri = _extensionUri;
        this._globalState = _globalState;
        this._disposables = [];
        this._viewContext = 'chat';
        this._sessions = [];
        this._activeSessionId = null;
        this._session = this.createNewSession();
        this._viewContext = viewContext;
    }
    resolveWebviewView(webviewView, _ctx, _token) {
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        webviewView.webview.onDidReceiveMessage((msg) => {
            switch (msg.type) {
                case 'sendMessage':
                    this._handleSendMessage(msg.text);
                    break;
                case 'newSession':
                    this._startNewSession();
                    break;
                case 'selectSession':
                    this._loadSession(msg.sessionId);
                    break;
                case 'deleteSession':
                    this._removeSession(msg.sessionId);
                    break;
                case 'requestSwitch':
                    if (this._globalState) {
                        const m = require('../commands/providerCommands');
                        m.showProviderQuickPick(this._globalState, this);
                    }
                    break;
                case 'requestNew':
                    if (this._globalState) {
                        const m = require('../commands/providerCommands');
                        m.configureProviderCommand(this._globalState, () => this.notifySelectionChanged());
                    }
                    break;
            }
        }, null, this._disposables);
        this._sessions = this._globalState ? (0, apiProvider_1.loadSessions)(this._globalState) : [];
        this._activeSessionId = this._globalState ? (0, apiProvider_1.loadActiveSessionId)(this._globalState) : null;
        this._pushSelectionToWebview();
    }
    _pushSelectionToWebview() {
        if (!this._view || !this._globalState)
            return;
        const sel = (0, apiProvider_1.loadActiveSelection)(this._globalState);
        const cfg = (0, apiProvider_1.getProviderConfig)(sel.providerId);
        this._view.webview.postMessage({
            type: 'currentSelection',
            selection: {
                providerId: sel.providerId,
                providerName: cfg ? cfg.name : sel.providerId,
                model: sel.model
            }
        });
    }
    _getSharedStyles() {
        return [
            '* { margin:0; padding:0; box-sizing:border-box; }',
            'html, body { margin:0; padding:0; height:100%; width:100%; overflow:hidden; }',
            'body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:13px; background:var(--vscode-sideBar-background,#1e1e1e); color:var(--vscode-foreground,#ccc); }',
            '.chat-app { display:flex; height:100%; width:100%; }',
            '.chat-sidebar { width:0; overflow:hidden; background:var(--vscode-sideBar-background); border-right:1px solid var(--vscode-widget-border,#3c3c3c); transition:width .2s; flex-shrink:0; }',
            '.chat-sidebar.open { width:220px; }',
            '.sidebar-header { display:flex; align-items:center; justify-content:space-between; padding:8px; border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); }',
            '.sidebar-title { font-size:.75rem; font-weight:600; color:#fff; }',
            '.sidebar-btn { background:none; border:none; color:#888; cursor:pointer; padding:2px 4px; border-radius:3px; display:flex; align-items:center; }',
            '.sidebar-btn:hover { background:var(--vscode-list-hoverBackground); color:#fff; }',
            '.sidebar-btn svg { width:14px; height:14px; display:block; }',
            '.sidebar-list { overflow-y:auto; height:calc(100% - 41px); }',
            '.session-item { display:flex; align-items:center; justify-content:space-between; padding:8px 10px; cursor:pointer; border-bottom:1px solid rgba(60,60,60,.3); }',
            '.session-item:hover { background:var(--vscode-list-hoverBackground,#2a2d2e); }',
            '.session-item.active { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.session-info { flex:1; min-width:0; }',
            '.session-name { font-size:.75rem; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }',
            '.session-meta { font-size:.65rem; color:#888; }',
            '.session-del { opacity:0; background:none; border:none; color:#888; cursor:pointer; padding:2px; border-radius:3px; }',
            '.session-item:hover .session-del { opacity:1; }',
            '.session-del:hover { color:#ff6b6b; background:rgba(255,107,107,.1); }',
            '.session-del svg { width:12px; height: display:block; }',
            '.session-new { display:flex; align-items:center; gap:6px; padding:8px 10px; cursor:pointer; font-size:.75rem; color:var(--vscode-foreground); font-weight:500; border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); }',
            '.session-new:hover { background:var(--vscode-list-hoverBackgroundd2e); }',
            '.session-new svg { width:14px; height:14px; display:block; }',
            '.chat-main { display:grid; grid-template-rows:auto 1fr auto; height:100%; flex:1; min-width:0; }',
            '.chat-header { display:flex; align-items:center; gap:6px; padding:6px 10px; background:var(--vscode-list-hoverBackground,#2a2d2e); border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); cursor:pointer; user-select:none; }',
            '.chat-header:hover { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.chat-header .header-history { display:flex; align-items:center; justify-content:center; width:22px; height:22px; border-radius:3px; }',
            '.chat-header .header-history svg { width:14px; height:14px; color:#888; }',
            '.chat-header .pname { font-weight:600; font-size:0.85rem; color:#fff; }',
            '.chat-header .mname { font-size:0.75rem; color:#888; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }',
            '.chat-header .chev { font-size:0.7rem; color:#888; display:flex; align-items:center; }',
            '.chat-header .chev svg { width:12px; height:12px; }',
            '.chat-messages { overflow-y:auto; padding:12px; min-height:0; }',
            '.welcome { text-align:center; padding:2rem 1rem; }',
            '.welcome-icon { font-size:2.5rem; margin-bottom:0.5rem; }',
            '.welcome h2 { font-size:1rem; margin-bottom:0.5rem; color:#fff; }',
            '.welcome p { font-size:0.8rem; color:#888; margin-bottom:1rem; }',
            '.quick-actions { display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:1rem; }',
            '.quick-action { padding:8px; border:1px solid var(--vscode-widget-border,#3c3c3c); border-radius:4px; background:var(--vscode-list-hoverBackground,#2a2d2e); cursor:pointer; font-size:0.75rem; text-align:center; }',
            '.quick-action:hover { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.message { margin-bottom:12px; }',
            '.message-user { text-align:right; }',
            '.message-bubble { display:inline-block; max-width:85%; padding:8px 12px; border-radius:8px; font-size:0.8rem; line-height:1.5; word-wrap:break-word; }',
            '.message-user .message-bubble { background:#094771; color:#fff; }',
            '.message-assistant .message-bubble { background:#2a2d2e; }',
            '.input-area { padding:12px; border-top:1px solid var(--vscode-widget-border,#3c3c3c); background:var(--vscode-sideBar-background,#1e1e1e); }',
            '.input-wrapper { display:flex; align-items:center; gap:6px; background:var(--vscode-input-background,#3c3c3c); border:1px solid var(--vscode-widget-border,#3c3c3c); border-radius:6px; padding:6px 8px; }',
            'textarea { flex:1; background:transparent; border:none; color:var(--vscode-input-foreground,#ccc); font-size:0.8rem; resize:none; outline:none; min-height:20px; max-height:100px; }',
            '.send-btn { width:28px; height:28px; border-radius:4px; border:none; background:var(--vscode-button-background,#0e639c); color:#fff; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; }',
            '.send-btn:hover { background:var(--vscode-button-hoverBackground,#1177bb); }',
            '.send-btn svg { width:16px; height:16px; }',
            '.btn-primary { padding:10px 16px; border:none; border-radius:4px; background:var(--vscode-button-background,#0e639c); color:#fff; cursor:pointer; font-size:0.8rem; }',
            '.btn-primary:hover { background:var(--vscode-button-hoverBackground,#1177bb); }',
            '.typing { animation:blink 1s infinite; }',
            '@keyframes blink { 50% { opacity:0.4; } }'
        ].join('\n');
    }
    _getHtmlForWebview(webview) {
        const jsPath = path.join(this._extensionUri.fsPath, 'out', 'webview.js');
        let js = '';
        try {
            js = fs.readFileSync(jsPath, 'utf-8');
        }
        catch {
            js = 'console.error("webview bundle missing — run: npm run bundle");';
        }
        const nonce = this._getNonce();
        const body = this._getBodyForContext();
        return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>' + this._getSharedStyles() + '</style></head><body data-context="' + this._viewContext + '">' + body + '<script nonce="' + nonce + '">' + js + '</script></body></html>';
    }
    _getBodyForContext() {
        switch (this._viewContext) {
            case 'chat': {
                const chevron = this._icon('chevron');
                const send = this._icon('send');
                const history = this._icon('history');
                const plus = this._icon('plus');
                const trash = this._icon('trash');
                const sessions = this._sessions || [];
                const activeId = this._activeSessionId;
                const sessionsHtml = sessions.slice(0, 20).map(s => {
                    const isActive = s.id === activeId ? ' active' : '';
                    const date = new Date(s.updatedAt).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
                    return '<div class="session-item' + isActive + '" onclick="window._selectSession(\'' + s.id + '\')">' +
                        '<div class="session-info">' +
                        '<div class="session-name">' + s.name + '</div>' +
                        '<div class="session-meta">' + date + ' &middot; ' + s.providerId + '</div>' +
                        '</div>' +
                        '<button class="session-del" onclick="event.stopPropagation();window._deleteSession(\'' + s.id + '\')">' + trash + '</button>' +
                        '</div>';
                }).join('');
                return '<div class="chat-app">' +
                    '<div class="chat-sidebar" id="historyPanel">' +
                    '<div class="sidebar-header">' +
                    '<span class="sidebar-title">Historico</span>' +
                    '<button class="sidebar-btn" onclick="window._toggleSidebar()">' + history + '</button>' +
                    '</div>' +
                    '<div class="sidebar-list">' +
                    '<div class="session-new" onclick="window._newSession()">' + plus + 'Nova conversa</div>' +
                    sessionsHtml +
                    '</div>' +
                    '</div>' +
                    '<div class="chat-main">' +
                    '<div class="chat-header" id="headerBtn" title="Trocar provider">' +
                    '<div class="header-history" onclick="event.stopPropagation();window._toggleSidebar()">' + history + '</div>' +
                    '<span class="pname" id="headerProvider">OpenRouter</span>' +
                    '<span class="mname" id="headerModel">auto</span>' +
                    '<span class="chev">' + chevron + '</span>' +
                    '</div>' +
                    '<div class="chat-messages" id="chatContainer">' +
                    '<div class="welcome" id="welcome">' +
                    '<div class="welcome-icon">�</div>' +
                    '<h2>Bem-vindo ao XForge Code AI</h2>' +
                    '<p>Seu assistente</p>' +
                    '<div class="quick-actions">' +
                    '<div class="quick-action" onclick="sendQuick(\'Crie uma API\')">Nova API</div>' +
                    '<div class="quick-action" onclick="sendQuick(\'Analise o projeto\')">Analisar</div>' +
                    '<div class="quick-action" onclick="sendQuick(\'Me ajude com testes\')">Testes</div>' +
                    '<div class="quick-action" onclick="sendQuick(\'/help\')">Comandos</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '<div class="input-area">' +
                    '<div class="input-wrapper">' +
                    '<textarea id="messageInput" placeholder="Mensagem... (@ contexto, / comandos)" rows="1"></textarea>' +
                    '<button class="send-btn" id="sendBtn">' + send + '</button>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>';
            }
            case 'welcome':
                return '<div style="padding:2rem 1rem; text-align:center;"><div style="font-size:2.5rem; margin-bottom:1rem;">]</div><h2>Bem-vindo ao XForge</h2><p>Configure para comecar</p><button class="btn-primary" style="width:100%;" onclick="requestNewProvider()">Configurar</button></div>';
            case 'agent-manager':
                return '<div class="chat-container" id="chatContainer"><div class="welcome" id="welcome"><h2>Agent Manager</h2><p>Multi-agent orchestration</p><div class="quick-actions"><div class="quick-action" onclick="sendQuick("Criar novo agente")">Novo Agente</div><div class="quick-action" onclick="sendQuick("Listar agentes")">Listar</div></div></div></div>';
            case 'modes':
            case 'settings':
                return '<div class="chat-container" id="chatContainer"><div class="welcome" id="welcome"><h2>Settings</h2><p>Use Ctrl+Shift+P</p><div class="quick-actions"><div class="quick-action" onclick="requestNewProvider()">+ Novo Provider</div><div class="quick-action" onclick="requestProviderSwitch()">Trocar</div></div></div></div>';
            default:
                return '';
        }
    }
    async _handleSendMessage(text) {
        if (!text.trim() || !this._view)
            return;
        const userMessage = { id: this._generateId(), role: 'user', content: text, timestamp: new Date() };
        this._session.messages.push(userMessage);
        this._session.updatedAt = new Date();
        if (text.startsWith('/')) {
            const response = this._handleCommand(text);
            const assistantMessage = { id: this._generateId(), role: 'assistant', content: response, timestamp: new Date() };
            this._session.messages.push(assistantMessage);
            this._view.webview.postMessage({ type: 'streamStart', id: assistantMessage.id });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantMessage.id, content: response });
            return;
        }
        this._persistSession(text);
        await this._callProvider(text);
    }
    _handleCommand(cmd) {
        const c = cmd.toLowerCase().trim();
        switch (c) {
            case '/xforge': return '## XForge Code AI\n\nBem-vindo!';
            case '/help': return '## Comandos\n- /menu\n- /analisar';
            case '/analisar': return '## Analise\n\n*A implementar*';
            default: return 'Comando nao reconhecido: ' + cmd;
        }
    }
    async _callProvider(userText) {
        if (!this._view)
            return;
        const sel = this._globalState ? this._globalState.get('xforge.selection', null) : null;
        const providerId = sel && sel.providerId ? sel.providerId : 'openrouter';
        const model = sel && sel.model ? sel.model : 'auto';
        const apiKey = this._globalState ? (0, apiProvider_1.resolveApiKey)(providerId, this._globalState) : '';
        const baseUrl = this._globalState ? (0, apiProvider_1.resolveBaseUrl)(providerId, this._globalState) : undefined;
        console.log(`[xforge] callProvider: providerId=${providerId} model=${model} apiKey=${apiKey ? '[SET]' : '[EMPTY]'} baseUrl=${baseUrl || '[DEFAULT]'}`);
        const assistantId = this._generateId();
        const assistantMessage = { id: assistantId, role: 'assistant', content: '', timestamp: new Date() };
        this._session.messages.push(assistantMessage);
        this._session.updatedAt = new Date();
        this._view.webview.postMessage({ type: 'streamStart', id: assistantId });
        try {
            const messages = this._session.messages.slice(0, -1).map(m => ({ role: m.role, content: m.content }));
            await (0, apiProvider_1.callProvider)({
                providerId, model, messages, apiKey, baseUrl,
                onToken: (token) => {
                    assistantMessage.content += token;
                    this._appendAssistantMessage(assistantMessage.content);
                    this._view?.webview.postMessage({ type: 'streamToken', id: assistantId, token });
                }
            });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: assistantMessage.content });
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : 'Erro desconhecido';
            assistantMessage.content = '**Erro:** ' + msg;
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: assistantMessage.content });
        }
    }
    newSession() {
        this._session = this.createNewSession();
        if (this._view)
            this._view.webview.postMessage({ type: 'clearMessages' });
    }
    notifySelectionChanged() { this._pushSelectionToWebview(); }
    createNewSession() {
        return { id: this._generateId(), name: 'Session ' + new Date().toLocaleTimeString(), messages: [], createdAt: new Date(), updatedAt: new Date() };
    }
    _generateId() { return Math.random().toString(36).substring(2, 15); }
    _getNonce() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < 32; i++)
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        return result;
    }
    _icon(name, size = 14) {
        const refIcon = (0, icons_1.icon)(name, size);
        if (refIcon)
            return refIcon;
        const s = 'xmlns="http://www.w3.org/2000/svg" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
        const icons = {
            chevron: '<polyline points="6 9 12 15 18 9"></polyline>',
            send: '<polyline points="7 11 12 6 17 11"></polyline><line x1="12" y1="6" x2="12" y2="18"></line>',
        };
        return '<svg ' + s + '>' + (icons[name] || '') + '</svg>';
    }
    _startNewSession() {
        this._activeSessionId = null;
        this._session = this.createNewSession();
        if (this._view)
            this._view.webview.postMessage({ type: 'clearMessages' });
        this._refreshSidebar();
    }
    _loadSession(sessionId) {
        const session = this._sessions.find(s => s.id === sessionId);
        if (!session)
            return;
        this._activeSessionId = sessionId;
        this._session = this.createNewSession();
        if (this._globalState)
            (0, apiProvider_1.saveActiveSessionId)(this._globalState, sessionId);
        if (!this._view)
            return;
        this._view.webview.postMessage({ type: 'clearMessages' });
        for (const msg of session.messages) {
            const id = this._generateId();
            const role = (msg.role === 'user' || msg.role === 'assistant' ? msg.role : 'user');
            this._session.messages.push({ id, role, content: msg.content, timestamp: new Date(msg.timestamp) });
            this._view.webview.postMessage({ type: 'streamStart', id });
            this._view.webview.postMessage({ type: 'streamEnd', id, content: msg.content });
        }
        this._refreshSidebar();
    }
    _removeSession(sessionId) {
        if (!this._globalState)
            return;
        this._sessions = this._sessions.filter(s => s.id !== sessionId);
        (0, apiProvider_1.saveSessions)(this._globalState, this._sessions);
        if (this._activeSessionId === sessionId)
            this._activeSessionId = null;
        this._refreshSidebar();
    }
    _refreshSidebar() {
        if (!this._view)
            return;
        this._view.webview.postMessage({ type: 'sessionsUpdated' });
    }
    _persistSession(userMessage) {
        if (!this._globalState)
            return;
        const now = new Date().toISOString();
        if (!this._activeSessionId) {
            this._activeSessionId = 'sess_' + Date.now();
            const sel = (0, apiProvider_1.loadActiveSelection)(this._globalState);
            this._sessions.unshift({
                id: this._activeSessionId,
                name: userMessage.substring(0, 40),
                messages: [],
                providerId: sel.providerId,
                model: sel.model,
                createdAt: now,
                updatedAt: now
            });
        }
        const session = this._sessions.find(s => s.id === this._activeSessionId);
        if (session) {
            session.messages.push({ role: 'user', content: userMessage, timestamp: now });
            session.updatedAt = now;
        }
        (0, apiProvider_1.saveSessions)(this._globalState, this._sessions);
        (0, apiProvider_1.saveActiveSessionId)(this._globalState, this._activeSessionId);
    }
    _appendAssistantMessage(text) {
        if (!this._globalState || !this._activeSessionId)
            return;
        const session = this._sessions.find(s => s.id === this._activeSessionId);
        if (session) {
            session.messages.push({ role: 'assistant', content: text, timestamp: new Date().toISOString() });
            session.updatedAt = new Date().toISOString();
            (0, apiProvider_1.saveSessions)(this._globalState, this._sessions);
        }
    }
    dispose() {
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x)
                x.dispose();
        }
    }
}
exports.ChatViewProvider = ChatViewProvider;
ChatViewProvider.viewType = 'xforge.chatView';
class WelcomeViewProvider {
    resolveWebviewView(webviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{display:flex;flex-direction:column;height:100vh;align-items:center;justify-content:center;background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:1rem;text-align:center}h2{margin-bottom:.5rem}p{color:#888;margin-bottom:1rem}.btn{padding:8px 16px;border:none;border-radius:4px;background:#0e639c;color:#fff;cursor:pointer}</style></head><body><h2>Bem-vindo ao XForge</h2><p>Configure seu provider</p><button class="btn" id="btn">Configurar agora</button><script>const vscode=acquireVsCodeApi();document.getElementById("btn").addEventListener("click",()=>vscode.postMessage({type:"openSettings"}));</script></body></html>';
        webviewView.webview.onDidReceiveMessage(msg => {
            if (msg.type === 'openSettings')
                vscode.commands.executeCommand('xforge.configureProvider');
        });
    }
}
exports.WelcomeViewProvider = WelcomeViewProvider;
WelcomeViewProvider.viewType = 'xforge.welcomeView';
class AgentManagerViewProvider {
    resolveWebviewView(webviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{display:flex;flex-direction:column;height:100vh;align-items:center;justify-content:center;background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:1rem;text-align:center}h2{margin-bottom:.5rem}p{color:#888}</style></head><body><h2>Agent Manager</h2><p>Multi-agent orchestration</p></body></html>';
    }
}
exports.AgentManagerViewProvider = AgentManagerViewProvider;
AgentManagerViewProvider.viewType = 'xforge.agentManagerView';
class SettingsViewProvider {
    constructor(_globalState) {
        this._globalState = _globalState;
    }
    resolveWebviewView(webviewView) {
        webviewView.webview.options = { enableScripts: true };
        const { loadSavedProviders, loadActiveSelection } = require('../services/apiProvider');
        const saved = loadSavedProviders(this._globalState);
        const sel = loadActiveSelection(this._globalState);
        const cards = saved.filter((p) => p.enabled).map((p) => {
            const isActive = p.id === sel.providerId;
            const keyMask = p.apiKey && p.apiKey.length > 4 ? ('...' + p.apiKey.slice(-4)) : '--';
            return '<div class="card' + (isActive ? ' card-active' : '') + '" style="padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer;"><div style="display:flex;justify-content:space-between;"><span style="font-weight:600;font-size:.85rem;">' + (isActive ? 'ok ' : '') + p.label + '</span><span style="font-size:.7rem;color:#888;">' + keyMask + '</span></div><div style="font-size:.75rem;color:#888;margin-top:4px;">' + (isActive ? ('model: ' + sel.model) : 'clique p/ ativar') + '</div></div>';
        }).join('');
        const emptyHtml = '<div style="text-align:center;padding:2rem;color:#888;"><p>Sem providers</p><p style="font-size:.7rem">Ctrl+Shift+P -> XForge: Configurar Provider</p></div>';
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:12px}h3{font-size:.9rem;color:#fff;margin:0 0 10px}.card-active{border-color:#22c55e!important;background:rgba(34,197,94,.05)}.btn{padding:6px 12px;border:none;border-radius:4px;background:var(--vscode-button-background,#0e639c);color:#fff;cursor:pointer;font-size:.75rem}.btn:hover{background:var(--vscode-button-hoverBackground,#1177bb)}.btn-secondary{background:transparent;border:1px solid var(--vscode-widget-border,#3c3c3c)}.actions{display:flex;gap:6px;margin-top:12px}</style></head><body><h3>Providers</h3>' + (cards || emptyHtml) + '<div class="actions"><button class="btn" onclick="vscode.postMessage({type:\'configure\'})">+Provider</button><button class="btn btn-secondary" onclick="vscode.postMessage({type:\'switch\'})">Trocar</button></div><script>const vscode=acquireVsCodeApi();</script></body></html>';
        webviewView.webview.onDidReceiveMessage(msg => {
            if (msg.type === 'configure')
                vscode.commands.executeCommand('xforge.configureProvider');
            if (msg.type === 'switch')
                vscode.commands.executeCommand('xforge.switchProvider');
        });
    }
}
exports.SettingsViewProvider = SettingsViewProvider;
SettingsViewProvider.viewType = 'xforge.settingsView';
class ModesViewProvider {
    resolveWebviewView(webviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:12px}.mc{padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer}.mc:hover{background:var(--vscode-list-hoverBackground,#2a2d2e)}.mn{font-weight:600;margin-bottom:4px}.md{font-size:.75rem;color:#888}</style></head><body><h3 style="font-size:.9rem;color:#fff;margin-bottom:12px">Modos</h3><div class="mc"><div class="mn">FAST</div><div class="md">Resposta rapida, custo alto</div></div><div class="mc"><div class="mn">CHEAP</div><div class="md">Baixo custo</div></div><div class="mc"><div class="mn">DEEP</div><div class="md">Reasoning profundo</div></div><div class="mc"><div class="mn">ENTERPRISE</div><div class="md">Qualidade maxima</div></div><div class="mc"><div class="mn">OFFLINE</div><div class="md">Local, sem cloud</div></div></body></html>';
    }
}
exports.ModesViewProvider = ModesViewProvider;
ModesViewProvider.viewType = 'xforge.modesView';
//# sourceMappingURL=ChatViewProvider.js.map