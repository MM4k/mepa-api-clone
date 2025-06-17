from datetime import datetime

from numpy import nan
from pandas import DataFrame

from recommendation_commons.recommendation_result import RecommendationResult


def __formatted_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d").date()


def fill_history_with_pending_dates(consumption_history: DataFrame, pending_bills_dates: list[str]):
    """FIXME: função temporária"""
    history_len = len(consumption_history)
    for i, date in enumerate(pending_bills_dates):
        consumption_history.loc[history_len + i] = [
            __formatted_date(date),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
    consumption_history.replace({nan: None}, inplace=True)
    consumption_history.sort_values(by="date", inplace=True)


def fill_with_pending_dates(
    recommendation: RecommendationResult,
    consumption_history: DataFrame,
    pending_bills_dates: list[str],
) -> None:
    """Essa função deve ser executada DEPOIS de
    `RecommendationCalculator.calculate()` porque `RecommendationCalculator`
    não foi feito pra lidar com buracos em `consumption_history`.

    NOTE: Pra entender a quantidade de itens em frame.loc[history_len+i] = [...]
    e o que eles são você deve consultar os HEADERS do respectivo dataframe
    em `calculator.py`."""

    history_len = len(consumption_history)
    for i, date in enumerate(pending_bills_dates):
        consumption_history.loc[history_len + i] = [
            __formatted_date(date),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
    consumption_history.replace({nan: None}, inplace=True)
    consumption_history.sort_values(by="date", inplace=True)

    peak_demand_in_kw = recommendation.frame.peak_demand_in_kw[0]
    off_peak_demand_in_kw = recommendation.frame.off_peak_demand_in_kw[0]
    for i, date in enumerate(pending_bills_dates):
        recommendation.frame.loc[history_len + i] = [
            __formatted_date(date),
            peak_demand_in_kw,
            off_peak_demand_in_kw,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
    recommendation.frame.replace({nan: None}, inplace=True)
    recommendation.frame.sort_values(by="date", inplace=True)

    for i, date in enumerate(pending_bills_dates):
        recommendation.current_contract.loc[history_len + i] = [
            __formatted_date(date),
            None,
            None,
            None,
            None,
            None,
        ]
    recommendation.current_contract.replace({nan: None}, inplace=True)
    recommendation.current_contract.sort_values(by="date", inplace=True)
