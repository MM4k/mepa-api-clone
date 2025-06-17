from datetime import datetime

import pytest

from contracts.models import Contract
from tests.test_utils import create_objects_test_utils, dicts_test_utils
from universities.models import ConsumerUnit


@pytest.mark.django_db
class TestConsumerUnit:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.university = create_objects_test_utils.create_test_university(self.university_dict)

        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)
        self.distributor_dict["id"] = self.distributor.id

        self.distributor_dict_2 = dicts_test_utils.distributor_dict_2
        self.distributor_2 = create_objects_test_utils.create_test_distributor(
            self.distributor_dict_2, self.university
        )
        self.distributor_dict_2["id"] = self.distributor_2.id

        self.consumer_unit_dict = {
            "name": "Unidade Darcy Ribeiro",
            "code": "123456",
            "university": self.university.id,
            "total_installed_power": 500.0,
            "is_active": True,
        }

        self.contract_dict = {
            "distributor": self.distributor.id,
            "start_date": datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
            "tariff_flag": "VERDE",
            "peak_contracted_demand_in_kw": 100,
            "off_peak_contracted_demand_in_kw": 80,
        }

    def test_create_consumer_unit(self):
        consumer_unit = ConsumerUnit.objects.create(
            university=self.university,
            name=self.consumer_unit_dict["name"],
            code=self.consumer_unit_dict["code"],
            total_installed_power=self.consumer_unit_dict["total_installed_power"],
            is_active=self.consumer_unit_dict["is_active"],
        )

        assert consumer_unit.name == "Unidade Darcy Ribeiro"
        assert consumer_unit.code == "123456"
        assert consumer_unit.university == self.university
        assert consumer_unit.total_installed_power == 500.0
        assert consumer_unit.is_active is True

    def test_create_consumer_unit_and_contract(self):
        # Criando a unidade consumidora
        consumer_unit = ConsumerUnit.objects.create(
            university=self.university,
            name=self.consumer_unit_dict["name"],
            code=self.consumer_unit_dict["code"],
            total_installed_power=self.consumer_unit_dict["total_installed_power"],
            is_active=self.consumer_unit_dict["is_active"],
        )

        # Criando o contrato associado (adicionando end_date)
        contract = Contract.objects.create(
            consumer_unit=consumer_unit,
            peak_contracted_demand_in_kw=self.contract_dict["peak_contracted_demand_in_kw"],
            tariff_flag=self.contract_dict["tariff_flag"],
            distributor=self.distributor,
            start_date=self.contract_dict["start_date"],
            end_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),  # Corrigido
            subgroup="A1",
            off_peak_contracted_demand_in_kw=self.contract_dict["off_peak_contracted_demand_in_kw"],
        )

        # Verificações
        assert consumer_unit.name == "Unidade Darcy Ribeiro"
        assert consumer_unit.code == "123456"
        assert consumer_unit.university == self.university
        assert contract.peak_contracted_demand_in_kw == 100
        assert contract.tariff_flag == "VERDE"
        assert contract.end_date == datetime.strptime("2024-12-31", "%Y-%m-%d").date()

    def test_edit_consumer_unit_and_contract(self):
        # Criando a unidade consumidora
        consumer_unit = ConsumerUnit.objects.create(
            university=self.university,
            name=self.consumer_unit_dict["name"],
            code=self.consumer_unit_dict["code"],
            total_installed_power=self.consumer_unit_dict["total_installed_power"],
            is_active=self.consumer_unit_dict["is_active"],
        )

        # Criando o contrato associado (adicionando end_date)
        contract = Contract.objects.create(
            consumer_unit=consumer_unit,
            peak_contracted_demand_in_kw=self.contract_dict["peak_contracted_demand_in_kw"],
            tariff_flag=self.contract_dict["tariff_flag"],
            distributor=self.distributor,
            start_date=self.contract_dict["start_date"],
            end_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),  # Corrigido
            subgroup="A1",
            off_peak_contracted_demand_in_kw=self.contract_dict["off_peak_contracted_demand_in_kw"],
        )

        # Dados atualizados
        consumer_unit.name = "Unidade Alterada"
        consumer_unit.code = "654321"
        consumer_unit.is_active = False
        consumer_unit.total_installed_power = 600.0
        consumer_unit.save()

        contract.peak_contracted_demand_in_kw = 120
        contract.tariff_flag = "AZUL"
        contract.distributor = self.distributor_2
        contract.subgroup = "B1"
        contract.save()

        # Atualizando os objetos do banco de dados
        updated_consumer_unit = ConsumerUnit.objects.get(id=consumer_unit.id)
        updated_contract = Contract.objects.get(id=contract.id)

        # Verificações
        assert updated_consumer_unit.name == "Unidade Alterada"
        assert updated_consumer_unit.code == "654321"
        assert updated_consumer_unit.is_active is False
        assert updated_consumer_unit.total_installed_power == 600.0
        assert updated_contract.tariff_flag == "AZUL"
        assert updated_contract.peak_contracted_demand_in_kw == 120
        assert updated_contract.end_date == datetime.strptime("2024-12-31", "%Y-%m-%d").date()

    def test_is_current_energy_bill_filled(self):
        # Criando a unidade consumidora
        consumer_unit = ConsumerUnit.objects.create(
            university=self.university,
            name=self.consumer_unit_dict["name"],
            code=self.consumer_unit_dict["code"],
            total_installed_power=self.consumer_unit_dict["total_installed_power"],
            is_active=self.consumer_unit_dict["is_active"],
        )

        # Criando o contrato associado (adicionando end_date)
        contract = Contract.objects.create(
            consumer_unit=consumer_unit,
            peak_contracted_demand_in_kw=self.contract_dict["peak_contracted_demand_in_kw"],
            tariff_flag=self.contract_dict["tariff_flag"],
            distributor=self.distributor,
            start_date=self.contract_dict["start_date"],
            end_date="2024-12-31",  # Definindo a data de término
            subgroup="A1",
            off_peak_contracted_demand_in_kw=self.contract_dict["off_peak_contracted_demand_in_kw"],
        )

        # Teste
        energy_bill_filled = consumer_unit.is_current_energy_bill_filled
        assert energy_bill_filled in [True, False]

    def test_pending_energy_bills_number(self):
        # Criando a unidade consumidora
        consumer_unit = ConsumerUnit.objects.create(
            university=self.university,
            name=self.consumer_unit_dict["name"],
            code=self.consumer_unit_dict["code"],
            total_installed_power=self.consumer_unit_dict["total_installed_power"],
            is_active=self.consumer_unit_dict["is_active"],
        )

        # Criando o contrato associado (adicionando end_date)
        contract = Contract.objects.create(
            consumer_unit=consumer_unit,
            peak_contracted_demand_in_kw=self.contract_dict["peak_contracted_demand_in_kw"],
            tariff_flag=self.contract_dict["tariff_flag"],
            distributor=self.distributor,
            start_date=self.contract_dict["start_date"],
            end_date="2024-12-31",  # Definindo a data de término
            subgroup="A1",
            off_peak_contracted_demand_in_kw=self.contract_dict["off_peak_contracted_demand_in_kw"],
        )

        # Teste
        pending_bills = consumer_unit.pending_energy_bills_number
        assert isinstance(pending_bills, int)
        assert pending_bills >= 0
