// Corrigir a linha 258 com problema de template literal quebrado
const fs = require('fs');
const path = require('path');

const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let lines = fs.readFileSync(fp, 'utf-8').split('\n');

// Procurar linha problemática (deve conter 'return ' seguido de outro 'return')
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  // Detecta o padrão: dois returns na mesma linha
  if (line.includes("return '             return")) {
    // Substitui com versão limpa
    lines[i] = `             return '<div class="card' + (isActive ? ' card-active' : '') + '" style="padding:10px;border:1px solid var(--vscode-widget-border,#3c3c3c);border-radius:6px;margin-bottom:8px;cursor:pointer;"><div style="display:flex;justify-content:space-between;"><span style="font-weight:600;font-size:.85rem;">' + (isActive ? 'ok ' : '') + p.label + '</span><span style="font-size:.7rem;color:#888;">' + keyMask + '</span></div><div style="font-size:.75rem;color:#888;margin-top:4px;">' + (isActive ? ('model: ' + sel.model) : 'clique p/ ativar') + '</div></div>';`;
    console.log('Fix line ' + (i + 1));
  }
}

fs.writeFileSync(fp, lines.join('\n'), 'utf-8');
console.log('OK (' + lines.length + ' lines)');
