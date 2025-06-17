import logging

from datetime import datetime
from pathlib import Path

import arrow

DATE_FORMAT = ["MMM/YYYY", "MM/YYYY", "MMM/YY", "DD/MM/YYYY", "YYYY-MM-DD", "YYYY-MM"]
logger = logging.getLogger("uc_sheet")


class ContractUtils:
    def validate_date(self, energy_bill_date):
        if isinstance(energy_bill_date, datetime):
            return energy_bill_date.date()
        try:
            date_obj = arrow.get(
                energy_bill_date,
                DATE_FORMAT,
                locale="pt_br",
            )
        except Exception:
            logger.error(f"Invalid date received: {energy_bill_date}")
            return energy_bill_date

        return date_obj.date()

    def check_file_extension(self, file_name):
        return Path(file_name).suffix[1:].lower()
