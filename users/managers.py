from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from utils.user.authentication import generate_random_password
from utils.user.user_type_util import UserType

from . import models


class CustomUserManager(BaseUserManager):
    def create(self, email, password=None, **extra_fields):
        from .authentications import Password

        try:
            if not email:
                raise ValueError(_("Email is required"))

            is_seed_user = extra_fields.pop("is_seed_user", False)
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)

            if not user.type:
                user.type = UserType.get_user_type_by_model(self.model)

            UserType.is_valid_user_type(user.type, self.model)

            if settings.ENVIRONMENT in ["production", "development"]:
                if user.type in models.CustomUser.university_user_types and not is_seed_user:
                    user.set_password(generate_random_password())
                    user.save()

                    Password.send_email_first_access_password(user)
                else:
                    user.set_password(password)
                    user.save()
            else:
                user.set_password(password)
                user.save()

            return user
        except Exception as error:
            raise Exception(f"Error Create User: {str(error)}")

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("type", models.CustomUser.super_user_type)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create(email, password, **extra_fields)
