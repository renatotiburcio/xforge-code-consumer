# Pack xforge-cnab

CNAB 240/400, remessa, retorno, boleto bancario, integracao bancaria.

## Conteudo

| Arquivo | Topico |
|---------|--------|
| `README.md` | Visao geral |
| `cnab-240.md` | Layout CNAB 240 (padrao FEBRABAN) |
| `cnab-400.md` | Layout CNAB 400 (legado) |
| `boleto.md` | Codigo de barras, linha digitavel, carteira |

## Stack

- Python parser (vanilla) ou C# (XForge)
- Validacao por tipo de registro (header, detalhe, trailer)
- Reconciliacao automatica via retorno

## Tags

cnab, banco, boleto, br, integracao, pagamento, febraban
