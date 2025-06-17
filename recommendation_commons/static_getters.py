import decimal

from pandas import DataFrame

from contracts.models import Contract
from recommendation_commons.headers import (
    CONSUMPTION_HISTORY_HEADERS,
    CURRENT_CONTRACT_HEADERS,
    RECOMMENDATION_FRAME_HEADERS,
)
from recommendation_commons.recommendation_result import RecommendationResult
from tariffs.models import Tariff
from universities.models import ConsumerUnit


class StaticGetters:
    @staticmethod
    def get_tariffs(subgroup: str, distributor_id: int):
        tariffs = Tariff.objects.filter(subgroup=subgroup, distributor_id=distributor_id)
        blue_tariff = tariffs.filter(flag=Tariff.BLUE).first()
        green_tariff = tariffs.filter(flag=Tariff.GREEN).first()
        return (blue_tariff, green_tariff)

    @staticmethod
    def get_consumption_history(consumer_unit: ConsumerUnit, contract: Contract):
        bills = consumer_unit.get_energy_bills_for_recommendation()
        pending_bills = consumer_unit.get_energy_bills_pending()
        bills_list: list[dict] = []
        atypical_bills_count = 0
        for bill in bills:
            if bill["energy_bill"] is None:
                continue

            if bool(bill["energy_bill"]["is_atypical"]):
                atypical_bills_count += 1
                bill["energy_bill"] = None
                pending_bills.append(bill)
                continue

            b = bill["energy_bill"]
            bills_list.append(
                {
                    "date": b["date"],
                    "peak_consumption_in_kwh": float(b["peak_consumption_in_kwh"]),
                    "off_peak_consumption_in_kwh": float(b["off_peak_consumption_in_kwh"]),
                    "peak_measured_demand_in_kw": float(
                        b["peak_measured_demand_in_kw"]
                        if b["peak_measured_demand_in_kw"] is not None
                        else float(b["off_peak_measured_demand_in_kw"])
                    ),
                    "off_peak_measured_demand_in_kw": float(b["off_peak_measured_demand_in_kw"]),
                    "contract_peak_demand_in_kw": float(contract.peak_contracted_demand_in_kw),
                    "contract_off_peak_demand_in_kw": float(contract.off_peak_contracted_demand_in_kw),
                    "peak_exceeded_in_kw": 0.0,
                    "off_peak_exceeded_in_kw": 0.0,
                }
            )

        bills_list.reverse()
        consumption_history = DataFrame(bills_list, columns=CONSUMPTION_HISTORY_HEADERS)

        if (consumption_history.peak_measured_demand_in_kw == 0).all():
            consumption_history.peak_measured_demand_in_kw = consumption_history.off_peak_measured_demand_in_kw

        base_to_exceed_peak = (
            consumption_history.contract_peak_demand_in_kw
            if contract.tariff_flag == Tariff.BLUE
            else consumption_history.contract_off_peak_demand_in_kw
        )

        consumption_history.peak_exceeded_in_kw = (
            consumption_history.peak_measured_demand_in_kw - base_to_exceed_peak
        ).clip(0.0)
        consumption_history.off_peak_exceeded_in_kw = (
            consumption_history.off_peak_measured_demand_in_kw - consumption_history.contract_off_peak_demand_in_kw
        ).clip(0.0)

        pending_bills_dates = [f"{b['year']}-{b['month']}-01" for b in pending_bills]
        return (consumption_history, pending_bills_dates, atypical_bills_count)

    @staticmethod
    def get_comsuption_cost(history: DataFrame, tariff: Tariff):
        return (
            history.peak_consumption_in_kwh
            * float(tariff.peak_tusd_in_reais_per_mwh + tariff.peak_te_in_reais_per_mwh)
            / 1000
            + history.off_peak_consumption_in_kwh
            * float(tariff.off_peak_tusd_in_reais_per_mwh + tariff.off_peak_te_in_reais_per_mwh)
            / 1000
        )

    @staticmethod
    def get_exceeded_demand_column(measured_demand, contracted_demand):
        return (measured_demand - contracted_demand).clip(0)

    @classmethod
    def get_demand_cost(cls, tariff: Tariff, history: DataFrame, demand_values):
        if tariff.is_green():
            tariff = tariff.as_green_tariff()
            demand = demand_values[1]
            exceeded_sum = cls.get_exceeded_demand_column(
                history.peak_measured_demand_in_kw, demand
            ) + cls.get_exceeded_demand_column(
                history.off_peak_measured_demand_in_kw, demand
            )  # Checar a utilização da coluna de ultrapassagem
            exceeded_val = exceeded_sum * 3
            return (demand + exceeded_val) * tariff.na_tusd_in_reais_per_kw
        elif tariff.is_blue():
            tariff = tariff.as_blue_tariff()
            (peak_demand, off_peak_demand) = (demand_values[0], demand_values[1])
            value_peak = peak_demand + 3 * cls.get_exceeded_demand_column(
                history.peak_measured_demand_in_kw, peak_demand
            )
            value_off_peak = off_peak_demand + 3 * cls.get_exceeded_demand_column(
                history.off_peak_measured_demand_in_kw, off_peak_demand
            )  # Checar a utilização da coluna de ultrapassagem
            return (tariff.peak_tusd_in_reais_per_kw * value_peak) + (
                tariff.off_peak_tusd_in_reais_per_kw * value_off_peak
            )

    ## REFACTOR: tanto current quanto recommended possuem algumas colunas em comun, dá pra reutilizar melhor o código
    @classmethod
    def calculate_current_contract(cls, history: DataFrame, tariff: Tariff):
        current_contract = DataFrame(columns=CURRENT_CONTRACT_HEADERS)
        current_contract.date = history.date
        current_contract.consumption_cost_in_reais = cls.get_comsuption_cost(history, tariff)
        demand_values = (history["contract_peak_demand_in_kw"], history["contract_off_peak_demand_in_kw"])
        current_contract.demand_cost_in_reais = cls.get_demand_cost(tariff, history, demand_values)

        return cls.atualize_frames_percentages(current_contract)

    @classmethod
    def get_recommendation_frame(cls, history: DataFrame, values: tuple, tariff: Tariff):
        recommendation_frame = DataFrame(columns=RECOMMENDATION_FRAME_HEADERS)
        recommendation_frame.date = history.date
        recommendation_frame.peak_demand_in_kw = values[0]
        recommendation_frame.off_peak_demand_in_kw = values[1]
        recommendation_frame.consumption_cost_in_reais = cls.get_comsuption_cost(history, tariff)
        recommendation_frame.demand_cost_in_reais = cls.get_demand_cost(tariff, history, values)

        return cls.atualize_frames_percentages(recommendation_frame)

    @classmethod
    def validate_recommendation_with_power_generation(
        cls,
        recommendation: RecommendationResult,
        current_tusd_g,
        rec_tusd_g,
        cur_demand_values: tuple,
        instaled_power_supply=None,
    ):
        if instaled_power_supply:
            rec_demand = (
                decimal.Decimal(recommendation.off_peak_demand_in_kw)
                if recommendation.tariff_flag == Tariff.GREEN
                else decimal.Decimal(max(recommendation.peak_demand_in_kw, recommendation.off_peak_demand_in_kw))
            )
            if rec_demand < instaled_power_supply:
                recommendation.frame["demand_cost_in_reais"] += float(
                    (instaled_power_supply - rec_demand) * rec_tusd_g
                )
                recommendation.current_contract["demand_cost_in_reais"] += float(
                    (instaled_power_supply - max(cur_demand_values)) * current_tusd_g
                )

                recommendation.frame = cls.atualize_frames_percentages(recommendation.frame)
                recommendation.current_contract = cls.atualize_frames_percentages(recommendation.current_contract)

        return recommendation

    @staticmethod
    def atualize_frames_percentages(frame: DataFrame):
        if "contract_cost_in_reais" in frame.columns:
            frame.contract_cost_in_reais = frame.consumption_cost_in_reais + frame.demand_cost_in_reais
            frame.percentage_consumption = frame.consumption_cost_in_reais / frame.contract_cost_in_reais
            frame.percentage_demand = frame.demand_cost_in_reais / frame.contract_cost_in_reais
        else:
            frame.cost_in_reais = frame.consumption_cost_in_reais + frame.demand_cost_in_reais
            frame.percentage_consumption = frame.consumption_cost_in_reais / frame.cost_in_reais
            frame.percentage_demand = frame.demand_cost_in_reais / frame.cost_in_reais
        return frame
