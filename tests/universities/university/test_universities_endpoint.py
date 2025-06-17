import json

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils import create_objects_test_utils, dicts_test_utils

ENDPOINT = "/api/universities/"


@pytest.mark.django_db
class TestUniversitiesEndpoint:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.super_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_super_user(self.user_dict)

        self.client = APIClient()
        self.client.login(email=self.user_dict["email"], password=self.user_dict["password"])

        self.university_to_be_created = {"name": "Universidade de Brasília", "cnpj": "00038174000143"}

    def test_create_university(self):
        response = self.client.post(ENDPOINT, self.university_to_be_created)

        created_university = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert created_university["cnpj"] == self.university_to_be_created["cnpj"]

    def test_reject_university_with_invalid_cnpj(self):
        self.university_to_be_created["cnpj"] = "F0038174000143"

        response = self.client.post(ENDPOINT, self.university_to_be_created)

        error_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "must contain exactly 14 numerical digits" in error_json["cnpj"][0]

    def test_reject_attempt_to_delete_university(self):
        response = self.client.delete(ENDPOINT, self.university_dict)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_reject_attempt_to_delete_university_by_id(self):
        delete_endpoint = f"{ENDPOINT}{self.university.id}/"
        response = self.client.delete(delete_endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
