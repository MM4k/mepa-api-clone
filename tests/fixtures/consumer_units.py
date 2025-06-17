import pytest

from universities.models import ConsumerUnit


@pytest.fixture
def consumer_unit_a(db, university_a):
    return ConsumerUnit.objects.create(
        name="Consumer Unit A",
        code="CUA-001",
        is_active=True,
        university=university_a,
    )


@pytest.fixture
def consumer_unit_b(db, university_b):
    return ConsumerUnit.objects.create(
        name="Consumer Unit B",
        code="CUB-001",
        is_active=True,
        university=university_b,
    )
