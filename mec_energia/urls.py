from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from contracts.urls import router as contracts_router
from recommendation_commons.urls import router as recommendation_router
from tariffs.urls import router as tariffs_router
from universities.urls import router as universities_router
from users.authentications import (
    Authentication,
    ConfirmResetPassword,
    Logout,
    ResetPassword,
    ResetPasswordByAdmin,
)
from users.urls import router as users_router

from .schema import Schema
from .views import ClearCacheView

router = DefaultRouter()
router.registry.extend(universities_router.registry)
router.registry.extend(contracts_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(tariffs_router.registry)
router.registry.extend(recommendation_router.registry)

schema_view = Schema.get_schema_view()

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    path("api/admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", Authentication.as_view()),
    path("api/token/logout/", Logout.as_view()),
    path("api/reset-password-admin/", ResetPasswordByAdmin.as_view()),
    path("api/reset-password/", ResetPassword.as_view()),
    path("api/reset-password/confirm", ConfirmResetPassword.as_view()),
    path("api/", include(router.urls), name="api-root"),
    path("api/swagger/schema/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/clear-cache/", ClearCacheView.as_view(), name="clear_cache"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
