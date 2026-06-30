const fs = require('fs');
const path = 'D:/dev/dev/xforge-code-ai/src/views/ChatViewProvider.ts';
let c = fs.readFileSync(path, 'utf-8');

// Encontrar a zona do cleanStreaming e resetCleanBuffer e reescrever limpo
const startMarker = 'let envBuffer =';
const endMarker = 'function resetCleanBuffer';

const si = c.indexOf(startMarker);
const ei = c.indexOf(endMarker);
if (si < 0 || ei < 0) { console.log('Nao achei'); process.exit(1); }

const zonaErrada = c.substring(si, ei);
console.log('zona len:', zonaErrada.length);

const novo = `let envBuffer = '';

function cleanStreaming(token: string): string {
    envBuffer += token;
    const hasEnd = envBuffer.includes('</environment_details>');
    const hasStart = envBuffer.includes('<environment_details>');
    if (hasEnd) {
        const idx1 = envBuffer.indexOf(ENV_BLOCK_START);
        const idx2 = envBuffer.indexOf(ENV_BLOCK_END);
        let out = '';
        if (idx1 >= 0) {
            out = clean(envBuffer.substring(0, idx1)) + clean(envBuffer.substring(idx2 + ENV_BLOCK_END.length));
        } else {
            out = clean(envBuffer.substring(0, idx2));
        }
        envBuffer = '';
        return out;
    }
    if (hasStart) return '';
    const out2 = clean(envBuffer);
    envBuffer = '';
    return out2;
}

`;

c = c.substring(0, si) + novo + c.substring(ei);
fs.writeFileSync(path, c, 'utf-8');
console.log('OK');
