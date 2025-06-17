import pytest

from rest_framework.test import APIClient

from tests.test_utils import create_objects_test_utils, dicts_test_utils
from universities.models import University
from users.models import CustomUser, UniversityUser

ENDPOINT = "/api/university-user/"
TOKEN_ENDPOINT = "/api/token/"
ENDPOINT_UNIVERSITY = "/api/universities/"


@pytest.mark.django_db
class TestUniversityPermissions:
    def setup_method(self):
        self.client = APIClient()
        self.university = University(name="UnB", cnpj="00038174000143")
        self.university.save()
        self.email_super_user = "admin@admin.com"
        self.email_university_admin_user = "arnold@user.com"
        self.email_university_user = "ronnie@user.com"

        self.super_user_dict = dicts_test_utils.super_user_dict_1
        self.super_user = create_objects_test_utils.create_test_super_user(self.super_user_dict)
        self.university_admin_user_dict = dicts_test_utils.university_user_dict_1
        self.university_admin_user = create_objects_test_utils.create_test_university_admin_user(
            self.university_admin_user_dict, self.university
        )

        self.university_user_dict = dicts_test_utils.university_user_dict_2
        self.university_user = create_objects_test_utils.create_test_university_user(
            self.university_user_dict, self.university
        )

    def test_super_user_already_created(self):
        assert type(self.super_user) is CustomUser
        assert self.super_user.email == self.email_super_user
        assert self.super_user.type == CustomUser.super_user_type

    def test_university_admin_user_already_created(self):
        assert type(self.university_admin_user) is UniversityUser
        assert self.university_admin_user.email == self.email_university_admin_user
        assert self.university_admin_user.university == self.university
        assert self.university_admin_user.type == CustomUser.university_admin_user_type

    def test_university_user_already_created(self):
        assert type(self.university_user) is UniversityUser
        assert self.university_user.email == self.email_university_user
        assert self.university_user.university == self.university
        assert self.university_user.type == CustomUser.university_user_type
