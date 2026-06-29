# Anti-padrões Identificados

## AP-1: God Object Extension
- **Onde**: Vários projetos têm extension.ts monolítico
- **Problema**: Difícil de manter e testar
- **Mitigação**: Modularização em serviços

## AP-2: Hardcoded Provider Assumptions
- **Onde**: Algumas ferramentas assumem formato OpenAI
- **Problema**: Quebra com outros provedores
- **Mitigação**: Provider-agnostic abstractions

## AP-3: No Compaction Strategy
- **Onde**: 9 de 10 projetos
- **Problema**: Context overflow = sessão perdida
- **Mitigaçãoeligente
- **Referência**: Kilo Code (único com compaction)

## AP-4: No Error Learning
- **Onde**: Todos os projetos
- **Problema**: Mesmos erros repetidos
- **Mitigação**: Error graph + self-healing

## AP-5: No Memory Isolation
- **Onde**: Todos os projetos
- **Problema**: Memória pode vazar entre projetos
- **Mitigação**: Memory namespace isolation

## AP-6: No Security Boundaries
- **Onde**: 9 de 10 projetos
- **Problema**: Pode ler qualquer arquivo
- **Mitigação**: Glob-pattern permissions
- **Referência**: Kilo Code

## AP-7: Single-Model Approach
- **Onde**: 9 de 10 projetos
- **Problema**: Caro para tarefas simples
- **Mitigação**: Router + Worker
- **Referência**: Kilo Code

## AP-8: No Decision Records
- **Onde**: Todos os projetos
- **Problema**: Decisões sem rastreabilidade
- **Mitigação**: DR automáticos via Genius Council

## AP-9: No Stack Adaptation
- **Onde**: Maioridade assume JS/TS
- **Problema**: Sugestões inadequadas
- **Mitigação**: Stack detection + specific patterns

## AP-10: Secrets in Code
- **Onde**: Alguns exemplos têm API keys hardcoded
- **Problema**: Security risk
- **Mitigação**: Secret detection + .env enforcement