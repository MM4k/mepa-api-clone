from datetime import datetime

import pytest

from contracts.models import EnergyBill


@pytest.fixture
def energy_bill_a(db, consumer_unit_a, contract_a):
    return EnergyBill.objects.create(
        consumer_unit=consumer_unit_a,
        contract=contract_a,
        date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        anotacoes="Test notes for energy bill A",
    )


@pytest.fixture
def energy_bill_b(db, consumer_unit_b, contract_b):
    return EnergyBill.objects.create(
        consumer_unit=consumer_unit_b,
        contract=contract_b,
        date=datetime.strptime("2023-02-01", "%Y-%m-%d").date(),
        anotacoes="Test notes for energy bill B",
        peak_consumption_in_kwh=500.00,
        off_peak_consumption_in_kwh=1000.00,
        peak_measured_demand_in_kw=100.00,
        off_peak_measured_demand_in_kw=200.00,
    )
