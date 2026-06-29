const fs = require('fs');
const c = fs.readFileSync('out/views/ChatViewProvider.js', 'utf-8');
const chatBlock = c.substring(c.indexOf("case 'chat':"), c.indexOf("case 'welcome':"));
fs.writeFileSync('temp/chat-block.txt', chatBlock, 'utf-8');
console.log('Wrote chat block, length:', chatBlock.length);
console.log(chatBlock);
