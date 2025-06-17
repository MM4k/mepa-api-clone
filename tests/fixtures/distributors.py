import pytest

from tariffs.models import Distributor


@pytest.fixture
def distributor_a(db, university_a):
    return Distributor.objects.create(
        name="Distributor A",
        cnpj="34884865000180",
        is_active=True,
        university=university_a,
    )


@pytest.fixture
def distributor_b(db, university_b):
    return Distributor.objects.create(
        name="Distributor B",
        cnpj="12345678000195",
        is_active=True,
        university=university_b,
    )
