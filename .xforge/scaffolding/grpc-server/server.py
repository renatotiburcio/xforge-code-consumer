"""
XForge gRPC Server
Provides RAG query, indexing, doctor, and agent listing via gRPC.
"""
import os
import sys
import json
import time
import subprocess
from concurrent import futures
from pathlib import Path

import grpc
from grpc import ServicerContext

# Add scripts to path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / ".kilo" / "automation" / "scripts" / "rag"))

# Generated proto stubs
sys.path.insert(0, str(Path(__file__).resolve().parent))
import xforge_pb2
import xforge_pb2_grpc

SCRIPT_DIR = ROOT / ".kilo" / "automation" / "scripts"
RAG_SCRIPT = str(SCRIPT_DIR / "rag" / "rag_local.py")
LDV_SCRIPT = str(ROOT / ".xforge" / "automation" / "scripts" / "ldv_engine.py")


def run_python(script_path: str, args: list, cwd: str = None) -> dict:
    """Run a Python script and return parsed JSON output."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        ["python", script_path] + args,
        capture_output=True, text=True, cwd=cwd or str(ROOT), env=env, timeout=120
    )
    if result.returncode != 0:
        return {"error": result.stderr or result.stdout}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout}


def find_project_root() -> Path:
    """Find project root by walking up from CWD."""
    current = Path.cwd()
    for _ in range(20):
        if (current / ".kilo").is_dir() or (current / "kilo.jsonc").exists():
            return current
        parent = current.parent
        if parent == current:
            break
    return current


class XForgeServicer(xforge_pb2_grpc.XForgeServiceServicer):
    """Implementation of XForge gRPC service."""

    def __init__(self):
        self.project_root = find_project_root()

    def QueryRag(self, request: xforge_pb2.RagQueryRequest, context: ServicerContext) -> xforge_pb2.RagQueryResponse:
        """Query the RAG index."""
        try:
            args = ["query", "--query", request.query, "--top", str(request.top or 5)]
            if request.source_type:
                args.extend(["--source-type", request.source_type])
            if request.semantic:
                args.append("--semantic")

            result = run_python(RAG_SCRIPT, args, str(self.project_root))

            response = xforge_pb2.RagQueryResponse()
            response.query = request.query
            response.mode = result.get("mode", "unknown")

            for r in result.get("results", []):
                chunk = response.results.add()
                chunk.chunk_id = r.get("chunkId", "")
                chunk.score = r.get("score", 0)
                chunk.lexical_score = r.get("lexicalScore", 0)
                chunk.semantic_score = r.get("semanticScore", 0)
                chunk.trust = r.get("trust", "")
                chunk.source_type = r.get("sourceType", "")
                chunk.path = r.get("path", "")
                chunk.start_line = r.get("startLine", 0)
                chunk.end_line = r.get("endLine", 0)
                chunk.excerpt = r.get("excerpt", "")

            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.RagQueryResponse()

    def IndexRag(self, request: xforge_pb2.IndexRequest, context: ServicerContext) -> xforge_pb2.IndexResponse:
        """Build or update the RAG index."""
        try:
            result = run_python(RAG_SCRIPT, ["index"], str(self.project_root))

            response = xforge_pb2.IndexResponse()
            response.version = result.get("version", "")
            response.last_indexed_at = result.get("lastIndexedAt", "")
            response.document_count = result.get("documentCount", 0)
            response.chunk_count = result.get("chunkCount", 0)
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.IndexResponse()

    def GetStatus(self, request: xforge_pb2.StatusRequest, context: ServicerContext) -> xforge_pb2.StatusResponse:
        """Get RAG index status."""
        try:
            result = run_python(RAG_SCRIPT, ["status"], str(self.project_root))

            response = xforge_pb2.StatusResponse()
            response.stale = result.get("stale", True)
            response.last_indexed_at = result.get("lastIndexedAt", "")
            response.current_document_count = result.get("currentDocumentCount", 0)
            response.indexed_document_count = result.get("indexedDocumentCount", 0)
            response.added_count = result.get("addedCount", 0)
            response.changed_count = result.get("changedCount", 0)
            response.removed_count = result.get("removedCount", 0)
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.StatusResponse()

    def RunDoctor(self, request: xforge_pb2.DoctorRequest, context: ServicerContext) -> xforge_pb2.DoctorResponse:
        """Run XForge doctor (pre-commit checks)."""
        try:
            script_path = str(self.project_root / ".kilo" / "automation" / "scripts" / "doctor.ps1")
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path],
                capture_output=True, text=True, cwd=str(self.project_root), timeout=60
            )

            response = xforge_pb2.DoctorResponse()
            response.healthy = result.returncode == 0
            response.output = result.stdout
            if result.stderr:
                response.errors = result.stderr
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.DoctorResponse()

    def ListAgents(self, request: xforge_pb2.AgentListRequest, context: ServicerContext) -> xforge_pb2.AgentListResponse:
        """List all available agents."""
        try:
            registry_path = self.project_root / ".kilo" / "core" / "registries" / "agent-registry.json"
            if not registry_path.exists():
                return xforge_pb2.AgentListResponse()

            data = json.loads(registry_path.read_text(encoding="utf-8"))
            response = xforge_pb2.AgentListResponse()

            for agent in data.get("agents", []):
                a = response.agents.add()
                a.name = agent.get("name", "")
                a.description = agent.get("description", "")
                a.mode = agent.get("mode", "primary")
                a.color = agent.get("color", "#666")

            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.AgentListResponse()

    def AnalyzeRequest(self, request: xforge_pb2.AnalyzeRequest, context: ServicerContext) -> xforge_pb2.AnalyzeResponse:
        """Run LDV analysis on a request."""
        try:
            result = run_python(LDV_SCRIPT, ["analyze", request.request], str(self.project_root))
            response = xforge_pb2.AnalyzeResponse()
            response.request_id = result.get("requestId", "")
            response.json_payload = json.dumps(result, ensure_ascii=False)
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return xforge_pb2.AnalyzeResponse()


def serve(port: int = 50051, max_workers: int = 10):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    xforge_pb2_grpc.add_XForgeServiceServicer_to_server(XForgeServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"XForge gRPC server started on port {port}")
    print(f"Project root: {find_project_root()}")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50051
    serve(port)
