---
id: playbook-esocial-vinculo-duplicado
type: playbook
title: eSocial Rejeicao Vinculo Empregaticio Duplicado
severity: critical
status: validated
trustScore: 91
source: esocial-oficial + suporte
lastValidated: 2026-06-14
tags: ["esocial", "vinculo", "duplicado", "s-2200", "s-2300", "trabalhista"]
---

## Sintoma
eSocial rejeita S-2200 (Admissao) ou S-2300 (TSVE) com mensagem: "Ja existe vinculo empregaticio ativo para este CPF/CNPJ".

## Causas
1. **Admissao dupla**: mesmo funcionario admitido 2x (erro operacional grave)
2. **TSVE duplicado**: Trabalhador Sem Vinculo de Emprego registrado 2x
3. **Vinculo anterior nao encerrado**: funcionario demitido mas S-2299 nao foi enviado
4. **Carga de eSocial antiga**: migracao de sistema pode ter gerado vinculos duplicados
5. **Multi-CNPJ**: funcionario admitido em 2 CNPJs do mesmo grupo (permitido mas com cuidado)
6. **CNPJ errado**: cadastro de funcionario com CNPJ/CPF que ja tem vinculo em outra empresa

## Diagnostico
```sql
-- Verificar vinculos ativos por CPF
SELECT v.id, v.cpf, v.cnpj, v.matricula, v.data_inicio, v.situacao, e.cnpj as cnpj_empregador
FROM vinculos v
JOIN empregadores e ON e.id = v.empregador_id
WHERE v.cpf = :cpf
  AND v.situacao = 'ATIVO'
ORDER BY v.data_inicio DESC;
```

```python
# Consultar eSocial via API
def verificar_vinculo_ativo(cpf: str, cnpj_empregador: str) -> dict:
    # Endpoint: https://webservices.esocial.gov.br/consulta/...
    # Retorna lista de vinculos ativos + empregador
    pass
```

## Decisao de Design
- **Permitir vinculo multi-CNPJ**: SIM (trabalhador pode ter 2 empregos)
- **Bloquear duplicado no mesmo CNPJ**: SIM (sempre erro)
- **Bloquear TSVE duplicado**: SIM (TSVE eh para vinculo especifico, nao cumulativo)

## Solucao por Cenario

### 1. Admissao Dupla Acidental (mesmo CNPJ)
- **Bloquear** completamente
- Mostrar alerta: "Funcionario X ja admitido em 15/03/2025 neste CNPJ"
- Cancelar fluxo de admissao
- Investigar: foi erro de digitacao de CPF? Ou duplicacao real?

### 2. Vinculo Anterior Nao Encerrado
- Verificar se S-2299 (desligamento) foi enviado
- Se nao: enviar S-2299 com data real do desligamento
- Se S-2299 foi enviado mas eSocial nao processou: aguardar processamento
- So enviar nova S-2200 apos vinculo anterior estar INATIVO

### 3. Multi-CNPJ (permitido)
- Admissao em CNPJ A nao bloqueia admissao em CNPJ B
- MAS: folha de pagamento precisa consolidar (INSS, IRRF)
- Validar: se CPF ja tem vinculo ativo, perguntar se eh o mesmo funcionario

### 4. Migracao de Dados
- Limpar vinculos duplicados antes de migrar
- Validar: 1 vinculo ativo por (CPF + CNPJ)
- Marcar como "migrado" para rastreio

## Caso Real (2024-12)
Grupo empresarial com 3 CNPJs. RH central admitiu funcionario 2x no mesmo CNPJ
(erro de fluxo: 2 admissoes para mesma vaga). eSocial rejeitou.
**Impacto**: 15 dias para corrigir (auditoria, retificacao, S-2299 retroativo).
**Fix**: trava no sistema ERP: 1 admissao aberta por CPF + CNPJ.

## Acoes Corretivas
```python
def corrigir_vinculo_duplicado(vinculo_id: int):
    """Encerra vinculo duplicado e notifica RH."""
    vinculo = vinculo_repo.get(vinculo_id)
    
    if not vinculo.eh_duplicado:
        raise ValueError("Vinculo nao eh duplicado")
    
    # 1. Enviar S-2299 retroativo (desligamento sem movimento)
    esocial_service.enviar_S2299(
        cpf=vinculo.cpf,
        cnpj=vinculo.cnpj,
        matricula=vinculo.matricula,
        data_desligamento=vinculo.data_inicio,  # mesmo dia = sem ter trabalhado
        motivo="DESLIGAMENTO_SEM_MOVIMENTO"
    )
    
    # 2. Marcar como cancelado no sistema local
    vinculo.situacao = "CANCELADO_DUPLICIDADE"
    vinculo_repo.save(vinculo)
    
    # 3. Auditar
    audit.log(
        event="vinculo_duplicado_corrigido",
        actor="sistema",
        before={"id": vinculo_id, "situacao": "ATIVO"},
        after={"situacao": "CANCELADO_DUPLICIDADE"}
    )
    
    # 4. Notificar RH
    notificar_rh(f"Vinculo duplicado {vinculo_id} foi encerrado")
```

## Prevencao
- **Trava no cadastro**: bloquear admissao se (CPF + CNPJ) ja tem vinculo ATIVO
- **Job diario**: detectar vinculos duplicados antes do eSocial rejeitar
- **Auditoria mensal**: relatorio de vinculos ativos por CPF (suspeitos: > 2)
- **Integracao com eSocial**: consultar vinculos ANTES de enviar S-2200
- **Treinamento RH**: fluxo claro de desligamento (sempre enviar S-2299)

## Fluxo de Admissao Recomendado
1. Cadastro inicial (dados pessoais)
2. Validacao CPF (DV + Receita)
3. **Verificar vinculos ativos** (consulta eSocial ou base local)
4. Se existe: investigar (mesmo CNPJ = bloqueia; CNPJ diferente = permite)
5. Prosseguir com S-2190 + S-2200
6. Confirmar processamento (consultar recibo)

## Referencias
- Manual eSocial S-2200 v2.5 - Vinculos
- Lei CLT Art. 442 - Empregado eh toda pessoa que presta servico
- S-2299 - Desligamento (evento de saida)
- ENCAT 91/2024 - Regras de validacao de vinculos
