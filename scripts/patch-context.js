const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// 1) Inserir helpers de contexto ANTES de _callProvider
const helpers = `
    private async _extractContext(raw) {
        if (!raw) return { text: '', ctx: '' };
        const lines = [];
        const re = /@((?:file|selection|branch|workspace|diff|code)(?::([^\\s]+))?)/gi;
        let m;
        const seen = new Set();
        while ((m = re.exec(raw)) !== null) {
            const kind = m[1].toLowerCase();
            const arg = m[2] || '';
            const key = kind + ':' + arg;
            if (seen.has(key)) continue;
            seen.add(key);
            try {
                if (kind === 'file') lines.push(await this._ctxFile(arg));
                else if (kind === 'selection') lines.push(this._ctxSelection());
                else if (kind === 'branch') lines.push(await this._ctxBranch());
                else if (kind === 'workspace') lines.push(await this._ctxWorkspace());
            } catch (e) { lines.push('@' + kind + ' erro: ' + e.message); }
        }
        const text = raw.replace(/@(?:file|selection|branch|workspace|diff|code)(?::([^\\s]+))?/gi, '').trim();
        return { text, ctx: lines.filter(Boolean).join('\\n\\n===\\n\\n') };
    }

    private async _ctxFile(p) {
        const folders = vscode.workspace.workspaceFolders;
        if (!folders) return '';
        let uri;
        if (p) {
            uri = path.isAbsolute(p) ? vscode.Uri.file(p) : vscode.Uri.joinPath(folders[0].uri, p);
        } else {
            const e = vscode.window.activeTextEditor;
            if (!e) return '';
            uri = e.document.uri;
        }
        const buf = await vscode.workspace.fs.readFile(uri);
        const content = Buffer.from(buf).toString('utf-8');
        const rel = vscode.workspace.asRelativePath(uri);
        const trunc = content.length > 6000 ? content.substring(0, 6000) + '\\n... (truncado)' : content;
        return '### @file ' + rel + '\\n' + trunc;
    }

    private _ctxSelection() {
        const e = vscode.window.activeTextEditor;
        if (!e || e.selection.isEmpty) return '';
        const text = e.document.getText(e.selection);
        const f = vscode.workspace.asRelativePath(e.document.uri);
        const l1 = e.selection.start.line + 1;
        const l2 = e.selection.end.line + 1;
        return '### @selection ' + f + ':' + l1 + '-' + l2 + '\\n```\\n' + text + '\\n```';
    }

    private async _ctxBranch() {
        const ext = vscode.extensions.getExtension('vscode.git');
        if (!ext) return '';
        const git = ext.isActive ? ext.exports : await ext.activate();
        const api = git.getAPI(1);
        if (!api.repositories.length) return '';
        const repo = api.repositories[0];
        const head = repo.state.HEAD || {};
        const changes = repo.state.workingTreeChanges.length;
        const staged = repo.state.indexChanges.length;
        return '### @branch ' + (head.name || 'unknown') + '\\nChanges: ' + changes + ' unstaged, ' + staged + ' staged';
    }

    private async _ctxWorkspace() {
        const folders = vscode.workspace.workspaceFolders;
        if (!folders) return '';
        const root = folders[0].uri.fsPath;
        let files = [];
        try { files = fs.readdirSync(root).slice(0, 30); } catch { /* noop */ }
        return '### @workspace ' + root + '\\n' + files.join(', ');
    }

`;

// Insere helpers antes de _callProvider
code = code.replace(
    '    private async _callProvider(userText: string) {',
    helpers + '    private async _callProvider(userText: string) {'
);

// 2) Atualizar _handleSendMessage para mostrar mensagem display e usar contexto
code = code.replace(
    /private async _handleSendMessage\(text: string\) \{[\s\S]*?\n    \}/,
    `private async _handleSendMessage(text: string) {
        if (!text.trim() || !this._view) return;
        // Processa contexto (@file, @selection, etc.)
        const { text: userText, ctx } = await this._extractContext(text);
        const displayText = userText + (ctx ? '\\n[contexto injetado]' : '');
        const userMessage: Message = { id: this._generateId(), role: 'user', content: text, timestamp: new Date() };
        this._session.messages.push(userMessage);
        this._session.updatedAt = new Date();
        if (text.startsWith('/')) {
            if (ctx) { this._session.messages.push({ id: this._generateId(), role: 'system', content: 'Contexto:\\n' + ctx, timestamp: new Date() }); }
            const response = this._handleCommand(userText);
            const assistantMessage: Message = { id: this._generateId(), role: 'assistant', content: response, timestamp: new Date() };
            this._session.messages.push(assistantMessage);
            this._view.webview.postMessage({ type: 'streamStart', id: assistantMessage.id });
            this._view.webview.postMessage({ type: 'streamEnd', id: assistantMessage.id, content: response });
            this._persistSession(displayText);
            return;
        }
        this._persistSession(displayText);
        // Injeta contexto na mensagem para o provider
        if (ctx) {
            this._session.messages.push({ id: this._generateId(), role: 'system', content: 'Contexto do projeto:\\n' + ctx, timestamp: new Date() });
        }
        await this._callProvider(userText);
    }`
);

// 3) Corrigir _callProvider para usar userText recebido (ja com contexto tratado)
const cp = code.match(/private async _Text: string\) \{[\s\S]*?\n    \}/);
if (cp) {
    const newCp = cp[0].replace(
        'console.log(`[xforge] callProvider: providerId=${providerId} model=${model}`);',
        "console.log('[xforge] callProvider: provider=' + providerId + ' model=' + model + ' ctx=' + (messages.some(m => m.role === 'system') ? 'yes' : 'no'));"
    );
    code = code.replace(cp[0], newCp);
}

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK patch aplicado');
