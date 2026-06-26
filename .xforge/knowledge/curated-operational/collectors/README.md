# Collectors

## Resumo Executivo

- **Tema**: Collectors
- **Descrição**: Coletores locais para executar no ambiente do usuário e popular a base de conhecimento com fontes públicas/oficiais.
- **Itens principais**: robots/termos de uso;; limites de requisição;; licenças;
- **Seções**: Objetivo, Importante, Estratégia
- **Categoria**: collectors | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Collectors |
| Categoria | collectors |
| Tipo | curated-operational |
| Seções | 3 |


## Objetivo

Coletores locais para executar no ambiente do usuário e popular a base de conhecimento com fontes públicas/oficiais.

## Importante

Os scripts devem respeitar:

- robots/termos de uso;
- limites de requisição;
- licenças;
- privacidade;
- segredos;
- validação humana.

## Estratégia

1. Baixar fonte.
2. Salvar raw.
3. Calcular hash.
4. Gerar manifest.
5. Enviar para `/xforge-ingerir-conhecimento`.
