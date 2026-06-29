// Corrigir SettingsViewProvider — duplicar return e string quebrada
const fs = require('fs');
const path = require('path');

const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let content = fs.readFileSync(fp, 'utf-8');

// Corrigir linha do SettingsViewProvider (return duplicado)
content = content.replace(
  /return\s+'(\s+return\s+)<div class="card'\s*\+\s*\(isActive\?\s*' card-active'\s*:\s*''\)\s*\+>/,
  "return '<div class=\"card' + (isActive ? ' card-active' : '') + '\" style=\"padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer;\"><div style=\"display:flex;justify-content:space-between;\"><span style=\"font-weight:600;font-size:.85rem;\">' + (isActive ? 'ok ' : '') + p.label + '</span><span style=\"color:#888;font-size:.7rem;\">' + keyMask + '</span style=\"font-size:.75rem;color:#884px;\">' + (isActive ? ('model: ' + sel.model) : 'clique p/ ativar') + '</span></div></div>';"
);

fs.writeFileSync(fp, content, 'utf-8');
console.log('OK');
