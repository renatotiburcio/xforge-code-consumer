# DR-2026-06-28 - Wireframe VS Code Native para Chat de IA

## Conselho dos Genios: Wireframe de extensao de chat de IA para VS Code

### 1. Discovery (Turing)
A tela precisa parecer uma parte nativa do VS Code, nao uma aplicacao web embutida. O requisito implicito e equilibrar completude com baixa friccao: chat, contexto, modelo, anexos, aprovacoes, historico, acoes de mensagem e status devem estar presentes sem virar painel administrativo.

### 2. Multi-Perspective Analysis
- Norman: priorizar reconhecimento visual, estados claros e comandos previsiveis.
- Nielsen: reduzir ruido, manter hierarquia simples e feedback imediato.
- Frost: tratar a UI como sistema de componentes pequenos e reutilizaveis.
- Shneiderman: expor atalhos e acoes consistentes para usuarios frequentes.
- Martin: manter o prototipo legivel, sem dependencias externas e sem logica acoplada demais.
- Schneier: evitar promessas automaticas perigosas; aprovacoes precisam ser visiveis.

### 3. Devil's Advocate (AG999)
1. A UI esta completa demais? Nao, os recursos aparecem como controles compactos.
2. Parece VS Code? Sim, usa tokens `--vscode-*`, Activity Bar, Side Bar, editor e status bar.
3. Tem excesso de cor? Nao, a cor principal e o accent do VS Code e estados semanticos.
4. Funciona estreito? Sim, a sidebar tem largura fluida e esconde painel secundario em telas pequenas.
5. Depende de rede? Nao, e HTML/CSS/JS autocontido.
6. O fluxo de permissao e claro? Sim, ha modo de aprovacao e um pending change set explicito.
7. Pode virar webview real depois? Sim, os elementos mapeiam para comandos comuns da extension API.

### 4. 5 Guardians Validation
- Architecture: OK - HTML autocontido, sem dependencias externas.
- Simplicity: OK - fluxo unico: contexto, conversa, composer, status.
- Security: OK - aprovacoes e contexto ficam visiveis; sem chamadas remotas.
- Quality: OK - encoding limpo, responsivo, controles com estados.
- Documentation: OK - decisao registrada antes da implementacao.

### 5. Consensus (AG100)
Refazer o candidato como prototipo VS Code-native, preservando a ideia de chat completo, mas removendo acoplamentos visuais de "dashboard" e textos corrompidos. A tela principal deve ser o proprio produto, nao uma landing page.

### 6. Decision Record
Substituir `docs/wireframes/candidatos/canditato-01.html` por uma versao limpa, responsiva, autocontida e alinhada aos tokens do VS Code.

### 7. Next Steps (AG102)
Implementar novo HTML, validar presenca de estrutura essencial e revisar visualmente em navegador quando possivel.
