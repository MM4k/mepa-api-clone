from datetime import datetime
from decimal import Decimal

import pytest

from rest_framework import status

from contracts.models import EnergyBill
from tests.fixtures import admin_a, consumer_unit_a, contract_a, distributor_a, university_a


@pytest.mark.django_db
class TestEnergyBillViewSetTests:
    def test_create_energy_bill_success(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "contract": contract_a.id,
            "date": "2023-01-01",
            "anotacoes": "Some notes",
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        energy_bill = EnergyBill.objects.get(consumer_unit=consumer_unit_a.id)
        assert energy_bill.anotacoes == data["anotacoes"]

    def test_create_energy_bill_invalid_date(self, admin_a, client, consumer_unit_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "date": "invalid_date",
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_energy_invalid_consumption(self, admin_a, client, consumer_unit_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "date": "2024-05-06",
            "off_peak_consumption_in_kwh": 0.00,
            "off_peak_measured_demand_in_kw": 0.00,
        }
        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_energy_bill_long_notes(self, admin_a, client, consumer_unit_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "date": "2023-01-01",
            "anotacoes": "A" * 1001,
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_duplicate_energy_bill(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "contract": contract_a.id,
            "date": "2023-01-01",
            "anotacoes": "Some notes",
        }

        client.force_authenticate(user=admin_a)
        response1 = client.post("/api/energy-bills/", data, format="json")
        assert response1.status_code == status.HTTP_201_CREATED

        response2 = client.post("/api/energy-bills/", data, format="json")
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_max_peak_and_offpeak_consumption_values(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "contract": contract_a.id,
            "date": "2023-01-01",
            "anotacoes": "Some notes",
            "peak_consumption_in_kwh": 9999999.99,
            "off_peak_consumption_in_kwh": 9999999.99,
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        energy_bill = EnergyBill.objects.get(
            consumer_unit=consumer_unit_a.id, date=datetime.strptime("2023-01-01", "%Y-%m-%d").date()
        )
        assert energy_bill.anotacoes == "Some notes"
        assert energy_bill.peak_consumption_in_kwh == Decimal("9999999.99")
        assert energy_bill.off_peak_consumption_in_kwh == Decimal("9999999.99")

    def test_max_peak_and_offpeak_measured_values(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "contract": contract_a.id,
            "date": "2023-01-01",
            "anotacoes": "Some notes",
            "peak_measured_demand_in_kw": 9999999.99,
            "off_peak_measured_demand_in_kw": 9999999.99,
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        energy_bill = EnergyBill.objects.get(
            consumer_unit=consumer_unit_a.id,
            date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        )
        assert energy_bill.anotacoes == "Some notes"
        assert energy_bill.peak_measured_demand_in_kw == Decimal("9999999.99")
        assert energy_bill.off_peak_measured_demand_in_kw == Decimal("9999999.99")

    def test_exceeding_values_energybill(self, admin_a, client, consumer_unit_a, contract_a):
        data = {
            "consumer_unit": consumer_unit_a.id,
            "contract": contract_a.id,
            "date": "2023-01-01",
            "anotacoes": "Some notes",
            "peak_consumption_in_kwh": 10000000,
            "off_peak_consumption_in_kwh": 10000000,
            "peak_measured_demand_in_kw": 10000000,
            "off_peak_measured_demand_in_kw": 10000000,
        }

        client.force_authenticate(user=admin_a)
        response = client.post("/api/energy-bills/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ensure that there are no more than 7 digits before the decimal point." in response.content.decode(
            "utf-8"
        )
