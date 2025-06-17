from datetime import datetime

import pytest

from contracts.models import Contract, EnergyBill
from tests.test_utils import create_objects_test_utils, dicts_test_utils
from universities.models import ConsumerUnit


@pytest.mark.django_db
class TestCheckEnergyBillCoveredByContract:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.university = create_objects_test_utils.create_test_university(dicts_test_utils.university_dict_1)
        self.consumer_unit = ConsumerUnit.objects.create(
            name="Faculdade do Gama",
            code="111111111",
            created_on="2022-10-02",
            is_active=True,
            university=self.university,
            total_installed_power=12,
        )
        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

    # CT1 quando não há nenhum contrato existente
    def test_no_contracts(self):
        result, date = EnergyBill.check_energy_bill_covered_by_contract(
            self.consumer_unit.id, datetime.strptime("2024-07-22", "%Y-%m-%d").date()
        )
        assert result is False
        assert date is None

    # CT2 quando não há nenhuma conta coberta por contrato
    def test_no_bills_covered(self):
        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-01-31", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-02-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-02-28", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        result, date = EnergyBill.check_energy_bill_covered_by_contract(
            self.consumer_unit.id, datetime.strptime("2023-01-31", "%Y-%m-%d").date()
        )
        assert result is False
        assert date == datetime.strptime("2024-02-01", "%Y-%m-%d").date()

    # CT3 quando há uma conta coberta com data maior ou igual apenas a data de início do contrato mais antigo
    def test_bill_covered_by_only_a_oldest_contract(self):
        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-01-31", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-02-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-02-28", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        result, date = EnergyBill.check_energy_bill_covered_by_contract(
            self.consumer_unit.id, datetime.strptime("2024-01-02", "%Y-%m-%d").date()
        )
        assert result is True
        assert date is None

    # CT4 quando há uma conta coberta com data maior ou igual a data de início de ambos os contratos
    def test_bill_covered_by_both_contracts(self):
        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-01-31", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        Contract.objects.create(
            consumer_unit=self.consumer_unit,
            start_date=datetime.strptime("2024-02-01", "%Y-%m-%d").date(),
            end_date=datetime.strptime("2024-02-28", "%Y-%m-%d").date(),
            subgroup="A2",
            distributor=self.distributor,
        )

        result, date = EnergyBill.check_energy_bill_covered_by_contract(
            self.consumer_unit.id,
            datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
        )
        assert result is True
        assert date is None
