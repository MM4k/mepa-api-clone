import json

from datetime import date

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils import create_objects_test_utils, dicts_test_utils
from universities.models import ConsumerUnit, University
from users.models import UniversityUser

TOKEN_ENDPOINT = "/api/token/"
ENDPOINT_UNIVERSITY = "/api/universities/"
ENDPOINT = "/api/university-user/"
ENDPOINT_USER_UNIVERSITY = "/api/university-user/"


@pytest.mark.django_db
class TestUsersEndpoint:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1
        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)
        self.super_user_dict = dicts_test_utils.super_user_dict_1
        self.super_user = create_objects_test_utils.create_test_super_user(self.super_user_dict)
        self.client = APIClient()
        self.client.login(email=self.super_user_dict["email"], password=self.super_user_dict["password"])

        self.consumer_units = []
        for i in range(3):
            self.consumer_units.append(
                ConsumerUnit(
                    id=i + 1,
                    name=f"UC {i + 1}",
                    code=f"{i + 1}",
                    university=self.university,
                    is_active=True,
                    created_on=date.today(),
                )
            )
        ConsumerUnit.objects.bulk_create(self.consumer_units)

    def test_university_user_already_created(self):
        assert type(self.user) is UniversityUser
        assert self.user.email == self.user_dict["email"]
        assert self.user.university == self.university

    def test_login_university_user_already_created(self):
        response = self.client.post(
            TOKEN_ENDPOINT,
            {
                "username": self.user_dict["email"],
                "password": self.user_dict["password"],
            },
        )

        assert status.HTTP_200_OK == response.status_code

    def test_endpoint_create_university_user(self):
        university_user_dict = dicts_test_utils.university_user_dict_2
        university_user_dict["university"] = self.university.id

        response = self.client.post(ENDPOINT_USER_UNIVERSITY, university_user_dict)
        assert status.HTTP_201_CREATED == response.status_code

        response_login_user = self.client.post(
            TOKEN_ENDPOINT,
            {
                "username": university_user_dict["email"],
                "password": university_user_dict["password"],
            },
        )
        assert status.HTTP_200_OK == response_login_user.status_code

    """
    def test_create_and_login_university_user_through_endpoints(self):
        university_user_dict = CreateObjectsUtil.get_university_user_dict(index = 2)
        university_user_dict['university'] = self.university.id

        response_create_user = self.client.post(ENDPOINT_USER_UNIVERSITY, university_user_dict)

        assert status.HTTP_201_CREATED == response_create_user.status_code

        json_response_create_user = json.loads(response_create_user.content)
        created_user = UniversityUser.objects.get(id = json_response_create_user['id'])

        assert type(created_user) == UniversityUser
        assert created_user.university.id == self.university.id

        response_login_user = self.client.post(TOKEN_ENDPOINT, {
                                "username": created_user.email,
                                "password": university_user_dict['password']
                            })

        logged_user = json.loads(response_login_user.content)

        assert status.HTTP_200_OK == response_login_user.status_code
        assert 'token' in logged_user
        assert 'university_id' in logged_user['user']
        assert logged_user['user']['email'] == created_user.email
        assert logged_user['user']['university_id'] == created_user.university.id """

    def test_university_user_starts_0_favorite_consumer_units(self):
        endpoint = f"{ENDPOINT}{self.user.id}/"
        favorite_consumer_units = self._get_user_as_response()
        assert 0 == favorite_consumer_units.count()

    def test_add_consumer_unit_to_favorite(self):
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"
        response = self._add_to_favorite_request(endpoint, self.consumer_units[0].id)
        assert status.HTTP_200_OK == response.status_code

        endpoint = f"{ENDPOINT}{self.user.id}/"
        favorite_consumer_units = self._get_user_as_response()
        assert 1 == favorite_consumer_units.count()

    def test_add_second_consumer_unit_to_favorite(self):
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"
        self._add_to_favorite_request(endpoint, self.consumer_units[0].id)
        self._add_to_favorite_request(endpoint, self.consumer_units[1].id)

        endpoint = f"{ENDPOINT}{self.user.id}/"
        favorite_consumer_units = self._get_user_as_response()
        assert 2 == favorite_consumer_units.count()

    def test_remove_second_consumer_unit_from_favorite(self):
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"

        self._add_to_favorite_request(endpoint, self.consumer_units[0].id)
        self._add_to_favorite_request(endpoint, self.consumer_units[1].id)
        self._remove_from_favorite_request(endpoint, self.consumer_units[1].id)

        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/"
        assert 1 == UniversityUser.objects.get(pk=self.user.id).favorite_consumer_units.count()

    def test_cannot_add_consumer_unit_from_unrelated_university_to_favorite(self):
        unrelated_university = University(name="UFMG", cnpj="17217985000104")
        unrelated_university.save()

        unit_from_unrelated_university = ConsumerUnit.objects.create(
            name="Unrelated UC", code="0", university=unrelated_university, is_active=True, created_on=date.today()
        )

        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"
        response = self._add_to_favorite_request(endpoint, unit_from_unrelated_university.id)

        assert status.HTTP_403_FORBIDDEN == response.status_code

        endpoint = f"{ENDPOINT}{self.user.id}/"
        favorite_consumer_units = self._get_user_as_response()
        assert 0 == favorite_consumer_units.count()

    def test_cannot_add_non_existing_consumer_unit_to_favorite(self):
        non_existent_consumer_unit_id = 5
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"

        response = self._add_to_favorite_request(endpoint, non_existent_consumer_unit_id)

        assert status.HTTP_404_NOT_FOUND == response.status_code

    def test_reject_request_with_missing_fields(self):
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"

        response = self.client.post(endpoint, {})
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert "This field is required" in error["consumer_unit_id"][0]
        assert "This field is required" in error["action"][0]

    def test_reject_request_with_wrong_action_value(self):
        endpoint = f"{ENDPOINT_USER_UNIVERSITY}{self.user.id}/favorite-consumer-units/"

        response = self.client.post(
            endpoint, {"consumer_unit_id": self.consumer_units[0].id, "action": "wrong action"}
        )
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert '"wrong action" is not a valid choice' in error["action"][0]

    """ def test_if_password_is_not_appearing_when_listing_users(self):
        response = self.client.get(f'{ENDPOINT}')

        assert 'password' not in response.content.decode('utf-8')

        response = self.client.get(f'{ENDPOINT_USER_UNIVERSITY}')

        assert 'password' not in response.content.decode('utf-8') """

    def _add_to_favorite_request(self, endpoint: str, consumer_unit_id: str):
        return self.client.post(endpoint, {"consumer_unit_id": consumer_unit_id, "action": "add"})

    def _remove_from_favorite_request(self, endpoint: str, consumer_unit_id: str):
        return self.client.post(endpoint, {"consumer_unit_id": consumer_unit_id, "action": "remove"})

    def _get_user_as_response(self):
        return UniversityUser.objects.get(pk=self.user.id).favorite_consumer_units
