from .common import *  # noqa
from .common import TEMPLATES, INSTALLED_APPS, MIDDLEWARE


DEBUG = True
ENVIRONMENT = "test"
SECRET_KEY = "django-insecure-#123!@#$%^&*()_+"

TEST_RUNNER = "django.test.runner.DiscoverRunner"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

TEMPLATES[0]["OPTIONS"]["debug"] = True
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_URL = "http://media.testserver"


# MEPA_FRONT_END_URL = "http://localhost:3000"
RECOMMENDATION_METHOD = "percentile"


# APPS - Remove unnecessary apps
# --------------------------------------------------------------------------------------
apps_to_remove = {
    "django.contrib.postgres",
    "drf_yasg",
    "easyaudit",
    "corsheaders",
}
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in apps_to_remove]


# MIDDLEWARE - Remove unnecessary middleware
# --------------------------------------------------------------------------------------
middleware_to_remove = {
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
}
MIDDLEWARE = [m for m in MIDDLEWARE if m not in middleware_to_remove]


# EASYAUDIT - Disable all audit events
# -------------------------------------------------------------------------------------
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False


# DATABASE - Use SQLite in-memory database
# --------------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# CACHE - Use mock cache for testing
# --------------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "tests.test_mock_cache.MockCacheTest",
        "LOCATION": "",
    },
}


# REST FRAMEWORK - Simplified configuration
# --------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


# LOGGING - Minimal configuration
# --------------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
    "django.db.backends": {
        "handlers": ["console"],
        "level": "DEBUG",  # Temporariamente para debug
        "propagate": False,
    },
}

# STATIC FILES
# --------------------------------------------------------------------------------------
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
