import pytest

from universities.models import University


@pytest.fixture
def university_a(db):
    return University.objects.create(
        name="University of Brasília",
        acronym="UnB",
        cnpj="15989610000137",
    )


@pytest.fixture
def university_b(db):
    return University.objects.create(
        name="University of São Paulo",
        acronym="USP",
        cnpj="47559477000175",
    )
