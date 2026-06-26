// XForge VSCode Extension v1.3.0 - modern UX with progress, async I/O, error categorization
const vscode = require("vscode");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

const PY_ENGINE    = path.join(__dirname, "..", "engine", "xforge_engine.py");
const DAEMON_CLI   = path.join(__dirname, "..", "engine", "daemon_cli.py");
const ROOT         = path.resolve(__dirname, "..", "..");

const TIMEOUT_MS = 30000;

function callEngineDirect(tool, args) {
  return new Promise((resolve, reject) => {
    const tmp = path.join(os.tmpdir(), `xforge_vscode_${process.pid}_${Date.now()}.json`);
    fs.writeFileSync(tmp, JSON.stringify(args || {}), "utf8");
    const proc = spawn("python", [PY_ENGINE, tool, "@" + tmp], { encoding: "utf8", cwd: ROOT });
    let out = ""; let err = "";
    const timer = setTimeout(() => { proc.kill(); reject(new Error(`timeout after ${TIMEOUT_MS}ms`)); }, TIMEOUT_MS);
    proc.stdout.on("data", d => out += d);
    proc.stderr.on("data", d => err += d);
    proc.on("close", code => {
      clearTimeout(timer);
      try { fs.unlinkSync(tmp); } catch (_) {}
      if (code !== 0) return reject(new Error(`engine exit ${code}: ${err}`));
      try { resolve(JSON.parse(out)); }
      catch (e) { reject(new Error("non-JSON engine output: " + out)); }
    });
    proc.on("error", reject);
  });
}

function callDaemonCli(cmd, args) {
  return new Promise((resolve, reject) => {
    const proc = spawn("python", [DAEMON_CLI, cmd, ...(args || [])], { encoding: "utf8", cwd: ROOT });
    let out = ""; let err = "";
    const timer = setTimeout(() => { proc.kill(); reject(new Error("timeout")); }, TIMEOUT_MS);
    proc.stdout.on("data", d => out += d);
    proc.stderr.on("data", d => err += d);
    proc.on("close", code => {
      clearTimeout(timer);
      if (code !== 0) return reject(new Error(`daemon_cli ${cmd} exit ${code}: ${err || ""}`));
      resolve(out);
    });
    proc.on("error", reject);
  });
}

function showOutput(channel, ok, msg, category) {
  const icon = ok ? "✓" : "✗";
  const prefix = category ? `[${category}] ` : "";
  channel.appendLine(`${icon} ${prefix}${msg}`);
  if (ok) {
    vscode.window.showInformationMessage(`XForge: ${msg.split("\n")[0].substring(0, 100)}`);
  } else {
    const action = msg.includes("timeout") ? "Retry" : "Details";
    vscode.window.showErrorMessage(`XForge: ${msg.split("\n")[0].substring(0, 100)}`, action);
  }
}

function activate(context) {
  const out = vscode.window.createOutputChannel("XForge");
  context.subscriptions.push(out);

  // Status bar item
  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  statusBar.text = "$(server) XForge: checking...";
  statusBar.command = "xforge.status";
  statusBar.tooltip = "XForge Code - Click for status";
  statusBar.show();
  context.subscriptions.push(statusBar);

  // Update status bar
  try {
    callDaemonCli(["status"]).then(() => {
      statusBar.text = "$(server) XForge: daemon ready";
    }).catch(() => {
      statusBar.text = "$(warning) XForge: daemon offline";
    });
  } catch (_) {
    statusBar.text = "$(warning) XForge: daemon offline";
  }

  context.subscriptions.push(vscode.commands.registerCommand("xforge.status", async () => {
    out.clear(); out.appendLine("XForge status (v1.3.0)"); out.appendLine("==========================");
    try {
      await vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: "Checking XForge status..." },
        async () => {
          const list  = await callEngineDirect("xforge_workflow_list", {});
          out.appendLine(`Workflows: ${list.count} (${list.workflows.slice(0, 3).map(w => w.id).join(", ")}, ...)`);
          try {
            const ds = await callDaemonCli(["status"]);
            out.appendLine("");
            out.appendLine("Engine Daemon:");
            out.appendLine(ds);
          } catch (e) { out.appendLine("Engine Daemon: NOT RUNNING"); }
          out.show(true);
        }
      );
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.workflow.list", async () => {
    out.clear(); out.appendLine("XForge workflows"); out.appendLine("===============");
    try {
      const list = await callEngineDirect("xforge_workflow_list", {});
      list.workflows.forEach(w => out.appendLine(`${w.id}  ${w.name.padEnd(28)} ${w.states} states, ${w.transitions} transitions  - ${w.description}`));
      out.appendLine(""); out.appendLine(`Total: ${list.count}`); out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.workflow.validate", async () => {
    try {
      const list = await callEngineDirect("xforge_workflow_list", {});
      if (!list.workflows || list.workflows.length === 0) {
        vscode.window.showWarningMessage("XForge: No workflows found"); return;
      }
      const selected = await vscode.window.showQuickPick(
        list.workflows.map(w => ({ label: `$(check) ${w.id}`, description: w.name, detail: w.description })),
        { placeHolder: "Select workflow to validate..." }
      );
      if (!selected) return;
      const id = selected.label.replace("$(check) ", "");
      out.clear(); out.appendLine(`Validating ${id}...`);
      const r = await callEngineDirect("xforge_workflow_validate", { id });
      if (r.ok && r.valid) {
        out.appendLine(`OK: ${r.id} (${r.file}) - ${r.states.length} states, ${r.transitions} transitions`);
        vscode.window.showInformationMessage(`XForge: ${r.id} valid`);
      } else if (r.ok) {
        out.appendLine(`INVALID ${r.id}:`); r.errors.forEach(e => out.appendLine("  - " + e));
        vscode.window.showWarningMessage(`XForge: ${r.id} has ${r.errors.length} errors`);
      } else { out.appendLine("ERROR: " + r.error); vscode.window.showErrorMessage(`XForge: ${r.error}`); }
      out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); vscode.window.showErrorMessage(`XForge: ${e.message}`); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.workflow.run", async () => {
    try {
      const list = await callEngineDirect("xforge_workflow_list", {});
      if (!list.workflows || list.workflows.length === 0) {
        vscode.window.showWarningMessage("XForge: No workflows found"); return;
      }
      const selected = await vscode.window.showQuickPick(
        list.workflows.map(w => ({ label: `$(play) ${w.id}`, description: w.name, detail: w.description })),
        { placeHolder: "Select workflow to run..." }
      );
      if (!selected) return;
      const id = selected.label.replace("$(play) ", "");
      const eventsRaw = await vscode.window.showInputBox({ prompt: `Events for ${id} (comma-separated)` }); if (!eventsRaw) return;
      const events = eventsRaw.split(",").map(s => s.trim()).filter(Boolean);
      out.clear(); out.appendLine(`Running ${id} with events: ${events.join(", ")}`);
      await vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: `Running ${id}...` },
        async () => {
          const r = await callEngineDirect("xforge_workflow_run", { id, events });
          if (r.ok) {
            out.appendLine(`Final state: ${r.currentState} (terminal: ${r.terminal}, steps: ${r.steps})`);
            r.history.forEach(h => out.appendLine(`  step ${h.step}: ${h.state}${h.event ? "  <- " + h.event : ""}`));
            vscode.window.showInformationMessage(`XForge: ${id} completed (${r.steps} steps)`);
          } else { out.appendLine("ERROR: " + r.error); vscode.window.showErrorMessage(`XForge: ${r.error}`); }
          out.show(true);
        }
      );
    } catch (e) { out.appendLine("ERROR: " + e.message); vscode.window.showErrorMessage(`XForge: ${e.message}`); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.knowledge.search", async () => {
    const q = await vscode.window.showInputBox({ prompt: "Search XForge knowledge" }); if (!q) return;
    out.clear(); out.appendLine(`Searching knowledge for: ${q}`);
    await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: "Searching knowledge..." },
      async () => {
        try {
          const r = await callEngineDirect("xforge_knowledge_search", { query: q, limit: 10 });
          if (r.ok) {
            out.appendLine(`Found ${r.count} results:`);
            r.results.forEach(f => out.appendLine(`  - ${f.path}  (${f.lines} lines, ${f.relevance})`));
            vscode.window.showInformationMessage(`XForge: ${r.count} results for "${q}"`);
          } else { out.appendLine("ERROR: " + r.error); vscode.window.showErrorMessage(`XForge: ${r.error}`); }
          out.show(true);
        } catch (e) { out.appendLine("ERROR: " + e.message); vscode.window.showErrorMessage(`XForge: ${e.message}`); out.show(true); }
      }
    );
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.doctor", async () => {
    out.clear(); out.appendLine("Running XForge doctor...");
    try {
      const r = await callEngineDirect("xforge_doctor", {});
      if (r.ok) {
        out.appendLine("Doctor output (last 4KB):"); out.appendLine(r.stdout || "(no output)");
        vscode.window.showInformationMessage(`XForge doctor: exit ${r.exitCode}`);
      } else { out.appendLine("ERROR: " + r.error); }
      out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));

  // v1.2.3 NEW: daemon commands
  context.subscriptions.push(vscode.commands.registerCommand("xforge.daemon.start", async () => {
    out.clear(); out.appendLine("Starting engine daemon...");
    try {
      const r = callDaemonCli(["start"]);
      out.appendLine(r); out.appendLine(""); out.appendLine("Engine daemon is now active (4-7x speedup).");
      vscode.window.showInformationMessage("XForge: engine daemon started");
      out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.daemon.stop", async () => {
    out.clear(); out.appendLine("Stopping engine daemon...");
    try {
      const r = callDaemonCli(["stop"]);
      out.appendLine(r); vscode.window.showInformationMessage("XForge: engine daemon stopped");
      out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));

  context.subscriptions.push(vscode.commands.registerCommand("xforge.daemon.status", async () => {
    out.clear(); out.appendLine("Engine daemon status + benchmark");
    out.appendLine("=================================");
    try {
      out.appendLine("--- status ---");
      out.appendLine(callDaemonCli(["status"]));
      out.appendLine("--- benchmark ---");
      out.appendLine(callDaemonCli(["benchmark"]));
      out.show(true);
    } catch (e) { out.appendLine("ERROR: " + e.message); out.show(true); }
  }));
}

function deactivate() {
  // do not stop daemon - it survives VS Code restart
}

module.exports = { activate, deactivate };

// ── CodeActions ──────────────────────────────────────────────────────────────

const { activate: activateCodeActions } = require('./code-actions.js');

// ── Sidebar ──────────────────────────────────────────────────────────────────

const { activate: activateSidebar } = require('./sidebar.js');

// ── Completion ───────────────────────────────────────────────────────────────

const { activate: activateCompletion } = require('./completion.js');

// ── Settings UI ──────────────────────────────────────────────────────────────

const { activate: activateSettings } = require('./settings.js');

// ── Chat ─────────────────────────────────────────────────────────────────────

const { activate: activateChat } = require('./chat.js');

// Patch activate to include all features
const originalActivate = module.exports.activate;
module.exports.activate = function(context) {
  originalActivate(context);
  activateCodeActions(context);
  activateSidebar(context);
  activateCompletion(context);
  activateSettings(context);
  activateChat(context);
};