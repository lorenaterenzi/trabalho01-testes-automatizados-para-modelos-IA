# Trabalho 1 - Testes Automatizados para ML (TDD e Hypothesis)

## MLOps Data Pipeline: Normalização e Validação de Lotes (`normalize_batch`)

Este repositório contém a implementação e a suíte de testes automatizados para a função `normalize_batch`, um componente essencial de pré-processamento em pipelines de Machine Learning para alinhamento de escala (Min-Max Scaling).

O projeto foi desenvolvido aplicando metodologias de Engenharia de Software e Qualidade para ML: **Test-Driven Development (TDD)** e **Property-Based Testing (PBT)**.

---

## Arquitetura e Decisões de Design

A função `normalize_batch(scores: list[float]) -> list[float]` realiza a transformação _min-max_ nos dados recebidos. Durante o desenvolvimento, foram tratadas as seguintes decisões de design e casos de borda (*corner cases*):

1. **Tratamento de Lote Constante ($max = min$):**
   - *Problema:* Quando todos os elementos de um lote são idênticos, a amplitude do intervalo ($max - min$) resulta em zero, o que provocaria uma exceção de divisão por zero (`ZeroDivisionError`).
   - *Decisão:* Em cenários de variância nula, a função retorna um vetor nulo (`0.0`) com o mesmo comprimento da entrada, garantindo a estabilidade numérica da esteira sem interromper o pipeline.

2. **Prevenção de Estouro de Precisão Numérica (*Float Overflow*):**
   - *Problema:* Em limites numéricos extremos do padrão IEEE 754 (e.g., $10^{308}$ contra $-10^{292}$), a diferença entre extremos ultrapassa a capacidade de precisão de 64-bits (`float64`), resultando em `inf` e convertendo a saída silenciosamente para `NaN`.
   - *Decisão:* Implementação de uma trava de verificação de escala. Caso $max - min == inf$, o lote é tratado preventivamente como constante para assegurar a integridade dos dados downstream.

3. **Invariância de Estruturas Vazias:**
   - Para vetores de entrada vazios (`[]`), a função preserva a dimensionalidade e retorna `[]`.

---

## 🧪 Estratégia de Testes

A suíte de testes foi estruturada em duas camadas complementares:

### 1. Desenvolvimento Guiado por Testes (TDD)
O ciclo **Red -> Green -> Refactor** foi aplicado e evidenciado no histórico de commits do Git:
- **RED:** Implementação prévia do teste de unidade (`test_normalize_batch_basic`), confirmando a falha por ausência do módulo.
- **GREEN:** Escrita da lógica mínima necessária para satisfazer a suíte de testes.
- **REFACTOR:** Expansão da cobertura para casos de borda (lotes vazios, lotes constantes e controle de *overflow*), refatorando o código sem quebrar a regressão.

### 2. Testes Baseados em Propriedades (Property-Based Testing)
Utilizando a biblioteca **`hypothesis`**, o teste de propriedade valida invariantes matemáticas sobre o comportamento do sistema, gerando centenas de combinações aleatórias de dados válidos:
- **Invariante de Limites:** Para qualquer vetor $X$ de entradas válidas em escala finita, a saída normalizada $Y$ DEVE satisfazer estritamente a condição $0.0 \le y_i \le 1.0, \forall y_i \in Y$.

### 3. Prova do Bug (*Test-the-Test*)
Para demonstrar que o teste de propriedade possui capacidade real de capturar defeitos em ambiente de produção, foi implementada a função `normalize_batch_buggy` (que omite a subtração do valor mínimo no numerador da fórmula). 
O teste `test_property_catches_bug` comprova que a invariante falha e gera uma asserção violada ao rodar contra a implementação com defeito.

---

## Execução do Projeto

### Pré-requisitos
- Python 3.10+
- `pytest`
- `hypothesis`

### Como rodar a suíte completa

1. Instalação das dependências:
```bash
pip install pytest hypothesis
```

2. Execução dos testes automatizados com relatório detalhado:
```bash
pytest -v
```

## Decisões de Design (`normalize_batch`)
1. **Lote Constante ($max = min$):** Para evitar divisão por zero quando a amplitude é nula, a função retorna uma lista de zeros (`0.0`), garantindo estabilidade numérica[cite: 4, 5].
2. **Tratamento de Overflow:** Se a diferença entre o maior e o menor valor ultrapassar a precisão de 64 bits (`float64`) e gerar `inf`, o lote é tratado de forma segura[cite: 4, 5].
3. **Lista Vazia:** Retorna `[]`[cite: 4, 5].

## Estrutura da Suíte de Testes
- **TDD:** Ciclo Red -> Green -> Refactor demonstrado no histórico de commits.
- **Teste de Propriedade:** Uso da biblioteca `hypothesis` para garantir a invariante de que qualquer entrada válida gera saídas dentro do intervalo $[0.0, 1.0]$[cite: 1, 4, 5].
- **Prova do Bug:** A função `normalize_batch_buggy` prova que o teste de propriedade captura uma falha real de escala em produção[cite: 5].