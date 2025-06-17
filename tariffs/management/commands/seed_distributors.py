import os
import re

import pandas as pd

from django.core.management.base import BaseCommand

from tariffs.models import Distributor
from universities.models import University

CURRENT_DIR = os.path.dirname(__file__)
DISTRIBUTORS_SHEET_PATH = os.path.join(CURRENT_DIR, "../distributors.csv")


class Command(BaseCommand):
    def handle(self, **options):
        print(f" Seeding distributors using: {DISTRIBUTORS_SHEET_PATH}")

        distributors = pd.read_csv(DISTRIBUTORS_SHEET_PATH)
        Distributor.objects.bulk_create(
            [
                Distributor(
                    name=dist["name"],
                    cnpj=re.sub(r"[^0-9]", "", dist["cnpj"]),
                    university=University.objects.get(pk=dist["university_id"]),
                )
                for _, dist in distributors.iterrows()
            ]
        )
        print("  Done.")
