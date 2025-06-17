from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


class Schema:
    @staticmethod
    def get_schema_view():
        return swagger_get_schema_view(
            openapi.Info(
                title="Mec Energia API",
                default_version="1.0.0",
                description="Mec Energia: API documentation",
            ),
            public=True,
        )
