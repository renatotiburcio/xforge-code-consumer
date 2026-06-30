const fs = require('fs');
const fp = 'src/views/ChatViewProvider.ts';
let lines = fs.readFileSync(fp, 'utf-8').split('\n');
// Remover linhas 359-362 (índices 358, 359, 360, 361) são as quebradas
lines.splice(358, 4);
fs.writeFileSync(fp, lines.join('\n'), 'utf-8');
console.log('OK removidas 4 linhas, total agora:', lines.length);
