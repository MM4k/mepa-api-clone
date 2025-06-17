import logging
import os

from datetime import date, timedelta
from random import choice, randint

from contracts.models import Contract, EnergyBill
from scripts.utils import (
    BLUE_TARIFF,
    ENERGY_DISTRIBUTORS,
    GREEN_TARIFF,
    REGIONS,
    TABLE_BILLS,
    UC_TEMPLATES,
    UNIVERSITY_TEMPLATES,
    add_random_variation,
    get_data_university,
)
from tariffs.models import Distributor, Tariff
from universities.models import ConsumerUnit, University
from users.models import UniversityUser

logger = logging.getLogger(__name__)


def create_users(university):
    admin_user = UniversityUser.objects.create(
        university=university,
        type=UniversityUser.university_admin_user_type,
        email=f"admin@{university.acronym}.com",
        password=university.acronym.lower().strip(),
        first_name=f"Admin {university.acronym}",
        is_seed_user=True,
    )

    regular_user = UniversityUser.objects.create(
        university=university,
        email=f"user@{university.acronym}.com",
        password=university.acronym.lower().strip(),
        first_name=f"Admin {university.acronym}",
        is_seed_user=True,
    )

    return {"admin": admin_user, "regular": regular_user}


def create_distributor(university):
    distributor_data = choice(ENERGY_DISTRIBUTORS)
    return Distributor.objects.create(
        university=university,
        **distributor_data,
    )


def create_tariffs(distributor) -> None:
    A3_START_DATE = date(2023, 1, 1)
    A3_END_DATE = date.today() + timedelta(weeks=12)
    A4_START_DATE = date(2023, 1, 1)
    A4_END_DATE = date.today() + timedelta(weeks=12)

    Tariff.objects.bulk_create(
        [
            Tariff(
                subgroup="A3",
                distributor=distributor,
                flag=Tariff.BLUE,
                **BLUE_TARIFF,
                start_date=A3_START_DATE,
                end_date=A3_END_DATE,
            ),
            Tariff(
                subgroup="A3",
                distributor=distributor,
                flag=Tariff.GREEN,
                **GREEN_TARIFF,
                start_date=A3_START_DATE,
                end_date=A3_END_DATE,
            ),
            Tariff(
                subgroup="A4",
                distributor=distributor,
                flag=Tariff.BLUE,
                **BLUE_TARIFF,
                start_date=A4_START_DATE,
                end_date=A4_END_DATE,
            ),
            Tariff(
                subgroup="A4",
                distributor=distributor,
                flag=Tariff.GREEN,
                **GREEN_TARIFF,
                start_date=A4_START_DATE,
                end_date=A4_END_DATE,
            ),
        ]
    )


def create_contract(distributor, consumer_unit):
    return Contract.objects.create(
        tariff_flag=Tariff.GREEN,
        consumer_unit=consumer_unit,
        distributor=distributor,
        start_date=date(2022, 1, 1),
        subgroup="A4",
        peak_contracted_demand_in_kw=150.0,
        off_peak_contracted_demand_in_kw=150.0,
    )


def create_consumer_unit(university, num_units):
    if num_units > len(UC_TEMPLATES):
        raise ValueError("Número de UCs maior que o número de templates")

    consumer_units = []
    for uc_name in UC_TEMPLATES[:num_units]:
        consumer_unit = ConsumerUnit.objects.create(
            name=uc_name,
            code=randint(100000, 999999),
            is_active=True,
            university=university,
        )
        consumer_units.append(consumer_unit)

    return consumer_units


def create_consumer_unit_and_contract(university, distributor, num_units=len(UC_TEMPLATES)):
    consumer_units = create_consumer_unit(university, num_units)

    contracts = []
    for consumer_unit in consumer_units:
        contract = create_contract(distributor, consumer_unit)
        contracts.append(contract)

    return consumer_units, contracts


def create_bills_from_table(contracts, consumer_units, table):
    for contract, uc in zip(contracts, consumer_units):
        for row in table:
            EnergyBill.objects.create(
                contract=contract,
                consumer_unit=uc,
                date=row[0],
                peak_consumption_in_kwh=add_random_variation(row[1]),
                off_peak_consumption_in_kwh=add_random_variation(row[2]),
                peak_measured_demand_in_kw=add_random_variation(row[3]),
                off_peak_measured_demand_in_kw=add_random_variation(row[4]),
                invoice_in_reais=row[5],
                is_atypical=(False if len(row) < 7 else row[6]),
            )


def seed_generator(num_universities):
    max_combinations = len(UNIVERSITY_TEMPLATES) * len(REGIONS)
    if NUM_UNIVERSITIES > max_combinations:
        raise ValueError(f"O número máximo de universidades é {max_combinations}")

    university_generator = get_data_university()
    for i in range(num_universities):
        data_university = next(university_generator)
        try:
            university = University.objects.create(**data_university)
            users = create_users(university)
            distributor = create_distributor(university)
            create_tariffs(distributor)
            consumer_units, contracts = create_consumer_unit_and_contract(university, distributor, NUM_CONSUMER_UNITS)
            create_bills_from_table(contracts, consumer_units, TABLE_BILLS)

            logger.info(f"{i} - {university.name}, criada com sucesso!")
            logger.info(f"Usuários: {users}")
            logger.info("-" * 100)
        except Exception as e:
            logger.error(f"Erro ao criar universidade {i}: {str(e)}")


# --------------------------------------------------------------------------------------
MAX_UNIVERSITIES = len(UNIVERSITY_TEMPLATES) * len(REGIONS)
NUM_UNIVERSITIES = int(os.getenv("NUM_UNIVERSITIES", MAX_UNIVERSITIES))
NUM_CONSUMER_UNITS = int(os.getenv("NUM_CONSUMER_UNITS", len(UC_TEMPLATES)))

seed_generator(NUM_UNIVERSITIES)
