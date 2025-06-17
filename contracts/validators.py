import csv
import logging

from io import TextIOWrapper

import pandas as pd

from django.utils.deconstruct import deconstructible
from rest_framework import serializers

from contracts.utils import ContractUtils

logger = logging.getLogger("uc_sheet")


@deconstructible
class CsvFileValidator:
    def __init__(self):
        self.allowed_extensions = ["csv", "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]

    def __call__(self, value):
        df = self._validate_file_extensions(ContractUtils().check_file_extension(value.name), value)
        return self._validate_headers(df)

    def _validate_file_extensions(self, file_extension, file):
        if file_extension not in self.allowed_extensions:
            raise serializers.ValidationError(
                f"Invalid file type '.{file_extension}'. Only CSV and XLSX files are accepted."
            )

        df = {}
        if file_extension == "csv":
            decoded_file = TextIOWrapper(file.file, encoding="utf-8")
            delimiter = self._get_csv_delimiter(decoded_file)
            if delimiter not in [",", ";"]:
                logger.error(f"Invalid csv delimiter {delimiter}. Only ; and , are accepted")
                raise serializers.ValidationError(f"Invalid csv delimiter {delimiter}. Only ; and , are accepted")
            try:
                df = pd.read_csv(decoded_file, sep=delimiter, decimal=",", header=1)
            except Exception as exc:
                logger.error(f"Invalid csv file: {exc}")
                raise serializers.ValidationError("Invalid csv file: ", exc)
        else:
            try:
                df = pd.read_excel(file, decimal=",", header=1)

            except Exception as exc:
                logger.error(f"Invalid excel file: {exc}")
                raise serializers.ValidationError("Invalid excel file: ", exc)
        return df

    def _validate_headers(self, df):
        translation_dict = {
            "Data": "date",
            "Valor (R$)": "invoice_in_reais",
            "Consumo Ponta (kWh)": "peak_consumption_in_kwh",
            "Consumo Fora Ponta (kWh)": "off_peak_consumption_in_kwh",
            "Demanda Ponta (kW)": "peak_measured_demand_in_kw",
            "Demanda Fora Ponta (kW)": "off_peak_measured_demand_in_kw",
        }

        try:
            df.rename(columns=translation_dict, inplace=True, errors="raise")
        except KeyError as e:
            logger.error(f"{e}")
            raise serializers.ValidationError(f"{e}")
        return df.to_dict(orient="records")

    def _get_csv_delimiter(self, decoded_file):
        decoded_file.seek(0)
        dialect = csv.Sniffer().sniff(decoded_file.read())
        decoded_file.seek(0)
        return dialect.delimiter
