# Breve explicação sobre os dados

## Visão geral

"Arquitetura" das calculadoras:

    RecommendationCalculator
        BlueCalculator | GreenCalculator
        ContractRecommendationCalculator

    Entrada -> RecommendationCalculator -> Saída

O `|` é pra indicar que não há uma ordem obrigatória entre verde e azul.

**Entrada**
- histórico de consumo
- bandeira tarifa atual
- tarifa azul
- tarifa verde

**Saída**
- tabela do contrato atual
- tabela do contrato recomendado
- e outras coisas a serem definidas

## Dados de entrada e saída

Os dados estão de entrada e saída estão em `recommendation/tests/data/`.

Até o momento desta escrita, o arquivo `data/consumption.csv` contém os dados de
entrada do cálculo, enquanto que os arquivos `data/{blue|green}_per_*.csv` são
respostas esperadas para os testes.

Cada conjunto de dados de uma unidade consumidora é um caso de teste. Esses
casos de teste são definidos em
[test_cases.py](/tests/recommendation/test_cases.py). Cada caso de teste é
identificado pelo **código** da unidade consumidora em
`tests/recommendation/data/uc_{code}`. Os casos de teste habilitados podem ser
conferidos executando

```
pytest -k recommendation --collect-only
```

Você deve ver algumas linhas do tipo:

```
<Package recommendation>
  <Module test_blue_percentile_calculator.py>
    <Function test_blue_per_calculator[1011101-5]>
  <Module test_green_percentile_calculator.py>
    <Function test_blue_per_calculator[1011101-5]>
  <Module test_recommendation.py>
    <Function test_recommendation[1011101-5]>
```

Para ter uma ideia dos dados de entrada e saída e suas formas, continue lendo.


## Estrutura de pastas

`data/uc_<id da UC>`:
- entradas:
    - histórico de consumo
    - modalidade tarifa atual
- saídas esperadas:
    - percentis azul/verde `[0.1 -> 0.98]`
    - resumo azul/verde. Com as colunas
        - demanda ponta
        - demanda fora de ponta
        - ultrapassagem ponta
        - ultrapassagem fora de ponta
        - valor total de demanda
    - recomendação de contrato
    - recomendação de bandeira de tarifa

### Valores escalares
Um `DataFrame` do Pandas não armazena valores escalares, apenas valores do
tipo lista (Series). Ainda assim, os valores dos arquivos a seguir foram
armazenados como colunas (Series) até ser encontrada uma representação melhor.

`per_total_in_reais.json`: contém os totais de valores em reais de cada
percentil (0.1 -> 0.98) pra cada modalidade (azul e verde).

`summary_scalar_values.json`: contém os dados:

```json
{
    "blue": {
        "smallest_total_demand_cost_in_reais": 0.00,
        "off_peak_demand_in_kw": 0.00,
        "peak_demand_in_kw": 0.00,
        "total_consumption_cost_in_reais": 0.00,
        "total_total_cost_in_reais": 0.00,
    },
    "green": {
        "smallest_total_demand_cost_in_reais": 0.00,
        "off_peak_demand_in_kw": 0.00,
        "total_consumption_cost_in_reais": 0.00,
        "total_demand_cost_in_reais": 0.00,
        "total_total_cost_in_reais": 0.00,
    }
}
```
