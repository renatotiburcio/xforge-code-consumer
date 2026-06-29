// XForge Code AI — Webview entry point (bundled by esbuild)
// This file is NOT compiled by tsc. It is bundled separately via esbuild into out/webview.js

declare const acquireVsCodeApi: () => {
    postMessage(message: unknown): void;
    getState(): unknown;
    setState(state: unknown): void;
};

interface VsCodeMessageEvent {
    data: {
        type: string;
        message?: { role: string; content: string };
        id?: string;
        token?: string;
        content?: string;
        selection?: { providerId: string; providerName: string; model: string };
    };
};

(function () {
    const vscode = acquireVsCodeApi();
    const chatContainer = document.getElementById('chatContainer') as HTMLElement;
    const welcomeEl = document.getElementById('welcome') as HTMLElement;
    const inputEl = document.getElementById('messageInput') as HTMLTextAreaElement;
    const sendBtn = document.getElementById('sendBtn') as HTMLButtonElement;
    const headerProvider = document.getElementById('headerProvider') as HTMLElement;
    const headerModel = document.getElementById('headerModel') as HTMLElement;
    const headerBtn = document.getElementById('headerBtn') as HTMLElement;

    let welcomeVisible = true;
    let currentStreamId: string | null = null;
    let currentSelection: { providerId: string; providerName: string; model: string } | null = null;

    function escapeHtml(text: string): string {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function renderMarkdown(text: string): string {
        let html = escapeHtml(text);
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/^### (.+)$/gm, '<h4 style="margin:6px 0 3px;font-size:0.8rem;">$1</h4>');
        html = html.replace(/^## (.+)$/gm, '<h3 style="margin:8px 0 4px;font-size:0.85rem;">$1</h3>');
        html = html.replace(/^- (.+)$/gm, '<li style="margin-left:16px;">$1</li>');
        html = html.replace(/\n/g, '<br>');
        return html;
    }

    function hideWelcome(): void {
        if (welcomeVisible && welcomeEl) {
            welcomeEl.style.display = 'none';
            welcomeVisible = false;
        }
    }

    function shortModel(modelId: string): string {
        if (!modelId || modelId === 'auto') return 'auto';
        // Remove prefixo do provider se houver
        const parts = modelId.split('/');
        let last = parts[parts.length - 1];
        // Sufixos
        last = last.replace(':free', ' (free)');
        if (last.length > 28) last = last.substring(0, 25) + '...';
        return last;
    }

    function updateHeaderSelection(sel: { providerId: string; providerName: string; model: string }): void {
        currentSelection = sel;
        if (headerProvider) headerProvider.textContent = sel.providerName;
        if (headerModel) headerModel.textContent = shortModel(sel.model);
        if (headerBtn) headerBtn.title = `${sel.providerName} / ${sel.model}`;
    }

    function addMessage(role: string, content: string): void {
        hideWelcome();
        const div = document.createElement('div');
        div.className = 'message message-' + role;
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = role === 'assistant' ? renderMarkdown(content) : escapeHtml(content);
        div.appendChild(bubble);
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function startStream(id: string): void {
        hideWelcome();
        currentStreamId = id;
        const div = document.createElement('div');
        div.className = 'message message-assistant';
        div.id = 'msg-' + id;
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = '<span class="typing">...</span>';
        div.appendChild(bubble);
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendToken(id: string, token: string): void {
        const div = document.getElementById('msg-' + id);
        if (!div) return;
        const bubble = div.querySelector('.message-bubble');
        if (!bubble) return;
        const typing = bubble.querySelector('.typing');
        if (typing) typing.remove();
        bubble.innerHTML += renderMarkdown(token);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function endStream(id: string, fullContent: string): void {
        const div = document.getElementById('msg-' + id);
        if (!div) return;
        const bubble = div.querySelector('.message-bubble') as HTMLElement;
        if (bubble) bubble.innerHTML = renderMarkdown(fullContent);
        if (currentStreamId === id) currentStreamId = null;
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function sendMessage(): void {
        const text = inputEl.value.trim();
        if (!text) return;
        hideWelcome();
        addMessage('user', text);
        vscode.postMessage({ type: 'sendMessage', text });
        inputEl.value = '';
        inputEl.style.height = 'auto';
    }

    function sendQuick(text: string): void {
        hideWelcome();
        addMessage('user', text);
        vscode.postMessage({ type: 'sendMessage', text });
    }

    function requestProviderSwitch(): void {
        vscode.postMessage({ type: 'requestSwitch' });
    }

    function requestNewProvider(): void {
        vscode.postMessage({ type: 'requestNew' });
    }

    function toggleSidebar(): void {
        const panel = document.getElementById('historyPanel');
        if (panel) panel.classList.toggle('open');
    }

    function selectSession(id: string): void {
        vscode.postMessage({ type: 'selectSession', sessionId: id });
    }

    function deleteSession(id: string): void {
        vscode.postMessage({ type: 'deleteSession', sessionId: id });
    }

    function newSession(): void {
        vscode.postMessage({ type: 'newSession' });
    }

    // Expose to global scope for onclick handlers
    (window as any).sendMessage = sendMessage;
    (window as any).sendQuick = sendQuick;
    (window as any).requestProviderSwitch = requestProviderSwitch;
    (window as any).requestNewProvider = requestNewProvider;
    (window as any)._toggleSidebar = toggleSidebar;
    (window as any)._selectSession = selectSession;
    (window as any)._deleteSession = deleteSession;
    (window as any)._newSession = newSession;

    sendBtn.addEventListener('click', sendMessage);
    if (headerBtn) headerBtn.addEventListener('click', requestProviderSwitch);

    inputEl.addEventListener('keydown', (e: KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    inputEl.addEventListener('input', () => {
        inputEl.style.height = 'auto';
        inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + 'px';
    });

    window.addEventListener('message', (event: VsCodeMessageEvent) => {
        const msg = event.data;
        switch (msg.type) {
            case 'streamStart':
                if (msg.id) startStream(msg.id);
                break;
            case 'streamToken':
                if (msg.id && msg.token) appendToken(msg.id, msg.token);
                break;
            case 'streamEnd':
                if (msg.id && msg.content) endStream(msg.id, msg.content);
                break;
            case 'clearMessages':
                chatContainer.innerHTML = '';
                if (welcomeEl) { welcomeEl.style.display = 'block'; welcomeVisible = true; }
                break;
            case 'selectionChanged':
            case 'currentSelection':
                if (msg.selection) updateHeaderSelection(msg.selection);
                break;
        }
    });
})();
