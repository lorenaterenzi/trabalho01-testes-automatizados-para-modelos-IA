def normalize_batch(scores: list[float]) -> list[float]:
    """
    Decisao de Design:
    - Se a lista estiver vazia, retorna lista vazia.
    - Se max(scores) == min(scores) (lote constante), retorna uma lista 
      de 0.0 do mesmo tamanho para evitar divisao por zero.
    - Se a diferenca estourar o limite de float (overflow), trata como constante.
    """
    if not scores:
        return []
    
    min_val = min(scores)
    max_val = max(scores)
    
    if max_val == min_val:
        return [0.0] * len(scores)
    
    diff = max_val - min_val
    if diff == float('inf'):
        return [0.0] * len(scores)
        
    return [(x - min_val) / diff for x in scores]