---
id: design-patterns-gof
type: knowledge
tags: [design-patterns, gof, padroes-criacionais, padroes-estruturais, padroes-comportamentais, dotnet]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Design Patterns GoF
- **Principais responsabilidades**: Documentar padrões criacionais, estruturais e comportamentais; Fornecer exemplos práticos em C# para cada padrão; Guiar a escolha do padrão adequad...
- **Seções principais**: Propósito, Responsabilidades, Padrões Criacionais, Padrões Estruturais
- **Tags**: design-patterns, gof, padroes-criacionais, padroes-estruturais, padroes-comportamentais, dotnet
- **Tipo**: knowledge | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `design-patterns-gof` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 9 |


# Design Patterns GoF

## Propósito
Catálogo dos padrões Gang of Four (GoF) aplicados no ERP, com exemplos em C# para os padrões mais utilizados no contexto de sistemas empresariais brasileiros.

## Responsabilidades
- Documentar padrões criacionais, estruturais e comportamentais
- Fornecer exemplos práticos em C# para cada padrão
- Guiar a escolha do padrão adequado para cada problema

## Padrões Criacionais

| Padrão | Descrição | Uso no ERP |
|--------|-----------|------------|
| **Factory Method** | Subclasse decide a classe | Criar documentos fiscais (NF-e, NFC-e, CT-e) |
| **Abstract Factory** | Família de fábricas relacionadas | Regimes tributários (Simples, Lucro Presumido, Lucro Real) |
| **Builder** | Construção passo a passo | Pedidos de venda com partes opcionais |
| **Singleton** | Única instância | Configurações globais do sistema |

## Padrões Estruturais

| Padrão | Descrição | Uso no ERP |
|--------|-----------|------------|
| **Adapter** | Interface compatível | Integração com múltiplos gateways de pagamento |
| **Facade** | Interface simplificada | Emissão de NF-e (cálculo + XML + assinatura + transmissão) |
| **Decorator** | Adicionar responsabilidades | Logging, cache, retry em serviços de estoque |
| **Composite** | Estrutura em árvore | Categorias de produtos hierárquicas |

## Padrões Comportamentais

| Padrão | Descrição | Uso no ERP |
|--------|-----------|------------|
| **Strategy** | Algoritmos intercambiáveis | Cálculo de impostos por regime tributário |
| **Observer** | Notificar mudanças | Eventos de venda, estoque baixo, vencimentos |
| **Mediator** | Comunicação centralizada | Desacoplar módulos (estoque, financeiro, fiscal) |
| **State** | Mudar comportamento | Estados de pedido (Pendente → Aprovado → Faturado → Entregue) |
| **Chain of Responsibility** | Cadeia de handlers | Validações sequenciais (estoque → crédito → fiscal → aprovação) |

## Exemplo: Strategy — Cálculo de Impostos

```csharp
public interface ICalculoImpostoStrategy {
    string Nome { get; }
    Impostos Calcular(decimal valorBase, ItemPedido item);
}

public class SimplesNacionalStrategy : ICalculoImpostoStrategy {
    public string Nome => "Simples Nacional";
    public Impostos Calcular(decimal valorBase, ItemPedido item) {
        decimal aliq = 0.06m;
        return new Impostos {
            ICMS = valorBase * aliq * 0.34m, PIS = valorBase * aliq * 0.23m,
            COFINS = valorBase * aliq * 0.12m, IRPJ = valorBase * aliq * 0.055m,
            CSLL = valorBase * aliq * 0.035m, CPP = valorBase * aliq * 0.435m
        };
    }
}

public class LucroRealStrategy : ICalculoImpostoStrategy {
    public string Nome => "Lucro Real";
    public Impostos Calcular(decimal valorBase, ItemPedido item) {
        return new Impostos {
            ICMS = valorBase * 0.18m, IPI = item.IncideIPI ? valorBase * 0.05m : 0,
            PIS = valorBase * 0.0165m, COFINS = valorBase * 0.076m,
            IRPJ = valorBase * 0.15m, CSLL = valorBase * 0.09m,
            AdicionalIRPJ = valorBase > 20000 ? valorBase * 0.10m : 0
        };
    }
}

public class CalculoFiscalService {
    private ICalculoImpostoStrategy _strategy;
    public CalculoFiscalService(ICalculoImpostoStrategy s) { _strategy = s; }
    public void DefinirEstrategia(ICalculoImpostoStrategy s) { _strategy = s; }
    public Impostos Calcular(decimal valor, ItemPedido item) => _strategy.Calcular(valor, item);
}
```

## Exemplo: Abstract Factory — Regimes Fiscais

```csharp
public interface IFiscalFactory {
    ICalculadorImposto CriarCalculadorImposto();
    IDocumentoFiscal CriarDocumentoFiscal();
    IValidadorFiscal CriarValidadorFiscal();
}

public class SimplesNacionalFactory : IFiscalFactory {
    public ICalculadorImposto CriarCalculadorImposto() => new CalculadorSimplesNacional();
    public IDocumentoFiscal CriarDocumentoFiscal() => new NFCeDocumento();
    public IValidadorFiscal CriarValidadorFiscal() => new ValidadorSimplesNacional();
}

public class LucroPresumidoFactory : IFiscalFactory {
    public ICalculadorImposto CriarCalculadorImposto() => new CalculadorLucroPresumido();
    public IDocumentoFiscal CriarDocumentoFiscal() => new NFeDocumento();
    public IValidadorFiscal CriarValidadorFiscal() => new ValidadorLucroPresumido();
}
```

## Dependências
- [clean-architecture.md](clean-architecture.md) — Camadas onde os padrões são aplicados
- [design-patterns-erp.md](design-patterns-erp.md) — Padrões específicos de domínio

## Restrições
- Não usar Singleton para estado mutável compartilhado — preferir DI com `IOptions<T>`
- Strategy deve ser stateless; estado vai no contexto da chamada
- Observer via XForge.MediatR (in-process) para desacoplamento sem mensageria externa

