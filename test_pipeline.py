import pytest
from pipeline import normalize_batch

def test_normalize_batch_basic():
    # Teste para verificar a normalizacao basica
    input_scores = [10.0, 20.0, 30.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_batch(input_scores) == expected