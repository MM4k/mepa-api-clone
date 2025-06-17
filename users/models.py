from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from universities.models import ConsumerUnit, University

from .managers import CustomUserManager


class UserTokenManager(models.Manager):
    def valid_tokens(self):
        expiration_time = timezone.now() - timedelta(minutes=settings.RESET_PASSWORD_TOKEN_TIMEOUT)
        return self.filter(created_at__gt=expiration_time)

    def get_user_users_waiting_to_send_email(self):
        expiration_time = timezone.now() - timedelta(minutes=settings.RESEND_EMAIL_RESET_PASSWORD_TIMEOUT)
        tokens = self.filter(invalid_tried_at__lte=expiration_time)
        return CustomUser.objects.filter(id__in=tokens.values_list("user_id", flat=True))


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invalid_tried_at = models.DateTimeField(null=True, blank=True)

    objects = UserTokenManager()

    @property
    def is_valid_token(self):
        expiration_time = self.created_at + timedelta(minutes=settings.RESET_PASSWORD_TOKEN_TIMEOUT)
        return timezone.now() < expiration_time

    def set_invalid_tried_datetime_to_send_new_email(self):
        if not self.invalid_tried_at:
            self.invalid_tried_at = timezone.now()
            self.save()

    @classmethod
    def get_user_by_token(cls, token):
        try:
            user_token = UserToken.objects.get(token=token)
            if not user_token.is_valid_token:
                raise Exception("Token inválido")

            return user_token.user
        except UserToken.DoesNotExist:
            raise Exception("Token inválido")

    @classmethod
    def get_user_by_token_and_set_invalid_tried(cls, token):
        from .authentications import CODE_PASSWORD_TOKEN_EXPIRED, CODE_PASSWORD_TOKEN_OK

        try:
            user_token = UserToken.objects.get(token=token)

            if user_token.user.account_password_status == "OK":
                raise Exception("Usuário já tem uma senha de acesso")

            if user_token.is_valid_token:
                return user_token.user, CODE_PASSWORD_TOKEN_OK
            else:
                user_token.set_invalid_tried_datetime_to_send_new_email()

                return user_token.user, CODE_PASSWORD_TOKEN_EXPIRED

        except UserToken.DoesNotExist:
            raise Exception("Token não existe ou já utilizado")

    @classmethod
    def get_enable_user_token_by_user(cls, user):
        valid_token = cls.objects.valid_tokens().filter(user=user)
        return valid_token.exists()


class CustomUser(AbstractUser):
    class Type(models.TextChoices):
        SUPER_USER = "super_user", _("super_user")
        UNIVERSITY_ADMIN = "university_admin", _("university_admin")
        UNIVERSITY_USER = "university_user", _("university_user")
        UNIVERSITY_GUEST = "university_guest", _("university_guest")

    class PasswordStatus(models.TextChoices):
        OK = "OK", _("OK")
        FIRST_ACCESS = "first_access", _("first_access")
        ADMIN_RESET = "admin_reset", _("admin_reset")
        USER_RESET = "user_reset", _("user_reset")

    super_user_type = Type.SUPER_USER
    university_admin_user_type = Type.UNIVERSITY_ADMIN
    university_user_type = Type.UNIVERSITY_USER
    university_guest_type = Type.UNIVERSITY_GUEST

    all_user_types = [super_user_type, university_admin_user_type, university_user_type, university_guest_type]
    university_user_types = [super_user_type, university_admin_user_type, university_user_type, university_guest_type]

    user_types = Type.choices
    password_status = PasswordStatus.choices

    username = None

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(_("Email"), unique=True, null=False)

    type = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        choices=user_types,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    account_password_status = models.CharField(
        default=PasswordStatus.OK,
        max_length=25,
        null=False,
        blank=False,
        choices=password_status,
    )

    objects = CustomUserManager()

    @property
    def have_reset_password_token_enable(self) -> bool:
        return UserToken.get_enable_user_token_by_user(user=self)

    @property
    def is_admin(self):
        return self.type == CustomUser.Type.SUPER_USER

    @property
    def is_manager(self):
        return self.type == CustomUser.Type.UNIVERSITY_ADMIN

    @property
    def is_operational(self):
        return self.type == CustomUser.Type.UNIVERSITY_USER

    @property
    def is_guest(self):
        return self.type == CustomUser.Type.UNIVERSITY_GUEST

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} [{self.email}]"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def change_user_password(self, current_password, new_password):
        if not self.check_password(current_password):
            raise Exception("Erro ao alterar senha: senha atual incorreta")
        self.set_password(new_password)
        self.save()

    @classmethod
    def search_user_by_id(cls, id):
        try:
            return cls.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Exception("User does not exist")

    @classmethod
    def search_user_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except ObjectDoesNotExist as error:
            raise error

    def change_user_password_by_reset_password_token(self, new_password, reset_password_token):
        from .authentications import Password

        try:
            Password._get_user_by_token(reset_password_token)
            self.set_password(new_password)
            self.save()
            return self
        except Exception as error:
            raise Exception(str(error))

    def set_account_password_status_to_ok(self):
        self.account_password_status = "OK"
        self.save()


class UniversityUser(CustomUser):
    university_admin_user_type = CustomUser.university_admin_user_type
    university_user_type = CustomUser.university_user_type

    favorite_consumer_units = models.ManyToManyField(ConsumerUnit, blank=True)
    university = models.ForeignKey(
        University,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Universidade",
        help_text=_("Um Usuário de Universidade deve estar ligado a uma Universidade"),
    )

    class Meta:
        verbose_name = _("University User")
        verbose_name_plural = _("University Users")

    def __str__(self):
        return self.email

    def add_or_remove_favorite_consumer_unit(self, consumer_unit_id: int | str, action: str):
        unit = ConsumerUnit.objects.get(pk=consumer_unit_id)

        if unit.university.id != self.university.id:
            raise Exception("Cannot add/remove consumer unit from another university")

        if action == "add":
            self.favorite_consumer_units.add(unit)
        elif action == "remove":
            self.favorite_consumer_units.remove(unit)
        else:
            raise Exception('"action" field must be "add" or "remove"')

    def get_user_favorite_consumer_units(self):
        return self.favorite_consumer_units.all()

    def check_if_consumer_unit_is_your_favorite(self, consumer_unit_id):
        favorite_consumer_units = self.get_user_favorite_consumer_units()

        if favorite_consumer_units.filter(id=consumer_unit_id):
            return True
        return False

    def change_university_user_type(self, new_user_type):
        if new_user_type not in CustomUser.university_user_types:
            raise Exception("New University User type does not exist")

        if self.type not in CustomUser.university_user_types:
            raise Exception("User is not User University")

        if self.type == CustomUser.university_admin_user_type:
            admin_university_users = UniversityUser.objects.all().filter(
                university=self.university, type=CustomUser.university_admin_user_type
            )

            if len(admin_university_users) == 1:
                raise Exception("This User is the last Admin University User")

        self.type = new_user_type
        self.save()
