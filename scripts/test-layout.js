const fs = require('fs');
const html = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; font-size:13px; background:var(--vscode-sideBar-background); color:var(--vscode-foreground); height:100%; width:100%; overflow:hidden; }
.container { display:flex; flex-direction:column; width:100%; height:100%; position:relative; }
.chat-messages-wrapper { position:relative; flex:1; overflow:hidden; min-height:0; }
.chat-messages { height:100%; overflow:auto; }
.chat-message-row { padding:2px 12px; }
.message-bubble { display:inline-block; max-width:85%; padding:8px 12px; border-radius:8px; font-size:0.8rem; line-height:1.5; }
.user .message-bubble { background:#094771; color:#fff; }
.assistant .message-bubble { background:#2a2d2e; }
.center { display:flex; align-items:center; justify-content:center; width:100%; }
textarea { width:100%; flex:1; background:transparent; border:none; color:var(--vscode-foreground,#ccc); font-size:0.8rem; resize:none; outline:none; min-height:20px; max-height:100px; }
</style>
</head>
<body>
<div class="container">
<div style="background:#111; color:#fff; padding:10px; text-align:center; border-bottom:1px solid #333;" id="headerBtn">
HEADER FIXO
</div>
<div class="chat-messages-wrapper">
<div class="chat-messages" id="msgList">
<div class="center" style="height:100%; color:#888;" id="welcome">BEM-VINDO</div>
</div>
</div>
<div style="background:#111; color:#fff; padding:10px; text-align:center; border-top:1px solid #333;">
FOOTER FIXO
</div>
</div>
<script>
function addMsg(role, text) {
  const w = document.getElementById('welcome'); if(w) w.remove();
  const d = document.createElement('div'); d.className='chat-message-row '+role;
  const b = document.createElement('div'); b.className='message-bubble'; b.textContent=text;
  d.appendChild(b); document.getElementById('msgList').appendChild(d);
  document.querySelector('.chat-messages-wrapper').scrollTop = 999999;
}
document.getElementById('headerBtn').onclick = () => { addMsg('assistant','Header clicado!'); addMsg('user','teste'); };
</script>
</body>
</html>
`;
fs.writeFileSync('temp/test-layout.html', html, 'utf-8');
console.log('OK');
