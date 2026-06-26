# UI/UX Flows - Personal Portfolio

## Wireframes (textuais)

### Tela 1: Hero (acima da fold)
```
+------------------------------------------------+
|  [Logo/Name]              [GitHub] [LinkedIn] |
+------------------------------------------------+
|                                                |
|  Joao Silva                                    |
|  Full-Stack Developer                          |
|                                                |
|  10+ anos construindo sistemas web             |
|  escalaveis.                                   |
|                                                |
|  [Ver Projetos]    [Contato]                   |
|                                                |
+------------------------------------------------+
|  v Scroll v                                    |
+------------------------------------------------+
```

### Tela 2: Projetos
```
+------------------------------------------------+
|  ## Projetos                                   |
+------------------------------------------------+
|  +----------+  +----------+  +----------+      |
|  | [thumb]  |  | [thumb]  |  | [thumb]  |      |
|  | Titulo   |  | Titulo   |  | Titulo   |      |
|  | Tech     |  | Tech     |  | Tech     |      |
|  | [link]   |  | [link]   |  | [link]   |      |
|  +----------+  +----------+  +----------+      |
|  (3 colunas desktop, 1 coluna mobile)          |
+------------------------------------------------+
```

### Tela 3: Experiencia
```
+------------------------------------------------+
|  ## Experiencia                                |
+------------------------------------------------+
|  2020 - Atual                                  |
|  Senior Full-Stack Developer @ Acme Corp       |
|  - Lideranca tecnica de squad de 5 devs        |
|  - Stack: React, Node.js, AWS                  |
|                                                |
|  2017 - 2020                                   |
|  Full-Stack Developer @ StartupXYZ              |
|  - ...                                         |
+------------------------------------------------+
```

## Estados por secao

| Secao | Loading | Empty | Error | Success |
|-------|---------|-------|-------|---------|
| Hero | n/a | n/a | n/a | n/a |
| Projetos | n/a | "Em breve..." | n/a | n/a |
| Experiencia | n/a | n/a | n/a | n/a |
| Form (opcional) | "Enviando..." | n/a | "Erro ao enviar. Tente email direto." | "Mensagem enviada!" |

## Fluxo de UX (happy path)

1. Visitante chega -> ve Hero (LCP < 2s)
2. Scrolla -> ve Projetos (RF-002)
3. Clica em um projeto -> abre URL externa (target=_blank, rel=noopener)
4. Scrolla -> ve Experiencia (RF-003)
5. Clica "Contato" -> smooth scroll ate form OU abre mailto:

## Acessibilidade

- Contraste minimo 4.5:1 (texto) / 3:1 (UI)
- Foco visivel em todos os links/botoes (`:focus-visible`)
- ARIA labels em icones (GitHub, LinkedIn, email)
- Navegacao por teclado completa
- `lang="pt-BR"` no `<html>`
- Heading hierarchy: 1 h1 (Hero), h2 (secoes), h3 (cards)
