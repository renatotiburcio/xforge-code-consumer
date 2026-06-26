# Manual Content Depth Standard (DR-0182, B-090 + DR-0184, B-092)

> **Regra de Ouro**: Cada pagina HTML em `docs/` deve espelhar o artefato real com **exatamente 6 secoes** na ordem canonica. Sem excecao.
>
> **B-092 Visual Lock (DR-0184)**: Regras inviolaveis abaixo. Violacao BLOQUEIA commit.

## 0. Proibicoes Inviolaveis (B-092, DR-0184)

Qualquer violacao destas regras faz o validator retornar exit 1 (BLOQUEIA commit):

1. **PROIBIDO**: `<script src="*.tailwindcss.com">` em qualquer manual page
   - Razao: Tailwind preflight reseta h1/h2/h3/p, sobrescreve style.css
   - Historia: v50.1.0 Ã¢â€ â€™ v50.2.5 teve 5 ciclos de regressao por causa disso
2. **PROIBIDO**: `<style>` inline em qualquer manual page (apenas index.html e _template.html podem ter)
   - Razao: HTML duplica CSS, fica fora de sincronia
3. **PROIBIDO**: Remover cache-busting `?v=VERSION` de style.css e script.js
   - Razao: browser serve versao antiga apos commit
4. **PROIBIDO**: Mover style.css de `docs/style.css` (path canonico)
5. **PROIBIDO**: Mais de 1 h1 por pagina (canonical = 1 h1 titulo da pagina)
6. **PROIBIDO**: Ordem das 6 secoes canonicas (template canonico)
7. **PROIBIDO**: Renomear classes `.hero`, `.card`, `.grid`, `.cta`, `.callout` (usadas por 18 paginas)

## 1. As 6 Secoes Canonicas

Toda pagina de manual (`docs/manual/*.html`, exceto `_template.html` e `index.html`) DEVE ter, NA ORDEM:

### 1.1 O que e
- 3-5 linhas
- Definicao concreta do artefato (nao abstrata)
- Resposta direta a "o que e isso?"

### 1.2 Quando usar
- 3-5 bullets
- Triggers de uso especificos
- NAO e uma lista generica

### 1.3 Como usar
- Bloco `<pre><code>` com sintaxe canonica
- Parametros posicionais vs nomeados visiveis
- Comandos copy-pasteable (sem pseudo-codigo)

### 1.4 Parametros
- Tabela `<table>`
- Colunas: Parametro, Tipo, Default, Descricao, Obrigatorio?
- TODOS os parametros listados (mesmo deprecated)

### 1.5 Exemplos praticos
- 3-7 cenarios REAIS
- Cada cenario: titulo, comando exato, output esperado, edge case
- Copy-pasteable sem edicao
- Cenarios cobrem variabilidade (nao duplicar)

### 1.6 Troubleshooting
- 2-5 problemas comuns
- Formato: Sintoma Ã¢â€ â€™ Causa Ã¢â€ â€™ Solucao
- Incluir mensagens de erro literais

## 2. Limites Numericos

| Metrica | Limite | Razao |
|---|---:|---|
| Tamanho HTML por pagina | < 25 KB | Sem text-walls; mobile-friendly. Excecao justificada em DR-0182 (catalogo de 397 artefatos justifica densidade). |
| Exemplos praticos | 3-7 | Quality > quantity; AG022 Rams |
| Tempo de leitura | 3-5 min | Jobs: "resolver em 5 min" |
| Sub-secoes por secao | <= 4 | Hierarquia rasa |
| Parametros por pagina | <= 15 | Tabela legivel |
| Linhas de codigo por exemplo | <= 30 | Copy-paste viavel |
| Issues no troubleshooting | 2-5 | Foco nos reais |

**Nota sobre limite de tamanho (historico)**: 15 KB (original) -> 18 KB (DR-0182 v50.4.0) -> 20 KB -> 21 KB (v50.31.0 aside) -> **25 KB (v50.35.0 catalog expansion)**. Paginas com conteudo narrativo devem continuar <= 18 KB; paginas-catalogos podem ir ate 25 KB (justificado em DR-0182 para listas de 30+ artefatos).

## 3. Templates por Secao

### 3.1 O que e (template)

```html
<h2>O que e</h2>
<p>[ARTEFATO] e [DEFINICAO CONCRETA] que [ACAO PRIMARIA].
Diferente de [ALTERNATIVA COMUM], [ARTEFATO] faz [DIFERENCIAL].
</p>
```

### 3.2 Quando usar (template)

```html
<h2>Quando usar</h2>
<ul>
  <li>Quando [TRIGGER 1]</li>
  <li>Quando [TRIGGER 2]</li>
  <li>Quando [TRIGGER 3]</li>
  <li>NAO use para [ANTI-TRIGGER 1]</li>
</ul>
```

### 3.3 Como usar (template)

```html
<h2>Como usar</h2>
<p>Sintaxe canonica:</p>
<pre><code>[COMANDO/SINTAXE COMPLETA]</code></pre>
<p>[BREVE EXPLICACAO]</p>
```

### 3.4 Parametros (template)

```html
<h2>Parametros</h2>
<table>
<tr><th>Parametro</th><th>Tipo</th><th>Default</th><th>Descricao</th></tr>
<tr><td><code>--nome</code></td><td>string</td><td>""</td><td>[DESCRICAO]</td><td>Nao</td></tr>
<tr><td><code>--flag</code></td><td>bool</td><td>false</td><td>[DESCRICAO]</td><td>Nao</td></tr>
</table>
```

### 3.5 Exemplos praticos (template)

```html
<h2>Exemplos praticos</h2>

<h3>Cenario 1: [NOME]</h3>
<p><strong>Contexto</strong>: [DESCRICAO DA SITUACAO REAL]</p>
<pre><code>[COMANDO REAL]</code></pre>
<p><strong>Output esperado</strong>:</p>
<pre><code>[OUTPUT REAL]</code></pre>
<p><strong>Edge case</strong>: [O QUE DA ERRADO E COMO TRATAR]</p>

<h3>Cenario 2: [NOME]</h3>
[mesmo formato]
```

### 3.6 Troubleshooting (template)

```html
<h2>Troubleshooting</h2>

<h3>[SINTOMA]</h3>
<p><strong>Causa</strong>: [CAUSA]</p>
<p><strong>Solucao</strong>: [PASSO 1] -> [PASSO 2]</p>
```

## 4. Caso Especial: xforge-init

A skill/comando `xforge-init` e o caso mais importante do manual. DEVE ter **5 cenarios explicitos** na secao Exemplos:

### Cenario 1: Projeto Limpo
Pasta vazia. Setup from scratch.

```bash
mkdir meu-projeto && cd meu-projeto
xforge init
# Output: instalacao completa + .kilo/ + .xforge/ criados
```

### Cenario 2: Projeto com Pasta de Documentos
Pasta tem specs, RFCs, decisoes previas. Init deve absorver, analisar, gerar docs canonicas.

```bash
xforge init --absorb-docs ./minha-pasta-docs/
# Output: 47 docs analisadas, 12 knowledge entries criadas
#          3 DRs sugeridas, project-dna.md gerado
# A pasta original pode ser deletada depois
```

### Cenario 3: Projeto Existente (sem docs)
Ja tem codigo, git, config. Init deve detectar e aprender.

```bash
cd projeto-legado
xforge init --analyze-existing
# Output: stack detectado (.NET 8), 53 arquivos analisados
#          PADROES identificados, .kilo/ + .xforge/ nao sobrescrevem
```

### Cenario 4: Projeto Existente + Documentos
Combinacao 2+3. Mais complexo.

```bash
cd projeto-legado
xforge init --analyze-existing --absorb-docs ./legado-docs/
# Output: stack + absorcao combinados
```

### Cenario 5: Customizacao Avancada
Template custom, variaveis de ambiente.

```bash
xforge init --template enterprise-v2 --config ./xforge.yaml
# Output: setup com template customizado
```

## 5. Aplicacao

Esta regra se aplica a:
- `docs/index.html` (versao resumida, nao completa)
- `docs/manual/01-quickstart.html` ate `11-faq.html`
- `docs/manual/_template.html` (referencia, nao validado)

Excluido:
- `docs/decisions/README.md` (stub canonico)
- `docs/README.md`, `docs/SUMMARY.md`, `docs/getting-started.md` (meta)

## 6. Validacao Automatica

Script `.kilo/automation/scripts/check-manual-content.ps1` valida:

```powershell
# Para cada pagina de manual:
# 1. Tem 6 secoes <h2> na ordem canonica?
# 2. Cada secao tem conteudo minimo (> 50 chars)?
# 3. Tem 3-7 exemplos praticos?
# 4. Tem tabela de parametros?
# 5. Tem troubleshooting?
# 6. Tamanho < 25 KB?
# Exit 0 se todas passam; 1 se qualquer falha
```

Integrado em `doctor.ps1` como **Gate 5** (apos Gate 4 do DR-0181).

## 7. Anti-Padroes

- **NAO** criar paginas < 30 linhas (placeholder)
- **NAO** duplicar exemplos entre paginas (cada exemplo deve ser unico)
- **NAO** usar pseudo-codigo (todos exemplos devem rodar)
- **NAO** listar mais de 15 parametros (refatorar)
- **NAO** ter mais de 7 exemplos (cortar excesso)
- **NAO** misturar linguas (pt-BR ou en-US, consistente)

## 8. Aplicacao Imediata (v50.1.0)

Todas as 12 paginas existentes serao refatoradas para conformar.

## 9. Referencias

- DR-0181 (estrutura canonica do manual)
- DR-0182 (este design)
- DR-0087 (release-immutability)
- AG005 Dijkstra (simplicidade)
- AG022 Rams (menos-mas-melhor)
- AG019 Norman (affordance)
- AG020 Nielsen (heuristicas)