import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export interface XforgeMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

export interface XforgeSession {
    id: string;
    name: string;
    messages: XforgeMessage[];
    providerId: string;
    model: string;
    createdAt: string;
    updatedAt: string;
}

const SESSIONS_DIR = '.xforge/sessions';

function getSessionsDir(): string {
    const folders = vscode.workspace.workspaceFolders;
    const root = folders ? folders[0].uri.fsPath : vscode.env.appRoot;
    return path.join(root, SESSIONS_DIR);
}

export function loadSessions(): XforgeSession[] {
    const dir = getSessionsDir();
    const idxFile = path.join(dir, 'index.json');
    if (!fs.existsSync(idxFile)) return [];
    try {
        const data = JSON.parse(fs.readFileSync(idxFile, 'utf-8'));
        return Array.isArray(data.sessions) ? data.sessions : [];
    } catch {
        return [];
    }
}

export function saveSessions(sessions: XforgeSession[]): void {
    const dir = getSessionsDir();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const idxFile = path.join(dir, 'index.json');
    fs.writeFileSync(idxFile, JSON.stringify({ sessions }, null, 2), 'utf-8');
}

export function saveActiveId(id: string | null): void {
    const dir = getSessionsDir();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, 'active.txt');
    if (id) fs.writeFileSync(file, id, 'utf-8');
    else if (fs.existsSync(file)) fs.unlinkSync(file);
}

export function loadActiveId(): string | null {
    const file = path.join(getSessionsDir(), 'active.txt');
    if (!fs.existsSync(file)) return null;
    return fs.readFileSync(file, 'utf-8').trim() || null;
}

export function addMessageToSession(sessionId: string, message: XforgeMessage): XforgeSession | null {
    const sessions = loadSessions();
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return null;
    session.messages.push(message);
    session.updatedAt = message.timestamp;
    saveSessions(sessions);
    return session;
}

export function createSession(name: string, providerId: string, model: string): XforgeSession {
    const now = new Date().toISOString();
    const session: XforgeSession = {
        id: 'sess_' + Date.now(),
        name,
        messages: [],
        providerId,
        model,
        createdAt: now,
        updatedAt: now
    };
    const sessions = loadSessions();
    sessions.unshift(session);
    saveSessions(sessions);
    return session;
}

export function deleteSession(sessionId: string): void {
    const sessions = loadSessions().filter(s => s.id !== sessionId);
    saveSessions(sessions);
    const activeId = loadActiveId();
    if (activeId === sessionId) saveActiveId(null);
}
