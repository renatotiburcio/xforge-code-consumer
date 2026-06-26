/**
 * XForge Webview Sidebar — Modern VSCode UI
 *
 * Provides a custom sidebar with workflow browser,
 * quick actions, and status overview.
 *
 * @module @xforge/sidebar
 */

const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

const PY_ENGINE = path.join(__dirname, '..', 'engine', 'xforge_engine.py');
const DAEMON_CLI = path.join(__dirname, '..', 'engine', 'daemon_cli.py');
const ROOT = path.join(__dirname, '..', '..');
const TIMEOUT_MS = 30000;

function callEngineDirect(tool, args) {
  return new Promise((resolve, reject) => {
    const tmp = path.join(os.tmpdir(), `xforge_sb_${process.pid}_${Date.now()}.json`);
    fs.writeFileSync(tmp, JSON.stringify(args || {}), 'utf8');
    const proc = spawn('python', [PY_ENGINE, tool, '@' + tmp], { encoding: 'utf8', cwd: ROOT });
    let out = ''; let err = '';
    const timer = setTimeout(() => { proc.kill(); reject(new Error('timeout')); }, TIMEOUT_MS);
    proc.stdout.on('data', d => out += d);
    proc.stderr.on('data', d => err += d);
    proc.on('close', code => {
      clearTimeout(timer);
      try { fs.unlinkSync(tmp); } catch (_) {}
      if (code !== 0) return reject(new Error(`exit ${code}: ${err}`));
      try { resolve(JSON.parse(out)); } catch { reject(new Error('non-JSON output')); }
    });
    proc.on('error', reject);
  });
}

class XForgeSidebarProvider {
  constructor(context) {
    this.context = context;
    this.view = null;
    this.workflows = [];
    this.sessions = [];
    this.daemonStatus = 'checking';
    this.activeTab = 'workflows';
  }

  async refresh() {
    if (this.view) {
      this.view.webview.html = this.getHtml();
    }
  }

  resolveWebviewView(webviewView) {
    this.view = webviewView;
    webviewView.webview.options = {
      enableScripts: true,
      retainContextWhenHidden: true,
      localResourceRoots: []
    };
    this.loadData().then(() => {
      webviewView.webview.html = this.getHtml();
    });
    webviewView.webview.onDidReceiveMessage(this.handleMessage.bind(this));
  }

  async loadData() {
    try {
      const list = await callEngineDirect('xforge_workflow_list', {});
      this.workflows = list.workflows || [];
    } catch {
      this.workflows = [];
    }
    try {
      this.sessions = await this.loadSessions();
    } catch {
      this.sessions = [];
    }
    try {
      await new Promise((resolve, reject) => {
        const proc = spawn('python', [DAEMON_CLI, 'status'], { encoding: 'utf8', cwd: ROOT });
        let out = '';
        proc.stdout.on('data', d => out += d);
        proc.on('close', code => { if (code === 0) resolve(out); else reject(new Error()); });
        proc.on('error', reject);
        setTimeout(() => { proc.kill(); reject(new Error('timeout')); }, 5000);
      });
      this.daemonStatus = 'connected';
    } catch {
      this.daemonStatus = 'disconnected';
    }
  }

  async loadSessions() {
    const sessionsDir = path.join(ROOT, '.xforge', 'memory', 'sessions');
    try {
      const entries = await fs.promises.readdir(sessionsDir, { withFileTypes: true });
      const sessions = [];
      for (const entry of entries) {
        if (entry.isDirectory()) {
          try {
            const metaPath = path.join(sessionsDir, entry.name, 'metadata.json');
            const meta = JSON.parse(await fs.promises.readFile(metaPath, 'utf8'));
            sessions.push({ id: entry.name, ...meta });
          } catch {
            sessions.push({ id: entry.name, mode: 'unknown', createdAt: 0 });
          }
        }
      }
      return sessions.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
    } catch {
      return [];
    }
  }

  handleMessage(message) {
    switch (message.type) {
      case 'navigate':
        vscode.commands.executeCommand(`xforge.${message.payload.page}`);
        break;
      case 'runWorkflow':
        vscode.commands.executeCommand('xforge.workflow.run');
        break;
      case 'validateWorkflow':
        vscode.commands.executeCommand('xforge.workflow.validate');
        break;
      case 'searchKnowledge':
        vscode.commands.executeCommand('xforge.knowledge.search');
        break;
      case 'refreshStatus':
        this.loadData().then(() => this.refresh());
        break;
      case 'switchTab':
        this.activeTab = message.payload.tab;
        this.refresh();
        break;
      case 'newSession':
        vscode.commands.executeCommand('xforge.session.new');
        break;
      case 'continueSession':
        vscode.commands.executeCommand('xforge.session.continue', message.payload.sessionId);
        break;
    }
  }

  getSessionsHtml() {
    if (this.sessions.length === 0) {
      return '<div class="empty-state">No sessions yet.<br>Start one with /xforge</div>';
    }
    return this.sessions.map(s => `
      <div class="session-item" onclick="sendMessage('continueSession', { sessionId: '${s.id}' })">
        <span class="session-icon">${s.mode === 'CLEAN' ? '🆕' : s.mode === 'CONTINUED' ? '🔄' : '📋'}</span>
        <div class="session-info">
          <span class="session-id">${s.id.substring(0, 16)}...</span>
          <span class="session-meta">${s.mode || 'Unknown'} • ${s.workingDir || 'No dir'}</span>
        </div>
      </div>
    `).join('');
  }

  getWorkflowListHtml() {
    if (this.workflows.length === 0) {
      return '<div class="empty-state">No workflows found.<br>Create one with /forge</div>';
    }
    return this.workflows.map(w => `
      <div class="workflow-item">
        <span class="workflow-icon">⚡</span>
        <div class="workflow-info">
          <span class="workflow-id">${w.id}</span>
          <span class="workflow-name">${w.name}</span>
        </div>
        <span class="workflow-states">${w.states || '?'} states</span>
      </div>
    `).join('');
  }

  getHtml() {
    const statusIcon = this.daemonStatus === 'connected' ? '🟢' : '🔴';
    const statusText = this.daemonStatus === 'connected' ? 'Daemon running' : 'Daemon offline';
    const tabWorkflows = this.activeTab === 'workflows' ? 'tab-active' : '';
    const tabSessions = this.activeTab === 'sessions' ? 'tab-active' : '';
    const contentWorkflows = this.activeTab === 'workflows' ? '' : 'display:none;';
    const contentSessions = this.activeTab === 'sessions' ? '' : 'display:none;';

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: var(--vscode-font-family); font-size: 13px; color: var(--vscode-foreground); background: var(--vscode-sideBar-background); padding: 8px; }
    .header { display: flex; align-items: center; gap: 8px; padding: 8px 4px; border-bottom: 1px solid var(--vscode-panel-border); margin-bottom: 12px; }
    .header h1 { font-size: 14px; font-weight: 600; }
    .version { font-size: 10px; color: var(--vscode-descriptionForeground); }
    .section { margin-bottom: 16px; }
    .section-title { font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--vscode-descriptionForeground); margin-bottom: 8px; }
    .action-btn { display: flex; align-items: center; gap: 8px; width: 100%; padding: 8px 12px; margin-bottom: 4px; background: transparent; color: var(--vscode-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 12px; text-align: left; }
    .action-btn:hover { background: var(--vscode-list-hoverBackground); }
    .action-btn .icon { font-size: 16px; width: 20px; text-align: center; }
    .status-indicator { display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: var(--vscode-editor-background); border-radius: 4px; margin-bottom: 8px; }
    .status-text { font-size: 11px; }
    .tabs { display: flex; gap: 4px; margin-bottom: 12px; }
    .tab { flex: 1; padding: 6px 8px; text-align: center; font-size: 11px; background: transparent; border: 1px solid transparent; border-radius: 4px; cursor: pointer; color: var(--vscode-descriptionForeground); }
    .tab-active { background: var(--vscode-list-activeSelectionBackground); color: var(--vscode-list-activeSelectionForeground); border-color: var(--vscode-panel-border); }
    .tab:hover { background: var(--vscode-list-hoverBackground); }
    .workflow-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; margin-bottom: 2px; border-radius: 4px; cursor: pointer; }
    .workflow-item:hover { background: var(--vscode-list-hoverBackground); }
    .workflow-icon { font-size: 14px; }
    .workflow-info { flex: 1; display: flex; flex-direction: column; }
    .workflow-id { font-size: 11px; font-weight: 600; }
    .workflow-name { font-size: 10px; color: var(--vscode-descriptionForeground); }
    .workflow-states { font-size: 10px; color: var(--vscode-descriptionForeground); }
    .session-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; margin-bottom: 2px; border-radius: 4px; cursor: pointer; }
    .session-item:hover { background: var(--vscode-list-hoverBackground); }
    .session-icon { font-size: 14px; }
    .session-info { flex: 1; display: flex; flex-direction: column; }
    .session-id { font-size: 11px; font-weight: 600; }
    .session-meta { font-size: 10px; color: var(--vscode-descriptionForeground); }
    .empty-state { text-align: center; padding: 24px 12px; color: var(--vscode-descriptionForeground); font-size: 11px; }
    .new-session-btn { width: 100%; padding: 8px; margin-bottom: 8px; background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
    .new-session-btn:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <div class="header">
    <span style="font-size:18px;">⚡</span>
    <div><h1>XForge Code</h1><span class="version">v1.4.0</span></div>
  </div>
  <div class="section">
    <div class="section-title">Status</div>
    <div class="status-indicator"><span>${statusIcon}</span><span class="status-text">${statusText}</span></div>
  </div>
  <div class="section">
    <div class="section-title">Quick Actions</div>
    <button class="action-btn" onclick="sendMessage('validateWorkflow')"><span class="icon">✅</span> Validate</button>
    <button class="action-btn" onclick="sendMessage('runWorkflow')"><span class="icon">▶️</span> Run</button>
    <button class="action-btn" onclick="sendMessage('searchKnowledge')"><span class="icon">🔍</span> Search</button>
    <button class="action-btn" onclick="sendMessage('refreshStatus')"><span class="icon">🔄</span> Refresh</button>
  </div>
  <div class="section">
    <div class="tabs">
      <button class="tab ${tabWorkflows}" onclick="sendMessage('switchTab', { tab: 'workflows' })">Workflows (${this.workflows.length})</button>
      <button class="tab ${tabSessions}" onclick="sendMessage('switchTab', { tab: 'sessions' })">Sessions (${this.sessions.length})</button>
    </div>
    <div style="${contentWorkflows}">${this.getWorkflowListHtml()}</div>
    <div style="${contentSessions}">
      <button class="new-session-btn" onclick="sendMessage('newSession')">+ New Session</button>
      ${this.getSessionsHtml()}
    </div>
  </div>
  <script>
    const vscode = acquireVsCodeApi();
    function sendMessage(type, payload) { vscode.postMessage({ type, payload: payload || {} }); }
  </script>
</body>
</html>`;
  }
}

function activate(context) {
  const provider = new XForgeSidebarProvider(context);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider('xforge-sidebar', provider, {
      webviewOptions: { retainContextWhenHidden: true }
    })
  );
}

module.exports = { activate };
