# Approved Pattern — Minimal API com endpoint limpo

## Resumo Executivo

- **Tema**: Approved Pattern — Minimal API com endpoint limpo
- **Itens principais**: Program.cs limpo;; endpoints agrupados por extension;; validação separada;
- **Seções**: Regra, Obrigatório, Anti-pattern relacionado
- **Categoria**: dotnet | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Approved Pattern — Minimal API com endpoint limpo |
| Categoria | dotnet |
| Tipo | curated-operational |
| Seções | 3 |


## Regra

Endpoint deve orquestrar entrada/saída e delegar caso de uso.

## Obrigatório

- Program.cs limpo;
- endpoints agrupados por extension;
- validação separada;
- handler/use case separado;
- Result Pattern;
- XForge.MediatR quando houver CQRS;
- AutoMapper quando houver mapping;
- testes.

## Anti-pattern relacionado

Endpoint com regra de negócio, SQL, mapping e validação misturados.
