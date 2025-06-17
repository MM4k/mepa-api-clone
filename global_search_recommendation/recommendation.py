from recommendation_commons.helpers import fill_history_with_pending_dates, fill_with_pending_dates
from recommendation_commons.recommendation_result import RecommendationResult
from recommendation_commons.response import build_response
from recommendation_commons.static_getters import StaticGetters
from tariffs.models import Tariff


class Recommendation:
    SAFETY_MARGIN = 1.05

    def __init__(self, flag, values, domain) -> None:
        self.domain = domain
        self.tariff = self.domain.green if flag == Tariff.GREEN else self.domain.blue
        self.values = (int(values[0] * self.SAFETY_MARGIN), int(values[1] * self.SAFETY_MARGIN))

    def build_response(self):
        self.current_contract_values = StaticGetters.calculate_current_contract(
            self.domain.consumption_history,
            self.domain.current_tariff,
        )
        result = RecommendationResult()
        result.current_contract = self.current_contract_values
        result.tariff_flag = self.tariff.flag
        result.peak_demand_in_kw, result.off_peak_demand_in_kw = self.values[0], self.values[1]
        result.frame = StaticGetters.get_recommendation_frame(
            self.domain.consumption_history,
            self.values,
            self.tariff,
        )

        cur_demand_values = (
            self.domain.current_contract.peak_contracted_demand_in_kw,
            self.domain.current_contract.off_peak_contracted_demand_in_kw,
        )

        result = StaticGetters.validate_recommendation_with_power_generation(
            result,
            self.domain.current_tariff.power_generation_tusd_in_reais_per_kw,
            self.tariff.power_generation_tusd_in_reais_per_kw,
            cur_demand_values,
            self.domain.consumer_unit.total_installed_power,
        )

        result.frame.absolute_difference = (
            self.current_contract_values.cost_in_reais - result.frame.contract_cost_in_reais
        )

        result.frame.percentage_difference = (
            1 - result.frame.contract_cost_in_reais / self.current_contract_values.cost_in_reais
        )

        if result.frame.absolute_difference.sum() <= 0:
            result = None
            fill_history_with_pending_dates(self.domain.consumption_history, self.domain.pending_bills_dates)
        else:
            fill_with_pending_dates(result, self.domain.consumption_history, self.domain.pending_bills_dates)

        return build_response(
            result,
            self.current_contract_values,
            self.domain.consumption_history,
            self.domain.current_contract,
            self.domain.consumer_unit,
            self.domain.blue,
            self.domain.green,
            self.domain.errors,
            self.domain.warnings,
            self.domain.consumption_history_length,
        )
