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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const ChatViewProvider_1 = require("./views/ChatViewProvider");
const providerCommands_1 = require("./commands/providerCommands");
const XOUT = vscode.window.createOutputChannel('XForge', { log: true });
function activate(context) {
    XOUT.appendLine('[xforge] ACTIVATE called');
    vscode.window.showInformationMessage('XForge ativado!');
    const globalState = context.globalState;
    // Register Chat view with globalState for API key persistence
    const chatProvider = new ChatViewProvider_1.ChatViewProvider(context.extensionUri, 'chat', globalState);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('xforge.chatView', chatProvider, {
        webviewOptions: { retainContextWhenHidden: true }
    }));
    // Other views
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('xforge.welcomeView', new ChatViewProvider_1.WelcomeViewProvider()));
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('xforge.agentManagerView', new ChatViewProvider_1.AgentManagerViewProvider()));
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('xforge.settingsView', new ChatViewProvider_1.SettingsViewProvider(globalState)));
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('xforge.modesView', new ChatViewProvider_1.ModesViewProvider()));
    // Commands
    context.subscriptions.push(vscode.commands.registerCommand('xforge.openChat', () => vscode.commands.executeCommand('xforge.chatView.focus')));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.openWelcome', () => vscode.commands.executeCommand('xforge.welcomeView.focus')));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.openSettings', () => vscode.commands.executeCommand('xforge.settingsView.focus')));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.openAgentManager', () => vscode.commands.executeCommand('xforge.agentManagerView.focus')));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.openModes', () => vscode.commands.executeCommand('xforge.modesView.focus')));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.newSession', () => chatProvider.newSession()));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.configureProvider', () => (0, providerCommands_1.configureProviderCommand)(globalState)));
    context.subscriptions.push(vscode.commands.registerCommand('xforge.switchProvider', () => (0, providerCommands_1.showProviderQuickPick)(globalState, chatProvider)));
}
function deactivate() { }
//# sourceMappingURL=extension.js.map