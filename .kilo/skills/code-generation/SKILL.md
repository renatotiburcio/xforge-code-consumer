---
name: code-generation
description: Use when writing, editing, or creating code files. Always use write_file or edit_file tools to write code directly to disk. Never output code in chat without writing it.
metadata:
  version: "6.0.0"
  xforge-category: "enterprise-engineer"
---

# code-generation

## Objetivo

Escrever codigo diretamente nos arquivos usando as ferramentas write_file e edit_file.
Nunca descreva codigo no chat sem escrever no arquivo.

## Regra CRITICA

SEMPRE que o usuario pedir para criar, modificar ou corrigir codigo:
1. Leia o arquivo existente primeiro (se existir)
2. Use edit_file para modificar ou write_file para criar
3. Escreva o codigo REAL no arquivo
4. Nunca diga "aqui esta o codigo" sem escrever no disco

## Procedimento

### Para criar arquivo novo:
1. Verifique se o diretorio existe (use bash ls)
2. Crie o diretorio se necessario (use bash mkdir -p)
3. Use write_file com o caminho completo e o codigo completo
4. Confirme que o arquivo foi criado

### Para modificar arquivo existente:
1. Leia o arquivo inteiro primeiro
2. Identifique as linhas exatas a modificar
3. Use edit_file com o bloco antigo e o novo
4. Verifique que a modificacao foi aplicada

### Para multiplas modificacoes:
1. Leia o arquivo uma vez
2. Faca todas as modificacoes em sequencia
3. Nao leia o arquivo novamente entre modificacoes

## Exemplo de Fluxo Completo

Usuario: "Crie um endpoint GET /api/clientes"

Resposta correta:
1. bash: ls src/Controllers/ (verificar estrutura)
2. read_file: src/Controllers/ClientesController.cs (se existir)
3. write_file ou edit_file: criar/modificar o arquivo
4. bash: dotnet build (validar)
5. Reportar o que foi feito

Resposta ERRADA (NAO FAZER):
- Mostrar o codigo no chat e pedir para o usuario copiar
- Dizer "voce pode usar o seguinte codigo"
- Escrever codigo em markdown sem salvar no arquivo

## Modelos Pequenos (64k context)

Quando o modelo tiver contexto pequeno:
1. Leia apenas as linhas necessarias (use offset e limit)
2. Faca uma modificacao por vez
3. Nao leia o arquivo inteiro se for grande
4. Use edit_file em vez de write_file (economiza contexto)
5. Se o contexto encher, salve o progresso e pare
