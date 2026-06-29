---
id: icons-rule
priority: high
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-29
updated: 2026-06-29
---

# Ícones SVG — Pasta de Referencia

> **obrigatorio**: Sempre reutilizar icones SVG da pasta `ref/icones/svg/` (Font Awesome). Nunca criar SVGs inline manualmente quando o icone ja existir la.

## Procedimento

1. Antes de criar qualquer icone, verifique se ja existe em `ref/icones/svg/`.
2. O arquivo segue o padrao `<icone>.svg` em caixa baixa com hifen.
3. O SVG da referencia contem `fill="currentColor"` — preservar para herdar cor do contexto.
4. Copie o arquivo para `src/webview/icons/` com nome curto (sem prefixo `fontawesome-`).
5. O build faz copia automatica para `out/webview/icons/` e o vsce empacota.
6. Referencia em runtime via `getSvgUri('nome.svg')` ou `loadSvg('nome.svg')`.

## Regra de Ouro

SE icone existe em ref/icones/svg → reutilize.
SE nao existe → crie SVG inline via `_icon()`.
