import pytest

from rest_framework import status

from tariffs.models import Tariff
from tests.fixtures import (
    admin_a,
    admin_b,
    consumer_unit_a,
    consumer_unit_b,
    contract_a,
    contract_b,
    distributor_a,
    distributor_b,
    guest_a,
    sysadmin,
    university_a,
    university_b,
    user_a,
)


@pytest.mark.django_db
class TestConsumerUnitViewSetPermissions:
    def test_manager_can_create_uc_and_contract_in_own_university(self, admin_a, client, contract_a):
        data = {
            "consumer_unit": {
                "name": "UC Teste",
                "code": "12345678",
                "total_installed_power": "100.50",
            },
            "contract": {
                "distributor": contract_a.distributor.id,
                "tariff_flag": contract_a.tariff_flag,
                "start_date": str(contract_a.start_date),
                "subgroup": contract_a.subgroup,
                "peak_contracted_demand_in_kw": str(contract_a.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_a.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=admin_a)
        response = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["consumer_unit"]["university"] == admin_a.university.id

    def test_manager_cannot_create_uc_and_contract_on_other_university(self, admin_a, client, contract_b):
        data = {
            "consumer_unit": {
                "name": "UC Teste Nova",
                "code": "98765432",
                "total_installed_power": "120.50",
            },
            "contract": {
                "distributor": contract_b.distributor.id,
                "tariff_flag": contract_b.tariff_flag,
                "start_date": str(contract_b.start_date),
                "subgroup": contract_b.subgroup,
                "peak_contracted_demand_in_kw": str(contract_b.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_b.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=admin_a)
        response = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["consumer_unit"]["university"] == admin_a.university.id

    def test_manager_can_edit_uc_in_own_university(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": {
                "name": "UC Teste Editada",
                "code": consumer_unit_a.code,
                "total_installed_power": "150.50",
            },
            "contract": {
                "distributor": contract_a.distributor.id,
                "tariff_flag": contract_a.tariff_flag,
                "start_date": str(contract_a.start_date),
                "subgroup": contract_a.subgroup,
                "peak_contracted_demand_in_kw": str(contract_a.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_a.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=admin_a)
        response = client.put(
            f"/api/consumer-units/{consumer_unit_a.id}/edit_consumer_unit_and_contract/", data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["consumer_unit"]["name"] == "UC Teste Editada"
        assert response.data["consumer_unit"]["university"] == admin_a.university.id

    def test_manager_cannot_edit_uc_in_other_university(self, admin_a, client, consumer_unit_b, contract_b):
        data = {
            "consumer_unit": {
                "name": "UC Teste Editada",
                "code": consumer_unit_b.code,
                "total_installed_power": "200.50",
            },
            "contract": {
                "distributor": contract_b.distributor.id,
                "tariff_flag": contract_b.tariff_flag,
                "start_date": str(contract_b.start_date),
                "subgroup": contract_b.subgroup,
                "peak_contracted_demand_in_kw": str(contract_b.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_b.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=admin_a)
        response = client.put(
            f"/api/consumer-units/{consumer_unit_b.id}/edit_consumer_unit_and_contract/", data, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_guest_cannot_create_or_edit_uc_and_contract(self, guest_a, client, contract_a):
        data = {
            "consumer_unit": {
                "name": "UC Teste Guest",
                "code": "11223344",
                "total_installed_power": "150.50",
            },
            "contract": {
                "distributor": contract_a.distributor.id,
                "tariff_flag": contract_a.tariff_flag,
                "start_date": str(contract_a.start_date),
                "subgroup": contract_a.subgroup,
                "peak_contracted_demand_in_kw": str(contract_a.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_a.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=guest_a)
        response_create = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response_create.status_code == status.HTTP_403_FORBIDDEN

        response_edit = client.put(
            f"/api/consumer-units/{contract_a.consumer_unit.id}/edit_consumer_unit_and_contract/", data, format="json"
        )
        assert response_edit.status_code == status.HTTP_403_FORBIDDEN

    def test_sysadmin_cannot_create_or_edit_uc_and_contract(self, sysadmin, client, contract_a):
        data = {
            "consumer_unit": {
                "name": "UC Teste Sysadmin",
                "code": "22334455",
                "total_installed_power": "100.50",
            },
            "contract": {
                "distributor": contract_a.distributor.id,
                "tariff_flag": contract_a.tariff_flag,
                "start_date": str(contract_a.start_date),
                "subgroup": contract_a.subgroup,
                "peak_contracted_demand_in_kw": str(contract_a.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_a.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=sysadmin)
        response_create = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response_create.status_code == status.HTTP_403_FORBIDDEN

        response_edit = client.put(
            f"/api/consumer-units/{contract_a.consumer_unit.id}/edit_consumer_unit_and_contract/", data, format="json"
        )
        assert response_edit.status_code == status.HTTP_403_FORBIDDEN

    def test_user_can_create_and_edit_uc_and_contract_in_own_university(self, user_a, client, contract_a):
        data = {
            "consumer_unit": {
                "name": "UC Teste User",
                "code": "33445566",
                "total_installed_power": "120.50",
            },
            "contract": {
                "distributor": contract_a.distributor.id,
                "tariff_flag": contract_a.tariff_flag,
                "start_date": str(contract_a.start_date),
                "subgroup": contract_a.subgroup,
                "peak_contracted_demand_in_kw": str(contract_a.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_a.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=user_a)
        response_create = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response_create.status_code == status.HTTP_201_CREATED
        assert response_create.data["consumer_unit"]["university"] == user_a.university.id

        data["consumer_unit"]["name"] = "UC Teste User Editada"

        response_edit = client.put(
            f"/api/consumer-units/{response_create.data['consumer_unit']['id']}/edit_consumer_unit_and_contract/",
            data,
            format="json",
        )

        assert response_edit.status_code == status.HTTP_201_CREATED
        assert response_edit.data["consumer_unit"]["name"] == "UC Teste User Editada"
        assert response_edit.data["consumer_unit"]["university"] == user_a.university.id

    def test_user_cannot_create_or_edit_in_other_university(self, user_a, client, contract_b):
        data = {
            "consumer_unit": {
                "name": "UC Teste User",
                "code": "55667788",
                "total_installed_power": "200.50",
            },
            "contract": {
                "distributor": contract_b.distributor.id,
                "tariff_flag": contract_b.tariff_flag,
                "start_date": str(contract_b.start_date),
                "subgroup": contract_b.subgroup,
                "peak_contracted_demand_in_kw": str(contract_b.peak_contracted_demand_in_kw),
                "off_peak_contracted_demand_in_kw": str(contract_b.off_peak_contracted_demand_in_kw),
            },
        }
        client.force_authenticate(user=user_a)
        response_create = client.post("/api/consumer-units/create_consumer_unit_and_contract/", data, format="json")
        assert response_create.status_code == status.HTTP_201_CREATED
        assert response_create.data["consumer_unit"]["university"] == user_a.university.id
        ct_b = contract_b.consumer_unit.id
        response_edit = client.put(f"/api/consumer-units/{ct_b}/edit_consumer_unit_and_contract/", data, format="json")
        assert response_edit.status_code == status.HTTP_404_NOT_FOUND
