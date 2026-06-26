// XForge Extension v1.2.3 syntax tests
const fs = require("fs");
const path = require("path");
const EXT = path.resolve(__dirname, "..");
const pkg = JSON.parse(fs.readFileSync(path.join(EXT, "package.json"), "utf8"));
const ext = fs.readFileSync(path.join(EXT, "extension.js"), "utf8");

let pass = 0; let fail = 0;
function check(name, cond) {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else      { fail++; console.log("  FAIL  " + name); }
}
console.log("XForge Extension v" + pkg.version + " tests");
console.log("===================================");
check("version is 1.2.3",                  pkg.version === "1.2.3");
check("name is xforge-kilo",               pkg.name === "xforge-kilo");
check("publisher is xforge",               pkg.publisher === "xforge");
check("node engine >=18.0.0",              /">=18\.0\.0"/.test(JSON.stringify(pkg.engines)));
check("xforge-code.kilo-code dependency",     (pkg.extensionDependencies || []).includes("xforge-code.kilo-code"));
check("xforge.doctor command",             pkg.contributes.commands.some(c => c.command === "xforge.doctor"));
check("xforge.status command",             pkg.contributes.commands.some(c => c.command === "xforge.status"));
check("xforge.workflow.list command",      pkg.contributes.commands.some(c => c.command === "xforge.workflow.list"));
check("xforge.workflow.validate command",  pkg.contributes.commands.some(c => c.command === "xforge.workflow.validate"));
check("xforge.workflow.run command",       pkg.contributes.commands.some(c => c.command === "xforge.workflow.run"));
check("xforge.knowledge.search command",   pkg.contributes.commands.some(c => c.command === "xforge.knowledge.search"));
check("xforge.daemon.start command (new)", pkg.contributes.commands.some(c => c.command === "xforge.daemon.start"));
check("xforge.daemon.stop command (new)",  pkg.contributes.commands.some(c => c.command === "xforge.daemon.stop"));
check("xforge.daemon.status command (new)",pkg.contributes.commands.some(c => c.command === "xforge.daemon.status"));
check("xforge.daemon.autoStart config",    pkg.contributes.configuration.properties["xforge.daemon.autoStart"]);
check("xforge.mcp.enabled config",         pkg.contributes.configuration.properties["xforge.mcp.enabled"]);
check("xforge.knowledge.autoload config",  pkg.contributes.configuration.properties["xforge.knowledge.autoload"]);
check("xforge.provider.preferLocal cfg",   pkg.contributes.configuration.properties["xforge.provider.preferLocal"]);
check("extension has daemon import",       ext.includes("DAEMON_CLI"));
check("extension has daemon start cmd",    ext.includes('"xforge.daemon.start"'));
check("extension has daemon stop cmd",     ext.includes('"xforge.daemon.stop"'));
check("extension has daemon status cmd",   ext.includes('"xforge.daemon.status"'));
check("extension auto-starts daemon",      ext.includes("daemon.autoStart"));
check("extension does not stop on deact",  ext.includes("do not stop daemon"));
check("extension uses spawnSync for CLI",  ext.includes("spawnSync"));
check("extension uses spawn for engine",   ext.includes("spawn("));
check("extension has callEngineDirect",    ext.includes("function callEngineDirect"));
check("extension has callDaemonCli",       ext.includes("function callDaemonCli"));
check("extension exports activate",        ext.includes("module.exports"));
console.log("===================================");
console.log("Result: " + pass + " passed, " + fail + " failed");
process.exit(fail === 0 ? 0 : 1);