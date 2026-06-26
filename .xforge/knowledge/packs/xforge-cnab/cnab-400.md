# CNAB 400 (Legado)

Layout antigo, ainda usado por alguns bancos.

## Estrutura

```
[Header]          Registro 0 (1 linha, 400 chars)
[Detalhe]         Registros 1, 2, 3, 4, 5, 6, 7 (N)
[Trailer]         Registro 9 (1 linha)
```

Cada registro = exatamente 400 caracteres.

## Tipos de registro (CNAB 400)

| Codigo | Tipo |
|--------|------|
| 0 | Header de Arquivo |
| 1 | Remessa - Registro 1 (titulos) |
| 2 | Remessa - Registro 2 (mensagens) |
| 3 | Remessa - Registro 3 (rateio) |
| 4 | Retorno - Titulo |
| 5 | Retorno - Rateio |
| 6 | Retorno - Mensagens |
| 7 | Retorno - Bloqueto |
| 8 | Retorno - Dados sacador |
| 9 | Trailer de Arquivo |

## Quando ainda usar

- Bradesco (alguns produtos legados)
- Itau (cobrancas antigas)
- HSBC (agora Bradesco)

Recomendacao: migrar tudo para CNAB 240 sempre que possivel.

## Tags

cnab, febraban, layout, banco, legado, br
