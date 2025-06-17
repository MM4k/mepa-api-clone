from typing import Literal

from pandas import DataFrame

from recommendation.blue import BluePercentileCalculator, BluePercentileResult
from recommendation.green import GreenPercentileCalculator, GreenPercentileResult
from recommendation_commons.recommendation_result import RecommendationResult
from recommendation_commons.static_getters import StaticGetters
from tariffs.models import Tariff

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


class ContractRecommendationCalculator:
    HEADERS = [
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

    def __init__(
        self,
        consumption_history: DataFrame,
        blue_summary: BluePercentileResult,
        green_summary: GreenPercentileResult,
        current_tariff_flag: Literal["blue", "green"],
        green_tariff: Tariff,
        blue_tariff: Tariff,
        current_contract: DataFrame,
    ):
        self.green_tariff = green_tariff
        self.blue_tariff = blue_tariff
        self.consumption_history = consumption_history
        self.current_tariff_flag = current_tariff_flag
        self.blue_summary = blue_summary
        self.green_summary = green_summary
        # FIXME: renomear essa variável pra um nome mais claro
        self.frame = DataFrame(columns=self.HEADERS)
        self.current_contract = current_contract

    def calculate(self, total_installed_power, sub_group, cur_demand_values):
        rec = RecommendationResult()
        rec.current_contract = self.current_contract
        skip_green = sub_group in ["A2", "A3"]

        if skip_green or self.blue_summary.total_total_cost_in_reais < self.green_summary.total_total_cost_in_reais:
            rec.tariff_flag = Tariff.BLUE
            rec.off_peak_demand_in_kw = self.blue_summary.off_peak_demand_in_kw[0]
            rec.peak_demand_in_kw = self.blue_summary.peak_demand_in_kw[0]
        else:
            rec.tariff_flag = Tariff.GREEN
            rec.off_peak_demand_in_kw = self.green_summary.off_peak_demand_in_kw[0]
            rec.peak_demand_in_kw = self.green_summary.off_peak_demand_in_kw[0]

        recommended_tariff = self.blue_tariff if rec.tariff_flag == Tariff.BLUE else self.green_tariff

        rec.frame = StaticGetters.get_recommendation_frame(
            self.consumption_history,
            (rec.peak_demand_in_kw, rec.off_peak_demand_in_kw),
            recommended_tariff,
        )

        rec_tariff_to_validation = (
            self.blue_tariff.power_generation_tusd_in_reais_per_kw
            if rec.tariff_flag == Tariff.BLUE
            else self.green_tariff.power_generation_tusd_in_reais_per_kw
        )
        current_tariff_to_validation = (
            self.blue_tariff.power_generation_tusd_in_reais_per_kw
            if self.current_tariff_flag == Tariff.BLUE
            else self.green_tariff.power_generation_tusd_in_reais_per_kw
        )

        rec = StaticGetters.validate_recommendation_with_power_generation(
            rec,
            current_tariff_to_validation,
            rec_tariff_to_validation,
            cur_demand_values,
            total_installed_power,
        )

        rec.frame.absolute_difference = self.current_contract.cost_in_reais - rec.frame.contract_cost_in_reais
        rec.frame.percentage_difference = 1 - rec.frame.contract_cost_in_reais / self.current_contract.cost_in_reais

        if rec.frame.absolute_difference.sum() <= 0:
            rec = None
        return rec


class RecommendationCalculator:
    CURRENT_CONTRACT_HEADERS = [
        "date",
        "consumption_cost_in_reais",
        "demand_cost_in_reais",
        "cost_in_reais",
        "percentage_consumption",
        "percentage_demand",
    ]

    def __init__(
        self,
        consumption_history: DataFrame,
        current_tariff_flag: str,
        blue_tariff: Tariff,
        green_tariff: Tariff,
        sub_group: str,
        cur_demand_values: tuple,
    ):
        self.current_tariff = current_tariff_flag
        self.blue_tariff = blue_tariff
        self.green_tariff = green_tariff
        self.consumption_history = consumption_history
        self.current_contract = StaticGetters.calculate_current_contract(
            consumption_history, blue_tariff if current_tariff_flag == Tariff.BLUE else green_tariff
        )
        self.sub_group = sub_group

        self.blue_calculator = BluePercentileCalculator(consumption_history, self.blue_tariff.as_blue_tariff())
        self.green_calculator = GreenPercentileCalculator(consumption_history, self.green_tariff.as_green_tariff())
        self.cur_demand_values = cur_demand_values

    def calculate(self, total_installed_power):
        """Essa função ainda deve voltar um RecommendationResult, manipulando
        ou incluindo ContractRecommendationResult"""
        b_result = self.blue_calculator.calculate()
        g_result = self.green_calculator.calculate()

        rec_calculator = ContractRecommendationCalculator(
            self.consumption_history,
            b_result.summary,
            g_result.summary,
            self.current_tariff,
            self.green_tariff,
            self.blue_tariff,
            current_contract=self.current_contract,
        )

        return rec_calculator.calculate(
            total_installed_power,
            self.sub_group,
            self.cur_demand_values,
        )
