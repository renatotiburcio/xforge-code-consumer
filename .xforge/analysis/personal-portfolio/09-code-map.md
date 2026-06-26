# Code Map - Personal Portfolio

## Estrutura Final

```
personal-portfolio/
├── index.html         # Pagina principal (~5-10KB)
├── README.md          # Instrucoes de deploy
├── .gitignore         # OS files, .DS_Store, etc
└── assets/
    └── projects/
        ├── erp.png
        ├── task-manager.png
        └── ...
```

## `index.html` estrutura (sugestao)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Joao Silva - Full-Stack Developer</title>
  <meta name="description" content="...">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="...">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: { brand: { 500: '#3b82f6' } },
          fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
        }
      }
    }
  </script>
  <style>
    /* CSS custom minimo */
    html { scroll-behavior: smooth; }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 antialiased">
  <!-- Navigation -->
  <nav>...</nav>

  <!-- Hero (RF-001) -->
  <section id="hero">...</section>

  <!-- Projetos (RF-002) -->
  <section id="projetos">...</section>

  <!-- Experiencia (RF-003) -->
  <section id="experiencia">...</section>

  <!-- Skills (RF-004) -->
  <section id="skills">...</section>

  <!-- Contato (RF-005) -->
  <section id="contato">...</section>

  <!-- Footer -->
  <footer>...</footer>

  <script>
    // Vanilla JS minimo (smooth scroll, mobile menu)
  </script>
</body>
</html>
```

## Linhas estimadas
- `index.html`: ~400-600 linhas (com tudo)
- `README.md`: ~50 linhas
- Total: < 700 linhas
