const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname, '..', 'out', 'webview', 'icons');
function icon(f, s) {
  s = s || 14;
  try {
    var c = fs.readFileSync(path.join(dir, f), 'utf-8').trim();
    return c.replace(/^<svg /, '<svg width="' + s + '" height="' + s + '" ');
  } catch (e) { console.log('ERR', f, e.message); return ''; }
}
var chevron = icon('chevron.svg', 14);
var history = icon('history.svg', 14);
var trash = icon('trash.svg', 14);
var plusSvg = icon('plus.svg', 14);
var send = icon('send.svg', 16);
var list = icon('list.svg', 14);
var html = '<!DOCTYPE html><html><head><style>\n';
html += 'body{background:#1e1e1e;color:#ccc;font-family:sans-serif;font-size:13px;margin:0;padding:10px}\n';
html += '.row{display:flex;align-items:center;gap:10px;padding:8px;border-bottom:1px solid #333}\n';
html += '.lbl{color:#888;width:80px}\n';
html += '</style></head><body>\n';
html += '<h3>SVG Icons Test</h3>\n';
html += '<div class="row"><span class="lbl">chevron:</span>' + chevron + '</div>\n';
html += '<div class="row"><span class="lbl">history:</span>' + history + '</div>\n';
html += '<div class="row"><span class="lbl">trash:</span>' + trash + '</div>\n';
html += '<div class="row"><span class="lbl">plus:</span>' + plusSvg + '</div>\n';
html += '<div class="row"><span class="lbl">send:</span>' + send + '</div>\n';
html += '<div class="row"><span class="lbl">list:</span>' + list + '</div>\n';
html += '</body></html>';
fs.writeFileSync(path.join(__dirname, '..', 'out', 'webview', 'test.html'), html, 'utf-8');
console.log('OK write, html len:', html.length);
console.log('chevron len:', chevron.length, 'history len:', history.length);
