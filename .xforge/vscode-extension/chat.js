/**
 * XForge Chat — VSCode Chat API Integration
 *
 * Provides a chat participant for VSCode's native chat API.
 * Enables XForge as a chat participant in the VSCode sidebar chat.
 *
 * Requires VSCode 1.90+ (chat API)
 *
 * @module @xforge/chat
 */

const vscode = require('vscode');

class XForgeChatParticipant {
  constructor() {
    this.id = 'xforge.chat';
    this.label = 'XForge';
    this.iconPath = vscode.Uri.file(__dirname + '/../resources/xforge-icon.svg');
  }

  async handleRequest(request, context, stream, token) {
    const query = request.prompt || '';
    
    stream.markdown(`🔍 **XForge** is analyzing your request: "${query}"\n\n`);

    // Simple echo for now — in production, this would call the engine
    const tools = this.suggestTools(query);
    
    if (tools.length > 0) {
      stream.markdown(`**Suggested actions:**\n`);
      for (const tool of tools) {
        stream.markdown(`- \`${tool.command}\` — ${tool.description}\n`);
      }
      stream.markdown(`\nRun one of these commands to proceed.`);
    } else {
      stream.markdown(`Try asking about:\n`);
      stream.markdown(`- \`/analyze\` — Analyze code or architecture\n`);
      stream.markdown(`- \`/create\` — Create projects, features, docs\n`);
      stream.markdown(`- \`/develop\` — Develop or fix code\n`);
      stream.markdown(`- \`/security\` — Run security audit\n`);
      stream.markdown(`- \`/knowledge\` — Search knowledge base\n`);
    }

    return { metadata: { command: 'xforge.chat' } };
  }

  suggestTools(query) {
    const suggestions = [];
    const q = query.toLowerCase();

    if (q.includes('analy') || q.includes('review') || q.includes('audit')) {
      suggestions.push({ command: '/analyze', description: 'Analyze code/architecture' });
    }
    if (q.includes('create') || q.includes('new') || q.includes('build') || q.includes('scaffold')) {
      suggestions.push({ command: '/create', description: 'Create projects, features, docs' });
    }
    if (q.includes('fix') || q.includes('develop') || q.includes('implement') || q.includes('code')) {
      suggestions.push({ command: '/develop', description: 'Develop or fix code' });
    }
    if (q.includes('security') || q.includes('lgpd') || q.includes('check')) {
      suggestions.push({ command: '/security', description: 'Run security audit' });
    }
    if (q.includes('knowledge') || q.includes('search') || q.includes('find')) {
      suggestions.push({ command: '/knowledge', description: 'Search knowledge' });
    }
    if (q.includes('release') || q.includes('deploy') || q.includes('ship')) {
      suggestions.push({ command: '/release', description: 'Release management' });
    }
    if (q.includes('workflow') || q.includes('state') || q.includes('process')) {
      suggestions.push({ command: '/xforge workflow list', description: 'List workflows' });
    }

    return suggestions;
  }

  provideFollowups(result, context, token) {
    return [
      { prompt: 'Tell me more about this', label: 'More details', command: 'xforge.chat' },
      { prompt: 'Show me examples', label: 'Examples', command: 'xforge.chat' },
      { helpText: 'Ask follow-up questions' }
    ];
  }

  welcomeMessage(histories) {
    return [
      { icon: { var: "robot" }, title: 'XForge AI Assistant' },
      'I can help you analyze code, create projects, develop features, run security audits, and more.',
      'Try: "analyze my project", "create a new API", "run security audit"'
    ];
  }
}

function activate(context) {
  try {
    if (vscode.chat) {
      const participant = new XForgeChatParticipant();
      
      // Try to register as chat participant (VSCode 1.90+)
      if (vscode.chat.createChatParticipant) {
        const chatParticipant = vscode.chat.createChatParticipant('xforge.chat', async (request, context, stream, token) => {
          return participant.handleRequest(request, context, stream, token);
        });
        
        chatParticipant.iconPath = vscode.Uri.file(__dirname + '/../resources/xforge-icon.png');
        context.subscriptions.push(chatParticipant);
      }
    }
  } catch (e) {
    // Chat API not available — silent fail
  }
}

module.exports = { activate, XForgeChatParticipant };
