import * as vscode from 'vscode';

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

export class ChatViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'xforge.chatView';
    private _view?: vscode.WebviewView;
    private _session: Session;
    private _disposables: vscode.Disposable[] = [];

    constructor(private readonly _extensionUri: vscode.Uri) {
        this._session = this.createNewSession();
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        webviewView.webview.onDidReceiveMessage(
            (message) => {
                switch (message.type) {
                    case 'sendMessage':
                        this._handleSendMessage(message.text);
                        break;
                    case 'newSession':
                        this.newSession();
                        break;
                }
            },
            null,
            this._disposables
        );
    }

    private _handleSendMessage(text: string) {
        if (!text.trim() || !this._view) return;

        const userMessage: Message = {
            id: this._generateId(),
            role: 'user',
            content: text,
            timestamp: new Date()
        };

        this._session.messages.push(userMessage);
        this._session.updatedAt = new Date();

        this._view.webview.postMessage({
            type: 'addMessage',
            message: userMessage
        });

        this._simulateResponse(text);
    }

    private _simulateResponse(userText: string) {
        if (!this._view) return;

        const config = vscode.workspace.getConfiguration('xforge');
        const provider = config.get<string>('provider', 'openrouter');
        const model = config.get<string>('model', 'claude-sonnet-4');

        setTimeout(() => {
            const response = this._generateResponse(userText, provider, model);
            const assistantMessage: Message = {
                id: this._generateId(),
                role: 'assistant',
                content: response,
                timestamp: new Date()
            };

            this._session.messages.push(assistantMessage);
            this._session.updatedAt = new Date();

            this._view?.webview.postMessage({
                type: 'addMessage',
                message: assistantMessage
            });
        }, 500);
    }

    private _generateResponse(userText: string, provider: string, model: string): string {
        if (userText.startsWith('/')) {
            return this._handleCommand(userText);
        }

        if (userText.toLowerCase().includes('ajuda') || userText.toLowerCase().includes('help')) {
            return `## XForge Code AI\n\nComandos disponiveis:\n- \`/xforge\` - Menu principal\n- \`/analisar-projeto\` - Analisa o projeto atual\n- \`/criar-projeto\` - Cria novo projeto\n- \`/desenvolver\` - Inicia desenvolvimento\n- \`/qualidade\` - Quality gates\n- \`/seguranca\` - Auditoria de seguranca\n\nProvider: **${provider}** | Model: **${model}**`;
        }

        return `Entendi sua solicitação: "${userText}"\n\nEstou processando com ${provider}/${model}...\n\n*Aqui sera implementada a integracao real com o provider configurado.*`;
    }

    private _handleCommand(command: string): string {
        const cmd = command.toLowerCase().trim();
        switch (cmd) {
            case '/xforge':
                return '## XForge Code AI\n\nBem-vindo ao XForge Code AI! Seu assistente de codigo inteligente.';
            case '/analisar-projeto':
                return '## Analise de Projeto\n\nAnalisando projeto atual...\n\n*A implementar*';
            case '/criar-projeto':
                return '## Criar Projeto\n\nPara criar um projeto, descreva o que deseja construir.';
            case '/desenvolver':
                return '## Modo Desenvolvimento\n\nModo desenvolvimento ativado. O que deseja implementar?';
            case '/qualidade':
                return '## Quality Gates\n\nRodando quality gates...\n\n*A implementar*';
            case '/seguranca':
                return '## Auditoria de Seguranca\n\nAnalisando seguranca do projeto...\n\n*A implementar*';
            default:
                return `Comando nao reconhecido: ${command}\n\nDigite /help para ver comandos disponiveis.`;
        }
    }

    public newSession() {
        this._session = this.createNewSession();
        if (this._view) {
            this._view.webview.postMessage({ type: 'clearMessages' });
        }
    }

    private createNewSession(): Session {
        return {
            id: this._generateId(),
            name: `Session ${new Date().toLocaleTimeString()}`,
            messages: [],
            createdAt: new Date(),
            updatedAt: new Date()
        };
    }

    private _generateId(): string {
        return Math.random().toString(36).substring(2, 15);
    }

    private _getHtmlForWebview(webview: vscode.Webview): string {
        return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XForge Code AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 13px;
            background: var(--vscode-sideBar-background, #1e1e1e);
            color: var(--vscode-foreground, #cccccc);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .chat-container { flex: 1; overflow-y: auto; padding: 12px; }
        .welcome {
            text-align: center;
            padding: 2rem 1rem;
        }
        .welcome-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .welcome h2 { font-size: 1rem; margin-bottom: 0.5rem; color: #fff; }
        .welcome p { font-size: 0.8rem; color: #888; margin-bottom: 1rem; }
        .quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 1rem; }
        .quick-action {
            padding: 8px;
            border: 1px solid var(--vscode-widget-border, #3c3c3c);
            border-radius: 4px;
            background: var(--vscode-list-hoverBackground, #2a2d2e);
            cursor: pointer;
            font-size: 0.75rem;
            text-align: center;
        }
        .quick-action:hover { background: var(--vscode-list-activeSelectionBackground, #094771); }
        .message { margin-bottom: 12px; }
        .message-user { text-align: right; }
        .message-bubble {
            display: inline-block;
            max-width: 85%;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            line-height: 1.5;
        }
        .message-user .message-bubble { background: #094771; color: #fff; }
        .message-assistant .message-bubble { background: #2a2d2e; }
        .input-area {
            padding: 12px;
            border-top: 1px solid var(--vscode-widget-border, #3c3c3c);
        }
        .input-wrapper {
            display: flex;
            align-items: flex-end;
            gap: 6px;
            background: var(--vscode-input-background, #3c3c3c);
            border: 1px solid var(--vscode-widget-border, #3c3c3c);
            border-radius: 6px;
            padding: 6px 8px;
        }
        textarea {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--vscode-input-foreground, #ccc);
            font-size: 0.8rem;
            resize: none;
            outline: none;
            min-height: 20px;
            max-height: 100px;
        }
        .send-btn {
            width: 28px;
            height: 28px;
            border-radius: 4px;
            border: none;
            background: var(--vscode-button-background, #0e639c);
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .send-btn:hover { background: var(--vscode-button-hoverBackground, #1177bb); }
    </style>
</head>
<body>
    <div class="chat-container" id="chatContainer">
        <div class="welcome" id="welcome">
            <div class="welcome-icon">&#9889;</div>
            <h2>Bem-vindo ao XForge Code AI</h2>
            <p>Seu assistente de codigo inteligente</p>
            <div class="quick-actions">
                <div class="quick-action" onclick="sendQuick('Crie uma API de pagamentos')">Nova API</div>
                <div class="quick-action" onclick="sendQuick('Analise o projeto')">Analisar</div>
                <div class="quick-action" onclick="sendQuick('Me ajude com testes')">Testes</div>
                <div class="quick-action" onclick="sendQuick('/help')">Comandos</div>
            </div>
        </div>
    </div>
    <div class="input-area">
        <div class="input-wrapper">
            <textarea id="input" placeholder="Digite sua mensagem... (@ para contexto, / para comandos)" rows="1"></textarea>
            <button class="send-btn" onclick="sendMessage()">&#10145;</button>
        </div>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        const chatContainer = document.getElementById('chatContainer');
        const input = document.getElementById('input');
        let welcomeVisible = true;

        function sendMessage() {
            const text = input.value.trim();
            if (!text) return;
            addMessage('user', text);
            vscode.postMessage({ type: 'sendMessage', text });
            input.value = '';
            input.style.height = 'auto';
        }

        function sendQuick(text) {
            addMessage('user', text);
            vscode.postMessage({ type: 'sendMessage', text });
        }

        function addMessage(role, content) {
            if (welcomeVisible) {
                document.getElementById('welcome').style.display = 'none';
                welcomeVisible = false;
            }
            const div = document.createElement('div');
            div.className = 'message message-' + role;
            div.innerHTML = '<div class="message-bubble">' + escapeHtml(content) + '</div>';
            chatContainer.appendChild(div);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 100) + 'px';
        });

        window.addEventListener('message', (event) => {
            const message = event.data;
            if (message.type === 'addMessage') {
                addMessage(message.message.role, message.message.content);
            } else if (message.type === 'clearMessages') {
                chatContainer.innerHTML = '';
                document.getElementById('welcome').style.display = 'block';
                welcomeVisible = true;
            }
        });
    </script>
</body>
</html>`;
    }

    dispose() {
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) x.dispose();
        }
    }
}