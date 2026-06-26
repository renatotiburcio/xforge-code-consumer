---
id: offline-mode
type: documentacao
tags: [docs, offline, ollama, cache, fallback]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

# Modo Offline

## Visao Geral

O XForge suporta operacao offline quando nao ha conexao com provedores de IA na nuvem. O modo offline usa:

1. **Ollama** como fallback para modelos locais
2. **Cache de respostas** para queries repetidas
3. **Fila pendente** para operacoes que requerem conexao

## Configuracao

Adicione ao `~/.xforge/config.json`:

```json
{
  "offline": {
    "enabled": false,
    "fallbackModel": "ollama/llama3",
    "cacheResponses": true,
    "cacheDir": "~/.xforge/cache",
    "maxCacheSize": "500MB",
    "pendingQueueDir": "~/.xforge/pending",
    "syncOnReconnect": true
  }
}
```

## Ollama Setup

1. Instalar Ollama: https://ollama.com/download
2. Baixar modelo: `ollama pull llama3`
3. Iniciar servidor: `ollama serve`

## Comandos

```powershell
# Verificar status
powershell -File .xforge/scripts/offline-manager.ps1 status

# Habilitar modo offline
powershell -File .xforge/scripts/offline-manager.ps1 enable

# Desabilitar modo offline
powershell -File .xforge/scripts/offline-manager.ps1 disable

# Sincronizar operacoes pendentes
powershell -File .xforge/scripts/offline-manager.ps1 sync
```

## Fluxo de Fallback

```
Request -> Cloud provider available?
  -> Yes: Use cloud model
  -> No:  Ollama running?
           -> Yes: Use local model (ollama/llama3)
           -> No:  Check response cache
                    -> Hit:  Return cached response
                    -> Miss: Queue operation for later sync
```
