from datetime import date

from dateutil.relativedelta import relativedelta

from contracts.models import EnergyBill
from utils.energy_bill_util import EnergyBillUtils


class Recommendation:
    @classmethod
    def get_energy_bills_for_recommendation(cls, consumer_unit_id):
        energy_bills = []

        try:
            date_for_recommendation = Recommendation.set_date_for_recommendation(consumer_unit_id)
            energy_bills_dates = EnergyBillUtils.generate_dates_for_recommendation(date_for_recommendation)

            for energy_bill_object in energy_bills_dates:
                energy_bill = EnergyBill.get_energy_bill(
                    consumer_unit_id, energy_bill_object["month"], energy_bill_object["year"]
                )

                if energy_bill:
                    energy_bill_object["energy_bill"] = EnergyBillUtils.energy_bill_dictionary(energy_bill)

                energy_bills.append(energy_bill_object)

            return energy_bills
        except Exception as e:
            raise Exception(f"Error get energy bills for recommendation: {str(e)}") from e

    @classmethod
    def get_all_energy_bills_by_consumer_unit(cls, consumer_unit_id, start_date):
        try:
            date_for_recommendation = Recommendation.set_date_for_recommendation(consumer_unit_id)

            energy_bills_recommendation_dates_list = EnergyBillUtils.generate_dates_for_recommendation(
                date_for_recommendation
            )
            energy_bills_lists = EnergyBillUtils.generate_dates(start_date, date.today())

            for years in energy_bills_lists:
                for energy_bill_object in energy_bills_lists[str(years)]:
                    energy_bill = EnergyBill.get_energy_bill(
                        consumer_unit_id, energy_bill_object["month"], energy_bill_object["year"]
                    )

                    is_date_be_on_recommendation_list = EnergyBillUtils.is_date_be_on_recommendation_list(
                        energy_bills_recommendation_dates_list, energy_bill_object
                    )

                    if energy_bill:
                        energy_bill_object["energy_bill"] = EnergyBillUtils.energy_bill_dictionary(energy_bill)
                        energy_bill_object["is_energy_bill_pending"] = False
                    else:
                        energy_bill_object["is_energy_bill_pending"] = is_date_be_on_recommendation_list

                    energy_bill_object["month"] -= 1

            return energy_bills_lists
        except Exception as e:
            raise Exception(f"Error get all energy bills by consumer unit: {str(e)}") from e

    @classmethod
    def set_date_for_recommendation(cls, consumer_unit_id):
        date_for_recommendation = date.today()

        current_energy_bill = EnergyBill.get_energy_bill(
            consumer_unit_id, date_for_recommendation.month, date_for_recommendation.year
        )

        if current_energy_bill:
            date_for_recommendation += relativedelta(months=1)

        return date_for_recommendation
