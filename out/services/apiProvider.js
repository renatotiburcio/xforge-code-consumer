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
exports.getProviderConfig = getProviderConfig;
exports.getAllProviders = getAllProviders;
exports.resolveApiKey = resolveApiKey;
exports.resolveBaseUrl = resolveBaseUrl;
exports.saveApiKey = saveApiKey;
exports.saveBaseUrl = saveBaseUrl;
exports.loadSavedProviders = loadSavedProviders;
exports.saveProviders = saveProviders;
exports.loadActiveSelection = loadActiveSelection;
exports.saveActiveSelection = saveActiveSelection;
exports.loadSessions = loadSessions;
exports.saveSessions = saveSessions;
exports.loadActiveSessionId = loadActiveSessionId;
exports.saveActiveSessionId = saveActiveSessionId;
exports.fetchModels = fetchModels;
exports.callProvider = callProvider;
const http = __importStar(require("http"));
const https = __importStar(require("https"));
const PROVIDERS = {
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
function getProviderConfig(providerId) {
    return PROVIDERS[providerId];
}
function getAllProviders() {
    return PROVIDERS;
}
function resolveApiKey(providerId, globalState) {
    const cfg = PROVIDERS[providerId];
    if (!cfg)
        return '';
    if (cfg.storageKey) {
        const stored = globalState.get(`xforge.key.${cfg.storageKey}`, '');
        if (stored)
            return stored;
    }
    if (cfg.envKeyName)
        return process.env[cfg.envKeyName] || '';
    return '';
}
function resolveBaseUrl(providerId, globalState) {
    const cfg = PROVIDERS[providerId];
    if (!cfg?.storageKey)
        return undefined;
    return globalState.get(`xforge.base.${cfg.storageKey}`, '') || undefined;
}
async function saveApiKey(globalState, providerId, apiKey) {
    const cfg = PROVIDERS[providerId];
    if (!cfg || !cfg.storageKey)
        return;
    await globalState.update(`xforge.key.${cfg.storageKey}`, apiKey.trim());
}
async function saveBaseUrl(globalState, providerId, baseUrl) {
    const cfg = PROVIDERS[providerId];
    if (!cfg || !cfg.storageKey)
        return;
    await globalState.update(`xforge.base.${cfg.storageKey}`, baseUrl.trim());
}
function loadSavedProviders(globalState) {
    return globalState.get('xforge.providers', []);
}
async function saveProviders(globalState, providers) {
    await globalState.update('xforge.providers', providers);
}
function loadActiveSelection(globalState) {
    const sel = globalState.get('xforge.selection', null);
    if (sel && PROVIDERS[sel.providerId] && sel.model && sel.model !== 'auto')
        return sel;
    return { providerId: 'openrouter', model: 'meta-llama/llama-3.1-8b-instruct:free' };
}
async function saveActiveSelection(globalState, providerId, model) {
    await globalState.update('xforge.selection', { providerId, model });
}
function loadSessions(globalState) {
    return globalState.get('xforge.sessions', []);
}
async function saveSessions(globalState, sessions) {
    await globalState.update('xforge.sessions', sessions);
}
function loadActiveSessionId(globalState) {
    return globalState.get('xforge.activeSessionId', null);
}
async function saveActiveSessionId(globalState, sessionId) {
    await globalState.update('xforge.activeSessionId', sessionId);
}
async function httpGetJson(url, headers) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const opts = {
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
                try {
                    resolve(JSON.parse(body));
                }
                catch {
                    reject(new Error('Invalid JSON from ' + url));
                }
            });
        });
        req.on('error', reject);
        req.setTimeout(15000, () => req.destroy(new Error('Timeout')));
        req.end();
    });
}
async function fetchModels(providerId, apiKey, baseUrl) {
    if (providerId === 'ollama') {
        try {
            const base = baseUrl || 'http://localhost:11434';
            const data = await httpGetJson(`${base}/api/tags`);
            return (data?.models || []).map((m) => ({
                id: m.name,
                name: m.name,
                description: m.size ? `${(m.size / 1e9).toFixed(1)}GB` : undefined
            }));
        }
        catch {
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
        if (!apiKey)
            throw new Error('API key required');
        const base = baseUrl || 'https://api.openai.com/v1';
        const data = await httpGetJson(`${base}/models`, { 'Authorization': `Bearer ${apiKey}` });
        return (data?.data || [])
            .filter((m) => m.id.startsWith('gpt') || m.id.startsWith('o1') || m.id.startsWith('o3'))
            .map((m) => ({ id: m.id, name: m.id.replace(/-/g, ' ') }));
    }
    if (providerId === 'openrouter') {
        const data = await httpGetJson('https://openrouter.ai/api/v1/models');
        const all = (data?.data || []).map((m) => ({
            id: m.id,
            name: m.name || m.id,
            context_length: m.context_length
        }));
        const free = all.filter((m) => m.id.includes(':free'));
        const paid = all.filter((m) => !free.includes(m));
        return [...free.slice(0, 25), ...paid.slice(0, 25)];
    }
    return [];
}
async function callProvider(opts) {
    const { providerId } = opts;
    const cfg = PROVIDERS[providerId];
    if (!cfg)
        throw new Error(`Unknown provider: ${providerId}`);
    if (providerId === 'ollama') {
        return callOllama(opts, cfg);
    }
    return callOpenAICompatible(opts, cfg);
}
async function callOpenAICompatible(opts, cfg) {
    const { model, messages, apiKey, baseUrl, onToken } = opts;
    let effectiveUrl = cfg.apiUrl;
    if (baseUrl && cfg.supportsCustomBaseUrl) {
        effectiveUrl = baseUrl.replace(/\/$/, '') + '/v1/chat/completions';
    }
    let modelToUse = model;
    if (!modelToUse || modelToUse === 'auto') {
        if (opts.providerId === 'openrouter')
            modelToUse = 'google/gemini-2.0-flash-001';
        else if (opts.providerId === 'openai')
            modelToUse = 'gpt-4o-mini';
        else if (opts.providerId === 'anthropic')
            modelToUse = 'claude-3-haiku-20240307';
    }
    const headers = { 'Content-Type': 'application/json' };
    if (apiKey)
        headers['Authorization'] = `Bearer ${apiKey}`;
    if (opts.providerId === 'openrouter') {
        headers['HTTP-Referer'] = 'https://xforge-code-ai';
        headers['X-Title'] = 'XForge Code AI';
    }
    const body = { model: modelToUse, messages, stream: true, max_tokens: 4096 };
    return streamSSERequest(effectiveUrl, body, headers, cfg.defaultTimeout, onToken);
}
async function callOllama(opts, cfg) {
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
    const headers = { 'Content-Type': 'application/json' };
    return streamNDJSONRequest(effectiveUrl, body, headers, cfg.defaultTimeout, onToken);
}
function streamSSERequest(url, body, headers, timeoutMs, onToken) {
    const postData = JSON.stringify(body);
    const urlObj = new URL(url);
    return new Promise((resolve, reject) => {
        const httpOptions = {
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
            res.on('data', (chunk) => {
                buffer += chunk.toString('utf-8');
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed || !trimmed.startsWith('data: '))
                        continue;
                    const data = trimmed.substring(6);
                    if (data === '[DONE]') {
                        if (fullContent)
                            resolve(fullContent);
                        return;
                    }
                    try {
                        const parsed = JSON.parse(data);
                        const content = parsed?.choices?.[0]?.delta?.content || '';
                        if (content) {
                            fullContent += content;
                            onToken(content);
                        }
                    }
                    catch { /* skip */ }
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
function streamNDJSONRequest(url, body, headers, timeoutMs, onToken) {
    const postData = JSON.stringify(body);
    const urlObj = new URL(url);
    return new Promise((resolve, reject) => {
        const httpOptions = {
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
            res.on('data', (chunk) => {
                buffer += chunk.toString('utf-8');
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed)
                        continue;
                    try {
                        const parsed = JSON.parse(trimmed);
                        const content = parsed?.message?.content || '';
                        if (content) {
                            fullContent += content;
                            onToken(content);
                        }
                        if (parsed.done === true)
                            resolve(fullContent);
                    }
                    catch { /* skip */ }
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
//# sourceMappingURL=apiProvider.js.map