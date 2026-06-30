const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let lines = fs.readFileSync(fp, 'utf-8').split('\n');

// Encontrar linhas 635-642 (appendAssistantMessage) e remover
let start = -1, end = -1;
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('private _appendAssistantMessage')) start = i;
  if (start >= 0 && i > start && lines[i].includes('private _persistAssistant')) end = i;
}

if (start >= 0 && end >= start) {
  console.log('Removendo linhas', start+1, '-', end);
  lines.splice(start, end - start);
  lines.splice(start, 0, '    private _persistAssistant(content: string): void {');
  fs.writeFileSync(fp, lines.join('\n'), 'utf-8');
  console.log('OK, removido _appendAssistantMessage');
} else {
  console.log('Nao encontrou:', start, end);
}

// Verificar se tem duplicidade
const persistedClauses = lines.filter(l => l.includes('_persistAssistant')).length;
console.log('_persistAssistant references:', persistedClauses);

// Também preciso corrigir a chamada: const finalPrompt cleanText + ...
let hasBug = false;
lines.forEach((l, i) => {
  if (l.includes('const finalPrompt cleanText')) {
    console.log('BUG na linha', i+1);
    lines[i] = '        const finalPrompt = contextBlock ? cleanText + "\n\n```context\n" + contextBlock + "\n```" : cleanText;';
    hasBug = true;
  }
});

if (hasBug) {
  fs.writeFileSync(fp, lines.join('\n'), 'utf-8');
  console.log('Corrigido finalPrompt bug');
}
