import * as vscode from 'vscode';
import * as http from 'http';
import * as https from 'https';

export interface ChatMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

export interface ModelInfo {
    id: string;
    name: string;
    description?: string;
    pricing?: { prompt?: number; completion?: number };
    context_length?: number;
}

export interface StoredProvider {
    id: string;
    label: string;
    apiKey: string;
    baseUrl?: string;
    enabled: boolean;
}

export interface ProviderConfig {
    name: string;
    apiUrl: string;
    envKeyName: string;
    storageKey: string;
    apiKeyPlaceholder: string;
    supportsCustomBaseUrl: boolean;
    defaultTimeout: number;
}

const PROVIDERS: Record<string, ProviderConfig> = {
    openrouter: {
        name: 'OpenRouter',
        apiUrl: 'https://openrouter.ai/api/v1/chat/completions',
        envKeyName: 'OPENROUTER_API_KEY',
        storageKey: 'openrouter',
        apiKeyPlaceholder: 'sk-or-v1-...',
        supportsCustomBaseUrl: false,
        defaultTimeout: 120000
    },
    openai: {
        name: 'OpenAI',
        apiUrl: 'https://api.openai.com/v1/chat/completions',
        envKeyName: 'OPENAI_API_KEY',
        storageKey: 'openai',
        apiKeyPlaceholder: 'sk-...',
        supportsCustomBaseUrl: true,
        defaultTimeout: 120000
    },
    anthropic: {
        name: 'Anthropic',
        apiUrl: 'https://api.anthropic.com/v1/messages',
        envKeyName: 'ANTHROPIC_API_KEY',
        storageKey: 'anthropic',
        apiKeyPlaceholder: 'sk-ant-...',
        supportsCustomBaseUrl: true,
        defaultTimeout: 120000
    },
    ollama: {
        name: 'Ollama (Local)',
        apiUrl: 'http://localhost:11434/api/chat',
        envKeyName: '',
        storageKey: 'ollama',
        apiKeyPlaceholder: '(no key)',
        supportsCustomBaseUrl: true,
        defaultTimeout: 300000
    }
};

export function getProviderConfig(providerId: string): ProviderConfig | undefined {
    return PROVIDERS[providerId];
}

export function getAllProviders(): Record<string, ProviderConfig> {
    return PROVIDERS;
}

export function resolveApiKey(providerId: string, globalState: vscode.Memento): string {
    const cfg = PROVIDERS[providerId];
    if (!cfg) return '';
    if (cfg.storageKey) {
        const stored = globalState.get<string>(`xforge.key.${cfg.storageKey}`, '');
        if (stored) return stored;
    }
    if (cfg.envKeyName) return process.env[cfg.envKeyName] || '';
    return '';
}

export function resolveBaseUrl(providerId: string, globalState: vscode.Memento): string | undefined {
    const cfg = PROVIDERS[providerId];
    if (!cfg?.storageKey) return undefined;
    return globalState.get<string>(`xforge.base.${cfg.storageKey}`, '') || undefined;
}

export async function saveApiKey(globalState: vscode.Memento, providerId: string, apiKey: string): Promise<void> {
    const cfg = PROVIDERS[providerId];
    if (!cfg || !cfg.storageKey) return;
    await globalState.update(`xforge.key.${cfg.storageKey}`, apiKey.trim());
}

export async function saveBaseUrl(globalState: vscode.Memento, providerId: string, baseUrl: string): Promise<void> {
    const cfg = PROVIDERS[providerId];
    if (!cfg || !cfg.storageKey) return;
    await globalState.update(`xforge.base.${cfg.storageKey}`, baseUrl.trim());
}

export function loadSavedProviders(globalState: vscode.Memento): StoredProvider[] {
    return globalState.get<StoredProvider[]>('xforge.providers', []);
}

export async function saveProviders(globalState: vscode.Memento, providers: StoredProvider[]): Promise<void> {
    await globalState.update('xforge.providers', providers);
}

export function loadActiveSelection(globalState: vscode.Memento): { providerId: string; model: string } {
    const sel = globalState.get<{ providerId: string; model: string }>('xforge.selection', null as any);
    if (sel && PROVIDERS[sel.providerId] && sel.model && sel.model !== 'auto') return sel;
    return { providerId: 'openrouter', model: 'meta-llama/llama-3.1-8b-instruct:free' };
}

export async function saveActiveSelection(globalState: vscode.Memento, providerId: string, model: string): Promise<void> {
    await globalState.update('xforge.selection', { providerId, model });
}

export interface SessionData {
    id: string;
    name: string;
    messages: { role: string; content: string; timestamp: string }[];
    providerId: string;
    model: string;
    createdAt: string;
    updatedAt: string;
}

export function loadSessions(globalState: vscode.Memento): SessionData[] {
    return globalState.get<SessionData[]>('xforge.sessions', []);
}

export async function saveSessions(globalState: vscode.Memento, sessions: SessionData[]): Promise<void> {
    await globalState.update('xforge.sessions', sessions);
}

export function loadActiveSessionId(globalState: vscode.Memento): string | null {
    return globalState.get<string | null>('xforge.activeSessionId', null);
}

export async function saveActiveSessionId(globalState: vscode.Memento, sessionId: string | null): Promise<void> {
    await globalState.update('xforge.activeSessionId', sessionId);
}

async function httpGetJson(url: string, headers?: Record<string, string>): Promise<any> {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const opts: http.RequestOptions = {
            hostname: urlObj.hostname,
            port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            headers: { 'Content-Type': 'application/json', ...(headers || {}) }
        };
        const protocol = urlObj.protocol === 'https:' ? https : http;
        const req = protocol.request(opts, (res) => {
            let body = '';
            res.on('data', (c) => { body += c; });
            res.on('end', () => {
                try { resolve(JSON.parse(body)); }
                catch { reject(new Error('Invalid JSON from ' + url)); }
            });
        });
        req.on('error', reject);
        req.setTimeout(15000, () => req.destroy(new Error('Timeout')));
        req.end();
    });
}

export async function fetchModels(providerId: string, apiKey: string, baseUrl?: string): Promise<ModelInfo[]> {
    if (providerId === 'ollama') {
        try {
            const base = baseUrl || 'http://localhost:11434';
            const data = await httpGetJson(`${base}/api/tags`);
            return (data?.models || []).map((m: any) => ({
                id: m.name,
                name: m.name,
                description: m.size ? `${(m.size / 1e9).toFixed(1)}GB` : undefined
            }));
        } catch {
            return [];
        }
    }
    if (providerId === 'anthropic') {
        return [
            { id: 'claude-sonnet-4-20250514', name: 'Claude Sonnet 4' },
            { id: 'claude-haiku-4', name: 'Claude Haiku 4' },
            { id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet' }
        ];
    }
    if (providerId === 'openai') {
        if (!apiKey) throw new Error('API key required');
        const base = baseUrl || 'https://api.openai.com/v1';
        const data = await httpGetJson(`${base}/models`, { 'Authorization': `Bearer ${apiKey}` });
        return (data?.data || [])
            .filter((m: any) => m.id.startsWith('gpt') || m.id.startsWith('o1') || m.id.startsWith('o3'))
            .map((m: any) => ({ id: m.id, name: m.id.replace(/-/g, ' ') }));
    }
    if (providerId === 'openrouter') {
        const data = await httpGetJson('https://openrouter.ai/api/v1/models');
        const all = (data?.data || []).map((m: any) => ({
            id: m.id,
            name: m.name || m.id,
            context_length: m.context_length
        }));
        const free = all.filter((m: ModelInfo) => m.id.includes(':free'));
        const paid = all.filter((m: ModelInfo) => !free.includes(m));
        return [...free.slice(0, 25), ...paid.slice(0, 25)];
    }
    return [];
}

export interface CallOptions {
    providerId: string;
    model: string;
    messages: ChatMessage[];
    apiKey: string;
    baseUrl?: string;
    onToken: (token: string) => void;
}

export async function callProvider(opts: CallOptions): Promise<string> {
    const { providerId } = opts;
    const cfg = PROVIDERS[providerId];
    if (!cfg) throw new Error(`Unknown provider: ${providerId}`);

    if (providerId === 'ollama') {
        return callOllama(opts, cfg);
    }
    return callOpenAICompatible(opts, cfg);
}

async function callOpenAICompatible(opts: CallOptions, cfg: ProviderConfig): Promise<string> {
    const { model, messages, apiKey, baseUrl, onToken } = opts;

    let effectiveUrl = cfg.apiUrl;
    if (baseUrl && cfg.supportsCustomBaseUrl) {
        effectiveUrl = baseUrl.replace(/\/$/, '') + '/v1/chat/completions';
    }

    let modelToUse = model;
    if (!modelToUse || modelToUse === 'auto') {
        if (opts.providerId === 'openrouter') modelToUse = 'google/gemini-2.0-flash-001';
        else if (opts.providerId === 'openai') modelToUse = 'gpt-4o-mini';
        else if (opts.providerId === 'anthropic') modelToUse = 'claude-3-haiku-20240307';
    }

    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;
    if (opts.providerId === 'openrouter') {
        headers['HTTP-Referer'] = 'https://xforge-code-ai';
        headers['X-Title'] = 'XForge Code AI';
    }

    const body = { model: modelToUse, messages, stream: true, max_tokens: 4096 };
    return streamSSERequest(effectiveUrl, body, headers, cfg.defaultTimeout, onToken);
}

async function callOllama(opts: CallOptions, cfg: ProviderConfig): Promise<string> {
    const { model, messages, baseUrl, onToken } = opts;
    const base = baseUrl || 'http://localhost:11434';
    const effectiveUrl = base.replace(/\/$/, '') + '/api/chat';

    const body = {
        model,
        messages,
        stream: true,
        keep_alive: '30m',
        options: { num_ctx: 4096 }
    };

    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    return streamNDJSONRequest(effectiveUrl, body, headers, cfg.defaultTimeout, onToken);
}

function streamSSERequest(url: string, body: any, headers: Record<string, string>, timeoutMs: number, onToken: (t: string) => void): Promise<string> {
    const postData = JSON.stringify(body);
    const urlObj = new URL(url);

    return new Promise((resolve, reject) => {
        const httpOptions: http.RequestOptions = {
            hostname: urlObj.hostname,
            port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
            path: urlObj.pathname,
            method: 'POST',
            headers: { ...headers, 'Content-Length': Buffer.byteLength(postData) }
        };
        const protocol = urlObj.protocol === 'https:' ? https : http;

        console.log(`[xforge] POST ${url} model=${body.model} stream=SSE`);

        const req = protocol.request(httpOptions, (res) => {
            console.log(`[xforge] Status ${res.statusCode} for ${body.model}`);
            if (res.statusCode && res.statusCode >= 400) {
                let errBody = '';
                res.on('data', (c) => { errBody += c; });
                res.on('end', () => {
                    console.error(`[xforge] Error body: ${errBody}`);
                    reject(new Error(`${res.statusCode}: ${errBody.substring(0, 300)}`));
                });
                return;
            }
            let buffer = '';
            let fullContent = '';
            res.on('data', (chunk: Buffer) => {
                buffer += chunk.toString('utf-8');
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed || !trimmed.startsWith('data: ')) continue;
                    const data = trimmed.substring(6);
                    if (data === '[DONE]') { if (fullContent) resolve(fullContent); return; }
                    try {
                        const parsed = JSON.parse(data);
                        const content = parsed?.choices?.[0]?.delta?.content || '';
                        if (content) { fullContent += content; onToken(content); }
                    } catch { /* skip */ }
                }
            });
            res.on('end', () => resolve(fullContent));
        });
        req.on('error', reject);
        req.setTimeout(timeoutMs, () => req.destroy(new Error(`Timeout ${timeoutMs / 1000}s`)));
        req.write(postData);
        req.end();
    });
}

function streamNDJSONRequest(url: string, body: any, headers: Record<string, string>, timeoutMs: number, onToken: (t: string) => void): Promise<string> {
    const postData = JSON.stringify(body);
    const urlObj = new URL(url);

    return new Promise((resolve, reject) => {
        const httpOptions: http.RequestOptions = {
            hostname: urlObj.hostname,
            port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
            path: urlObj.pathname,
            method: 'POST',
            headers: { ...headers, 'Content-Length': Buffer.byteLength(postData) }
        };
        const protocol = urlObj.protocol === 'https:' ? https : http;

        console.log(`[xforge] POST ${url} model=${body.model} stream=NDJSON`);

        const req = protocol.request(httpOptions, (res) => {
            console.log(`[xforge] Status ${res.statusCode} for ${body.model}`);
            if (res.statusCode && res.statusCode >= 400) {
                let errBody = '';
                res.on('data', (c) => { errBody += c; });
                res.on('end', () => {
                    console.error(`[xforge] Error body: ${errBody}`);
                    reject(new Error(`${res.statusCode}: ${errBody.substring(0, 300)}`));
                });
                return;
            }
            let buffer = '';
            let fullContent = '';
            res.on('data', (chunk: Buffer) => {
                buffer += chunk.toString('utf-8');
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed) continue;
                    try {
                        const parsed = JSON.parse(trimmed);
                        const content = parsed?.message?.content || '';
                        if (content) { fullContent += content; onToken(content); }
                        if (parsed.done === true) resolve(fullContent);
                    } catch { /* skip */ }
                }
            });
            res.on('end', () => resolve(fullContent || ''));
        });
        req.on('error', reject);
        req.setTimeout(timeoutMs, () => req.destroy(new Error(`Timeout ${timeoutMs / 1000}s`)));
        req.write(postData);
        req.end();
    });
}
