from datetime import date

from django.conf import settings


class EnergyBillUtils:
    @classmethod
    def generate_dates_for_recommendation(cls, date):
        energy_bills_list = []
        month = date.month
        year = date.year

        for _ in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bills_list, month, year = cls.update_date_and_insert_energy_bill_on_list(
                energy_bills_list,
                month,
                year,
            )

        return energy_bills_list

    @classmethod
    def is_date_be_on_recommendation_list(cls, energy_bills_recommendation_dates_list, search_energy_bill_date):
        return search_energy_bill_date in energy_bills_recommendation_dates_list

    @classmethod
    def generate_dates(cls, start_date, end_date):
        years = {}
        month = end_date.month
        year = end_date.year
        start_date_year = start_date.year

        while year >= start_date_year:
            years[str(year)] = []
            start_month = 0

            if start_date.year == year:
                start_month = start_date.month - 1

            for i in range(12, start_month, -1):
                month = i
                date = cls.create_energy_bill_date(month, year)
                years[str(year)].append(date)

            year -= 1

        return years

    @classmethod
    def energy_bill_dictionary(cls, energy_bill):
        if energy_bill is None:
            return None

        return {
            "id": energy_bill.id,
            "date": energy_bill.date,
            "invoice_in_reais": energy_bill.invoice_in_reais,
            "is_atypical": energy_bill.is_atypical,
            "peak_consumption_in_kwh": energy_bill.peak_consumption_in_kwh,
            "off_peak_consumption_in_kwh": energy_bill.off_peak_consumption_in_kwh,
            "peak_measured_demand_in_kw": energy_bill.peak_measured_demand_in_kw,
            "off_peak_measured_demand_in_kw": energy_bill.off_peak_measured_demand_in_kw,
        }

    @classmethod
    def update_date_and_insert_energy_bill_on_list(cls, energy_bills_list, month, year):
        month, year = (month - 1, year) if month != 1 else (12, year - 1)
        energy_bill = cls.create_energy_bill_date(month, year)
        energy_bills_list.append(energy_bill)
        return (energy_bills_list, month, year)

    @classmethod
    def create_energy_bill_date(cls, month, year):
        return {"month": month, "year": year, "energy_bill": None}

    @classmethod
    def generate_latest_dates_for_recommendation(cls):
        energy_bills_list = []
        month = date.today().month
        year = date.today().year

        for _ in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @classmethod
    def generate_dates_by_year(cls, year):
        energy_bills_list = []

        month = 12
        year = year

        for _ in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @staticmethod
    def _create_energy_bill_date(month, year):
        energy_bill = {
            "month": month,
            "year": year,
        }

        month, year = (month - 1, year) if month != 1 else (12, year - 1)
        return (energy_bill, month, year)

    @classmethod
    def check_valid_consumption_demand(cls, energy_bill):
        off_peak_consumption = energy_bill.off_peak_consumption_in_kwh
        off_peak_measured_demand = energy_bill.off_peak_measured_demand_in_kw
        peak_consumption = energy_bill.peak_consumption_in_kwh
        peak_measured_demand = energy_bill.peak_measured_demand_in_kw

        ## retomar essa lógica quando retirar valores zerados do seed
        return True

        if (
            (off_peak_consumption and off_peak_consumption == 0)
            or (off_peak_measured_demand and off_peak_consumption == 0)
            or (peak_consumption and peak_consumption == 0)
            or (peak_measured_demand and peak_measured_demand == 0)
        ):
            return False
        return True
