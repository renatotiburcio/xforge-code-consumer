/**
 * XForge Node.js SDK
 * Shells out to the Python automation scripts for RAG, LDV, and ACE.
 */
import { execFile } from "child_process";
import { promisify } from "util";
import * as path from "path";
import * as fs from "fs";

const execFileAsync = promisify(execFile);

const SCRIPT_DIR = path.resolve(__dirname, "../../../.kilo/automation/scripts");
const RAG_SCRIPT = path.join(SCRIPT_DIR, "rag/rag_local.py");
const RAG_CACHE_SCRIPT = path.join(SCRIPT_DIR, "rag/rag_cache.py");
const LGPD_SCRIPT = path.join(SCRIPT_DIR, "../.xforge/automation/scripts/lgpd_scanner.py");

export interface QueryOptions {
  top?: number;
  sourceType?: string;
  semantic?: boolean;
}

export interface QueryResult {
  chunkId: string;
  score: number;
  lexicalScore: number;
  semanticScore: number;
  trust: string;
  sourceType: string;
  path: string;
  startLine: number;
  endLine: number;
  excerpt: string;
}

export interface QueryResponse {
  query: string;
  sourceType: string | null;
  mode: string;
  results: QueryResult[];
}

export interface IndexManifest {
  version: string;
  lastIndexedAt: string;
  documentCount: number;
  chunkCount: number;
}

export interface StatusResult {
  stale: boolean;
  lastIndexedAt: string | null;
  currentDocumentCount: number;
  indexedDocumentCount: number;
  addedCount: number;
  changedCount: number;
  removedCount: number;
}

export interface DoctorResult {
  healthy: boolean;
  checks: { name: string; status: string; message: string }[];
  errors: string[];
  warnings: string[];
}

export interface AgentInfo {
  name: string;
  description: string;
  mode: string;
  color: string;
}

export interface SkillInfo {
  name: string;
  description: string;
  path: string;
}

function findProjectRoot(): string {
  let current = process.cwd();
  for (let i = 0; i < 20; i++) {
    if (fs.existsSync(path.join(current, ".kilo")) || fs.existsSync(path.join(current, "kilo.jsonc"))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return process.cwd();
}

async function runPython(scriptPath: string, args: string[], cwd?: string): Promise<any> {
  const env = { ...process.env, PYTHONIOENCODING: "utf-8" };
  const { stdout } = await execFileAsync("python", [scriptPath, ...args], {
    cwd: cwd || findProjectRoot(),
    env,
    maxBuffer: 10 * 1024 * 1024,
  });
  return JSON.parse(stdout);
}

/**
 * Query the RAG index.
 */
export async function queryRag(query: string, options: QueryOptions = {}): Promise<QueryResponse> {
  const args = ["query", "--query", query];
  if (options.top) args.push("--top", String(options.top));
  if (options.sourceType) args.push("--source-type", options.sourceType);
  if (options.semantic) args.push("--semantic");
  return runPython(RAG_SCRIPT, args);
}

/**
 * Build or update the RAG index.
 */
export async function indexRag(): Promise<IndexManifest> {
  return runPython(RAG_SCRIPT, ["index"]);
}

/**
 * Check RAG index status.
 */
export async function statusRag(): Promise<StatusResult> {
  return runPython(RAG_SCRIPT, ["status"]);
}

/**
 * Run incremental cache-based reindex.
 */
export async function incrementalIndex(): Promise<{ changes: number; message: string }> {
  const root = findProjectRoot();
  const scriptPath = path.join(root, ".kilo/automation/scripts/rag/rag_cache.py");
  const env = { ...process.env, PYTHONIOENCODING: "utf-8" };
  const { stdout, stderr } = await execFileAsync("python", [scriptPath], {
    cwd: root,
    env,
    maxBuffer: 1024 * 1024,
  });
  const changes = parseInt(stdout.match(/Changes detected: (\d+)/)?.[1] || "0", 10);
  return { changes, message: stdout };
}

/**
 * Run LGPD compliance scan.
 */
export async function scanLgpd(rootDir?: string): Promise<any> {
  const target = rootDir || findProjectRoot();
  return runPython(
    path.join(findProjectRoot(), ".xforge/automation/scripts/lgpd_scanner.py"),
    [target]
  );
}

/**
 * Run the XForge doctor (pre-commit checks).
 */
export async function doctor(): Promise<DoctorResult> {
  const root = findProjectRoot();
  const scriptPath = path.join(root, ".kilo/automation/scripts/doctor.ps1");
  const checks: { name: string; status: string; message: string }[] = [];
  const errors: string[] = [];
  const warnings: string[] = [];

  try {
    const { stdout, stderr } = await execFileAsync("powershell", [
      "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", scriptPath
    ], { cwd: root, maxBuffer: 1024 * 1024 });

    for (const line of (stdout || "").split("\n")) {
      if (line.includes("[ERROR]")) {
        errors.push(line.replace("[ERROR]", "").trim());
        checks.push({ name: "check", status: "error", message: line });
      } else if (line.includes("[WARN]")) {
        warnings.push(line.replace("[WARN]", "").trim());
        checks.push({ name: "check", status: "warn", message: line });
      } else if (line.includes("[OK]")) {
        checks.push({ name: "check", status: "ok", message: line.replace("[OK]", "").trim() });
      }
    }
  } catch (e: any) {
    errors.push(e.message);
  }

  return { healthy: errors.length === 0, checks, errors, warnings };
}

/**
 * List all available agents from the registry.
 */
export async function listAgents(): Promise<AgentInfo[]> {
  const root = findProjectRoot();
  const registryPath = path.join(root, ".kilo/core/registries/agent-registry.json");
  if (!fs.existsSync(registryPath)) return [];
  const data = JSON.parse(fs.readFileSync(registryPath, "utf-8"));
  return (data.agents || []).map((a: any) => ({
    name: a.name,
    description: a.description,
    mode: a.mode || "primary",
    color: a.color || "#666",
  }));
}

/**
 * List all available skills from the registry.
 */
export async function listSkills(): Promise<SkillInfo[]> {
  const root = findProjectRoot();
  const registryPath = path.join(root, ".kilo/core/registries/skill-registry.json");
  if (!fs.existsSync(registryPath)) return [];
  const data = JSON.parse(fs.readFileSync(registryPath, "utf-8"));
  return (data.skills || []).map((s: any) => ({
    name: s.name,
    description: s.description,
    path: s.path || "",
  }));
}

/**
 * Run LDV analysis on a request.
 */
export async function analyzeRequest(request: string): Promise<any> {
  const root = findProjectRoot();
  const scriptPath = path.join(root, ".xforge/automation/scripts/ldv_engine.py");
  return runPython(scriptPath, ["analyze", request]);
}

/**
 * Run LDV full loop on a request.
 */
export async function runLoop(request: string): Promise<any> {
  const root = findProjectRoot();
  const scriptPath = path.join(root, ".xforge/automation/scripts/ldv_engine.py");
  return runPython(scriptPath, ["run", request]);
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "query": {
      const query = args.slice(1).join(" ");
      const result = await queryRag(query);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case "index": {
      const result = await indexRag();
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case "status": {
      const result = await statusRag();
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case "doctor": {
      const result = await doctor();
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.healthy ? 0 : 1);
      break;
    }
    case "agents": {
      const agents = await listAgents();
      console.log(JSON.stringify(agents, null, 2));
      break;
    }
    case "skills": {
      const skills = await listSkills();
      console.log(JSON.stringify(skills, null, 2));
      break;
    }
    case "analyze": {
      const request = args.slice(1).join(" ");
      const result = await analyzeRequest(request);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case "run": {
      const request = args.slice(1).join(" ");
      const result = await runLoop(request);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    default:
      console.log("XForge Node.js SDK");
      console.log("Usage: node index.js <command> [args]");
      console.log("Commands: query, index, status, doctor, agents, skills, analyze, run");
      process.exit(1);
  }
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
