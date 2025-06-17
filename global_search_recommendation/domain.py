from datetime import date

from django.conf import settings
from rest_framework import status

from mec_energia.error_response_manage import (
    ErrorMensageParser,
    ExpiredTariffWarnning,
    NotEnoughEnergyBills,
    NotEnoughEnergyBillsWithAtypical,
    PendingBillsWarnning,
    TariffsNotFoundError,
)
from recommendation_commons.static_getters import StaticGetters
from tariffs.models import Tariff
from universities.models import ConsumerUnit


class Domain:
    def __init__(self, uc_id: int):
        self.uc_id = uc_id
        self.errors = []
        self.warnings = []

    def _exceeded_demand(self, meassured_demand: 0.0, contracted_demand: 0.0) -> 0.0:
        if meassured_demand <= contracted_demand:
            return 0
        else:
            return meassured_demand - contracted_demand

    def mount(self):
        try:
            self.consumer_unit = ConsumerUnit.objects.get(pk=self.uc_id)
        except ConsumerUnit.DoesNotExist:
            return ({"errors": ["Consumer unit does not exist"]}, status.HTTP_404_NOT_FOUND)

        if not self.consumer_unit.is_active:
            return ({"errors": ["Consumer unit is not active"]}, status.HTTP_400_BAD_REQUEST)

        self.current_contract = self.consumer_unit.current_contract
        self.distributor = self.current_contract.distributor
        self.blue, self.green = StaticGetters.get_tariffs(self.current_contract.subgroup, self.distributor.id)

        is_missing_tariff = (
            self.blue is None or self.current_contract.subgroup not in ["A2", "A3"] and self.green is None
        )
        if is_missing_tariff:
            self.errors.append(TariffsNotFoundError)

        self.current_tariff = self.green if self.current_contract.tariff_flag == Tariff.GREEN else self.blue
        self.consumption_history, self.pending_bills_dates, atypical_bills_count = (
            StaticGetters.get_consumption_history(self.consumer_unit, self.current_contract)
        )

        self.consumption_history_length = len(self.consumption_history)
        pending_num = len(self.pending_bills_dates) - atypical_bills_count
        has_enough_energy_bills = self.consumption_history_length >= settings.MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION

        if not has_enough_energy_bills:
            self.errors.append(
                ErrorMensageParser.parse(
                    NotEnoughEnergyBills if atypical_bills_count == 0 else NotEnoughEnergyBillsWithAtypical,
                    (6) if atypical_bills_count == 0 else (6 + atypical_bills_count),
                )
            )

        elif self.consumption_history_length + atypical_bills_count < settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION:
            self.warnings.append(
                ErrorMensageParser.parse(
                    PendingBillsWarnning, (pending_num, "fatura" if pending_num == 1 else "faturas")
                )
            )

        if not is_missing_tariff and (
            self.blue.end_date < date.today()
            or (self.current_contract.subgroup not in ["A2", "A3"] and self.green.end_date < date.today())
        ):
            self.warnings.append(ExpiredTariffWarnning)

        self.base_consumption_history = self.consumption_history[
            [
                "peak_consumption_in_kwh",
                "off_peak_consumption_in_kwh",
                "peak_measured_demand_in_kw",
                "off_peak_measured_demand_in_kw",
                "contract_peak_demand_in_kw",
                "contract_off_peak_demand_in_kw",
            ]
        ].values.astype(float)

        if len(self.errors) == 0:
            self.consumption_cost_on_blue = StaticGetters.get_comsuption_cost(
                self.consumption_history,
                self.blue,
            ).sum()

            self.consumption_cost_on_green = StaticGetters.get_comsuption_cost(
                self.consumption_history,
                self.green,
            ).sum()
        else:
            return len(self.errors)

        return None

    def green_objective_func(self, demands) -> 0.0:
        demand_value = 0
        for bill in self.base_consumption_history:
            demand_value += demands[0] + 3 * (
                self._exceeded_demand(bill[2], demands[0])
                + self._exceeded_demand(
                    bill[3],
                    demands[0],
                )
            )

        return float(self.green.na_tusd_in_reais_per_kw) * demand_value + self.consumption_cost_on_green

    def blue_objective_func(self, demands) -> 0.0:
        peak_demand_value = 0
        off_peak_demand_value = 0
        for bill in self.base_consumption_history:
            peak_demand_value += demands[0] + 3 * self._exceeded_demand(bill[2], demands[0])
            off_peak_demand_value += demands[1] + 3 * self._exceeded_demand(bill[3], demands[1])

        return (
            (float(self.blue.peak_tusd_in_reais_per_kw) * peak_demand_value)
            + (float(self.blue.off_peak_tusd_in_reais_per_kw) * off_peak_demand_value)
            + self.consumption_cost_on_blue
        )
