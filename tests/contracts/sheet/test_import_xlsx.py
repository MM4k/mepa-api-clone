import json
import os

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from tests.contracts.sheet import dict_test_response
from tests.test_utils import create_objects_test_utils, dicts_test_utils


@pytest.mark.django_db
class TestImportXlsx:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1
        self.contracts_dict = dicts_test_utils.contract_dict_1
        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.consumer_unit_dict = dicts_test_utils.consumer_unit_dict_1
        self.energy_bill_dict = dicts_test_utils.energy_bill_dict_2
        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)
        self.consumer_unit = create_objects_test_utils.create_test_consumer_unit(
            self.consumer_unit_dict, self.university
        )
        self.contract = create_objects_test_utils.create_test_contract(
            self.contracts_dict, self.distributor, self.consumer_unit
        )
        self.energy_bill = create_objects_test_utils.create_test_energy_bill(
            self.energy_bill_dict, self.contract, self.consumer_unit
        )

        self.client = APIClient()
        self.client.login(email=self.user_dict["email"], password=self.user_dict["password"])

    def test_invalid_xlsx_header(self):
        xlsx_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_header.xlsx")
        print(xlsx_path)
        with open(xlsx_path, "rb") as xlsx_file:
            xlsx_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (xlsx_file, "file_invalid_header.xlsx")},
            )
        assert xlsx_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        xlsx_content = json.loads(xlsx_response.content)
        assert xlsx_content == dict_test_response.invalid_header_dict

    def test_invalid_date_format(self):
        xlsx_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_date_format.xlsx")
        print(xlsx_path)
        with open(xlsx_path, "rb") as xlsx_file:
            xlsx_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (xlsx_file, "file_invalid_date_format.xlsx")},
            )
        assert xlsx_response.status_code == status.HTTP_200_OK

        xlsx_content = json.loads(xlsx_response.content)
        assert xlsx_content == dict_test_response.invalid_date_format_dict

    def test_invalid_date_all(self):
        xlsx_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_date_all.xlsx")
        print(xlsx_path)
        with open(xlsx_path, "rb") as xlsx_file:
            xlsx_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (xlsx_file, "file_invalid_date_all.xlsx")},
            )
        assert xlsx_response.status_code == status.HTTP_200_OK

        xlsx_content = json.loads(xlsx_response.content)
        assert xlsx_content == dict_test_response.invalid_date_all_dict

    def test_invalid_number(self):
        xlsx_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_numbers.xlsx")
        print(xlsx_path)
        with open(xlsx_path, "rb") as xlsx_file:
            xlsx_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (xlsx_file, "file_invalid_numbers.xlsx")},
            )
        assert xlsx_response.status_code == status.HTTP_200_OK

        xlsx_content = json.loads(xlsx_response.content)
        assert xlsx_content == dict_test_response.invalid_number_dict_xlsx
