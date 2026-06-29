import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { callProvider, resolveApiKey, resolveBaseUrl, loadActiveSelection, StoredProvider, getProviderConfig, SessionData, loadSessions, saveSessions, loadActiveSessionId, saveActiveSessionId } from '../services/apiProvider';

export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}

export interface Session {
    id: string;
    name: string;
    messages: Message[];
    createdAt: Date;
    updatedAt: Date;
}

type ViewContext = 'chat' | 'welcome' | 'agent-manager' | 'settings' | 'modes';

export class ChatViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.chatView';
    private _view?: vscode.WebviewView;
    private _session: Session;
    private _disposables: vscode.Disposable[] = [];
    private _viewContext: ViewContext = 'chat';
    private _sessions: SessionData[] = [];
    private _activeSessionId: string | null = null;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        viewContext: ViewContext = 'chat',
        private readonly _globalState?: vscode.Memento
    ) {
        this._session = this.createNewSession();
        this._viewContext = viewContext;
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        _ctx: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        webviewView.webview.onDidReceiveMessage(
            (msg) => {
                switch (msg.type) {
                    case 'sendMessage': this._handleSendMessage(msg.text); break;
                    case 'newSession': this.newSession(); break;
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
            }, null, this._disposables
        );
        this._sessions = this._globalState ? loadSessions(this._globalState) : [];
        this._activeSessionId = this._globalState ? loadActiveSessionId(this._globalState) : null;
        this._pushSelectionToWebview();
    }

    private _pushSelectionToWebview(): void {
        if (!this._view || !this._globalState) return;
        const sel = loadActiveSelection(this._globalState);
        const cfg = getProviderConfig(sel.providerId);
        this._view.webview.postMessage({
            type: 'currentSelection',
            selection: {
                providerId: sel.providerId,
                providerName: cfg ? cfg.name : sel.providerId,
                model: sel.model
            }
        });
    }

    private _getSharedStyles(): string {
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
            '.sidebar-btn svg { width:14px; height:14px; }',
            '.sidebar-list { overflow-y:auto; height:calc(100% - 41px); }',
            '.session-item { display:flex; align-items:center; justify-content:space-between; padding:8px 10px; cursor:pointer; border-bottom:1px solid rgba(60,60,60,.3); }',
            '.session-item:hover { background:var(--vscode-list-hoverBackground,#2a2d2e); }',
            '.session-item.active { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.session-info { flex:1; min-width:0; }',
            '.session-name { font-size:.75rem; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }',
            '.session-meta { font-size:.65rem; color:#888; }',
            '.session-del { opacity:0; background:none; border:none; color:#888; cursor:pointer; padding:2px; border-radius:3px; }',
            '.session-item:hover .session-del { opacity:1; }',
            '.session-del:hover { color:#ff6b6b; }',
            '.session-del svg { width:12px; height:12px; }',
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

    private _getHtmlForWebview(webview: vscode.Webview): string {
        const jsPath = path.join(this._extensionUri.fsPath, 'out', 'webview.js');
        let js = '';
        try { js = fs.readFileSync(jsPath, 'utf-8'); }
        catch { js = 'console.error("webview bundle missing — run: npm run bundle");'; }
        const nonce = this._getNonce();
        const body = this._getBodyForContext();
        return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>' + this._getSharedStyles() + '</style></head><body data-context="' + this._viewContext + '">' + body + '<script nonce="' + nonce + '">' + js + '</script></body></html>';
    }

    private _getBodyForContext(): string {
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
                    const date = new Date(s.updatedAt).toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit' });
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
                            '<div class="session-item active" style="background:var(--vscode-list-hoverBackground,#2a2d2e);margin-bottom:4px;cursor:pointer" onclick="window._newSession()">' +
                                '<div class="session-info"><div class="session-name">+ Nova conversa</div></div>' +
                            '</div>' +
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

    private async _handleSendMessage(text: string) {
        if (!text.trim() || !this._view) return;
        const userMessage: Message = { id: this._generateId(), role: 'user', content: text, timestamp: new Date() };
        this._session.messages.push(userMessage);
        this._session.updatedAt = new Date();
        if (text.startsWith('/')) {
            const response = this._handleCommand(text);
            const assistantMessage: Message = { id: this._generateId(), role: 'assistant', content: response, timestamp: new Date() };
            this._session.messages.push(assistantMessage);
            this._view.webview.postMessage({ type: 'streamStart', id: assistantMessage.id });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantMessage.id, content: response });
            return;
        }
        this._persistSession(text);
        await this._callProvider(text);
    }

    private _handleCommand(cmd: string): string {
        const c = cmd.toLowerCase().trim();
        switch (c) {
            case '/xforge': return '## XForge Code AI\n\nBem-vindo!';
            case '/help': return '## Comandos\n- /menu\n- /analisar';
            case '/analisar': return '## Analise\n\n*A implementar*';
            default: return 'Comando nao reconhecido: ' + cmd;
        }
    }

    private async _callProvider(userText: string) {
        if (!this._view) return;
        const sel = this._globalState ? this._globalState.get<{ providerId: string; model: string }>('xforge.selection', null as any) : null;
        const providerId = sel && sel.providerId ? sel.providerId : 'openrouter';
        const model = sel && sel.model ? sel.model : 'auto';
        const apiKey = this._globalState ? resolveApiKey(providerId, this._globalState) : '';
        const baseUrl = this._globalState ? resolveBaseUrl(providerId, this._globalState) : undefined;
        console.log(`[xforge] callProvider: providerId=${providerId} model=${model} apiKey=${apiKey ? '[SET]' : '[EMPTY]'} baseUrl=${baseUrl || '[DEFAULT]'}`);
        const assistantId = this._generateId();
        const assistantMessage: Message = { id: assistantId, role: 'assistant', content: '', timestamp: new Date() };
        this._session.messages.push(assistantMessage);
        this._session.updatedAt = new Date();
        this._view.webview.postMessage({ type: 'streamStart', id: assistantId });
        try {
            const messages = this._session.messages.slice(0, -1).map(m => ({ role: m.role, content: m.content }));
            await callProvider({
                providerId, model, messages, apiKey, baseUrl,
                 onToken: (token) => {
                    assistantMessage.content += token;
                    this._appendAssistantMessage(assistantMessage.content);
                    this._view?.webview.postMessage({ type: 'streamToken', id: assistantId, token });
                 }
            });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: assistantMessage.content });
        } catch (err) {
            const msg = err instanceof Error ? err.message : 'Erro desconhecido';
            assistantMessage.content = '**Erro:** ' + msg;
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: assistantMessage.content });
        }
    }

    public newSession() {
        this._session = this.createNewSession();
        if (this._view) this._view.webview.postMessage({ type: 'clearMessages' });
    }

    public notifySelectionChanged() { this._pushSelectionToWebview(); }

    private createNewSession(): Session {
        return { id: this._generateId(), name: 'Session ' + new Date().toLocaleTimeString(), messages: [], createdAt: new Date(), updatedAt: new Date() };
    }

    private _generateId(): string { return Math.random().toString(36).substring(2, 15); }

    private _getNonce(): string {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < 32; i++) result += chars.charAt(Math.floor(Math.random() * chars.length));
        return result;
    }

    private _icon(name: string): string {
        const icons: Record<string, string> = {
            chevron: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
            send: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 11l5-5 5 5M12 6v12"/></svg>',
            plus: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
            history: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg>',
            trash: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/></svg>',
        };
        return icons[name] || '';
    }

    private _persistSession(userMessage: string): void {
        if (!this._globalState) return;
        const now = new Date().toISOString();
        if (!this._activeSessionId) {
            this._activeSessionId = 'sess_' + Date.now();
            const sel = loadActiveSelection(this._globalState);
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
        saveSessions(this._globalState, this._sessions);
        saveActiveSessionId(this._globalState, this._activeSessionId);
    }

    private _appendAssistantMessage(text: string): void {
        if (!this._globalState || !this._activeSessionId) return;
        const session = this._sessions.find(s => s.id === this._activeSessionId);
        if (session) {
            session.messages.push({ role: 'assistant', content: text, timestamp: new Date().toISOString() });
            session.updatedAt = new Date().toISOString();
            saveSessions(this._globalState, this._sessions);
        }
    }

    dispose() {
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) x.dispose();
        }
    }
}


export class WelcomeViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.welcomeView';
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{display:flex;flex-direction:column;height:100vh;align-items:center;justify-content:center;background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:1rem;text-align:center}h2{margin-bottom:.5rem}p{color:#888;margin-bottom:1rem}.btn{padding:8px 16px;border:none;border-radius:4px;background:#0e639c;color:#fff;cursor:pointer}</style></head><body><h2>Bem-vindo ao XForge</h2><p>Configure seu provider</p><button class="btn" id="btn">Configurar agora</button><script>const vscode=acquireVsCodeApi();document.getElementById("btn").addEventListener("click",()=>vscode.postMessage({type:"openSettings"}));</script></body></html>';
        webviewView.webview.onDidReceiveMessage(msg => {
            if (msg.type === 'openSettings') vscode.commands.executeCommand('xforge.configureProvider');
        });
    }
}

export class AgentManagerViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.agentManagerView';
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{display:flex;flex-direction:column;height:100vh;align-items:center;justify-content:center;background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:1rem;text-align:center}h2{margin-bottom:.5rem}p{color:#888}</style></head><body><h2>Agent Manager</h2><p>Multi-agent orchestration</p></body></html>';
    }
}

export class SettingsViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.settingsView';
    constructor(private readonly _globalState: vscode.Memento) {}
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        const { loadSavedProviders, loadActiveSelection } = require('../services/apiProvider');
        const saved = loadSavedProviders(this._globalState);
        const sel = loadActiveSelection(this._globalState);
        const cards = saved.filter((p: StoredProvider) => p.enabled).map((p: StoredProvider) => {
            const isActive = p.id === sel.providerId;
            const keyMask = p.apiKey && p.apiKey.length > 4 ? ('...' + p.apiKey.slice(-4)) : '--';
             return '<div class="card' + (isActive ? ' card-active' : '') + '" style="padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer;"><div style="display:flex;justify-content:space-between;"><span style="font-weight:600;font-size:.85rem;">' + (isActive ? 'ok ' : '') + p.label + '</span><span style="font-size:.7rem;color:#888;">' + keyMask + '</span></div><div style="font-size:.75rem;color:#888;margin-top:4px;">' + (isActive ? ('model: ' + sel.model) : 'clique p/ ativar') + '</div></div>';
        }).join('');
        const emptyHtml = '<div style="text-align:center;padding:2rem;color:#888;"><p>Sem providers</p><p style="font-size:.7rem">Ctrl+Shift+P -> XForge: Configurar Provider</p></div>';
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:12px}h3{font-size:.9rem;color:#fff;margin:0 0 10px}.card-active{border-color:#22c55e!important;background:rgba(34,197,94,.05)}.btn{padding:6px 12px;border:none;border-radius:4px;background:var(--vscode-button-background,#0e639c);color:#fff;cursor:pointer;font-size:.75rem}.btn:hover{background:var(--vscode-button-hoverBackground,#1177bb)}.btn-secondary{background:transparent;border:1px solid var(--vscode-widget-border,#3c3c3c)}.actions{display:flex;gap:6px;margin-top:12px}</style></head><body><h3>Providers</h3>' + (cards || emptyHtml) + '<div class="actions"><button class="btn" onclick="vscode.postMessage({type:\'configure\'})">+Provider</button><button class="btn btn-secondary" onclick="vscode.postMessage({type:\'switch\'})">Trocar</button></div><script>const vscode=acquireVsCodeApi();</script></body></html>';
        webviewView.webview.onDidReceiveMessage(msg => {
            if (msg.type === 'configure') vscode.commands.executeCommand('xforge.configureProvider');
            if (msg.type === 'switch') vscode.commands.executeCommand('xforge.switchProvider');
        });
    }
}

export class ModesViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.modesView';
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{background:var(--vscode-editor-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:-apple-system,sans-serif;font-size:13px;padding:12px}.mc{padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer}.mc:hover{background:var(--vscode-list-hoverBackground,#2a2d2e)}.mn{font-weight:600;margin-bottom:4px}.md{font-size:.75rem;color:#888}</style></head><body><h3 style="font-size:.9rem;color:#fff;margin-bottom:12px">Modos</h3><div class="mc"><div class="mn">FAST</div><div class="md">Resposta rapida, custo alto</div></div><div class="mc"><div class="mn">CHEAP</div><div class="md">Baixo custo</div></div><div class="mc"><div class="mn">DEEP</div><div class="md">Reasoning profundo</div></div><div class="mc"><div class="mn">ENTERPRISE</div><div class="md">Qualidade maxima</div></div><div class="mc"><div class="mn">OFFLINE</div><div class="md">Local, sem cloud</div></div></body></html>';
    }
}
