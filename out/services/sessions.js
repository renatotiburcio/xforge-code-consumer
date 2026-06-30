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
exports.loadSessions = loadSessions;
exports.saveSessions = saveSessions;
exports.saveActiveId = saveActiveId;
exports.loadActiveId = loadActiveId;
exports.addMessageToSession = addMessageToSession;
exports.createSession = createSession;
exports.deleteSession = deleteSession;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const SESSIONS_DIR = '.xforge/sessions';
function getSessionsDir() {
    const folders = vscode.workspace.workspaceFolders;
    const root = folders ? folders[0].uri.fsPath : vscode.env.appRoot;
    return path.join(root, SESSIONS_DIR);
}
function loadSessions() {
    const dir = getSessionsDir();
    const idxFile = path.join(dir, 'index.json');
    if (!fs.existsSync(idxFile))
        return [];
    try {
        const data = JSON.parse(fs.readFileSync(idxFile, 'utf-8'));
        return Array.isArray(data.sessions) ? data.sessions : [];
    }
    catch {
        return [];
    }
}
function saveSessions(sessions) {
    const dir = getSessionsDir();
    if (!fs.existsSync(dir))
        fs.mkdirSync(dir, { recursive: true });
    const idxFile = path.join(dir, 'index.json');
    fs.writeFileSync(idxFile, JSON.stringify({ sessions }, null, 2), 'utf-8');
}
function saveActiveId(id) {
    const dir = getSessionsDir();
    if (!fs.existsSync(dir))
        fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, 'active.txt');
    if (id)
        fs.writeFileSync(file, id, 'utf-8');
    else if (fs.existsSync(file))
        fs.unlinkSync(file);
}
function loadActiveId() {
    const file = path.join(getSessionsDir(), 'active.txt');
    if (!fs.existsSync(file))
        return null;
    return fs.readFileSync(file, 'utf-8').trim() || null;
}
function addMessageToSession(sessionId, message) {
    const sessions = loadSessions();
    const session = sessions.find(s => s.id === sessionId);
    if (!session)
        return null;
    session.messages.push(message);
    session.updatedAt = message.timestamp;
    saveSessions(sessions);
    return session;
}
function createSession(name, providerId, model) {
    const now = new Date().toISOString();
    const session = {
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
function deleteSession(sessionId) {
    const sessions = loadSessions().filter(s => s.id !== sessionId);
    saveSessions(sessions);
    const activeId = loadActiveId();
    if (activeId === sessionId)
        saveActiveId(null);
}
//# sourceMappingURL=sessions.js.map