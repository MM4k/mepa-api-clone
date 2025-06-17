from pandas import DataFrame


class RecommendationResult:
    def __init__(self):
        self.frame: DataFrame
        self.current_contract: DataFrame
        self.tariff_flag = ""
        self.off_peak_demand_in_kw = 0.0
        self.peak_demand_in_kw = 0.0
