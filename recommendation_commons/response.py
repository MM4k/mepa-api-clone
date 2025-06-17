from datetime import datetime

from django.conf import settings
from numpy import nan
from pandas import DataFrame
from rest_framework.response import Response

from contracts.models import Contract
from recommendation_commons.recommendation_result import RecommendationResult
from tariffs.models import Tariff
from tariffs.serializers import BlueTariffSerializer, GreenTariffSerializer
from universities.models import ConsumerUnit

HEADERS_FOR_CONSUMPTION_HISTORY = [
    "date",
    "peak_consumption_in_kwh",
    "off_peak_consumption_in_kwh",
    "peak_measured_demand_in_kw",
    "off_peak_measured_demand_in_kw",
]


def _get_tariff_billing_time(tariff_label: str):
    if "off_peak" in tariff_label:
        return "Fora ponta"
    elif "peak" in tariff_label:
        return "Ponta"
    return "NA"


def _generate_tariffs_as_table(blue_tariff: Tariff, green_tariff: Tariff):
    serialized_blue = BlueTariffSerializer(blue_tariff).data
    serialized_green = GreenTariffSerializer(green_tariff).data
    # ????? serialized_green['missing_field_in_green'] = None

    tariff_labels = {*serialized_blue, *serialized_green}

    tariffs_table: list[dict] = []
    for label in tariff_labels:
        row = {"label": label, "billingTime": _get_tariff_billing_time(label)}
        row["blue"] = serialized_blue[label] if label in serialized_blue else None
        row["green"] = serialized_green[label] if label in serialized_green else None
        tariffs_table.append(row)

    return tariffs_table


def _generate_plot_demand_and_consumption_costs_in_current_contract(current_contract_costs: DataFrame):
    if current_contract_costs.empty:
        return None, None

    current_demand_and_consumption_costs: DataFrame = current_contract_costs[
        ["consumption_cost_in_reais", "demand_cost_in_reais"]
    ]

    return current_demand_and_consumption_costs.to_dict(
        "list"
    ), current_contract_costs.consumption_cost_in_reais.sum() + current_contract_costs.demand_cost_in_reais.sum()


def _generate_plot_costs_comparison(recommendation: RecommendationResult):
    result = DataFrame()
    result.insert(0, "total_cost_in_reais_in_current", recommendation.current_contract.cost_in_reais)
    result.insert(0, "total_cost_in_reais_in_recommended", recommendation.frame.contract_cost_in_reais)
    result.insert(0, "date", recommendation.frame.date)

    result.replace({nan: None}, inplace=True)
    result_dict = result.to_dict("list")
    result_dict["total_total_cost_in_reais_in_current"] = recommendation.current_contract.cost_in_reais.sum()
    result_dict["total_total_cost_in_reais_in_recommended"] = recommendation.frame.contract_cost_in_reais.sum()
    return result_dict


def _generate_plot_detailed_contracts_costs_comparison(recommendation: RecommendationResult):
    result = DataFrame()
    result.insert(0, "consumptionCostInReaisInRecommended", recommendation.frame.consumption_cost_in_reais)
    result.insert(0, "demandCostInReaisInRecommended", recommendation.frame.demand_cost_in_reais)
    result.insert(0, "totalCostInReaisInCurrent", recommendation.current_contract.cost_in_reais)
    return result.to_dict("list")


def _generate_table_contracts_comparison(recommendation: RecommendationResult):
    result = DataFrame()
    result.insert(0, "absolute_difference", recommendation.frame.absolute_difference)
    result.insert(0, "consumption_cost_in_reais_in_recommended", recommendation.frame.consumption_cost_in_reais)
    result.insert(0, "demand_cost_in_reais_in_recommended", recommendation.frame.demand_cost_in_reais)
    result.insert(0, "total_cost_in_reais_in_recommended", recommendation.frame.contract_cost_in_reais)
    result.insert(0, "consumption_cost_in_reais_in_current", recommendation.current_contract.consumption_cost_in_reais)
    result.insert(0, "demand_cost_in_reais_in_current", recommendation.current_contract.demand_cost_in_reais)
    result.insert(0, "total_cost_in_reais_in_current", recommendation.current_contract.cost_in_reais)
    result.insert(0, "date", recommendation.frame.date)

    contracts_comparison_totals: dict[str, float] = {
        "absolute_difference": result.absolute_difference.sum(),
        "consumption_cost_in_reais_in_recommended": result.consumption_cost_in_reais_in_recommended.sum(),
        "demand_cost_in_reais_in_recommended": result.demand_cost_in_reais_in_recommended.sum(),
        "total_cost_in_reais_in_recommended": result.total_cost_in_reais_in_recommended.sum(),
        "consumption_cost_in_reais_in_current": result.consumption_cost_in_reais_in_current.sum(),
        "demand_cost_in_reais_in_current": result.demand_cost_in_reais_in_current.sum(),
        "total_cost_in_reais_in_current": result.total_cost_in_reais_in_current.sum(),
    }

    result.replace({nan: None}, inplace=True)
    return (result.to_dict("records"), contracts_comparison_totals)


def build_response(
    recommendation: RecommendationResult,
    current_contract: DataFrame,
    consumption_history: DataFrame,
    contract: Contract,
    consumer_unit: ConsumerUnit,
    blue: Tariff,
    green: Tariff,
    errors: list[str],
    warnings: list[str],
    energy_bills_count: int,
):
    """Reponsável por APENAS construir o objeto `Response` de endpoint"""
    dates = consumption_history.date
    current_contract_costs, current_total_cost = _generate_plot_demand_and_consumption_costs_in_current_contract(
        current_contract
    )

    # FIXME: refatorar
    if recommendation is None:
        return Response(
            {
                "generated_on": datetime.now(),
                "errors": errors,
                "warnings": warnings,
                "dates": dates,
                "current_contract": {
                    "university": consumer_unit.university.name,
                    "distributor": contract.distributor.name,
                    "consumer_unit": consumer_unit.name,
                    "consumer_unit_code": consumer_unit.code,
                    "tariff_flag": contract.tariff_flag,
                    "subgroup": contract.subgroup,
                    "peak_demand_in_kw": contract.peak_contracted_demand_in_kw,
                    "off_peak_demand_in_kw": contract.off_peak_contracted_demand_in_kw,
                },
                "should_renew_contract": False,
                "consumption_history_plot": consumption_history[
                    HEADERS_FOR_CONSUMPTION_HISTORY + ["contract_peak_demand_in_kw", "contract_off_peak_demand_in_kw"]
                ].to_dict("list"),
                "current_contract_costs_plot": current_contract_costs,
                "current_total_cost": current_total_cost,
            }
        )

    costs_comparison = _generate_plot_costs_comparison(recommendation)
    contracts_comparison, totals = _generate_table_contracts_comparison(recommendation)
    detailed_contracts_costs_comparison = _generate_plot_detailed_contracts_costs_comparison(recommendation)
    table_tariffs = _generate_tariffs_as_table(blue, green)
    costs_ratio = totals["absolute_difference"] / totals["total_cost_in_reais_in_current"]
    nominal_savings_percentage = max(0, round(costs_ratio, 3) * 100)

    return Response(
        {
            "generated_on": datetime.now(),
            "errors": errors,
            "warnings": warnings,
            "dates": dates,
            "should_renew_contract": costs_ratio > settings.MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION,
            "energy_bills_count": energy_bills_count,
            "nominal_savings_percentage": nominal_savings_percentage,
            "current_contract": {
                "university": consumer_unit.university.name,
                "distributor": contract.distributor.name,
                "consumer_unit": consumer_unit.name,
                "consumer_unit_code": consumer_unit.code,
                "tariff_flag": contract.tariff_flag,
                "subgroup": contract.subgroup,
                "peak_demand_in_kw": contract.peak_contracted_demand_in_kw,
                "off_peak_demand_in_kw": contract.off_peak_contracted_demand_in_kw,
            },
            "consumption_history_table": consumption_history[HEADERS_FOR_CONSUMPTION_HISTORY].to_dict("records"),
            "consumption_history_plot": consumption_history[
                HEADERS_FOR_CONSUMPTION_HISTORY + ["contract_peak_demand_in_kw", "contract_off_peak_demand_in_kw"]
            ].to_dict("list"),
            "detailed_contracts_costs_comparison_plot": detailed_contracts_costs_comparison,
            "current_contract_costs_plot": current_contract_costs,
            "tariff_dates": {
                # Podiam ser as datas do green também. Qualquer um dos dois serve.
                "start_date": blue.start_date,
                "end_date": blue.end_date,
            },
            "tariffs_table": table_tariffs,
            "recommended_contract": {
                "university": consumer_unit.university.name,
                "distributor": contract.distributor.name,
                "consumer_unit": consumer_unit.name,
                "consumer_unit_code": consumer_unit.code,
                "subgroup": contract.subgroup,
                "tariff_flag": recommendation.tariff_flag,
                "off_peak_demand_in_kw": recommendation.off_peak_demand_in_kw,
                "peak_demand_in_kw": recommendation.peak_demand_in_kw,
            },
            "costs_comparison_plot": costs_comparison,
            "contracts_comparison_table": contracts_comparison,
            "contracts_comparison_totals": totals,
            "current_total_cost": current_total_cost,
        }
    )
