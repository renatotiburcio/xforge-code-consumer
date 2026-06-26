/**
 * XForge Inline Completion — Autocomplete for XForge Commands
 *
 * Provides VSCode InlineCompletionItemProvider for XForge commands.
 * Suggests commands as the user types in the editor or terminal.
 *
 * @module @xforge/completion
 */

const vscode = require('vscode');

const XFORGE_COMMANDS = [
  { label: '/xforge', description: 'Main orchestration router', detail: 'Route any request to the right agent' },
  { label: '/xforge-init', description: 'Initialize XForge system', detail: 'Validate and setup entire system' },
  { label: '/analyze', description: 'Analyze code/architecture/product', detail: 'Deep analysis with Genius Council' },
  { label: '/create', description: 'Create anything', detail: 'Projects, features, APIs, docs, training' },
  { label: '/develop', description: 'Develop/fix/refactor code', detail: 'Development with quality gates' },
  { label: '/security', description: 'Security audit', detail: 'Full security and compliance check' },
  { label: '/memory', description: 'Memory management', detail: 'Context, learning, TTL, cycles' },
  { label: '/knowledge', description: 'Knowledge management', detail: 'Search, ingest, curate, trust' },
  { label: '/learn', description: 'Onboarding & learning', detail: 'Project onboarding, Genius training' },
  { label: '/release', description: 'Release management', detail: 'Prepare, validate, ship, rollback' },
];

class XForgeCompletionProvider {
  provideInlineCompletionItems(document, position) {
    const linePrefix = document.lineAt(position).text.substring(0, position.character);

    if (!linePrefix.includes('/xforge') && !linePrefix.includes('/') && linePrefix.length < 2) {
      return undefined;
    }

    const completions = XFORGE_COMMANDS.map(cmd => {
      const item = new vscode.InlineCompletionItem(cmd.label);
      item.command = {
        command: 'editor.action.triggerSuggest',
        title: 'Trigger Suggest'
      };
      return item;
    });

    return completions;
  }
}

function activate(context) {
  const provider = new XForgeCompletionProvider();
  context.subscriptions.push(
    vscode.languages.registerInlineCompletionItemProvider({ pattern: '**' }, provider)
  );
}

module.exports = { activate };
