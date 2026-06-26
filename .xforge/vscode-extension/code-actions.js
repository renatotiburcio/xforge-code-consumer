/**
 * XForge CodeActions — Inline Actions for Workflow Files
 *
 * Provides VSCode CodeActions for .xforge/workflow/ files.
 * - Validate workflow on save
 * - Run workflow from editor
 * - Go to definition for state references
 *
 * @module @xforge/code-actions
 */

import * as vscode from 'vscode';

export class WorkflowCodeActionProvider implements vscode.CodeActionProvider {
  private diagnosticCollection: vscode.DiagnosticCollection;

  constructor() {
    this.diagnosticCollection = vscode.languages.createDiagnosticCollection('xforge-workflows');
  }

  provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range,
    context: vscode.CodeActionContext,
    token: vscode.CancellationToken
  ): vscode.CodeAction[] {
    const actions: vscode.CodeAction[] = [];

    if (!document.fileName.includes('.xforge/workflow')) {
      return actions;
    }

    for (const diagnostic of context.diagnostics) {
      if (diagnostic.source !== 'xforge') continue;

      const fix = new vscode.CodeAction(
        `XForge: ${this.getFixLabel(diagnostic.message)}`,
        vscode.CodeActionKind.QuickFix
      );
      fix.command = {
        command: 'xforge.workflow.validate',
        title: 'Validate Workflow',
        arguments: [document.fileName]
      };
      fix.diagnostics = [diagnostic];
      fix.isPreferred = true;
      actions.push(fix);
    }

    const runAction = new vscode.CodeAction(
      'XForge: Run this workflow',
      vscode.CodeActionKind.Empty
    );
    runAction.command = {
      command: 'xforge.workflow.run',
      title: 'Run Workflow'
    };
    actions.push(runAction);

    return actions;
  }

  activate(context: vscode.ExtensionContext): void {
    context.subscriptions.push(
      vscode.languages.registerCodeActionsProvider(
        [{ pattern: '**/.xforge/workflow/**/*.yaml' }, { pattern: '**/.xforge/workflow/**/*.yml' }],
        this
      )
    );

    context.subscriptions.push(
      vscode.workspace.onDidSaveTextDocument((doc) => {
        if (doc.fileName.includes('.xforge/workflow')) {
          this.validateWorkflow(doc);
        }
      })
    );

    context.subscriptions.push(this.diagnosticCollection);
  }

  private validateWorkflow(document: vscode.TextDocument): void {
    const diagnostics: vscode.Diagnostic[] = [];
    const text = document.getText();

    const requiredFields = ['name', 'states', 'transitions'];
    for (const field of requiredFields) {
      if (!text.includes(field)) {
        const range = new vscode.Range(0, 0, 0, 10);
        diagnostics.push(new vscode.Diagnostic(
          range,
          `Missing required field: ${field}`,
          vscode.DiagnosticSeverity.Error
        ));
      }
    }

    this.diagnosticCollection.set(document.uri, diagnostics);
  }

  private getFixLabel(message: string): string {
    if (message.includes('Missing required field')) return 'Add missing field template';
    if (message.includes('Invalid state reference')) return 'Fix state reference';
    return 'Fix issue';
  }

  dispose(): void {
    this.diagnosticCollection.dispose();
  }
}

export function activate(context: vscode.ExtensionContext): void {
  const provider = new WorkflowCodeActionProvider();
  provider.activate(context);
  context.subscriptions.push(provider);
}
