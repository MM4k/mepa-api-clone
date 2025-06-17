from django.conf import settings
from rest_framework.routers import DefaultRouter

from global_search_recommendation.views import GlobalSearchRecommendationViewSet
from recommendation.views import RecommendationViewSet
from recommendation_commons.recommendation_settings import RecommendationSettings

router = DefaultRouter()

router.register(
    r"recommendation",
    GlobalSearchRecommendationViewSet if settings.RECOMMENDATION_METHOD == "global-search" else RecommendationViewSet,
    basename="recommendation",
)
router.register(r"recommendation-settings", RecommendationSettings, basename="recommendation-settings")

if settings.ENVIRONMENT != "production":
    router.register(
        r"global-search-recommendation",
        GlobalSearchRecommendationViewSet,
        basename="global-search-recommendation",
    )
    router.register(r"percentile-recommendation", RecommendationViewSet, basename="percentile-recommendation")
