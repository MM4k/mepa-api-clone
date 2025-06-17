from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tariffs import views

router = DefaultRouter()

router.register(r"tariffs", views.TariffViewSet)
router.register(r"distributors", views.DistributorViewSet)
router.register(r"download-step-by-step-pdf", views.DownloadPDFViewSet, basename="download-pdf")

urlpatterns = [
    path("", include(router.urls)),
]
