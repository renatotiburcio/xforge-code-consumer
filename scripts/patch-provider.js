const fs = require('fs');
const path = require('path');
const fp = path.join(__dirname, '..', 'src', 'views', 'ChatViewProvider.ts');
let code = fs.readFileSync(fp, 'utf-8');

// 1. Adicionar loadSvg apos o import
const importLine = "import { icon } from '../webview/icons';";
const loadSvgFn = `
function loadSvg(file, size) {
  size = size || 14;
  try {
    const svgPath = path.resolve(__dirname, '..', 'icons', file);
    let content = fs.readFileSync(svgPath, 'utf-8').trim();
    content = content.replace(/^<svg /, '<svg width="' + size + '" height="' + size + '" ');
    return content;
  } catch (e) {
    return '';
  }
}
`;
code = code.replace(importLine, importLine + '\n' + loadSvgFn);

// 2. Atualizar _icon() para usar loadSvg como fallback
code = code.replace(
  /private _icon\(name, size = 14\) \{[\s\S]*?\n    \}/,
  `private _icon(name, size = 14) {
    const refIcon = loadSvg(name + '.svg', size);
    if (refIcon) return refIcon;
    const s = 'xmlns="http://www.w3.org/2000/svg" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
    return '<svg ' + s + '></svg>';
  }`
);

// 3. Remover _appendAssistantMessage
code = code.replace(/\s*private _appendAssistantMessage\(text\) \{[\s\S]*?\n    \}/g, '');

fs.writeFileSync(fp, code, 'utf-8');
console.log('OK');
