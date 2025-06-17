import pytest

from rest_framework import status

from tests.fixtures import distributor_a, university_a, user_a


@pytest.mark.django_db
class TestTariffFlagSubgroup:
    endpoint = "/api/consumer-units/create_consumer_unit_and_contract/"

    @pytest.fixture
    def base_payload(self, distributor_a):
        return {
            "consumer_unit": {
                "name": "Unb",
                "code": "00540",
                "is_active": True,
                "totalInstalledPower": None,
            },
            "contract_data": {
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "distributor": distributor_a.id,
                "peak_contracted_demand_in_kw": 33,
                "off_peak_contracted_demand_in_kw": 33,
            },
        }

    @pytest.mark.parametrize(
        "contract_data_update,expected_error",
        [
            ({}, {"contract": ["This field is required."]}),
            ({"subgroup": "A2"}, {"contract": ["This field is required."]}),
            ({"subgroup": "A2", "tariff_flag": "X"}, {"contract": ["This field is required."]}),
            ({"tariff_flag": "B"}, {"contract": ["This field is required."]}),
            ({"subgroup": "A7", "tariff_flag": "B"}, {"contract": ["This field is required."]}),
        ],
    )
    def test_create_contract_validation(self, client, user_a, base_payload, contract_data_update, expected_error):
        client.force_authenticate(user_a)
        payload = base_payload.copy()
        payload["contract_data"].update(contract_data_update)
        response = client.post(self.endpoint, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_error
