const fs = require('fs');
// Simula HTML gerado
const c = fs.readFileSync('out/views/ChatViewProvider.js', 'utf-8');
// Extrai parte que gera HTML
const startIdx = c.indexOf('_getHtmlForWebview(');
const bodyIdx = c.indexOf('switch (this._viewContext)');
console.log('_getHtmlForWebview at:', startIdx);
console.log('switch at:', bodyIdx);

// Simula execução manual do HTML
const iconFn = (name) => {
  const icons = {
    chevron: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
    send: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 11l5-5 5 5M12 6v12"/></svg>',
  };
  return icons[name] || '';
};

const chevron = iconFn('chevron');
const send = iconFn('send');

const body = '<div class="chat-grid">' +
  '<div class="chat-header" id="headerBtn" title="Test"><span class="pname" id="headerProvider">OpenRouter</span><span class="mname">auto</span><span class="chev">' + chevron + '</span></div>' +
  '<div class="chat-container" id="chatContainer"><div class="welcome" id="welcome"><h2>Bem-vindo!</h2></div></div>' +
  '<div class="input-area"><div class="input-wrapper"><textarea id="messageInput"></textarea><button class="send-btn">' + send + '</button></div></div>' +
  '</div>';

const styles = [
  '* { margin:0; padding:0; box-sizing:border-box; }',
  'html, body { margin:0; padding:0; height:100%; }',
  'body { font-family:sans-serif; font-size:13px; }',
  '.chat-grid { display:grid; grid-template-rows:auto 1fr auto; height:100%; }',
  '.chat-header { padding:8px; background:red; }',
  '.chat-container { overflow-y:auto; padding:12px; min-height:0; }',
  '.input-area { padding:12px; background:green; }',
].join('\n');

const html = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><style>${styles}</style></head><body data-context="chat">${body}<script></script></body></html>`;
fs.writeFileSync('temp/test-render.html', html, 'utf-8');
console.log(html);
console.log('File written to temp/test-render.html');
