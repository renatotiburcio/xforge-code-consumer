// Corrigir layout do chat - CommonJS script
const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let c = fs.readFileSync(fp, 'utf-8');

// 1. Body precisa display:flex flex-direction:column para o layout funcionar
c = c.replace(
  'height:100vh; display:flex; flex-direction:column; }',
  'height:100vh; display:flex; flex-direction:column; overflow:hidden; }'
);

// 2. chat-container precisa min-height:0 para não expandir além do disponível
c = c.replace(
  'overflow-y:auto; padding:12px; min-height:0;',
  'overflow-y:auto; padding:12px; min-height:0; scroll-behavior:smooth;'
);

// 3. Adicionar chat-layout nova regra CSS
c = c.replace(
  '}',
  '}\n.chat-layout { display:flex; flex-direction:column; height:100vh; flex:1; }'
);

// 4. input-area borda fundo
c = c.replace(
  '.input-area { padding:12px; border-top:1px solid var(--vscode-widget-border,#3c3c3c); }',
  '.input-area { padding:12px; border-top:1px solid var(--vscode-widget-border,#3c3c3c); background:var(--vscode-sideBar-background,#1e1e1e); }'
);

fs.writeFileSync(fp, c, 'utf-8');
console.log('OK');
