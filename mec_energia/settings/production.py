import environ

from .common import *  # noqa
from .common import BASE_DIR, LOGGING

env = environ.Env()
ENV_FILE = BASE_DIR / ".envs" / ".env.prod"
env.read_env(ENV_FILE)

SITE_NAME = "MEPA - Monitoramento de Energia em Plataforma Aberta"
ADMIN_URL = env("DJANGO_ADMIN_URL", default="management/")

ENVIRONMENT = env("ENVIRONMENT")
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)

LOG_LEVEL = env("LOG_LEVEL", default="ERROR")
LOGGING["loggers"]["django"]["level"] = LOG_LEVEL
LOGGING["loggers"]["apps"]["level"] = LOG_LEVEL

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS")

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "content-disposition",
    "accept-encoding",
    "content-type",
    "accept",
    "origin",
    "authorization",
]


# REDIS CACHES
# -------------------------------------------------------------------------------------
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

DATABASES["default"]["ATOMIC_REQUESTS"] = env.bool("POSTGRES_ATOMIC_REQUESTS", default=False)
DATABASES["default"]["CONN_MAX_AGE"] = env.int("POSTGRES_CONN_MAX_AGE", default=300)


# MEC ENERGIA
# -------------------------------------------------------------------------------------
MEPA_FRONT_END_URL = env("FRONT_END_URL")
RECOMMENDATION_METHOD = env("RECOMMENDATION_METHOD")

# Password reset
RESET_PASSWORD_TOKEN_TIMEOUT = env.int("RESET_PASSWORD_TOKEN_TIMEOUT")
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = env.int("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT")

# Configurações do servidor SMTP
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
