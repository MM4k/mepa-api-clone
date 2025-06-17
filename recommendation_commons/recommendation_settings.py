from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from recommendation_commons.serializers import RecommendationSettingsSerializerForDocs


class RecommendationSettings(ViewSet):
    http_method_names = ["get"]

    @swagger_auto_schema(responses={200: RecommendationSettingsSerializerForDocs()})
    def list(self, _):
        config = {
            "MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION": settings.MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION,
            "IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION": settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION,
            "MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION": settings.MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION,  # noqa
            "METHOD": settings.RECOMMENDATION_METHOD,
        }

        return Response(config)
