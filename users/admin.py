# admin.py
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from users.models import CustomUser, UniversityUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return bool(request.user.is_superuser)

    def has_change_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

    list_display = (
        "email",
        "get_full_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_on",
    )
    list_filter = ("type", "is_active")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("created_on",)
    ordering = ("-created_on",)

    actions = [
        "activate_users",
        "deactivate_users",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "user_permissions")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    get_full_name.short_description = "Full Name"

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} usuários foram ativados com sucesso.", messages.SUCCESS)

    activate_users.short_description = "Ativar usuários selecionados"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} usuários foram desativados com sucesso.",
            messages.SUCCESS,
        )

    deactivate_users.short_description = "Desativar usuários selecionados"


@admin.register(UniversityUser)
class UniversityUserAdmin(CustomUserAdmin):
    list_display = (
        "email",
        "get_full_name",
        "is_active",
        "type",
        "university",
        "get_password_status",
        "get_favorite_units_count",
        "created_on",
    )
    list_filter = CustomUserAdmin.list_filter + ("university",)
    search_fields = CustomUserAdmin.search_fields + ("university__name",)

    fieldsets = (
        (None, {"fields": ("email", "password", "is_active")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("University Info", {"fields": ("university", "type", "account_password_status")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "university",
                    "type",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_password_status(self, obj):
        if obj.account_password_status == "OK":
            return format_html('<span style="color: green;">✓ OK</span>')
        elif obj.account_password_status == "first_access":
            return format_html('<span style="color: orange;">✓ First Access</span>')
        else:
            return format_html(f'<span style="color: red;">✗ {obj.account_password_status} </span>')

    get_password_status.short_description = "Password Status"
    get_password_status.admin_order_field = "account_password_status"

    def get_favorite_units_count(self, obj):
        count = obj.favorite_consumer_units.count()
        return format_html(
            '<a href="{}?user_id={}">{} unidades</a>',
            reverse("admin:universities_consumerunit_changelist"),
            obj.id,
            count,
        )

    get_favorite_units_count.short_description = "Favorite Consumer Units"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("university",)
        return self.readonly_fields
