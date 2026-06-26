# CNAB 240 (Padrao FEBRABAN)

Layout padrao para troca de arquivos com bancos brasileiros.

## Estrutura do arquivo

```
[Header Arquivo]       Registro 0 (1 linha)
[Header Lote]          Registro 1 (1 por lote)
[Registros Detalhe]    Registros 3, 4, 5, 6, 7, 8 (N por lote)
[Trailer Lote]         Registro 9 (1 por lote)
[Trailer Arquivo]      Registro 9 (1 linha)
```

Cada registro = exatamente 240 caracteres.

## Tipos de registro

| Codigo | Tipo |
|--------|------|
| 0 | Header de Arquivo |
| 1 | Header de Lote |
| 3 | Detalhe - Segmento A (vencimento, valor) |
| 4 | Detalhe - Segmento B (codigo, juros, multa) |
| 5 | Detalhe - Segmento C (informacoes complementares) |
| 6 | Detalhe - Segmento J (remessa) ou Z (autorizacao) |
| 7 | Detalhe - Segmento S (autorizacao) |
| 8 | Detalhe - Segmento N (remessa) ou Y (autorizacao) |
| 9 | Trailer de Lote ou Arquivo |

## Exemplo: Header de Arquivo (Remessa)

```
Pos  Conteudo
001  0             (tipo registro)
002  0             (lote)
003-007  00000      (uso FEBRABAN)
008-011  0001       (tipo inscricao: 1=CPF, 2=CNPJ)
012-026  00000000000000  (inscricao)
027-038  EMPRESA LTDA   (nome empresa)
039-040  01          (agencia)
041-042  00          (digito agencia)
043-058  00000000000000000  (conta)
059-059  0           (digito conta)
060-060  0           (uso)
061-071  0           (DAC)
072-072  C           (cliente)
073-103  0           (uso FEBRABAN)
104-107  0001        (numero remessa)
108-113  140626      (data gravacao YYMMDD)
114-127  0           (reservado banco)
128-138  00000000000 (zeros)
139-143  00000       (uso FEBRABAN)
144-151  0           (reservado banco)
152-240  0           (uso)
```

## Tags

cnab, febraban, layout, banco, br, integracao
