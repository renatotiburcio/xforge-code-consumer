# Property-Based Testing com Hypothesis / FsCheck

Testes baseados em propriedades: gere inputs aleatorios e verifique invariantes.

## Conceito

Em vez de:
```python
def test_soma_2_mais_2():
    assert soma(2, 2) == 4
```

Voce afirma uma propriedade:
```python
@given(st.integers(), st.integers())
def test_soma_e_comutativa(a, b):
    assert soma(a, b) == soma(b, a)
```

Hypothesis/FsCheck gera centenas de combinacoes e procura um caso que
quebre a propriedade.

## Python (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(), min_size=1))
def test_soma_lista_e_igual_soma_reversed(xs):
    assert sum(xs) == sum(reversed(xs))

@given(st.text(min_size=1))
def test_upper_lower_roundtrip(s):
    assert s.lower().upper().lower() == s.lower()

@given(st.integers(), st.integers())
def test_divisao_por_zero_lanca(a):
    if a != 0:
        with pytest.raises(ZeroDivisionError):
            1 / a
```

## C# (FsCheck)

```csharp
[Property]
public bool Soma_Comutativa(int a, int b) {
    return Soma(a, b) == Soma(b, a);
}

[Property]
public bool UpperLower_Roundtrip(string s) {
    return s.ToLower().ToUpper().ToLower() == s.ToLower();
}

[Property(Arbitrary = new[] { typeof(NonEmptyListArbitrary) })]
public bool SomaLista_Reordering(NonEmptyList<int> xs) {
    var original = xs.Item.Sum();
    var reordered = xs.Item.OrderBy(x => x).Sum();
    return original == reordered;
}
```

## Quando usar

- Operacoes comutativas, associativas, idempotentes
- Serializacao/deserializacao (roundtrip)
- Parsers/validadores
- Algoritmos de busca/ordenacao

## Cuidado

- Nao usar para testar cenarios de erro especificos
- Manter strategies pequenas (max_examples=100) para suites rapidas
- Usar `assume(x != 0)` para pular inputs invalidos

## Tags

testing, property-based, hypothesis, fscheck, dotnet
