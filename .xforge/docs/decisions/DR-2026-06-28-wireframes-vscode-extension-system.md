# DR-2026-06-28 - Redesign completo dos wireframes como extensao VS Code

## Conselho dos Genios: Wireframes VS Code-native para XForge Code AI

### 1. Discovery (Turing)
O pedido explicito e melhorar todas as paginas de `docs/wireframes` com base em `docs/analysis`. O requisito implicito mais importante e nao transformar o produto em uma web app generica: XForge Code AI deve parecer e funcionar como extensao do VS Code, usando Webview, Side Bar, painel, editor, comandos e status bar.

### 2. Multi-Perspective Analysis
- Norman: cada tela precisa comunicar affordance de extensao: comandos, contexto, aprovacao, diff e feedback imediato.
- Nielsen: recognition over recall; slash commands, `@context`, historico e settings devem ser descobriveis.
- Rams: interface compacta, utilitaria e neutra, sem hero page, sem marketing e sem decoracao.
- Shneiderman: overview, filtros e details-on-demand para sessoes, agents, tools, memoria e auditoria.
- Frost: criar um template comum com componentes repetiveis para todas as paginas.
- Schneier: permissoes, sandbox, arquivos sensiveis e audit trail devem aparecer como fluxos reais.
- Martin: usar HTML estatico simples, autocontido por pagina, sem dependencias externas.
- Dijkstra: uma responsabilidade por pagina; telas de exemplo podem ser muitas, mas cada uma deve ser direta.

### 3. Devil's Advocate (AG999)
1. Refazer tudo e excesso? Nao, o conjunto atual tem padroes inconsistentes e deve alinhar-se ao docs/analysis.
2. Devemos incluir desktop/web/TUI? Como exemplos de extensao, sim apenas quando fazem parte do produto, sem tirar o foco do VS Code.
3. Uma pagina home e aceitavel? Sim se for command center dentro do VS Code, nao landing page.
4. Quantas paginas? O suficiente para cobrir P0-P3: chat, context, diff, agents, settings, security, tools, memory, providers, performance e exemplos.
5. Usar imagens? Como extensao do VS Code, o proprio shell visual da IDE e o produto; icones inline bastam.
6. Manter compatibilidade? Sim, preservar nomes existentes e adicionar novos exemplos.
7. Como validar? Checar HTML essencial, links do indice e ausencia de mojibake.

### 4. 5 Guardians Validation
- Architecture: OK - sistema de paginas estaticas com CSS comum.
- Simplicity: OK - cada tela tem uma finalidade e componentes compactos.
- Security: OK - telas dedicadas a permissoes, approvals, RBAC e audit trail.
- Quality: OK - padrao visual unico, responsivo e sem caracteres corrompidos.
- Documentation: OK - decisao registrada antes da implementacao.

### 5. Consensus (AG100)
Refazer `docs/wireframes` como biblioteca de wireframes VS Code-native. A tela deve sempre lembrar: "isto e uma extensao do VS Code". O padrao oficial sera Activity Bar + Side Bar/Webview + editor/painel opcional + status bar.

### 6. Decision Record
Substituir paginas HTML existentes por versoes consistentes, criar novas paginas de exemplo, gerar um indice navegavel e manter `style.css` como design system comum.

### 7. Next Steps (AG102)
Criar gerador local, emitir paginas, validar links e estrutura, e revisar resultado final.
