# Instalacao

## Regra importante

Copie tambem os arquivos e pastas ocultos:

- `.kilo`
- `.xforge`
- `.kilocodeignore`

Sem eles, o template nao funciona.

## Projeto novo

1. Crie a pasta do projeto.
2. Copie todo o conteudo de `terminal/` para a raiz do projeto, incluindo ocultos.
3. Rode:

```powershell
.\.kilo\automation\scripts\bootstrap-project.ps1
```

4. No KiloCode, execute:

```text
/criar-projeto
```

## Projeto existente

1. Faca backup do projeto.
2. Copie o template para a raiz sem apagar `.xforge` existente.
3. Rode:

```powershell
.\.kilo\automation\scripts\bootstrap-project.ps1
```

4. No KiloCode, execute:

```text
/analisar-projeto
```

## Atualizacao do Engineer

Antes de atualizar:

```powershell
.\.kilo\automation\scripts\backup-engineer.ps1
```

Depois de atualizar:

```powershell
.\.kilo\automation\scripts\doctor.ps1
.\.kilo\automation\scripts\validate-engineer.ps1
.\.kilo\automation\scripts\final-doctor.ps1
```

