import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("ENVIRONMENT", "production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"mec_energia.settings.{environment}")

application = get_wsgi_application()
