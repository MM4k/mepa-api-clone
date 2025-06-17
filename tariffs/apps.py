from django.apps import AppConfig


class TariffsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tariffs"

    def ready(self):
        import tariffs.signals  # noqa F401
