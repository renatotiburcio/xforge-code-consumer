#!/usr/bin/env node
// XForge MCP Server - thin JSON-RPC 2.0 dispatcher that shells out to the Python engine.
// All real work happens in xforge_engine.py. This file is just the protocol layer.

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");

const MANIFEST = require(path.join(__dirname, "manifest.json"));
const ENGINE = path.join(__dirname, "..", "engine", "xforge_engine.py");
const ROOT = path.resolve(__dirname, "..", "..");

function logErr(msg) {
  process.stderr.write("[xforge-mcp] " + msg + "\n");
}

function callEngine(tool, args) {
  const tmp = path.join(os.tmpdir(), `xforge_args_${process.pid}_${Date.now()}.json`);
  fs.writeFileSync(tmp, JSON.stringify(args || {}), "utf8");
  try {
    const r = spawnSync("python", [ENGINE, tool, "@" + tmp], {
      encoding: "utf8",
      timeout: 120000,
      cwd: ROOT,
    });
    if (r.error) return { ok: false, error: r.error.message };
    if (r.status !== 0) {
      return { ok: false, error: "engine non-zero exit", status: r.status, stderr: r.stderr, stdout: r.stdout };
    }
    try {
      return JSON.parse(r.stdout);
    } catch (e) {
      return { ok: false, error: "engine returned non-JSON", stdout: r.stdout };
    }
  } finally {
    try { fs.unlinkSync(tmp); } catch (_) {}
  }
}

function reply(id, result) {
  process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result }) + "\n");
}

function replyError(id, code, message) {
  process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } }) + "\n");
}

let buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (!line) continue;
    let req;
    try { req = JSON.parse(line); } catch (e) { logErr("bad json: " + e.message); continue; }
    handle(req);
  }
});

function handle(req) {
  const { id, method, params } = req;
  if (method === "initialize") {
    return reply(id, {
      protocolVersion: "2024-11-05",
      serverInfo: { name: "xforge-mcp", version: "1.0.0" },
      capabilities: { tools: {} },
    });
  }
  if (method === "tools/list") {
    return reply(id, { tools: MANIFEST.tools });
  }
  if (method === "tools/call") {
    const name = params && params.name;
    const args = (params && params.arguments) || {};
    if (!name) return replyError(id, -32602, "missing tool name");
    const result = callEngine(name, args);
    return reply(id, {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      isError: !result.ok,
    });
  }
  if (method === "ping") return reply(id, { pong: true });
  return replyError(id, -32601, "method not found: " + method);
}

logErr("started, " + MANIFEST.tools.length + " tools, engine=" + ENGINE);