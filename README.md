# XForge Code AI

Extensao VS Code de proxima generacao com Genius Council Framework.

## Funcionalidades

- **Chat com AI** - Streaming em tempo real com multiplos providers
- **Genius Council** - 38+ especialistas virtuais debatem decisoes
- **Multi-sessao** - Agent Manager com worktree isolation
- **@context** - Sistema de contexto inteligente
- **Self-Healing** - 12 regras de auto-correcao

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/xforge` | Menu principal |
| `/analisar-projeto` | Analisa projeto atual |
| `/criar-projeto` | Cria novo projeto |
| `/desenvolver` | Inicia desenvolvimento |
| `/qualidade` | Quality gates |
| `/seguranca` | Auditoria de seguranca |

## Configuracao

```json
{
  "xforge.provider": "openrouter",
  "xforge.model": "claude-sonnet-4",
  "xforge.streaming": true,
  "xforge.autoAccept": false
}
```

## Desenvolvimento

```bash
npm install
npm run compile
# F5 para debug
```