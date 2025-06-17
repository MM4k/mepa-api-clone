from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

DEBUG = True
ALLOWED_HOSTS = []


# APPS
# -------------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

EXTERNAL_APPS = [
    "corsheaders",
    "drf_yasg",
    "rest_framework",
    "rest_framework.authtoken",
    "easyaudit",
]

LOCAL_APPS = [
    "contracts",
    "global_search_recommendation",
    "recommendation",
    "tariffs",
    "users",
    "universities",
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS


# TEMPLATES
# -------------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# MIDDLEWARE
# -------------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]


# GENERAL
# -------------------------------------------------------------------------------------
ROOT_URLCONF = "mec_energia.urls"
WSGI_APPLICATION = "mec_energia.wsgi.application"
AUTH_USER_MODEL = "users.CustomUser"

APPEND_SLASH = True
LOGIN_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# PASSWORD VALIDATORS
# -------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# INTERNATIONALIZATION
# -------------------------------------------------------------------------------------
TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "en-us"

USE_I18N = True
USE_L10N = True
USE_TZ = False


# STATIC FILES & MEDIA FILES (CSS, JavaScript, Images)
# -------------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


# DJANGO REST FRAMEWORK
# -------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.auth.UniversityUserTokenAuthentication",
        "users.auth.UniversityUserSessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}


# EASYAUDIT
# -------------------------------------------------------------------------------------
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True


# LOGGING
# -------------------------------------------------------------------------------------
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)-8s: %(message)s",
        },
        "middle": {
            "format": "%(module)-12s: [line: %(lineno)-3s] %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "verbose": {
            "format": "%(asctime)-15s | %(levelname)-8s | %(filename)-15s | line:%(lineno)-3s | %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "django_logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,  # 5 files = 50MB total
            "formatter": "verbose",
        },
        "apps_logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "apps.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,  # 5 files = 50MB total
            "formatter": "verbose",
        },
        "uc_sheet_logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "uc_sheet.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,  # 5 files = 50MB total
            "formatter": "verbose",
        },
        "tasks": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "tasks.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "formatter": "middle",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "django_logfile"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "django_logfile"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["django_logfile"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "apps_logfile"],
            "level": "INFO",
            "propagate": False,
        },
        "uc_sheet": {
            "handlers": ["console", "uc_sheet_logfile"],
            "level": "INFO",
            "propagate": False,
        },
        "tasks": {
            "handlers": ["console", "tasks"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# MEC ENERGIA
# -------------------------------------------------------------------------------------
# Parâmetros de recomendação de contrato
MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION = 6
IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION = 12
MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION = 0.05

# Valor de demanda mínimo na nova resolução
NEW_RESOLUTION_MINIMUM_DEMAND = 30

MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS = "definir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET = "redefinir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET = "definir-senha"
