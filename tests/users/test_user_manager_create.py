import pytest
from django.conf import settings
from users import models
from users.models import CustomUser, UniversityUser
from users.managers import CustomUserManager
from universities.models import University
from unittest.mock import patch


@pytest.mark.django_db
class TestUserManagerCreate:

    def setup_method(self):
        self.manager = CustomUserManager()
        self.manager.model = UniversityUser
        self.university = University.objects.create(name="Test University", acronym="TU")

        settings.MEPA_FRONT_END_URL = "http://fake-front-end.test"
        settings.RESET_PASSWORD_TOKEN_TIMEOUT = 30
        settings.RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = 10

    def test_create_user_with_valid_email_and_type_defined(self):
        """CT1 - Criar usuário com e-mail válido e tipo definido (ambiente production, não seed user)"""
        settings.ENVIRONMENT = "production"
        user = self.manager.create(
            email="user@fake.com",
            password="Password123!",
            type=CustomUser.Type.UNIVERSITY_USER,
            is_seed_user=False,
            university=self.university,
        )
        assert user.email == "user@fake.com"
        assert user.type == CustomUser.Type.UNIVERSITY_USER
        assert not user.check_password("Password123!")

    def test_create_user_in_test_environment(self):
        """CT2 - Criar usuário com tipo definido fora de production/development"""
        settings.ENVIRONMENT = "test"
        user = self.manager.create(
            email="user@fake.com",
            password="TestPassword",
            type=CustomUser.Type.UNIVERSITY_USER,
            is_seed_user=False
        )
        assert user.email == "user@fake.com"
        assert user.check_password("TestPassword")

    def test_create_university_user_as_seed_user(self):
        """CT3 - Criar usuário universitário, ambiente production, mas seed user"""
        settings.ENVIRONMENT = "production"
        user = self.manager.create(
            email="user@fake.com",
            password="SeedPassword",
            type=CustomUser.Type.UNIVERSITY_USER,
            is_seed_user=True,
            university=self.university,
        )
        assert user.email == "user@fake.com"
        assert user.check_password("SeedPassword")

    def test_create_user_without_type(self):
        """CT4 - Criar usuário sem tipo definido"""
        settings.ENVIRONMENT = "production"
        user = self.manager.create(
            email="user@fake.com",
            password="DefaultPassword",
            is_seed_user=False,
            university=self.university,
        )
        assert user.email == "user@fake.com"
        assert user.type in CustomUser.Type.values
        assert not user.check_password("DefaultPassword")

    def test_create_user_without_email(self):
        """CT5 - Chamar o método sem e-mail"""
        settings.ENVIRONMENT = "production"
        with pytest.raises(Exception) as exc_info:
            self.manager.create(
                email=None,
                password="AnyPassword",
                type=CustomUser.Type.UNIVERSITY_USER,
                is_seed_user=False,
                university=self.university,
            )
        assert "Email is required" in str(exc_info.value)

    def test_create_user_with_non_university_type(self):
        """CT6 - Criar usuário de outro tipo (não universitário)"""
        settings.ENVIRONMENT = "production"

        with patch.object(models.CustomUser, 'university_user_types', []):
            user = self.manager.create(
                email="admin@fake.com",
                password="AdminPassword",
                type=CustomUser.Type.SUPER_USER,
                is_seed_user=False,
            )

        assert user.email == "admin@fake.com"
        assert user.type == CustomUser.Type.SUPER_USER
        assert user.check_password("AdminPassword")
