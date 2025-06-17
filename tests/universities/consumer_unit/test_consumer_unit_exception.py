import pytest

from django.db.models import ProtectedError

from universities.models import ConsumerUnit, University


@pytest.mark.django_db
def test_throws_exception_when_deleting_university():
    university = University.objects.create(name="unb", cnpj="01234567891234")

    ConsumerUnit.objects.create(name="Darcy Ribeiro", code="123456789", university=university)

    with pytest.raises(Exception) as e:
        university.delete()

    assert type(e.value) is ProtectedError
    assert "Cannot delete some instances " + "of model 'University'" in str(e.value)
