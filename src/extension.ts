import * as vscode from 'vscode';
import { ChatViewProvider } from './views/ChatViewProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('XForge Code AI is now active!');

    const chatViewProvider = new ChatViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('xforge.chatView', chatViewProvider, {
            webviewOptions: { retainContextWhenHidden: true }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openChat', () => {
            vscode.commands.executeCommand('xforge.chatView.focus');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openWelcome', () => {
            vscode.commands.executeCommand('xforge.chatView.focus');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openSettings', () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'xforge');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.openAgentManager', () => {
            vscode.window.showInformationMessage('Agent Manager - Coming soon!');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('xforge.newSession', () => {
            chatViewProvider.newSession();
        })
    );
}

export function deactivate() {}