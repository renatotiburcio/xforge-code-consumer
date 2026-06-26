# Blazor Server vs WebAssembly vs Hybrid

Guia de decisao para escolher o modelo de hospedagem Blazor certo para cada cenario.

## Blazor Server

- Renderiza no servidor, envia HTML/diffs via SignalR
- Latencia tipica: 30-100ms (depende de round-trip ao servidor)
- Conexao persistente: ~10KB por cliente conectado
- Carga no servidor: alta para muitos usuarios simultaneos
- SEO: nativo (HTML renderizado no servidor)
- Offline: nao suporta

**Quando usar:**
- Apps internos (LAN/VPN) com ate ~500 usuarios simultaneos
- Cenarios com dados sensiveis que nao podem sair do servidor
- Acessos a recursos do servidor (filesystem, banco direto)
- Ambientes com pouca banda para download inicial

## Blazor WebAssembly

- Executa no browser (WebAssembly + runtime .NET)
- Latencia tipica: 5-20ms (apos download)
- Download inicial: 2-10 MB (cached depois)
- Carga no servidor: minima (apenas APIs)
- SEO: limitado (requer pre-rendering)
- Offline: suporta (com Service Worker)

**Quando usar:**
- Apps publicos (internet) com muitos usuarios
- PWAs (Progressive Web Apps)
- Mobile-first ou responsive
- Ambientes com banda alta mas latencia servidor alta

## Blazor Hybrid (.NET MAUI)

- Renderiza nativo (WebView wrapped)
- Latencia: ~0ms (in-process)
- Acessa 100% da plataforma (cameras, GPS, sensores)
- Distribuicao via stores (iOS, Android, Windows, macOS)

**Quando usar:**
- Apps mobile (iOS + Android)
- Apps desktop (Windows + macOS)
- Apps que precisam de UI consistente multiplataforma

## Recomendacao XForge

| Cenario | Modelo |
|---------|--------|
| ERP interno ate 200 usuarios | Blazor Server |
| Portal de cliente (B2B) ate 5000 usuarios | Blazor WebAssembly |
| App de campo (coleta, OS mobile) | Blazor Hybrid |
| Dashboard executivo | Blazor Server |
| Marketplace publico | Blazor WebAssembly |

## Render Modes (.NET 8+)

Com `Blazor Web App` template voce pode misturar:
- `Static SSR`: HTML estatico, sem interatividade
- `Interactive Server`: SignalR, low latency local
- `Interactive WebAssembly`: cliente roda tudo
- `Interactive Auto`: cliente faz upgrade para WASM apos download

## Tags

blazor, server, webassembly, hybrid, maui, signalr, performance, architecture
