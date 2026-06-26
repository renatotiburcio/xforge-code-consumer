# Self-Healing Rules — XForge Engineer

## Visão Geral

Regras de correção automática que detectam e corrigem problemas comuns sem intervenção humana. Rodam como pré-checks antes de commit, build e deploy.

## Regras Ativas

### SH-001: Unused Imports
- **Detecta**: `using` declarations sem uso no arquivo
- **Ação**: Remove imports não utilizados
- **Severidade**: low
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  using System.Linq;
  using System.Collections.Generic;
  using Newtonsoft.Json; // não usado

  // DEPOIS (auto-corrigido)
  using System.Linq;
  using System.Collections.Generic;
  ```

### SH-002: Missing Async Suffix
- **Detecta**: Métodos async sem sufixo `Async`
- **Ação**: Adiciona sufixo `Async` ao nome do método
- **Severidade**: medium
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  public async Task<List<Produto>> GetProdutos()

  // DEPOIS
  public async Task<List<Produto>> GetProdutosAsync()
  ```

### SH-003: Null-Conditional Access
- **Detecta**: Property/field access em variável que pode ser null
- **Ação**: Adiciona `?.` (null-conditional operator)
- **Severidade**: high
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  var nome = cliente.Nome.ToUpper();

  // DEPOIS
  var nome = cliente?.Nome?.ToUpper();
  ```

### SH-004: Missing Null Check
- **Detecta**: Resultado de FirstOrDefault()/SingleOrDefault() usado sem null check
- **Ação**: Adiciona `if (result == null) return NotFound();`
- **Severidade**: high
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  var produto = await _context.Produtos.FirstOrDefaultAsync(x => x.Id == id);
  return Ok(produto.Nome); // NullReferenceException!

  // DEPOIS
  var produto = await _context.Produtos.FirstOrDefaultAsync(x => x.Id == id);
  if (produto == null) return NotFound();
  return Ok(produto.Nome);
  ```

### SH-005: Async Over Sync
- **Detecta**: Chamadas síncronas (.Result, .Wait(), SaveChanges()) em contexto async
- **Ação**: Substitui por variante Async
- **Severidade**: high
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  _context.SaveChanges();

  // DEPOIS
  await _context.SaveChangesAsync();
  ```

### SH-006: Missing Using Declaration
- **Detecta**: IDisposable sem using/await using
- **Ação**: Adiciona `using` declaration ou `await using`
- **Severidade**: medium
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  var stream = new FileStream("file.txt", FileMode.Open);
  var reader = new StreamReader(stream);

  // DEPOIS
  await using var stream = new FileStream("file.txt", FileMode.Open);
  await using var reader = new StreamReader(stream);
  ```

### SH-007: Parameterized Query
- **Detecta**: SQL query com interpolação de string
- **Ação**: Converte para parameterized query
- **Severidade**: critical (security)
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  var result = await _context.Produtos
      .FromSqlRaw($"SELECT * FROM Produtos WHERE Nome = '{nome}'")
      .ToListAsync();

  // DEPOIS
  var result = await _context.Produtos
      .FromSqlRaw("SELECT * FROM Produtos WHERE Nome = {0}", nome)
      .ToListAsync();
  ```

### SH-008: Secret Detection
- **Detecta**: Padrões de secret no código (API key, password, token)
- **Ação**: Move para variável de ambiente ou appsettings.json
- **Severidade**: critical (security)
- **Auto-fix**: parcial (movê-lo, não o valor)
- **Exemplo**:
  ```csharp
  // ANTES
  var apiKey = "sk-1234567890abcdef";

  // DEPOIS
  var apiKey = _configuration["ExternalServices:ApiKey"]
      ?? throw new InvalidOperationException("ApiKey not configured");
  ```

### SH-009: Cancellation Token
- **Detecta**: Métodos async sem CancellationToken parameter
- **Ação**: Adiciona `CancellationToken cancellationToken = default` como último parâmetro
- **Severidade**: medium
- **Auto-fix**: sim
- **Exemplo**:
  ```csharp
  // ANTES
  public async Task<List<Produto>> GetProdutosAsync()

  // DEPOIS
  public async Task<List<Produto>> GetProdutosAsync(CancellationToken cancellationToken = default)
  ```

### SH-010: IHttpClientFactory
- **Detecta**: `new HttpClient()` direto
- **Ação**: Substitui por IHttpClientFactory injeção
- **Severidade**: high (performance)
- **Auto-fix**: parcial (sugere refactoring)

### SH-011: Missing ConfigureAwait
- **Detecta**: Await sem ConfigureAwait(false) em bibliotecas/classes de serviço
- **Ação**: Adiciona `ConfigureAwait(false)` após await
- **Severidade**: low
- **Auto-fix**: sim

### SH-012: Disposable Pattern
- **Detecta**: Classe que implementa IDisposable mas não chama GC.SuppressFinalize
- **Ação**: Completa o padrão Dispose
- **Severidade**: medium
- **Auto-fix**: parcial

## Configuração

As regras são avaliadas nesta ordem:
1. **Critical** (SH-007, SH-008) — sempre aplicar
2. **High** (SH-003, SH-004, SH-005, SH-010) — aplicar com confirmação
3. **Medium** (SH-002, SH-006, SH-009, SH-012) — aplicar se auto-fix habilitado
4. **Low** (SH-001, SH-011) — aplicar silenciosamente

## Integração com Quality Gates

```
Pré-commit → SH-001, SH-003, SH-004, SH-005, SH-007, SH-008
Pré-build  → SH-002, SH-006, SH-009, SH-013
Pré-push   → SH-010, SH-014, SH-015, SH-016
Pós-merge  → Todos os SH rules
```

## Métricas

| Métrica | Meta |
|---------|------|
| Auto-fix success rate | > 95% |
| False positive rate | < 5% |
| Time per check | < 2s |
| Issues caught per build | 3-8 (média) |
