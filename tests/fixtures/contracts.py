from datetime import datetime

import pytest

from contracts.models import Contract
from tariffs.models import Tariff


@pytest.fixture
def contract_a(db, consumer_unit_a, distributor_a):
    return Contract.objects.create(
        consumer_unit=consumer_unit_a,
        distributor=distributor_a,
        tariff_flag=Tariff.BLUE,
        start_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        subgroup="A3",
        peak_contracted_demand_in_kw=100.00,
        off_peak_contracted_demand_in_kw=50.00,
    )


@pytest.fixture
def contract_b(db, consumer_unit_b, distributor_b):
    return Contract.objects.create(
        consumer_unit=consumer_unit_b,
        distributor=distributor_b,
        tariff_flag=Tariff.GREEN,
        start_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        subgroup="A3",
        peak_contracted_demand_in_kw=200.00,
        off_peak_contracted_demand_in_kw=100.00,
    )
