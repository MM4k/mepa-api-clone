from django.contrib import admin

from tariffs.models import Distributor, Tariff


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "is_in_new_resolution",
        "university",
    )
    search_fields = ("name",)
    list_filter = ("university", "is_active", "is_in_new_resolution")
    ordering = ("university", "name", "is_active")


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        "distributor",
        "subgroup",
        "flag",
        "start_date",
        "end_date",
    )
    search_fields = ("distributor",)
    ordering = ("distributor", "start_date", "end_date")
    list_filter = ("distributor", "flag", "subgroup")
