import * as vscode from 'vscode';
import {
    getAllProviders,
    getProviderConfig,
    saveApiKey,
    saveBaseUrl,
    loadSavedProviders,
    saveProviders,
    loadActiveSelection,
    saveActiveSelection,
    fetchModels,
    StoredProvider,
    ModelInfo,
    ProviderConfig
} from '../services/apiProvider';

/**
 * Command: xforge.configureProvider
 * Kilocode-style UI:
 *  1) QuickPick provider
 *  2) InputBox API key
 *  3) (Optional) InputBox Base URL se suportar
 *  4) Auto-save, entao quickSwitch imediatamente abre
 */
export async function configureProviderCommand(globalState: vscode.Memento, onDone?: () => void): Promise<void> {
    const providers = getAllProviders();

    const items = Object.entries(providers).map(([id, cfg]) => ({
        label: `$(server) ${cfg.name}`,
        description: cfg.apiUrl.replace('https://', '').split('/')[0],
        detail: cfg.supportsCustomBaseUrl ? 'Suporta URL customizada' : '',
        id
    }));

    items.push({ label: '$(add) Custom Provider', description: 'Configure um provider qualquer', detail: '', id: '__custom__' });

    const selected = await vscode.window.showQuickPick(items, {
        title: 'Selecionar Provider',
        placeHolder: 'Escolha o provider AI para configurar',
        matchOnDetail: true
    });
    if (!selected) return;

    let providerId: string;
    let cfg = providers[selected.id];

    if (selected.id === '__custom__') {
        const custom = await vscode.window.showInputBox({
            title: 'Custom Provider',
            prompt: 'Identificador unico (ex: lmstudio)',
            placeHolder: 'lmstudio',
            validateInput: v => v.trim().length < 2 ? 'Minimo 2 caracteres' : null
        });
        if (!custom) return;
        providerId = custom.trim();
        cfg = {
            name: providerId,
            apiUrl: '',
            envKeyName: '',
            storageKey: providerId,
            apiKeyPlaceholder: '',
            supportsCustomBaseUrl: true,
            defaultTimeout: 120000
        };
        // Save custom provider config
        const savedCustom = globalState.get<Record<string, ProviderConfig>>('xforge.customProviders', {});
        savedCustom[providerId] = cfg;
        await globalState.update('xforge.customProviders', savedCustom);
    } else {
        providerId = selected.id;
    }

    // API Key
    const existing = loadSavedProviders(globalState).find(p => p.id === providerId);
    const existingKey = existing?.apiKey || '';

    const apiKey = await vscode.window.showInputBox({
        title: `API Key — ${cfg.name}`,
        prompt: providerId === 'ollama'
            ? 'Ollama nao usa API key (deixe vazio)'
            : `Cole a API key de ${cfg.name}`,
        value: existingKey ? '••••••••••••' + existingKey.slice(-4) : '',
        password: providerId !== 'ollama',
        placeHolder: cfg.apiKeyPlaceholder,
        ignoreFocusOut: true,
        validateInput: (val) => {
            if (providerId !== 'ollama' && !val.replace(/•/g, '').trim()) {
                return 'API key e obrigatoria';
            }
            return null;
        }
    });
    if (apiKey === undefined) return;
    const newKey = apiKey.replace(/•/g, '') || existingKey;

    await saveApiKey(globalState, providerId, newKey);

    // Base URL (se suportar)
    if (cfg.supportsCustomBaseUrl) {
        const defaultBase = providerId === 'ollama' ? 'http://localhost:11434'
            : providerId === 'openai' ? 'https://api.openai.com/v1'
            : '';
        const baseUrl = await vscode.window.showInputBox({
            title: `Base URL — ${cfg.name}`,
            prompt: `URL base da API (${providerId === 'ollama' ? 'host:porta' : 'com /v1'})\nDeixe vazio para usar padrao`,
            value: existing?.baseUrl || defaultBase,
            placeHolder: defaultBase,
            ignoreFocusOut: true
        });
        if (baseUrl !== undefined && baseUrl.trim()) {
            await saveBaseUrl(globalState, providerId, baseUrl.trim());
        }
    }

    // Save to list
    let list = loadSavedProviders(globalState);
    const entry: StoredProvider = {
        id: providerId,
        label: cfg.name,
        apiKey: newKey,
        baseUrl: cfg.supportsCustomBaseUrl ? (globalState.get(`xforge.base.${providerId}`, '') || undefined) : undefined,
        enabled: !!newKey || providerId === 'ollama'
    };
    const idx = list.findIndex(p => p.id === providerId);
    if (idx >= 0) list[idx] = entry; else list.push(entry);
    await saveProviders(globalState, list);

    // Set as active
    await saveActiveSelection(globalState, providerId, 'auto');

    vscode.window.showInformationMessage(`✓ ${cfg.name} configurado!`);

    if (onDone) onDone();
}

/**
 * Command: xforge.switchProvider
 * QuickPick com modelos buscados da API em tempo real
 */
export async function showProviderQuickPick(globalState: vscode.Memento, chatProvider?: any): Promise<void> {
    const saved = loadSavedProviders(globalState);
    const sel = loadActiveSelection(globalState);

    // Se nao tem nenhum configurado, abre configuracao
    if (saved.length === 0) {
        const action = await vscode.window.showWarningMessage(
            'Nenhum provider configurado.',
            'Configurar Agora'
        );
        if (action === 'Configurar Agora') {
            await configureProviderCommand(globalState, () => showProviderQuickPick(globalState, chatProvider));
        }
        return;
    }

    const items: any[] = saved.map(p => {
        const isActive = p.id === sel.providerId;
        return {
            label: isActive ? `$(check) ${p.label}` : `     ${p.label}`,
            description: `${p.id === 'ollama' ? 'Local' : 'API'} • ${isActive ? `model: ${sel.model}` : 'clique para usar'}`,
            detail: p.baseUrl ? `Base: ${p.baseUrl}` : '',
            id: p.id
        };
    });

    items.push({ label: '$(add) Configurar Novo Provider', description: '', detail: '', id: '__new__' });

    const picked = await vscode.window.showQuickPick(items, {
        title: 'Selecionar Provider',
        placeHolder: 'Escolha o provider para o chat',
        matchOnDetail: true
    });

    if (!picked) return;

    if (picked.id === '__new__') {
        await configureProviderCommand(globalState, () => showProviderQuickPick(globalState, chatProvider));
        return;
    }

    const cfg = getAllProviders()[picked.id] || {
        name: picked.label,
        apiUrl: '',
        envKeyName: '',
        storageKey: picked.id,
        apiKeyPlaceholder: '',
        supportsCustomBaseUrl: false
    };
    const resolvedKey = resolveApiKeyForProvider(globalState, picked.id, saved);
    const resolvedBase = globalState.get<string>(`xforge.base.${picked.id}`, '') || undefined;

    // Buscar modelos da API
    let models: ModelInfo[] = [];
    try {
        await vscode.window.withProgress(
            { location: vscode.ProgressLocation.Notification, title: `Buscando modelos ${cfg.name}...` },
            async () => {
                models = await fetchModels(picked.id, resolvedKey, resolvedBase);
            }
        );
    } catch (err: any) {
        // fallback: input manual
        models = [];
    }

    if (models.length === 0) {
        const manual = await vscode.window.showInputBox({
            title: `Modelo — ${cfg.name}`,
            prompt: 'Nao foi possivel buscar modelos via API. Digite o ID manualmente',
            value: sel.providerId === picked.id ? sel.model : '',
            placeHolder: 'gpt-4o, claude-sonnet-4, llama3...',
            ignoreFocusOut: true
        });
        if (!manual) return;
        await saveActiveSelection(globalState, picked.id, manual.trim());
        chatProvider?.notifySelectionChanged?.();
        return;
    }

    const modelPick = await vscode.window.showQuickPick(
        models.map(m => ({
            label: m.name.length > 60 ? m.name.substring(0, 57) + '...' : m.name,
            description: m.pricing?.prompt !== undefined
                ? `$${(Number(m.pricing.prompt) * 1e6).toFixed(2)}/1M prompt`
                : '',
            detail: m.context_length ? `${(m.context_length / 1000).toFixed(0)}K ctx` : '',
            value: m.id
        })),
        {
            title: `Modelo — ${cfg.name} (${models.length} disponiveis)`,
            placeHolder: 'Selecione o modelo',
            matchOnDescription: true,
            matchOnDetail: true
        }
    );

    if (!modelPick) return;
    await saveActiveSelection(globalState, picked.id, modelPick.value);
    chatProvider?.notifySelectionChanged?.();
    vscode.window.showInformationMessage(`✓ ${cfg.name} / ${modelPick.label}`);
}

function resolveApiKeyForProvider(globalState: vscode.Memento, providerId: string, list: StoredProvider[]): string {
    const found = list.find(p => p.id === providerId);
    if (found?.apiKey) return found.apiKey;
    const cfg = getAllProviders()[providerId];
    if (cfg?.envKeyName) return process.env[cfg.envKeyName] || '';
    return '';
}
