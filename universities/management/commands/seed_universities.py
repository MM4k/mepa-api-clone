import os
import re

import pandas as pd

from django.core.management.base import BaseCommand

from universities.models import University

CURRENT_DIR = os.path.dirname(__file__)
UNIVERSITIES_SHEET_PATH = os.path.join(CURRENT_DIR, "../universities.csv")


class Command(BaseCommand):
    def handle(self, **options):
        print(f" Seeding universities using: {UNIVERSITIES_SHEET_PATH}")

        universities = pd.read_csv(UNIVERSITIES_SHEET_PATH)
        University.objects.bulk_create(
            [
                University(
                    name=university["name"],
                    acronym=university["acronym"],
                    cnpj=re.sub(r"[^0-9]", "", university["cnpj"]),
                )
                for _, university in universities.iterrows()
            ]
        )

        print("  Done.")
