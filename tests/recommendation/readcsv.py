import json

from datetime import date
from os.path import join

import pandas as pd

from pandas import DataFrame

from recommendation.blue import BluePercentileCalculator, BlueTariff
from recommendation.calculator import (
    CONSUMPTION_HISTORY_HEADERS,
    ContractRecommendationCalculator,
    RecommendationCalculator,
)
from recommendation.green import GreenPercentileCalculator, GreenTariff

B_PERCENTILES = BluePercentileCalculator.PERCENTILES
B_PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
B_SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS
G_PERCENTILES = GreenPercentileCalculator.PERCENTILES
G_PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
G_SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS
RECOMENDATION_HEADERS = ContractRecommendationCalculator.HEADERS
CURRENT_CONTRACT_HEADERS = RecommendationCalculator.CURRENT_CONTRACT_HEADERS
SEP = "\t"


class CsvData:
    current_tariff_flag: str
    consumption_history: DataFrame
    blue_tariff: BlueTariff
    green_tariff: GreenTariff
    expected_recommended_tariff_flag: str
    expected_blue_percentiles: dict[str, DataFrame]
    expected_blue_percentiles_total_in_reais: dict[str, float]
    expected_green_percentiles_total_in_reais: dict[str, float]
    expected_green_percentiles: dict[str, DataFrame]
    expected_summary_scalar_values: dict[str, dict]
    expected_blue_summary: DataFrame
    expected_green_summary: DataFrame
    expected_current_contract: DataFrame
    expected_recommendation: DataFrame


class CsvReader:
    def __init__(self, uc_id: str):
        data_path = join("tests", "recommendation", "data")
        self.path = join(data_path, f"uc_{uc_id}")

    def run(self) -> CsvData:
        data = CsvData()
        data.consumption_history = self._read_consumption_history(CONSUMPTION_HISTORY_HEADERS)
        data.expected_blue_percentiles = self._read_expected_percentiles(
            "blue_per_%s.csv", B_PERCENTILES, B_PERCENTILE_HEADERS
        )
        expected_percentiles_total_in_reais = self._read_expected_percentiles_total_in_reais()
        data.expected_blue_percentiles_total_in_reais = expected_percentiles_total_in_reais["blue"]
        data.expected_green_percentiles_total_in_reais = expected_percentiles_total_in_reais["green"]
        data.expected_green_percentiles = self._read_expected_percentiles(
            "green_per_%s.csv", G_PERCENTILES, G_PERCENTILE_HEADERS
        )
        data.expected_summary_scalar_costs = self._read_expected_summary_scalar_costs()
        data.expected_blue_summary = self._read_expected_summary("blue", B_SUMMARY_HEADERS)
        data.expected_green_summary = self._read_expected_summary("green", G_SUMMARY_HEADERS)
        data.expected_recommendation = self._read_expected_recommendation(RECOMENDATION_HEADERS)
        data.expected_current_contract = self._read_expected_current_contract(CURRENT_CONTRACT_HEADERS)

        tariff = self._read_tariff()
        data.blue_tariff = BlueTariff(**tariff["blue"])
        data.green_tariff = GreenTariff(**tariff["green"])
        data.expected_recommended_tariff_flag = tariff["recommended_flag"]
        data.current_tariff_flag = tariff["current_flag"]
        return data

    def _read_expected_percentiles_total_in_reais(self):
        f = open(join(self.path, "per_total_in_reais.json"))
        total_in_reais = json.load(f)
        f.close()
        return {"blue": {**total_in_reais["blue"]}, "green": {**total_in_reais["green"]}}

    def _read_consumption_history(self, headers: list[str]) -> DataFrame:
        # FIXME: corrigir essa gambiarra com a coluna date
        _headers = headers.copy()
        _headers.remove("date")
        history = pd.read_csv(join(self.path, "consumption.csv"), sep=SEP, names=_headers)
        history.insert(0, "date", [date.today()] * len(history))
        return history

    def _read_expected_percentiles(
        self, filename_template: str, percentiles: list[float], percentile_headers: list[str]
    ) -> "dict[str, DataFrame]":
        expected_percentiles = {}
        for p in percentiles:
            p_str = str(p)
            frame = pd.read_csv(join(self.path, filename_template % p_str), sep=SEP, names=percentile_headers)
            expected_percentiles[p_str] = frame
        return expected_percentiles

    def _read_expected_summary_scalar_costs(self) -> dict:
        f = open(join(self.path, "summary_scalar_values.json"))
        scalar_costs = json.load(f)
        f.close()
        return scalar_costs

    def _read_expected_summary(self, flag: str, summary_headers: list[str]) -> DataFrame:
        return pd.read_csv(join(self.path, f"{flag}_per_summary.csv"), sep=SEP, names=summary_headers)

    def _read_tariff(self):
        f = open(join(self.path, "tariff.json"))
        tariff = json.load(f)
        f.close()
        return tariff

    def _read_expected_recommendation(self, headers: list[str]):
        _headers = headers.copy()
        _headers.remove("date")
        recommendation = pd.read_csv(join(self.path, "recommendation.csv"), names=_headers, sep=SEP)
        recommendation.insert(0, "date", [date.today()] * len(recommendation))
        return recommendation

    def _read_expected_current_contract(self, headers: list[str]):
        _headers = headers.copy()
        _headers.remove("date")
        contract = pd.read_csv(join(self.path, "current_contract.csv"), names=_headers, sep=SEP)
        contract.insert(0, "date", [date.today()] * len(contract))
        return contract
