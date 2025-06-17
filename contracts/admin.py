from django.contrib import admin

from contracts.models import Contract, EnergyBill


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "get_consumer_unit_university",
        "distributor",
        "consumer_unit",
        "start_date",
        "end_date",
        "tariff_flag",
        "subgroup",
    )
    search_fields = ("consumer_unit", "distributor")
    list_filter = (
        "consumer_unit__university__acronym",
        "distributor",
        "tariff_flag",
        "end_date",
    )
    ordering = ("distributor", "start_date")

    def get_consumer_unit_university(self, obj):
        return obj.consumer_unit.university.acronym

    get_consumer_unit_university.short_description = "University"


@admin.register(EnergyBill)
class EnergyBillAdmin(admin.ModelAdmin):
    list_display = (
        "contract",
        "consumer_unit",
        "date",
        "invoice_in_reais",
        "peak_consumption_in_kwh",
        "off_peak_consumption_in_kwh",
        "energy_bill_file",
    )
    search_fields = ("contract", "consumer_unit")
    ordering = ("contract", "date")
    list_filter = ("contract", "consumer_unit")
