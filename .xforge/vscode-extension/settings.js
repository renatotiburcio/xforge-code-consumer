/**
 * XForge Settings UI — Graphical Configuration Panel
 *
 * Provides a webview-based settings panel for XForge configuration.
 *
 * @module @xforge/settings-ui
 */

const vscode = require('vscode');

class SettingsPanel {
  static createOrShow(context) {
    const column = vscode.window.activeTextEditor
      ? vscode.window.activeTextEditor.viewColumn
      : undefined;

    const panel = vscode.window.createWebviewPanel(
      'xforgeSettings',
      'XForge Settings',
      column || vscode.ViewColumn.One,
      { enableScripts: true, retainContextWhenHidden: true }
    );

    panel.webview.html = this.getHtml(context);
    panel.webview.onDidReceiveMessage(message => {
      switch (message.type) {
        case 'save':
          this.saveSettings(message.payload);
          vscode.window.showInformationMessage('XForge: Settings saved');
          break;
        case 'reset':
          this.resetSettings();
          vscode.window.showInformationMessage('XForge: Settings reset to defaults');
          break;
      }
    });
  }

  static saveSettings(config) {
    const vscodeConfig = vscode.workspace.getConfiguration('xforge');
    for (const [key, value] of Object.entries(config)) {
      vscodeConfig.update(key, value, vscode.ConfigurationTarget.Global);
    }
  }

  static resetSettings() {
    const vscodeConfig = vscode.workspace.getConfiguration('xforge');
    const defaults = {
      'daemon.autoStart': true,
      'daemon.port': 8765,
      'output.format': 'text'
    };
    for (const [key, value] of Object.entries(defaults)) {
      vscodeConfig.update(key, value, vscode.ConfigurationTarget.Global);
    }
  }

  static getHtml(context) {
    const config = vscode.workspace.getConfiguration('xforge');
    const autoStart = config.get('daemon.autoStart', true);
    const port = config.get('daemon.port', 8765);
    const format = config.get('output.format', 'text');

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: var(--vscode-font-family); padding: 20px; color: var(--vscode-foreground); }
    h1 { font-size: 18px; margin-bottom: 20px; }
    .section { margin-bottom: 24px; }
    .section-title { font-size: 13px; font-weight: 600; text-transform: uppercase; color: var(--vscode-descriptionForeground); margin-bottom: 12px; }
    .field { margin-bottom: 16px; }
    label { display: block; font-size: 12px; margin-bottom: 4px; }
    input, select { width: 100%; padding: 6px 8px; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; }
    .checkbox { display: flex; align-items: center; gap: 8px; }
    .checkbox input { width: auto; }
    .actions { display: flex; gap: 8px; margin-top: 24px; }
    button { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
    .btn-primary { background: var(--vscode-button-background); color: var(--vscode-button-foreground); }
    .btn-secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
  </style>
</head>
<body>
  <h1>XForge Settings</h1>
  <div class="section">
    <div class="section-title">Daemon</div>
    <div class="field checkbox">
      <input type="checkbox" id="autoStart" ${autoStart ? 'checked' : ''}>
      <label for="autoStart">Auto-start daemon on activation</label>
    </div>
    <div class="field">
      <label for="port">Daemon Port</label>
      <input type="number" id="port" value="${port}" min="1024" max="65535">
    </div>
  </div>
  <div class="section">
    <div class="section-title">Output</div>
    <div class="field">
      <label for="format">Output Format</label>
      <select id="format">
        <option value="text" ${format === 'text' ? 'selected' : ''}>Text</option>
        <option value="json" ${format === 'json' ? 'selected' : ''}>JSON</option>
        <option value="markdown" ${format === 'markdown' ? 'selected' : ''}>Markdown</option>
      </select>
    </div>
  </div>
  <div class="actions">
    <button class="btn-primary" onclick="save()">Save</button>
    <button class="btn-secondary" onclick="reset()">Reset to Defaults</button>
  </div>
  <script>
    const vscode = acquireVsCodeApi();
    function save() {
      vscode.postMessage({
        type: 'save',
        payload: {
          'daemon.autoStart': document.getElementById('autoStart').checked,
          'daemon.port': parseInt(document.getElementById('port').value),
          'output.format': document.getElementById('format').value
        }
      });
    }
    function reset() {
      vscode.postMessage({ type: 'reset' });
    }
  </script>
</body>
</html>`;
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('xforge.settings', () => {
      SettingsPanel.createOrShow(context);
    })
  );
}

module.exports = { activate };
