from django.conf import settings


class RecommendationUtils:
    @classmethod
    def generate_dates_for_recommendation(cls, date):
        energy_bills_list = []
        month = date.month - 1
        year = date.year

        for _ in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bills_list, month, year = cls.update_date_and_insert_energy_bill_on_list(
                energy_bills_list,
                month,
                year,
            )

        return energy_bills_list

    @classmethod
    def update_date_and_insert_energy_bill_on_list(cls, energy_bills_list, month, year):
        energy_bill, month, year = cls.create_energy_bill_date(month, year)
        energy_bills_list.append(energy_bill)
        return (energy_bills_list, month, year)

    @classmethod
    def create_energy_bill_date(cls, month, year):
        month, year = (month - 1, year) if month != 1 else (12, year - 1)
        energy_bill = {"month": month, "year": year, "energy_bill": None}
        return (energy_bill, month, year)
