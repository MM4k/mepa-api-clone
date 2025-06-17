import environ

from .common import *  # noqa
from .common import BASE_DIR, INSTALLED_APPS, LOGGING, MIDDLEWARE, REST_FRAMEWORK

env = environ.Env()
ENV_FILE = BASE_DIR / ".envs" / ".env.test"
env.read_env(ENV_FILE)

ENVIRONMENT = env("ENVIRONMENT")
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", True)
TEST = env.bool("IS_TESTING", default=False)

LOG_LEVEL = env("LOG_LEVEL", default="INFO")
LOGGING["loggers"]["apps"]["level"] = LOG_LEVEL

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["mepa-api", "localhost", "127.0.0.1", "[::1]"],
)

CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=[
        "http://mepa-api:8000",
        "http://localhost:3001",
        "http://localhost:8000",
    ],
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=["http://localhost:3001"])


# BACKEND CACHE
# -------------------------------------------------------------------------------------
if TEST:
    CACHES = {
        "default": {
            "BACKEND": "tests.test_mock_cache.MockCacheTest",
            "LOCATION": "",
        },
    }

else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"


# DATABASES
# -------------------------------------------------------------------------------------
# database with in memory database for pytest.
if TEST:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
        }
    }


# STORAGE CONFIGURATION
# -------------------------------------------------------------------------------------
# WhiteNoise middleware should be placed directly after the Django SecurityMiddleware
if not TEST:
    index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
    MIDDLEWARE.insert(index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


# MEC ENERGIA
# -------------------------------------------------------------------------------------
MEPA_FRONT_END_URL = env("FRONT_END_URL")
RECOMMENDATION_METHOD = env("RECOMMENDATION_METHOD")

# Password reset
RESET_PASSWORD_TOKEN_TIMEOUT = env.int("RESET_PASSWORD_TOKEN_TIMEOUT")
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = env.int("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT")

# Configurações do servidor SMTP
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env.int("EMAIL_PORT", default=1025)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@seudominio.com")

# DJANGO EXTENSIONS
# -------------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]


# DEBUG TOOLBAR
# -------------------------------------------------------------------------------------
if not TEST:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
        "INTERCEPT_REDIRECTS": False,
        "ALLOWED_HOSTS": ["*"],
    }


# PYTEST SETTINGS
# -------------------------------------------------------------------------------------
if TEST:
    del REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    del REST_FRAMEWORK["DEFAULT_PARSER_CLASSES"]
    SOUTH_TESTS_MIGRATE = False

    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
