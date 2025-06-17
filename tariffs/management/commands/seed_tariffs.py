import os

from datetime import datetime

import pandas as pd

from django.core.management.base import BaseCommand

from tariffs.models import Distributor, Tariff

CURRENT_DIR = os.path.dirname(__file__)
TARIFFS_SHEET_PATH = os.path.join(CURRENT_DIR, "../tariffs.xlsx")

COLUMNS = ["Sigla", "Início Vigência", "Fim Vigência", "Subgrupo", "Modalidade", "Posto", "Unidade", "TUSD", "TE"]


class Command(BaseCommand):
    def handle(self, **options):
        distributors = Distributor.objects.all()

        if len(distributors) == 0:
            print("Distributors registers not found!")
            return

        tariffs = pd.read_excel(TARIFFS_SHEET_PATH, usecols=COLUMNS, decimal=",", date_format="dd/MM/yyyy")
        tariffs["Fim Vigência"] = pd.to_datetime(tariffs["Fim Vigência"], format="%d/%m/%Y")
        today = datetime.today()
        tariffs = tariffs[tariffs["Fim Vigência"] > today]
        tariffs["Unidade"] = tariffs["Unidade"].str.replace("R$/", "")
        tariffs.replace("Não se aplica", "NA", inplace=True)

        for distributor in distributors:
            distributors_tariffs = tariffs[tariffs["Sigla"].str.lower() == distributor.name.lower()]
            if distributors_tariffs.empty:
                print(f"  Not found tariffs to distributor: {distributor.name}")

            sub_groups = distributors_tariffs["Subgrupo"].unique()
            for sg in sub_groups:
                sg_tariffs = distributors_tariffs[distributors_tariffs["Subgrupo"] == sg]
                tusd_g_row = sg_tariffs[sg_tariffs["Modalidade"] == "Geração"]
                tusd_g = 0 if tusd_g_row.empty else tusd_g_row["TUSD"].iloc[0]
                blue_tariffs = sg_tariffs[sg_tariffs["Modalidade"] == "Azul"]

                if not blue_tariffs.empty:
                    self.create_tariff(sg, distributor, Tariff.BLUE, blue_tariffs, tusd_g)

                green_tariffs = sg_tariffs[sg_tariffs["Modalidade"] == "Verde"]
                if not green_tariffs.empty:
                    self.create_tariff(sg, distributor, Tariff.GREEN, green_tariffs, tusd_g)

    def create_tariff(self, sg: str, distributor: Distributor, flag: str, tariffs, tusd_g):
        print(
            f" Creating subgroup {sg} "
            f"{'green' if flag == Tariff.GREEN else 'blue'} "
            f"tariff to distributor: {distributor.name}"
        )

        tariff = {
            "peak_tusd_in_reais_per_mwh": tariffs[(tariffs["Posto"] == "Ponta") & (tariffs["Unidade"] == "MWh")][
                "TUSD"
            ].iloc[0],
            "peak_te_in_reais_per_mwh": tariffs[(tariffs["Posto"] == "Ponta") & (tariffs["Unidade"] == "MWh")][
                "TE"
            ].iloc[0],
            "off_peak_tusd_in_reais_per_mwh": tariffs[
                (tariffs["Posto"] == "Fora ponta") & (tariffs["Unidade"] == "MWh")
            ]["TUSD"].iloc[0],
            "off_peak_te_in_reais_per_mwh": tariffs[
                (tariffs["Posto"] == "Fora ponta") & (tariffs["Unidade"] == "MWh")
            ]["TE"].iloc[0],
            "power_generation_tusd_in_reais_per_kw": tusd_g,
        }

        if flag == Tariff.GREEN:
            tariff.update(
                {
                    "na_tusd_in_reais_per_kw": tariffs[(tariffs["Posto"] == "NA") & (tariffs["Unidade"] == "kW")][
                        "TUSD"
                    ].iloc[0]
                }
            )
        else:
            tariff.update(
                {
                    "peak_tusd_in_reais_per_kw": 0
                    if sg == "A1"
                    else tariffs[(tariffs["Posto"] == "Ponta") & (tariffs["Unidade"] == "kW")]["TUSD"].iloc[0],
                    "off_peak_tusd_in_reais_per_kw": 0
                    if sg == "A1"
                    else tariffs[(tariffs["Posto"] == "Fora ponta") & (tariffs["Unidade"] == "kW")]["TUSD"].iloc[0],
                }
            )

        start_date = tariffs["Início Vigência"].iloc[0]
        end_date = tariffs["Fim Vigência"].iloc[0]

        Tariff.objects.create(
            subgroup=sg,
            distributor=distributor,
            flag=flag,
            **tariff,
            start_date=start_date,
            end_date=end_date,
        )
        print("  Done!")
