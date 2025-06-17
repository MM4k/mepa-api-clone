from django.contrib import admin

from universities.models import ConsumerUnit, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "acronym",
        "cnpj",
        "is_active",
        "created_on",
    )
    search_fields = ("name", "acronym", "cnpj")
    list_filter = ("is_active", "created_on")
    ordering = ("name", "acronym", "cnpj", "is_active", "created_on")
    readonly_fields = ("created_on",)


@admin.register(ConsumerUnit)
class ConsumerUnitAdmin(admin.ModelAdmin):
    list_display = (
        "university",
        "code",
        "name",
        "is_active",
        "total_installed_power",
        "created_on",
    )
    search_fields = ("name", "code")
    ordering = ("university", "name", "code")
    list_filter = ("university", "is_active", "created_on")
