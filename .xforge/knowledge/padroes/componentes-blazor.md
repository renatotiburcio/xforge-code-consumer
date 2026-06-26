---
id: componentes-blazor
type: pattern
tags: [blazor, components, ui, erp, razor, input, display, navigation]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Componentes Blazor para ERP
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: blazor, components, ui, erp, razor, input, display, navigation
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `componentes-blazor` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Componentes Blazor para ERP

## Propósito

Definir padrões reutilizáveis de componentes Blazor para sistemas ERP, cobrindo entradas com máscara, exibição formatada, navegação e comunicação entre componentes.

## Descrição do Padrão

### Componentes de Entrada

- **InputCurrency**: Herda de `InputBase<TValue>`, formata valores monetários (R$ 1.234,56) com suporte a casas decimais configuráveis, prefixo customizado e valores negativos.
- **InputMask**: Herda de `InputText`, aplica máscaras (CPF, CNPJ, CEP, telefone) via string pattern com placeholder `0` para dígitos.
- **InputAutocomplete**: Componente genérico com debounce (300ms), navegação por teclado, template de item e seleção/clear.
- **InputCodigoBarras**: Detecta leitura de scanner por velocidade de digitação (50ms) com auto-submit.
- **InputSelectEnum**: Renderiza enums como `<select>` com suporte a `[Display(Name)]`.

### Componentes de Exibição

- **DisplayCurrency**: Valor monetário formatado em pt-BR com destaque para negativos.
- **DisplayDocumento**: Formata CPF (000.000.000-00) e CNPJ (00.000.000/0000-00) automaticamente.
- **DisplayStatus**: Badge com cores e ícones configuráveis (ex: StatusNFe.Autorizada → verde).

### Navegação

- **SidebarMenu**: Menu lateral com módulos/submódulos, usa `NavLink` com `Match="NavLinkMatch.Prefix"`.
- **Breadcrumb**: Gera trilha a partir da rota via `BreadcrumbHelper.FromRoute()`.
- **NavTabs**: Abas com contadores e ícones.

### Comunicação entre Componentes

- **EventCallback**: Comunicação pai-filho via `@bind-Value` e `ValueChanged`.
- **CascadingParameter**: Compartilha estado entre componentes aninhados sem acoplamento direto.
- **EventCallback<T> assíncrono**: Operações async entre componentes com `InvokeAsync()`.

### Render Modes (.NET 8+)

| Modo | Uso no ERP |
|------|-----------|
| `Static SSR` | Conteúdo público, SEO |
| `InteractiveServer` | Apps internos, ERP intranet |
| `InteractiveWebAssembly` | PWAs, SaaS público |
| `InteractiveAuto` | Melhor dos dois — começa Server, migra para WASM |

**Configuração Server:**
```csharp
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(Client._Imports).Assembly);
```

## Quando Usar

- Formulários com máscaras brasileiras (CPF, CNPJ, CEP, moeda).
- Gráficos/dashboards que exigem atualização em tempo real (Server + SignalR).
- Apps offline ou campo (WASM como PWA).
- Quando performance de UI é crítica (WASM com AOT).

## Exemplo de Uso

```razor
<EditForm Model="@_model" OnValidSubmit="Salvar">
    <DataAnnotationsValidator />
    <InputCurrency @bind-Value="_model.Preco" CasasDecimais="4" />
    <InputMask @bind-Value="_model.CNPJ" Mask="@MaskTypes.CNPJ" />
    <InputAutocomplete TItem="Cliente"
        SearchFunc="@BuscarClientes"
        DisplaySelector="@(c => c.Nome)"
        OnSelected="@((c) => _model.ClienteId = c.Id)">
        <ItemTemplate>@context.Nome (@context.CNPJ)</ItemTemplate>
    </InputAutocomplete>
</EditForm>
```

## Padrões Relacionados

- [[autenticacao-autorizacao]] — proteção de rotas no Blazor
- [[ef-core-patterns]] — persistência de dados dos formulários
- [[validacao]] — validação de inputs com FluentValidation

