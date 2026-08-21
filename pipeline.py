def normalize_batch(scores: list[float]) -> list[float]:
    """
    Decisao de Design:
    - Se a lista estiver vazia, retorna lista vazia.
    - Se max(scores) == min(scores) (lote constante), retorna uma lista 
      de 0.0 do mesmo tamanho para evitar divisao por zero.
    """
    if not scores:
        return []
    
    min_val = min(scores)
    max_val = max(scores)
    
    if max_val == min_val:
        return [0.0] * len(scores)
        
    return [(x - min_val) / (max_val - min_val) for x in scores]