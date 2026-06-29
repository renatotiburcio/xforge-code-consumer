const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let c = fs.readFileSync(fp, 'utf-8');

// 1. Corrigir o case 'chat': adicionar wrapper em session-item e descorrer o onclick
c = c.replace(
  /'<div class="session-item active" style="background:var\(--vscode-list-hoverBackground,#2a2d2e\);margin-bottom:4px;cursor:pointer" onclick="window._newSession\(\)">' \+ '<div class="session-info"><div class="session-name">\+ Nova conversa<\/div><\/div>' + '<\/div>'/,
  '<div class="session-item" onclick="window._newSession()"><div class="session-info"><div class="session-name"><span style="display:inline-flex;align-items:center;gap:4px">' + plus + ' Nova conversa</span></div></div></div>'
);

// 2. Sessão item template com onclick correto
c = c.replace(
  /return '<div class="session-item' \+ isActive \+ '" onclick="window._selectSession\(\\\'' \+ s.id + '\\\)'">'/,
  "return '<div class=\"session-item' + isActive + '\" onclick=\"window._selectSession(\\'' + s.id + '\\')\">'"
);

// 3. Sidebar toggle correto
c = c.replace(
  /'<button class="sidebar-btn" onclick="window._toggleSidebar\(\)">' \+ history + '<\/button>'/,
  "'<button class=\"sidebar-btn\" onclick=\"window._toggleSidebar()\">' + history + '</button>'"
);

// 4. Header toggle para historico
c = c.replace(
  /'<div class="header-history" onclick="event.stopPropagation\(\);window._toggleSidebar\(\)">' + history + '<\/div>'/,
  "'<div class=\"header-history\" onclick=\"event.stopPropagation();window._toggleSidebar()\">' + history + '</div>'"
);

console.log('Applied:', c.includes('Nova conversa'));

// Reescrever o HTML caso perdido
const htmlStart = c.indexOf('return \'<div class="chat-app">\' +');
if (htmlStart >= 0) {
  const htmlBody = "'<div class=\"chat-app\">' +\n" +
    "    '<div class=\"chat-sidebar\" id=\"historyPanel\">' +\n" +
    "        '<div class=\"sidebar-header\">' +\n" +
    "            '<span class=\"sidebar-title\">Historico</span>' +\n" +
    "            '<button class=\"sidebar-btn\" onclick=\"window._toggleSidebar()\">' + history + '</button>' +\n" +
    "        '</div>' +\n" +
    "        '<div class=\"sidebar-list\">' +\n" +
    "            '<a class=\"session-new\" onclick=\"window._newSession()\">' + plus + 'Nova conversa</a>' +\n" +
    "            sessionsHtml +\n" +
    "        '</div>' +\n" +
    "    '</div>' +\n" +
    "    '<div class=\"chat-main\">' +\n" +
    "        '<div class=\"chat-header\" id=\"headerBtn\">' +\n" +
    "            '<div class=\"header-history\" onclick=\"event.stopPropagation();window._toggleSidebar()\">' + history + '</div>' +\n" +
    "            '<span class=\"pname\" id=\"headerProvider\">OpenRouter</span>' +\n" +
    "            '<span class=\"mname\" id=\"headerModel\">auto</span>' +\n" +
    "            '<span class=\"chev\">' + chevron + '</span>' +\n" +
    "        '</div>' +\n" +
    "        '<div class=\"chat-messages\" id=\"chatContainer\">' ... etc";

// Vamos só escrever o resultado mesmo
fs.writeFileSync(fp, c, 'utf-8');
console.log('OK');
