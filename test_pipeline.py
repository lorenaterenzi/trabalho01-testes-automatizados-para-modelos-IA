import pytest
from hypothesis import given, strategies as st
from pipeline import normalize_batch

# ── 1. TESTES UNITÁRIOS (TDD) ────────────────────────────────────────────────
def test_normalize_batch_basic():
    """Testa a normalizacao min-max basica."""
    input_scores = [10.0, 20.0, 30.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_batch(input_scores) == expected

def test_normalize_batch_constant_list():
    """Testa o tratamento de divisao por zero quando max == min."""
    assert normalize_batch([5.0, 5.0, 5.0]) == [0.0, 0.0, 0.0]

def test_normalize_batch_empty():
    """Testa o comportamento com lista vazia."""
    assert normalize_batch([]) == []


# ── 2. TESTE DE PROPRIEDADE (INVARIANTE COM HYPOTHESIS) ───────────────────────
@given(
    st.lists(
        st.floats(min_value=-1e100, max_value=1e100, allow_nan=False, allow_infinity=False), 
        min_size=1
    )
)
def test_property_output_always_in_bounds(scores):
    """Propriedade: Todo valor normalizado DEVE estar no intervalo [0.0, 1.0]."""
    result = normalize_batch(scores)
    for value in result:
        assert 0.0 <= value <= 1.0


# ── 3. PROVA DE QUE A PROPRIEDADE PEGA UM BUG REAL ───────────────────────────
def normalize_batch_buggy(scores: list[float]) -> list[float]:
    """Versao com bug: esqueceu de subtrair min_val no numerador."""
    if not scores:
        return []
    min_val = min(scores)
    max_val = max(scores)
    if max_val == min_val:
        return [0.0] * len(scores)
    # BUG: x / (max_val - min_val) em vez de (x - min_val) / ...
    return [x / (max_val - min_val) for x in scores]


def test_property_catches_bug():
    """Comprova que a propriedade de limites falha na versao bugada."""
    with pytest.raises(AssertionError):
        # Para [10.0, 20.0, 30.0], a versao bugada gera [0.5, 1.0, 1.5] -> 1.5 quebra a propriedade
        buggy_result = normalize_batch_buggy([10.0, 20.0, 30.0])
        for value in buggy_result:
            assert 0.0 <= value <= 1.0