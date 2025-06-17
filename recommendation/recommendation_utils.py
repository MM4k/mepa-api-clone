import json

from collections import OrderedDict
from datetime import date, datetime

from django.conf import settings
from pandas import DataFrame
from rest_framework import status
from rest_framework.response import Response

from contracts.models import Contract
from mec_energia.error_response_manage import (
    ErrorMensageParser,
    ExpiredTariffWarnning,
    NotEnoughEnergyBills,
    NotEnoughEnergyBillsWithAtypical,
    PendingBillsWarnning,
    TariffsNotFoundError,
)
from recommendation.calculator import RecommendationCalculator
from recommendation_commons.helpers import fill_history_with_pending_dates, fill_with_pending_dates
from recommendation_commons.recommendation_result import RecommendationResult
from recommendation_commons.response import (
    _generate_plot_costs_comparison,
    _generate_plot_demand_and_consumption_costs_in_current_contract,
    _generate_plot_detailed_contracts_costs_comparison,
    _generate_table_contracts_comparison,
)
from recommendation_commons.static_getters import StaticGetters
from tariffs.models import Tariff
from universities.models import ConsumerUnit

from .models import Recommendation


def serialize_with_order(data):
    # Se data for um OrderedDict, use json.dumps diretamente
    if isinstance(data, OrderedDict):
        return json.dumps(data)
    # Caso contrário, converta para OrderedDict e serialize
    return json.dumps(OrderedDict(data))


def process_recommendation(consumer_unit_id):
    try:
        consumer_unit = ConsumerUnit.objects.get(pk=consumer_unit_id)
    except ConsumerUnit.DoesNotExist:
        return Response({"errors": ["Consumer unit does not exist"]}, status=status.HTTP_404_NOT_FOUND)

    if not consumer_unit.is_active:
        return Response({"errors": ["Consumer unit is not active"]}, status=status.HTTP_400_BAD_REQUEST)

    contract = consumer_unit.current_contract
    distributor_id = contract.distributor.id
    blue, green = StaticGetters.get_tariffs(contract.subgroup, distributor_id)
    errors = []
    warnings = []

    is_missing_tariff = blue is None or (contract.subgroup not in ["A2", "A3"] and green is None)
    if is_missing_tariff:
        errors.append(TariffsNotFoundError)

    consumption_history, pending_bills_dates, atypical_bills_count = StaticGetters.get_consumption_history(
        consumer_unit, contract
    )

    consumption_history_length = len(consumption_history)
    pending_num = len(pending_bills_dates) - atypical_bills_count
    has_enough_energy_bills = consumption_history_length >= settings.MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION

    if not has_enough_energy_bills:
        errors.append(
            ErrorMensageParser.parse(
                NotEnoughEnergyBills if atypical_bills_count == 0 else NotEnoughEnergyBillsWithAtypical,
                (6) if atypical_bills_count == 0 else (6 + atypical_bills_count),
            )
        )

    elif consumption_history_length + atypical_bills_count < settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION:
        warnings.append(
            ErrorMensageParser.parse(PendingBillsWarnning, (pending_num, "fatura" if pending_num == 1 else "faturas"))
        )

    if not is_missing_tariff and (
        blue.end_date < date.today() or (contract.subgroup not in ["A2", "A3"] and green.end_date < date.today())
    ):
        warnings.append(ExpiredTariffWarnning)

    calculator = None
    if not is_missing_tariff:
        calculator = RecommendationCalculator(
            consumption_history=consumption_history,
            current_tariff_flag=contract.tariff_flag,
            blue_tariff=blue,
            green_tariff=green,
            sub_group=contract.subgroup,
            cur_demand_values=(contract.peak_contracted_demand_in_kw, contract.off_peak_contracted_demand_in_kw),
        )

    recommendation = None
    current_contract = calculator.current_contract if calculator else DataFrame()

    if calculator and has_enough_energy_bills:
        recommendation = calculator.calculate(consumer_unit.total_installed_power)
        if recommendation:
            fill_with_pending_dates(recommendation, consumption_history, pending_bills_dates)
    else:
        # FIXME: temporário
        fill_history_with_pending_dates(consumption_history, pending_bills_dates)

    rc = (
        recommendation,
        current_contract,
        consumption_history,
        contract,
        consumer_unit,
        blue,
        green,
        errors,
        warnings,
        consumption_history_length,
    )

    return rc


def serializeSeries(serie, a):
    def convert_item(item):
        # Handle "None" string
        if item == "None":
            return None

        if isinstance(item, str):
            # Remove leading/trailing whitespace and quotes
            item = item.strip().strip('"')

            # Try to parse as a date or datetime
            try:
                # Attempt to parse as ISO format datetime
                return datetime.fromisoformat(item)
            except ValueError:
                # If not a datetime, try to parse as a number
                try:
                    # Check if the string is a valid number
                    if item.isdigit() or (item.replace(".", "", 1).isdigit() and item.count(".") < 2):
                        num = float(item)
                        return int(num) if num.is_integer() else num
                except ValueError:
                    # If not a number, return as string
                    return item

        # Handle non-string types
        try:
            return float(item)
        except (ValueError, TypeError):
            return str(item)

    return [convert_item(item) for item in serie]


def save_recommendation(
    consumer_unit_id,
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
    dates = consumption_history.date
    dates_list = [date_obj for date_obj in dates]

    current_contract_costs, current_total_cost = _generate_plot_demand_and_consumption_costs_in_current_contract(
        current_contract
    )

    if recommendation is None:
        recommendation_instance, created = Recommendation.objects.update_or_create(
            consumer_unit_id=consumer_unit_id.id,
            defaults={
                "consumer_unit_id": consumer_unit_id,
                "isValid": True,
                "generatedOn": datetime.now(),
                "errors": errors,
                "warnings": warnings,
                "dates": dates_list,
                "shouldRenewContract": False,
                "currentContractCostsPlot": {
                    "consumptionCostInReais": serializeSeries(
                        current_contract_costs["consumption_cost_in_reais"], "consumption_cost_in_reais"
                    ),
                    "demandCostInReais": serializeSeries(
                        current_contract_costs["demand_cost_in_reais"], "demand_cost_in_reais"
                    ),
                },
                "currentTotalCost": current_total_cost,
            },
        )
        return recommendation_instance, created
    else:
        costs_comparison = _generate_plot_costs_comparison(recommendation)
        contracts_comparison, totals = _generate_table_contracts_comparison(recommendation)
        costs_ratio = totals["absolute_difference"] / totals["total_cost_in_reais_in_current"]
        nominal_savings_percentage = max(0, round(costs_ratio, 3) * 100)
        detailed_contracts_costs_comparison = _generate_plot_detailed_contracts_costs_comparison(recommendation)

        contracts_comparison_table = []
        for comparison in contracts_comparison:
            entry = {
                "absoluteDifference": comparison["absolute_difference"],
                "consumptionCostInReaisInRecommended": comparison["consumption_cost_in_reais_in_recommended"],
                "demandCostInReaisInRecommended": comparison["demand_cost_in_reais_in_recommended"],
                "totalCostInReaisInRecommended": comparison["total_cost_in_reais_in_recommended"],
                "consumptionCostInReaisInCurrent": comparison["consumption_cost_in_reais_in_current"],
                "demandCostInReaisInCurrent": comparison["demand_cost_in_reais_in_current"],
                "totalCostInReaisInCurrent": comparison["total_cost_in_reais_in_current"],
                "date": comparison["date"].isoformat(),
            }
            contracts_comparison_table.append(entry)

        recommendation_instance, created = Recommendation.objects.update_or_create(
            consumer_unit_id=consumer_unit_id,
            defaults={
                "consumer_unit_id": consumer_unit_id.id,
                "isValid": True,
                "generatedOn": datetime.now(),
                "currentContract_id": contract.id,
                "errors": errors,
                "warnings": warnings,
                "dates": dates_list,
                "shouldRenewContract": costs_ratio > settings.MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION,
                "energyBillsCount": energy_bills_count,
                "nominalSavingsPercentage": nominal_savings_percentage,
                "tariffStartDate": blue.start_date,
                "tariffEndDate": blue.end_date,
                "recommendedContract": {
                    "subgroup": contract.subgroup,
                    "tariffFlag": recommendation.tariff_flag,
                    "offPeakDemandInKw": float(recommendation.off_peak_demand_in_kw),
                    "peakDemandInKw": float(recommendation.peak_demand_in_kw),
                },
                "costsComparisonPlot": {
                    "date": serializeSeries(costs_comparison["date"], "date"),
                    "totalCostInReaisInRecommended": serializeSeries(
                        costs_comparison["total_cost_in_reais_in_recommended"], "total_cost_in_reais_in_recommended"
                    ),
                    "totalCostInReaisInCurrent": serializeSeries(
                        costs_comparison["total_cost_in_reais_in_current"], "total_cost_in_reais_in_current"
                    ),
                    "totalTotalCostInReaisInCurrent": costs_comparison["total_total_cost_in_reais_in_current"],
                    "totalTotalCostInReaisInRecommended": (
                        costs_comparison["total_total_cost_in_reais_in_recommended"]
                    ),
                },
                "contractsComparisonTotals": {
                    "absoluteDifference": totals["absolute_difference"],
                    "consumptionCostInReaisInRecommended": totals["consumption_cost_in_reais_in_recommended"],
                    "demandCostInReaisInRecommended": totals["demand_cost_in_reais_in_recommended"],
                    "totalCostInReaisInRecommended": totals["total_cost_in_reais_in_recommended"],
                    "consumptionCostInReaisInCurrent": totals["consumption_cost_in_reais_in_current"],
                    "demandCostInReaisInCurrent": totals["demand_cost_in_reais_in_current"],
                    "totalCostInReaisInCurrent": totals["total_cost_in_reais_in_current"],
                },
                "currentContractCostsPlot": {
                    "consumptionCostInReais": serializeSeries(
                        current_contract_costs["consumption_cost_in_reais"], "consumption_cost_in_reais"
                    ),
                    "demandCostInReais": serializeSeries(
                        current_contract_costs["demand_cost_in_reais"], "demand_cost_in_reais"
                    ),
                },
                "detailedContractsCostsComparisonPlot": detailed_contracts_costs_comparison,
                "currentTotalCost": current_total_cost,
            },
        )

        return recommendation_instance, created


def get_recommendation(consumer_unit_id):
    try:
        recommendation = Recommendation.objects.get(consumer_unit_id=consumer_unit_id)
    except Recommendation.DoesNotExist:
        recommendation = None
    return recommendation
