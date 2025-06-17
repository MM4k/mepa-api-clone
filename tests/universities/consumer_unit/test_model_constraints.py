import pytest

from django.db.utils import IntegrityError

from tests.fixtures import consumer_unit_a, university_a, university_b
from universities.models import ConsumerUnit


class TestConsumerUnitConstraints:
    def test_reject_duplicate_name_same_university(self, consumer_unit_a):
        data = {
            "name": consumer_unit_a.name,
            "code": "new-code",
            "university": consumer_unit_a.university,
            "total_installed_power": 100,
            "is_active": True,
        }

        with pytest.raises(IntegrityError) as error:
            ConsumerUnit.objects.create(**data)

        assert "UNIQUE constraint failed" in str(error)
        assert "universities_consumerunit.name" in str(error)

    def test_reject_duplicate_code_same_university(self, consumer_unit_a):
        data = {
            "name": "New Consumer Unit",
            "code": consumer_unit_a.code,
            "university": consumer_unit_a.university,
            "total_installed_power": 100,
            "is_active": True,
        }

        with pytest.raises(IntegrityError) as error:
            ConsumerUnit.objects.create(**data)

        assert "UNIQUE constraint failed" in str(error)
        assert "universities_consumerunit.code" in str(error)

    def test_allow_same_name_different_university(self, consumer_unit_a, university_b):
        data = {
            "name": consumer_unit_a.name,
            "code": "unique-code-b",
            "university": university_b,
            "total_installed_power": 100,
            "is_active": True,
        }

        consumer_unit = ConsumerUnit.objects.create(**data)
        assert consumer_unit.name == data["name"]
        assert consumer_unit.code == data["code"]
        assert consumer_unit.university == university_b
        assert consumer_unit.total_installed_power == data["total_installed_power"]
        assert consumer_unit.is_active == data["is_active"]
        assert ConsumerUnit.objects.filter(name=consumer_unit_a.name, university=university_b).exists()

    def test_allow_same_code_different_university(self, consumer_unit_a, university_b):
        data = {
            "name": "New Consumer Unit",
            "code": consumer_unit_a.code,
            "university": university_b,
            "total_installed_power": 100,
            "is_active": True,
        }

        consumer_unit = ConsumerUnit.objects.create(**data)
        assert consumer_unit.name == data["name"]
        assert consumer_unit.code == data["code"]
        assert consumer_unit.university == university_b
        assert consumer_unit.total_installed_power == data["total_installed_power"]
        assert consumer_unit.is_active == data["is_active"]
        assert ConsumerUnit.objects.filter(code=consumer_unit_a.code, university=university_b).exists()

    def test_allow_same_name_and_code_different_university(self, consumer_unit_a, university_b):
        data = {
            "name": consumer_unit_a.name,
            "code": consumer_unit_a.code,
            "university": university_b,
            "total_installed_power": 100,
            "is_active": True,
        }
        consumer_unit = ConsumerUnit.objects.create(**data)
        assert consumer_unit.name == data["name"]
        assert consumer_unit.code == data["code"]
        assert consumer_unit.university == university_b
        assert consumer_unit.total_installed_power == data["total_installed_power"]
        assert consumer_unit.is_active == data["is_active"]
        assert ConsumerUnit.objects.filter(name=data["name"], university=university_b).exists()
