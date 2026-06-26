---
id: playbook-esocial-cpf-invalido
type: playbook
title: eSocial Rejeicao CPF do Trabalhador Invalido
severity: high
status: validated
trustScore: 90
source: esocial-oficial + suporte
lastValidated: 2026-06-14
tags: ["esocial", "cpf", "validacao", "rejeicao", "trabalhista"]
---

## Sintoma
eSocial rejeita evento S-2190 (Cadastro Inicial) ou S-2200 (Admissao) com codigo: "CPF do trabalhador invalido".

## Causas Comuns
1. **Digitos verificadores errados**: CPF matematicamente invalido
2. **CPF zerado ou com mascara errada**: `000.000.000-00` ou `1234567890`
3. **CPF de pessoa falecida**: base do CPF detecta obito (impacto fiscal)
4. **CPF cancelado**: Receita Federal pode ter cancelado por fraude
5. **CPF alfanumerico**: (planejado para 2027+) ainda nao suportado em 2026
6. **HomONimos**: nomes iguais mas CPF diferentes (erro de digitacao comum)

## Diagnostico
```python
def validar_cpf(cpf: str) -> Tuple[bool, str]:
    cpf = "".join(c for c in cpf if c.isdigit())
    if len(cpf) != 11: return False, "tamanho != 11"
    if cpf == cpf[0] * 11: return False, "todos digitos iguais"
    # Validar DV
    pesos1 = list(range(10, 1, -1))
    pesos2 = list(range(11, 1, -1))
    d1 = sum(int(c) * p for c, p in zip(cpf[:9], pesos1)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    d2 = sum(int(c) * p for c, p in zip(cpf[:10], pesos2)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    if cpf[9:11] != f"{d1}{d2}": return False, "DV invalido"
    return True, ""
```

```python
# Validar contra base da Receita (requer certificado digital)
import zeep
from zeep import Client

def consultar_cpf_receita(cpf: str, cert_path: str, senha: str) -> dict:
    """Consulta situacao cadastral do CPF na Receita Federal."""
    client = Client("https://www.receita.fazenda.gov.br/.../ConsultaCPF.wsdl")
    return client.service.consultarCPF(
        cpf=cpf,
        cert=cert_path,
        senha=senha
    )
# Retorna: nome, situacao (REGULAR, PENDENTE, CANCELADO, FALECIDO)
```

## Solucao
1. **Validar CPF no cadastro do funcionario** (antes de gerar S-2200)
2. **Bloquear admissao** se CPF invalido
3. **Para CPFs cancelados/falecidos**: NAO admitir, comunicar RH
4. **Para CPFs em DV errado**: corrigir (geralmente erro de digitacao)
5. **Para homonimos**: confirmar com documento oficial (RG ou CNH)

## Caso Real (2024-10)
Loja de varejo admitindo 50 funcionarios/semana. 8% tinham CPF com DV errado.
eSocial rejeitava 4 dias depois (apos transmissao em lote).
**Impacto**: funcionarios sem registro, multa por atraso, retrabalho do RH.
**Fix**: validacao em tempo real no cadastro + consulta Receita Federal em homolog.

## Prevencao
- Validar CPF no momento do cadastro (regex + DV)
- Integrar com API de consulta CPF (Receita Federal via certificado digital A1)
- Cache de 7 dias para consulta (evitar consultas repetidas)
- Bloquear admissao se CPF em situacao irregular
- Alerta se cadastro parecer homonimo (nome + data nasc similares)

## Codigos de Rejeicao eSocial
- "CPF invalido": DV errado
- "CPF nao encontrado": nao existe na base
- "CPF em situacao irregular": cancelado, falecido, pendente
- "CPF ja cadastrado": outro vinculo ativo

## Acoes por Situacao
| Situacao | Acao |
|----------|------|
| REGULAR | Prosseguir |
| PENDENTE | Pedir regularizacao ao funcionario (ex: declaracao IR atrasada) |
| CANCELADO | Bloquear — CPF nao pode ser usado |
| FALECIDO | Bloquear — verificar se nao eh homonimo (RG + certidao) |
| NULO | Erro de digitacao — corrigir |

## Referencias
- Manual eSocial S-2200 v2.5
- API Receita Federal: https://www.receita.fazenda.gov.br/interface/lista-cnpj
- Decreto 8.373/2014 - Numero Unico do CPF
- Lei 13.444/2017 - Identificacao Civil Nacional
