import * as vscode from 'vscode';
import {
    ChatViewProvider,
    WelcomeViewProvider,
    AgentManagerViewProvider,
    SettingsViewProvider,
    ModesViewProvider
} from './views/ChatViewProvider';
import { configureProviderCommand, showProviderQuickPick } from './commands/providerCommands';

const XOUT = vscode.window.createOutputChannel('XForge', { log: true });

export function activate(context: vscode.ExtensionContext) {
    XOUT.appendLine('[xforge] ACTIVATE called');
    vscode.window.showInformationMessage('XForge ativado!');
    const globalState = context.globalState;

    // Register Chat view with globalState for API key persistence
    const chatProvider = new ChatViewProvider(context.extensionUri, 'chat', globalState);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.chatView', chatProvider, {
            webviewOptions: { retainContextWhenHidden: true }
        })
    );

    // Other views
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.welcomeView', new WelcomeViewProvider(context.extensionUri))
    );
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.agentManagerView', new AgentManagerViewProvider())
    );
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.settingsView', new SettingsViewProvider(globalState))
    );
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.modesView', new ModesViewProvider())
    );

    // Commands
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openChat', () => vscode.commands.executeCommand('xforge.chatView.focus'))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openWelcome', () => vscode.commands.executeCommand('xforge.welcomeView.focus'))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openSettings', () => vscode.commands.executeCommand('xforge.settingsView.focus'))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openAgentManager', () => vscode.commands.executeCommand('xforge.agentManagerView.focus'))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openModes', () => vscode.commands.executeCommand('xforge.modesView.focus'))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.newSession', () => {
            if ('_startNewSession' in chatProvider) (chatProvider as any)._startNewSession();
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.configureProvider', () => configureProviderCommand(globalState))
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.switchProvider', () => showProviderQuickPick(globalState, chatProvider))
    );
}

export function deactivate() {}
