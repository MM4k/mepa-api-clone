import json
import os

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from tests.contracts.sheet import dict_test_response
from tests.test_utils import create_objects_test_utils, dicts_test_utils


@pytest.mark.django_db
class TestImportXslx:
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

    def test_invalid_csv_header(self):
        csv_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_header.csv")
        print(csv_path)
        with open(csv_path, "rb") as csv_file:
            csv_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (csv_file, "file_invalid_header.csv")},
            )
        assert csv_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        csv_content = json.loads(csv_response.content)
        assert csv_content == dict_test_response.invalid_header_dict

    def test_invalid_separator(self):
        csv_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_separator.csv")
        print(csv_path)
        with open(csv_path, "rb") as csv_file:
            csv_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (csv_file, "file_invalid_separator.csv")},
            )
        assert csv_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        csv_content = json.loads(csv_response.content)
        assert csv_content == {
            "file": [
                "\"['Data', 'Valor (R$)', 'Consumo Ponta (kWh)', 'Consumo Fora "
                "Ponta (kWh)', 'Demanda Ponta (kW)', 'Demanda Fora Ponta (kW)'] not "
                'found in axis"',
            ],
        }

    def test_invalid_date_format(self):
        csv_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_date_format.csv")
        print(csv_path)
        with open(csv_path, "rb") as csv_file:
            csv_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (csv_file, "file_invalid_date_format.csv")},
            )
        assert csv_response.status_code == status.HTTP_200_OK

        csv_content = json.loads(csv_response.content)
        assert csv_content == dict_test_response.invalid_date_format_dict

    def test_invalid_date_all(self):
        csv_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_date_all.csv")
        print(csv_path)
        with open(csv_path, "rb") as csv_file:
            csv_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (csv_file, "file_invalid_date_all.csv")},
            )
        assert csv_response.status_code == status.HTTP_200_OK

        csv_content = json.loads(csv_response.content)
        assert csv_content == dict_test_response.invalid_date_all_dict

    def test_invalid_number(self):
        csv_path = os.path.join(os.path.dirname(__file__), "files", "file_invalid_numbers.csv")
        print(csv_path)
        with open(csv_path, "rb") as csv_file:
            csv_response = self.client.post(
                "/api/energy-bills/upload/",
                format="multipart",
                data={"consumer_unit_id": 1, "file": (csv_file, "file_invalid_numbers.csv")},
            )
        assert csv_response.status_code == status.HTTP_200_OK

        csv_content = json.loads(csv_response.content)
        assert csv_content == dict_test_response.invalid_number_dict_csv
