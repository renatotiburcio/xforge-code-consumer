# ttl-rules

Conhecimento tem validade e deve ser revalidado periodicamente.

## Regras de Revalidação

### Por Tipo de Dependência

| Dependência | TTL | Ação ao expirar |
|-------------|:---:|-----------------|
| Legislação (LGPD, CLT, fiscal) | 6 meses | Revalidar com fonte oficial |
| API externa | 3 meses | Verificar se endpoint mudou |
| Provider de IA | 1 mês | Verificar se modelo ainda existe |
| Package NuGet/npm | 3 meses | Verificar versão estável |
| Padrão de código | 6 meses | Verificar se ainda best practice |

### Por Domínio

| Domínio | TTL | Motivo |
|---------|:---:|--------|
| Fiscal/contábil | 3 meses | Legislação muda frequentemente |
| Trabalhista | 6 meses | CLT e eSocial atualizações |
| Segurança | 1 mês | Novas vulnerabilidades diárias |
| Arquitetura | 12 meses | Técnicas evoluem mais devagar |
| UI/UX | 6 meses | Design trends mudam |

### Por Idade

| Idade | Ação |
|-------|------|
| < 30 dias | Ativo, usar sem revalidação |
| 30-90 dias | Marcar para revalidação |
| 90-180 dias | Revalidar antes de usar |
| > 180 dias | Revalidação obrigatória |

## Procedimento

1. Identificar entrada com TTL expirado
2. Verificar se fonte ainda é válida
3. Se válida → atualizar `lastValidated`
4. Se inválida → marcar deprecated
5. Se parcialmente válida → atualizar conteúdo
6. Registrar no audit trail

## Gatilhos de Revalidação Imediata

- Contradição com código atual detectada
- Incidente que envolve conhecimento afetado
- Release nova do provider/framework
- Mudança de legislação

## Regras

- Nunca usar conhecimento com TTL expirado sem revalidar
- Fiscal/legal → sempre revalidar antes de usar
- Documentar data da última revalidação
- Conhecimento deprecated → não usar, apenas referenciar
