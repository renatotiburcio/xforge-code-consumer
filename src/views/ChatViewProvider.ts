import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { callProvider, resolveApiKey, resolveBaseUrl, loadActiveSelection, getProviderConfig } from '../services/apiProvider';
import { icon } from '../webview/icons';
import { loadSessions, saveSessions, loadActiveId, saveActiveId, createSession, addMessageToSession, deleteSession, XforgeSession } from '../services/sessions';

// ==================== TYPES ====================
export interface XforgeProviderChatMessage {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}

export interface XforgeProviderSession {
    id: string;
    name: string;
    messages: XforgeProviderChatMessage[];
    createdAt: Date;
    updatedAt: Date;
}

type ViewContext = 'chat' | 'welcome' | 'agent-manager' | 'settings' | 'modes';

// ==================== CLEAN RESPONSE (stream-safe) ====================
const ENV_BLOCK_START = '<environment_details>';
const ENV_BLOCK_END = '</environment_details>';
const ENV_TAG_RE = /<\/?environment_details>/gi;
const ENV_KEY_LINE_RE = /^(Current time|Working directory|Workspace root|User Home Path|Active branch|Platform|Shell|OS|Default shell):.*$/gim;

function clean(text: string): string {
    if (!text) return '';
    let t = text;
    // Remove blocos completos
    t = t.replace(/<environment_details>[\s\S]*?<\/environment_details>/gi, '');
    // Remove tags isoladas
    t = t.replace(ENV_TAG_RE, '');
    // Remove linhas-chave
    t = t = t.replace(ENV_KEY_LINE_RE, '');
    // Colapsa 3+ newlines em 1
    t = t.replace(/\n{3,}/g, '\n\n');
    return t.trim();
}

// Buffer para blocos environment_details abertos mas nao fechados
let envBuffer = '';

function cleanStreamingToken(token: string): { output: string; complete: boolean } {
    envBuffer += token;
    // Se ha bloco completo, extrair e limpar
    const startIdx = envBuffer.indexOf(ENV_BLOCK_START);
    const endIdx = envBuffer.indexOf(ENV_BLOCK_END);
    
    if (startIdx >= 0 && endIdx > startIdx) {
        // Extrai tudo após o fechamento
        const after = envBuffer.substring(endIdx + ENV_BLOCK_END.length);
        envBuffer = '';
        return { output: clean(after), complete: true };
    }
    
    if (startIdx >= 0) {
        // Bloco aberto mas nao fechado — segura o output
        return { output: '', complete: false };
    }
    
    if (endIdx >= 0 && startIdx === -1) {
        // Fechamento sem abertura (caso estranho) — ignora
        envBuffer = '';
        return { output: '', complete: true };
    }
    
    // Sem bloco — safe pra output
    const output = clean(envBuffer);
    envBuffer = '';
    return { output, complete: true };
}

// ==================== PROVIDER ====================
export class ChatViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.chatView';
    private _view?: vscode.WebviewView;
    private _session: XforgeProviderSession;
    private _disposables: vscode.Disposable[] = [];
    private _viewContext: ViewContext = 'chat';
    private _sessions: XforgeSession[] = [];
    private _activeSessionId: string | null = null;
    private _currentStreamId: string | null = null;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        viewContext: ViewContext = 'chat',
        private readonly _globalState?: vscode.Memento
    ) {
        this._session = this._newSession();
        this._viewContext = viewContext;
    }

    private _newSession(): XforgeProviderSession {
        return {
            id: 'local_' + Date.now(),
            name: 'Nova conversa',
            messages: [],
            createdAt: new Date(),
            updatedAt: new Date()
        };
    }

    private _genId(): string {
        return Math.random().toString(36).substring(2, 10);
    }

    private _nonce(): string {
        return Math.random().toString(36).substring(2, 34);
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        _ctx: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        console.log('[xforge] resolve');
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri, vscode.Uri.file(path.dirname(this._extensionUri.fsPath))] };
        
        this._sessions = loadSessions();
        this._activeSessionId = loadActiveId();
        console.log('[xforge] carregou', this._sessions.length, 'sessões, activeId=', this._activeSessionId);

        webviewView.webview.html = this._getHtml(webviewView.webview);
        
        webviewView.webview.onDidReceiveMessage(async (msg) => {
            console.log('[xforge] msg=' + msg.type);
            switch (msg.type) {
                case 'sendMessage':
                    await this._onSendMessage(String(msg.text || ''));
                    break;
                case 'newSession':
                    this._onNewSession();
                    break;
                case 'selectSession':
                    this._onSelectSession(String(msg.sessionId));
                    break;
                case 'deleteSession':
                    this._onDeleteSession(String(msg.sessionId));
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
                        m.configureProviderCommand(this._globalState, () => this._notifySelection());
                    }
                    break;
            }
        }, null, this._disposables);

        this._pushSelection();
    }

    private _notifySelection(): void {
        if (!this._view) return;
        const sel = loadActiveSelection(this._globalState!);
        const cfg = getProviderConfig(sel.providerId);
        this._view.webview.postMessage({ type: 'currentSelection', selection: { providerId: sel.providerId, providerName: cfg ? cfg.name : sel.providerId, model: sel.model } });
    }

    private _pushSelection(): void {
        this._notifySelection();
    }

    private async _onSendMessage(text: string) {
        console.log('[xforge] sendMessage:', clean(text).substring(0, 50));
        const cleanText = clean(text);
        if (!cleanText.trim() || !this._view) return;

        if (cleanText.startsWith('/')) {
            const response = this._handleCommand(cleanText);
            this._session.messages.push({ id: this._genId(), role: 'user', content: cleanText, timestamp: new Date() });
            this._session.messages.push({ id: this._genId(), role: 'assistant', content: response, timestamp: new Date() });
            this._view.webview.postMessage({ type: 'streamStart', id: 'cmd_' + Date.now() });
            this._view.webview.postMessage({ type: 'streamEnd', id: 'cmd_' + Date.now(), content: response });
            return;
        }

        const userMsg = { id: this._genId(), role: 'user' as const, content: cleanText, timestamp: new Date() };
        this._session.messages.push(userMsg);
        this._session.updatedAt = new Date();

        const sel = loadActiveSelection(this._globalState!);
        const active = this._sessions.find(s => s.id === this._activeSessionId);
        if (!active) {
            // Criar sessão nova automaticamente na primeira mensagem
            const created = createSession(cleanText.substring(0, 40), sel.providerId, sel.model);
            this._activeSessionId = created.id;
            saveActiveId(this._activeSessionId);
            this._sessions = loadSessions();
            console.log('[xforge] criou sessão:', created.id);
        } else {
            addMessageToSession(this._activeSessionId!, { role: 'user', content: cleanText, timestamp: new Date().toISOString() });
        }
        this._refreshSidebar();

        // Chama provider
        const assistantId = 'ast_' + Date.now();
        this._currentStreamId = assistantId;
        const assistantMessage = { id: assistantId, role: 'assistant' as const, content: '', timestamp: new Date() };
        this._session.messages.push(assistantMessage);
        this._view.webview.postMessage({ type: 'streamStart', id: assistantId });

        try {
            const messages = this._session.messages.slice(0, -1).map(m => ({ role: m.role === 'user' || m.role === 'assistant' ? m.role : 'user', content: m.content }));
            const cfg = getProviderConfig(sel.providerId);
            const apiKey = resolveApiKey(sel.providerId, this._globalState!);
            const baseUrl = sel.providerId === 'ollama' ? undefined : undefined;
            await callProvider({
                providerId: sel.providerId,
                model: sel.model,
                messages,
                apiKey: apiKey,
                baseUrl: undefined,
                onToken: (token) => {
                    assistantMessage.content += token;
                    const result = cleanStreamingToken(token);
                    if (result.output) {
                        this._view?.webview.postMessage({ type: 'streamToken', id: assistantId, token: result.output });
                    }
                }
            });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: clean(assistantMessage.content) });
            if (this._activeSessionId) {
                addMessageToSession(this._activeSessionId, { role: 'assistant', content: clean(assistantMessage.content), timestamp: new Date().toISOString() });
            }
        } catch (err) {
            const msg = err instanceof Error ? err.message : 'Erro desconhecido';
            const errMsg = '**Erro:** ' + msg + ' (provider: ' + sel.providerId + ')';
            assistantMessage.content = errMsg;
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantId, content: errMsg });
            if (this._activeSessionId) {
                addMessageToSession(this._activeSessionId, { role: 'assistant', content: errMsg, timestamp: new Date().toISOString() });
            }
        }
        this._currentStreamId = null;
        this._sessions = loadSessions();
        this._refreshSidebar();
    }

    private _onNewSession() {
        this._activeSessionId = null;
        saveActiveId(null);
        this._session = this._newSession();
        if (this._view) {
            this._view.webview.postMessage({ type: 'clearMessages' });
        }
        this._refreshSidebar();
    }

    private _onSelectSession(id: string) {
        const session = this._sessions.find(s => s.id === id);
        if (!session) return;
        this._activeSessionId = id;
        saveActiveId(id);
        this._session = this._newSession();
        if (!this._view) return;
        this._view.webview.postMessage({ type: 'clearMessages' });
        for (const msg of session.messages) {
            const mid = this._genId();
            this._session.messages.push({ id: mid, role: msg.role, content: msg.content, timestamp: new Date(msg.timestamp) });
            this._view.webview.postMessage({ type: 'streamStart', id: mid });
            this._view.webview.postMessage({ type: 'streamEnd', id: mid, content: clean(msg.content) });
        }
        this._refreshSidebar();
    }

    private _onDeleteSession(id: string) {
        deleteSession(id);
        if (this._activeSessionId === id) {
            this._activeSessionId = null;
            saveActiveId(null);
        }
        this._sessions = loadSessions();
        this._refreshSidebar();
    }

    private _refreshSidebar() {
        if (!this._view) return;
        console.log('[xforge] refresh sidebar sessions=', this._sessions.length, 'active=', this._activeSessionId);
        const trash = this._icon('trash', 12);
        const plus = this._icon('plus', 14);
        const activeId = this._activeSessionId;

        const sessionsHtml = this._sessions.slice(0, 30).map(s => {
            const isActive = s.id === activeId ? ' active' : '';
            const date = new Date(s.updatedAt).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
            const name = (s.name || 'Sem nome').replace(/[<>&]/g, '');
            return '<div class="session-item' + isActive + '" onclick="_xfSelectSession(\'' + s.id + '\')">' +
                '<div class="session-info">' +
                    '<div class="session-name">' + name + '</div>' +
                    '<div class="session-meta">' + date + ' | ' + s.providerId + '</div>' +
                '</div>' +
                '<button class="session-del" onclick="event.stopPropagation();_xfDeleteSession(\'' + s.id + '\')">' + trash + '</button>' +
            '</div>';
        }).join('');

        const sidebarHtml = '<div class="session-new" onclick="_xfNewSession()">' + plus + ' Nova conversa</div>' + sessionsHtml;
        this._view?.webview.postMessage({ type: 'refreshSidebar', html: sidebarHtml });
    }

    private _handleCommand(cmd: string): string {
        const c = cmd.toLowerCase().trim();
        switch (c) {
            case '/help':
            case '/ajuda':
                return '## Comandos\n\n' +
                    '- `/help` — mostra esta lista\n' +
                    '- `/analisar` — analisa o projeto\n' +
                    '- `/limpar` — limpa o chat\n' +
                    '- `/provedor` — mostra provider ativo\n' +
                    '- `/configurar` — abre config provider\n' +
                    '- `/novo` — nova sessão';
            case '/analisar':
            case '/analyze': {
                const folders = vscode.workspace.workspaceFolders;
                if (!folders) return '## Análise\n\nNenhum workspace aberto.';
                const root = folders[0].uri.fsPath;
                let hints: string[] = [];
                try {
                    const files = fs.readdirSync(root);
                    if (files.includes('package.json')) hints.push('Node.js / npm');
                    if (files.includes('requirements.txt') || files.includes('pyproject.toml')) hints.push('Python');
                    if (files.includes('go.mod')) hints.push('Go');
                    if (files.includes('Cargo.toml')) hints.push('Rust');
                    if (files.includes('.sln') || files.includes('*.csproj')) hints.push('.NET');
                    } catch { /* noop */ }
                return '## Análise\n\n**Root:** `' + root + '`\n**Stack:** ' + (hints.join(', ') || 'desconhecida');
            }
            case '/limpar':
                this._onNewSession();
                return 'Chat limpo.';
            case '/provider':
            case '/provedor': {
                const sel = loadActiveSelection(this._globalState!);
                const cfg = getProviderConfig(sel.providerId);
                const key = resolveApiKey(sel.providerId, this._globalState!);
                return '## Provider Ativo\n\n**Provider:** ' + (cfg ? cfg.name : sel.providerId) + '\n**Modelo:** ' + sel.model + '\n**API Key:** ' + (key ? 'Configurada' : 'NÃO CONFIGURADA');
            }
            case '/configurar':
                if (this._globalState) {
                    const m = require('../commands/providerCommands');
                    setTimeout(() => m.configureProviderCommand(this._globalState!, () => this._notifySelection()), 50);
                }
                return 'Abrindo configuração...';
            case '/novo':
                this._onNewSession();
                return 'Nova sessão iniciada.';
            default:
                return 'Comando desconhecido: `' + cmd + '`\n\nUse `/help` para ver comandos.';
        }
    }

    private _getHtml(webview: vscode.Webview): string {
        const jsPath = path.join(this._extensionUri.fsPath, 'out', 'webview.js');
        let js = '';
        try { js = fs.readFileSync(jsPath, 'utf-8'); } catch { /* noop */ }
        const nonce = this._nonce();
        const body = this._getBody();

        return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><style>' +
            this._getCss() +
            '</style></head><body data-context="' + this._viewContext + '">' +
            body +
            '<script nonce="' + nonce + '">' + js + '</script>' +
            '</body></html>';
    }

    private _getCss(): string {
        return [
            '* { margin:0; padding:0; box-sizing:border-box; }',
            'html, body { height:100%; width:100%; overflow:hidden; }',
            'body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto; font-size:13px; background:var(--vscode-sideBar-background,#1e1e1e); color:var(--vscode-foreground,#ccc); }',
            '.chat-app { display:flex; height:100%; width:100%; }',
            '.chat-sidebar { width:0; overflow:hidden; background:var(--vscode-editor-background,#1e1e1e); border-right:1px solid var(--vscode-widget-border,#3c3c3c); transition:width .2s; flex-shrink:0; display:flex; flex-direction:column; }',
            '.chat-sidebar.open { width:220px; }',
            '.sidebar-header { display:flex; align-items:center; justify-content:space-between; padding:6px 8px; border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); flex-shrink:0; }',
            '.sidebar-title { font-size:.75rem; font-weight:600; color:#fff; }',
            '.sidebar-btn { background:none; border:none; color:#888; cursor:pointer; padding:2px; border-radius:3px; }',
            '.sidebar-btn:hover { background:var(--vscode-list-hoverBackground); color:#fff; }',
            '.sidebar-list { overflow-y:auto; flex:1; }',
            '.session-new { padding:6px 10px; cursor:pointer; font-size:.75rem; color:#888; border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); display:flex; align-items:center; gap:6px; }',
            '.session-new:hover { background:var(--vscode-list-hoverBackground); color:#fff; }',
            '.session-item { display:flex; align-items:center; padding:5px 10px; cursor:pointer; border-bottom:1px solid rgba(60,60,60,.3); }',
            '.session-item:hover { background:var(--vscode-list-hoverBackground,#2a2d2e); }',
            '.session-item.active { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.session-info { flex:1; min-width:0; }',
            '.session-name { font-size:.75rem; color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }',
            '.session-meta { font-size:.65rem; color:#666; }',
            '.session-del { opacity:0; background:none; border:none; color:#888; cursor:pointer; padding:2px; border-radius:3px; flex-shrink:0; }',
            '.session-item:hover .session-del { opacity:1; }',
            '.session-del:hover { color:#ff6b6b; }',
            '.chat-main { display:grid; grid-template-rows:auto 1fr auto; height:100%; flex:1; min-width:0; overflow:hidden; }',
            '.chat-header { display:flex; align-items:center; gap:6px; padding:6px 10px; background:var(--vscode-list-hoverBackground,#2a2d2e); border-bottom:1px solid var(--vscode-widget-border,#3c3c3c); cursor:pointer; user-select:none; flex-shrink:0; }',
            '.chat-header:hover { background:var(--vscode-list-activeSelectionBackground,#094771); }',
            '.header-history { display:flex; align-items:center; justify-content:center; width:22px; height:22px; border-radius:3px; }',
            '.header-history svg { width:14px; height:14px; color:#888; }',
            '.chat-header .pname { font-weight:600; font-size:0.8rem; color:#fff; }',
            '.chat-header .mname { font-size:0.7rem; color:#888; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }',
            '.chat-header .chev { display:flex; align-items:center; color:#888; }',
            '.chat-header .chev svg { width:12px; height:12px; }',
            '.chat-messages { overflow-y:auto; padding:10px; min-height:0; flex:1; }',
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
            '.input-area { padding:10px; border-top:1px solid var(--vscode-widget-border,#3c3c3c); background:var(--vscode-sideBar-background,#1e1e1e); flex-shrink:0; }',
            '.input-wrapper { display:flex; align-items:center; gap:6px; background:var(--vscode-input-background,#3c3c3c); border:1px solid var(--vscode-widget-border,#3c3c3c); border-radius:6px; padding:6px 8px; }',
            'textarea { flex:1; background:transparent; border:none; color:var(--vscode-input-foreground,#ccc); font-size:0.8rem; resize:none; outline:none; min-height:20px; max-height:100px; }',
            '.send-btn { width:28px; height:28px; border-radius:4px; border:none; background:var(--vscode-button-background,#0e639c); color:#fff; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; }',
            '.send-btn:hover { background:var(--vscode-button-hoverBackground,#1177bb); }',
            '.btn-primary { padding:10px 16px; border:none; border-radius:4px; background:var(--vscode-button-background,#0e639c); color:#fff; cursor:pointer; font-size:0.8rem; }',
            '.btn-primary:hover { background:var(--vscode-button-hoverBackground,#1177bb); }',
            '.typing { animation:blink 1s infinite; }',
            '@keyframes blink { 50% { opacity:0.4; } }',
        ].join('\n');
    }

    private _getBody(): string {
        const chevron = this._icon('chevron', 12);
        const send = this._icon('send', 16);
        const history = this._icon('history', 14);
        const plus = this._icon('plus', 14);

        return '<div class="chat-app">' +
            '<div class="chat-sidebar" id="historyPanel">' +
                '<div class="sidebar-header">' +
                    '<span class="sidebar-title">Historico</span>' +
                    '<button class="sidebar-btn" onclick="_xfToggleSidebar()">' + history + '</button>' +
                '</div>' +
                '<div class="sidebar-list" id="sidebarList">' +
                    '<div class="session-new" onclick="_xfNewSession()">' + plus + ' Nova conversa</div>' +
                '</div>' +
            '</div>' +
            '<div class="chat-main">' +
                '<div class="chat-header" id="headerBtn" title="Trocar provider (Ctrl+Shift+P)">' +
                    '<div class="header-history" onclick="event.stopPropagation();_xfToggleSidebar()">' + history + '</div>' +
                    '<span class="pname" id="headerProvider">OpenRouter</span>' +
                    '<span class="mname" id="headerModel">auto</span>' +
                    '<span class="chev">' + chevron + '</span>' +
                '</div>' +
                '<div class="chat-messages" id="chatContainer">' +
                    '<div class="welcome" id="welcome">' +
                        '<div class="welcome-icon">X</div>' +
                        '<h2>Bem-vindo ao XForge Code AI</h2>' +
                        '<p>Seu assistente de codigo inteligente</p>' +
                        '<div class="quick-actions">' +
                            '<div class="quick-action" onclick="sendQuick(\'Crie uma API de pagamentos\')">Nova API</div>' +
                            '<div class="quick-action" onclick="sendQuick(\'Analise o projeto\')">Analisar</div>' +
                            '<div class="quick-action" onclick="sendQuick(\'Me ajude com testes\')">Testes</div>' +
                            '<div class="quick-action" onclick="sendQuick(\'/help\')">Comandos</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="input-area">' +
                    '<div class="input-wrapper">' +
                        '<textarea id="messageInput" placeholder="Mensagem... (@file, @selection ou /help)" rows="1"></textarea>' +
                        '<button class="send-btn" id="sendBtn">' + send + '</button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            '</div>';
    }

    private _icon(name: string, size = 14): string {
        const refFile = path.resolve(__dirname, '..', 'webview', 'icons', name + '.svg');
        try {
            let content = fs.readFileSync(refFile, 'utf-8').trim();
            content = content.replace(/^<svg /, '<svg width="' + size + '" height="' + size + '" ');
            return content;
        } catch {
            return '<svg xmlns="http://www.w3.org/2000/svg" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>';
        }
    }

    dispose() {
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}

// ==================== Other ViewProviders ====================
export class WelcomeViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.welcomeView';

    constructor(private _extensionUri: vscode.Uri) {}

    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        webviewView.webview.html = this._getWelcomeHtml(webviewView.webview);
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        webviewView.webview.html = this._getWelcomeHtml(webviewView.webview);
        webviewView.webview.onDidReceiveMessage((m) => {
            if (m.type === 'newSession') vscode.commands.executeCommand('xforge.openChat');
            if (m.type === 'openSettings') vscode.commands.executeCommand('xforge.configureProvider');
            if (m.type === 'openHistory') vscode.commands.executeCommand('xforge.chatView.focus');
        });
    }

    private _getWelcomeHtml(webview: vscode.Webview): string {
        return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2b3a 100%);
    color: #e6edf3;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow: hidden;
}
.welcome-container {
    text-align: center;
    max-width: 320px;
    width: 100%;
}
.logo {
    width: 100px;
    height: 100px;
    margin: 0 auto 1.5rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #1c2b40 0%, #0d1117 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.logo img {
    width: 72px;
    height: 72px;
}
.logo-placeholder {
    font-size: 2.5rem;
    font-weight: bold;
    color: #fff;
}
h1 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.5rem;
}
.tagline {
    font-size: 0.85rem;
    color: #8b949e;
    margin-bottom: 2rem;
}
.options {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.option {
    padding: 12px 16px;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 10px;
}
.option:hover {
    background: #30363d;
    border-color: #58a6ff;
}
.option-icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: #58a6ff;
}
.option-icon svg {
    width: 100%;
    height: 100%;
}
.option-text {
    flex: 1;
}
.option-title {
    font-size: 0.85rem;
    font-weight: 500;
    color: #e6edf3;
}
.option-desc {
    font-size: 0.7rem;
    color: #8b949e;
    margin-top: 2px;
}
</style>
</head>
<body>
<div class="welcome-container">
    <div class="logo">
        <span class="logo-placeholder">XF</span>
    </div>
    <h1>XForge Code AI</h1>
    <p class="tagline">Seu assistente de código inteligente</p>
    <div class="options">
        <div class="option" onclick="_xfAction('newSession')">
            <div class="option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
            </div>
            <div class="option-text">
                <div class="option-title">Nova Sessão</div>
                <div class="option-desc">Iniciar uma conversa com IA</div>
            </div>
        </div>
        <div class="option" onclick="_xfAction('openProject')">
            <div class="option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/></svg>
            </div>
            <div class="option-text">
                <div class="option-title">Abrir Projeto</div>
                <div class="option-desc">Analisar projeto existente</div>
            </div>
        </div>
        <div class="option" onclick="_xfAction('openDocs')">
            <div class="option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 20.477 5.754 21 7.5 21s3.332-.477 4.5-1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 19.477 18.247 19 16.5 19c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <div class="option-text">
                <div class="option-title">Com Documentação</div>
                <div class="option-desc">Analisar docs/URLs junto</div>
            </div>
        </div>
        <div class="option" onclick="_xfAction('openHistory')">
            <div class="option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg>
            </div>
            <div class="option-text">
                <div class="option-title">Sessões Recentes</div>
                <div class="option-desc">Continuar conversa anterior</div>
            </div>
        </div>
        <div class="option" onclick="_xfAction('openSettings')">
            <div class="option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06A1.65 1.65 0 004.6 15a1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06A1.65 1.65 0 009 4.6a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09c0 .67.39 1.27 1 1.51a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06A1.65 1.65 0 0019.4 9c.24.6.84 1 1.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
            </div>
            <div class="option-text">
                <div class="option-title">Configurar</div>
                <div class="option-desc">Providers, modelos e preferências</div>
            </div>
        </div>
    </div>
</div>
<script>
const vscode = acquireVsCodeApi();
function _xfAction(action) { vscode.postMessage({ type: action }); }
</script>
</body>
</html>`;
    }
}

export class AgentManagerViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.agentManagerView';
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><style>body{display:flex;align-items:center;justify-content:center;height:100vh;background:var(--vscode-sideBar-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:sans-serif;font-size:13px}</style></head><body><h2>Agent Manager</h2><p>Em breve</p></body></html>';
    }
}

export class SettingsViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.settingsView';
    constructor(private readonly _gs: vscode.Memento) {}
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        const cfg = vscode.workspace.getConfiguration('xforge');
        const provider = cfg.get<string>('provider', 'openrouter');
        const model = cfg.get<string>('model', 'auto');
        webviewView.webview.html = `<!DOCTYPE html><html><head><style>body{background:var(--vscode-sideBar-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:sans-serif;font-size:13px;padding:12px}.row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #333}.row label{font-size:.8rem}.row select{background:#333;color:#ccc;border:1px solid #555;border-radius:3px;padding:3px 6px;font-size:.8rem}.btn{margin-top:10px;padding:6px 12px;border:none;border-radius:4px;background:#0e639c;color:#fff;cursor:pointer;font-size:.8rem}</style></head><body><h3 style="margin:0 0 10px">Provider</h3><div class="row"><label>Provider</label><select id="p"><option value="openrouter" ${provider==='openrouter'?'selected':''}>OpenRouter</option><option value="openai" ${provider==='openai'?'selected':''}>OpenAI</option><option value="anthropic" ${provider==='anthropic'?'selected':''}>Anthropic</option><option value="ollama" ${provider==='ollama'?'selected':''}>Ollama</option></select></div><div class="row"><label>Modelo</label><select id="m"><option value="auto" ${model==='auto'?'selected':''}>auto</option><option value="gpt-4o-mini" ${model==='gpt-4o-mini'?'selected':''}>GPT-4o Mini</option><option value="claude-3-haiku-20240307" ${model==='claude-3-haiku-20240307'?'selected':''}>Claude Haiku</option><option value="llama3" ${model==='llama3'?'selected':''}>Llama 3</option></select></div><button class="btn" id="sv">Salvar</button><script>const vs=acquireVsCodeApi();document.getElementById("sv").onclick=()=>{vs.postMessage({type:"save",provider:document.getElementById("p").value,model:document.getElementById("m").value})}</script></body></html>`;
        webviewView.webview.onDidReceiveMessage((msg) => {
            if (msg.type === 'save') {
                const sel = loadActiveSelection(this._gs);
                if (msg.provider !== sel.providerId || msg.model !== sel.model) {
                    import('../services/apiProvider').then(m => m.saveActiveSelection(this._gs, msg.provider, msg.model));
                    vscode.window.showInformationMessage(`Salvo: ${msg.provider}/${msg.model}`);
                }
            }
        });
    }
}

export class ModesViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.modesView';
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = '<!DOCTYPE html><html><head><style>body{background:var(--vscode-sideBar-background,#1e1e1e);color:var(--vscode-foreground,#ccc);font-family:sans-serif;font-size:13px;padding:12px}.card{padding:10px;border:1px solid #333;border-radius:6px;margin-bottom:8px;cursor:pointer}.card:hover{background:#2a2d2e}.cn{font-weight:600;margin-bottom:4px}.cd{font-size:.75rem;color:#888}</style></head><body><h3 style="margin:0 0 10px">Modos</h3><div class="card"><div class="cn">FAST</div><div class="cd">Resposta rapida, custo alto</div></div><div class="card"><div class="cn">CHEAP</div><div class="cd">Baixo custo, qualidade padrao</div></div><div class="card"><div class="cn">DEEP</div><div class="cd">Reasoning profundo</div></div><div class="card"><div class="cn">ENTERPRISE</div><div class="cd">Qualidade maxima, compliance</div></div><div class="card"><div class="cn">OFFLINE</div><div class="cd">Modelo local, sem cloud</div></div></body></html>';
    }
}

export class HistoryViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.historyView';
    constructor(private _gs: vscode.Memento) {}

    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        this._render(webviewView);
        webviewView.webview.onDidReceiveMessage((msg) => {
            if (msg.type === 'selectSession') {
                vscode.window.showInformationMessage('Sessão: ' + msg.sessionId);
            }
            if (msg.type === 'deleteSession') {
                vscode.window.showInformationMessage('Deletar: ' + msg.sessionId);
            }
        });
    }

    private _render(webviewView: vscode.WebviewView) {
        const sessions = loadSessions();
        const list = sessions.slice(0, 20).map(s => {
            const date = new Date(s.updatedAt).toLocaleDateString('pt-BR');
            const time = new Date(s.updatedAt).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
            const name = (s.name || 'Sem nome').replace(/[<>&]/g, '');
            const msgCount = s.messages ? s.messages.length : 0;
            return '<div class="session-row" onclick="_xfSelectSession(\'' + s.id + '\')">' +
                '<div class="session-main">' +
                    '<div class="session-title">' + name + '</div>' +
                    '<div class="session-sub">' + date + ' · ' + time + ' · ' + msgCount + ' msgs</div>' +
                '</div>' +
                '<button class="session-del" onclick="event.stopPropagation();_xfDeleteSession(\'' + s.id + '\')">' +
                    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6"/></svg>' +
                '</button>' +
            '</div>';
        }).join('');

        const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:var(--vscode-sideBar-background,#1e1e1e); color:var(--vscode-foreground,#ccc); font-size:13px; height:100vh; display:flex; flex-direction:column; }
.header { padding:10px 12px; border-bottom:1px solid #333; flex-shrink:0; }
.header h3 { font-size:0.85rem; color:#fff; margin:0; }
.session-list { flex:1; overflow-y:auto; padding:4px 0; }
.session-row { display:flex; align-items:center; padding:8px 12px; cursor:pointer; }
.session-row:hover { background:#2a2d2e; }
.session-main { flex:1; min-width:0; }
.session-title { font-size:0.8rem; color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.session-sub { font-size:0.7rem; color:#666; margin-top:2px; }
.session-del { opacity:0; background:none; border:none; color:#888; cursor:pointer; padding:2px; border-radius:3px; flex-shrink:0; }
.session-row:hover .session-del { opacity:1; }
.session-del:hover { color:#ff6b6b; }
.empty { text-align:center; padding:2rem; color:#666; }
</style>
</head>
<body>
<div class="header"><h3>Histórico de Sessões</h3></div>
<div class="session-list">
${list || '<div class="empty">Nenhuma sessão salva</div>'}
</div>
<script>
const vscode = acquireVsCodeApi();
function _xfSelectSession(id) { vscode.postMessage({ type: 'selectSession', sessionId: id }); }
function _xfDeleteSession(id) { vscode.postMessage({ type: 'deleteSession', sessionId: id }); }
</script>
</body>
</html>`;
        webviewView.webview.html = html;
    }
}
