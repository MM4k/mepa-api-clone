CONSUMPTION_HISTORY_HEADERS = [
    # A coluna 'date' não é utilizada no cálculo, mas ela está presente porque
    # facilita a manipulação posterior do dataframe
    "date",
    "peak_consumption_in_kwh",
    "off_peak_consumption_in_kwh",
    "peak_measured_demand_in_kw",
    "off_peak_measured_demand_in_kw",
    "contract_peak_demand_in_kw",
    "contract_off_peak_demand_in_kw",
    "peak_exceeded_in_kw",
    "off_peak_exceeded_in_kw",
]

CURRENT_CONTRACT_HEADERS = [
    "date",
    "consumption_cost_in_reais",
    "demand_cost_in_reais",
    "cost_in_reais",
    "percentage_consumption",
    "percentage_demand",
]

RECOMMENDATION_FRAME_HEADERS = [
    "date",
    "peak_demand_in_kw",
    "off_peak_demand_in_kw",
    "consumption_cost_in_reais",
    "demand_cost_in_reais",
    "contract_cost_in_reais",
    "percentage_consumption",
    "percentage_demand",
    "absolute_difference",
    "percentage_difference",
]

SAFETY_MARGIN = 1.05
