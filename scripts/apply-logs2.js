const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// Adicionar logs extras em _persistSession
code = code.replace(
    /outLine\('\[xforge\] persistSession: ' \+ userMessage\.substring\(0, 50\)\);[\s\S]*?const existingSession[\s\S]*?\};/,
    match => {
        return match.replace(
            /const session = this\._sessions\.find\(s => s\.id === this\._activeSessionId\);\s*if \(session\) \{/,
            `const session = this._sessions.find(s => s.id === this._activeSessionId);
        outLine('[xforge] activeSessionId=' + this._activeSessionId + ' session=' + (session ? 'found' : 'NOT FOUND'));
        if (session) {`
        );
    }
);

// E refreshSidebar
code = code.replace(
    /private _refreshSidebar\(\): void \{\s*if \(!this\._view\) return;[\s\S]*?this\._view\.webview\.postMessage[\s\S]*?\};/,
    `private _refreshSidebar(): void {
        if (!this._view) return;
        outLine('[xforge] refreshSidebar: sessions=' + (this._sessions ? this._sessions.length : 0) + ' activeId=' + this._activeSessionId);
        const trash = this._icon('trash');
        const plus = this._icon('plus');
        const activeId = this._activeSessionId;
        const sessionsHtml = (this._sessions || []).slice(0, 30).map(s => {
            const isActive = s.id === activeId ? ' active' : '';
            const msgCount = s.messages ? s.messages.length : 0;
            const date = s.updatedAt ? new Date(s.updatedAt).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }) : '';
            return '<div class="session-item' + isActive + '" onclick="window._selectSession(\\'' + s.id + '\\')">' +
                '<div class="session-info">' +
                    '<div class="session-name">' + (s.name || 'Sem nome') + '</div>' +
                    '<div class="session-meta">' + date + ' &middot; ' + s.providerId + '</div>' +
                '</div>' +
                '<button class="session-del" onclick="event.stopPropagation();window._deleteSession(\\'' + s.id + '\\')">' + trash + '</button>' +
            '</div>';
        }).join('');
        const sidebarHtml = '<div class="session-new" onclick="window._newSession()">' + plus + 'Nova conversa</div>' + sessionsHtml;
        outLine('[xforge] sending refreshSidebar html, len=' + sidebarHtml.length);
        this._view.webview.postMessage({ type: 'refreshSidebar', html: sidebarHtml });
    }`
);

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK');
