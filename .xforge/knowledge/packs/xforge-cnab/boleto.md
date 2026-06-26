# Boleto Bancario - Linha Digitavel e Codigo de Barras

Calculo do codigo de barras, linha digitavel e DAC.

## Estrutura do codigo de barras (44 digitos)

```
Posicoes  Conteudo
1-3        Codigo do banco (ex: 001 = Banco do Brasil)
4          Codigo da moeda (9 = Real)
5-9        Codigo do cliente (5 digitos)
10         DAC geral (modulo 11)
11-20      Campo livre (carteira, nosso numero, etc)
21-25      Codigo do cliente (ultimos 5)
26-32      Nosso numero (7 digitos + DAC)
33-37      Agencia + conta
38-44      Valor do titulo (8 digitos, sem virgula)
```

## DAC - Modulo 11

```python
def dac_modulo11(numero):
    peso = 2
    soma = 0
    for c in reversed(str(numero)):
        soma += int(c) * peso
        peso = 2 if peso == 9 else peso + 1
    resto = soma % 11
    dac = 11 - resto
    if dac in (0, 10, 11):
        dac = 1
    return dac
```

## Linha digitavel (47 digitos)

```
Bloco 1 (10): BBB9.XDDDD
  B = codigo banco (3)
  9 = moeda (1)
  X = 5 digitos do codigo barras
  D = DAC bloco 1

Bloco 2 (11): DDDDD.YYYYY.Z
  D = proximos 5 digitos
  Y = proximos 5 + valor (10)
  Z = DAC bloco 2

Bloco 3 (11): WWW.ZZZZZZ.Y
  W = proximos 5
  Z = proximos 6
  Y = DAC bloco 3

Bloco 4 (1): K = DAC geral
```

## Carteiras comuns

| Banco | Carteira | Nosso numero |
|-------|----------|--------------|
| BB | 11, 17, 18, 31 | 1-99999999 |
| Bradesco | 06, 09, 19 | 1-99999999 |
| Itau | 109, 174, 175 | 1-99999999 |
| Santander | 101, 121 | 1-99999999 |
| Caixa | 14, 24, 26 | 1-99999999 |

## Tags

boleto, codigo-barras, dac, modulo-11, banco, br
