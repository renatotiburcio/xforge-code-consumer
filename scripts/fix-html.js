const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let lines = fs.readFileSync(fp, 'utf-8').split('\n');

// Encontrar e re-escrever o case 'chat' no _getBodyForContext
const chatIdx = lines.findIndex(l => l.trim() === "case 'chat':");
if (chatIdx >= 0) {
  // A próxima linha é o return
  lines[chatIdx + 1] = "                return '<div class=\"chat-view\"><div class=\"chat-header\" id=\"headerBtn\" title=\"Trocar provider (XForge: Trocar Provider)\"><span class=\"pname\" id=\"headerProvider\">OpenRouter</span><span class=\"mname\" id=\"headerModel\">auto</span><span class=\"chev\">v</span></div><div class=\"chat-messages-wrapper\"><div class=\"chat-messages\" id=\"chatContainer\"><div class=\"welcome\" id=\"welcome\"><div class=\"welcome-icon\">></div><h2>Bem-vindo ao XForge Code AI</h2><p>Seu assistente</p><div class=\"quick-actions\"><div class=\"quick-action\" onclick=\"sendQuick(\\\"Crie uma API\\\")\">Nova API</div><div class=\"quick-action\" onclick=\"sendQuick(\\\"Analise o projeto\\\")\">Analisar</div><div class=\"quick-action\" onclick=\"sendQuick(\\\"Me ajude com testes\\\")\">Testes</div><div class=\"quick-action\" onclick=\"sendQuick(\\\"/help\\\")\">Comandos</div></div></div></div></div><div class=\"input-area\"><div class=\"input-wrapper\"><textarea id=\"messageInput\" placeholder=\"Mensagem... (@ contexto, / comandos)\" rows=\"1\"></textarea><button class=\"send-btn\" id=\"sendBtn\">></button></div></div></div>';";
}

// Atualizar _getHtmlForWebview pra remover #app wrapper
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("'<div id=\"app\">'")) {
    lines[i] = lines[i].replace("'<div id=\"app\">' + body", "' body");
    break;
  }
}

fs.writeFileSync(fp, lines.join('\n'), 'utf-8');
console.log('OK');
