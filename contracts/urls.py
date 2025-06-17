from django.urls import include, path
from rest_framework.routers import DefaultRouter

from contracts import views

router = DefaultRouter()
router.register(r"contracts", views.ContractViewSet)
router.register(r"energy-bills", views.EnergyBillViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("CSV/upload/", views.EnergyBillViewSet.upload_csv, name="upload_csv"),
]
