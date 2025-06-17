import pytest

from rest_framework.test import APIClient

from tests.test_utils import create_objects_test_utils, dicts_test_utils


@pytest.mark.django_db
class TestContractEndpoint:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1
        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(email=self.user_dict["email"], password=self.user_dict["password"])
        self.university_to_be_created = {"name": "Universidade de Brasília", "cnpj": "00038174000143"}
        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)
        self.consumer_unit_test_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test = create_objects_test_utils.create_test_consumer_unit(
            self.consumer_unit_test_dict,
            self.university,
        )
        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_2_dict = dicts_test_utils.contract_dict_2
        self.contract_test_3_dict = dicts_test_utils.contract_dict_3
        self.contract_test_1 = create_objects_test_utils.create_test_contract(
            self.contract_test_1_dict,
            self.distributor,
            self.consumer_unit_test,
        )
        self.contract_test_2 = create_objects_test_utils.create_test_contract(
            self.contract_test_2_dict,
            self.distributor,
            self.consumer_unit_test,
        )
        self.contract_test_3 = create_objects_test_utils.create_test_contract(
            self.contract_test_3_dict,
            self.distributor,
            self.consumer_unit_test,
        )

    def test_read_contract_subgroup_A3(self):
        assert self.contract_test_3.subgroup == "A3"

    def test_read_contract_subgroup_A2(self):
        assert self.contract_test_1.subgroup == "A2"

    def test_read_contract_subgroup_A1(self):
        assert self.contract_test_2.subgroup == "A1"

    # TODO:
    # Fazer testes de endpoint de contratos
