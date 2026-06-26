# Playbook: Debug de Erros Fiscais

## Fluxo de Debug

### 1. Identificar o Erro
```
Erro: "Cálculo ICMS retornou R$ 0,00"
→ Verificar: CFOP, UF destino, regime tributário
```

### 2. Verificar Tabelas
- [ ] Tabela ICMS da UF destino atualizada?
- [ ] Alíquota correta para o CFOP?
- [ ] Base de cálculo descontada corretamente?

### 3. Verificar Regras
- [ ] Regime Simples Nacional → alíquota diferente
- [ ] Lucro Presumido → base 32% (serviço) ou 8% (comércio)
- [ ] Substituição Tributária aplicável?

### 4. Testar com Dados Conhecidos
```csharp
// Teste: NF-e de venda interestadual
var icms = CalcularICMS(
    valor: 1000.00m,
    cfop: "6102",  // Venda interestadual
    ufOrigem: "SP",
    ufDestino: "RJ",
    regimeTributario: "Lucro Presumido"
);
// Esperado: 12% (alíquota interestadual RJ)
// Resultado: R$ 120,00
```

### 5. Documentar Solução
- [ ] Criar/actualizar knowledge file com a solução
- [ ] Adicionar ao errors-solutions-graph.json
- [ ] Criar teste que reproduz o erro
