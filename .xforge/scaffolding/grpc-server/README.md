# XForge gRPC Headless Server

## Setup

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. xforge.proto
```

## Run

```bash
python server.py
```

## Endpoints

| Method | Description |
|--------|-------------|
| `Doctor` | Run doctor validation |
| `IndexRag` | Index RAG knowledge base |
| `QueryRag` | Query RAG index |
| `RagHealth` | RAG health check |
| `ListAgents` | List all agents |
| `GetAgent` | Get agent details |
| `ListSkills` | List all skills |
