from contracts.models import Contract, EnergyBill
from tariffs.models import Distributor, Tariff
from universities.models import ConsumerUnit, University
from users.models import CustomUser, UniversityUser


def create_test_university(dict: dict) -> University:
    university = University.objects.create(
        name=dict["name"],
        cnpj=dict["cnpj"],
    )

    return university


def create_test_consumer_unit(dict: dict, university: University) -> ConsumerUnit:
    consumer_unit = ConsumerUnit.objects.create(
        name=dict["name"], code=dict["code"], is_active=dict["is_active"], university=university
    )

    return consumer_unit


def create_test_contract(dict: dict, distributor: Distributor, consumer_unit: ConsumerUnit) -> Contract:
    contract = Contract.objects.create(
        start_date=dict["start_date"],
        tariff_flag=dict["tariff_flag"],
        subgroup=dict["subgroup"],
        peak_contracted_demand_in_kw=dict["peak_contracted_demand_in_kw"],
        off_peak_contracted_demand_in_kw=dict["off_peak_contracted_demand_in_kw"],
        distributor=distributor,
        consumer_unit=consumer_unit,
    )

    return contract


def create_test_energy_bill(dict: dict, contract: Contract, consumer_unit: ConsumerUnit) -> EnergyBill:
    energy_bill = EnergyBill.objects.create(
        date=dict["date"],
        invoice_in_reais=dict["invoice_in_reais"],
        is_atypical=dict["is_atypical"],
        peak_consumption_in_kwh=dict["peak_consumption_in_kwh"],
        off_peak_consumption_in_kwh=dict["off_peak_consumption_in_kwh"],
        peak_measured_demand_in_kw=dict["peak_measured_demand_in_kw"],
        off_peak_measured_demand_in_kw=dict["off_peak_measured_demand_in_kw"],
        contract=contract,
        consumer_unit=consumer_unit,
    )

    return energy_bill


def create_test_distributor(dict: dict, university: University) -> Distributor:
    distributor = Distributor.objects.create(name=dict["name"], cnpj=dict["cnpj"], university=university)

    return distributor


def create_test_tariffs(dict: dict):
    blue_tariff = create_test_blue_tariff(dict)
    green_tariff = create_test_green_tariff(dict)

    return blue_tariff, green_tariff


def create_test_blue_tariff(dict: dict, distributor: Distributor) -> Tariff:
    blue_tarif = Tariff.objects.create(
        subgroup=dict["subgroup"],
        start_date=dict["start_date"],
        end_date=dict["start_date"],
        peak_tusd_in_reais_per_kw=dict["peak_tusd_in_reais_per_kw"],
        peak_tusd_in_reais_per_mwh=dict["peak_tusd_in_reais_per_mwh"],
        peak_te_in_reais_per_mwh=dict["peak_te_in_reais_per_mwh"],
        off_peak_tusd_in_reais_per_kw=dict["off_peak_tusd_in_reais_per_kw"],
        off_peak_tusd_in_reais_per_mwh=dict["off_peak_tusd_in_reais_per_mwh"],
        off_peak_te_in_reais_per_mwh=dict["off_peak_te_in_reais_per_mwh"],
        power_generation_tusd_in_reais_per_kw=dict["power_generation_tusd_in_reais_per_kw"],
        distributor_id=distributor.id,
        flag=Tariff.BLUE,
    )

    return blue_tarif


def create_test_green_tariff(dict: dict, distributor: Distributor) -> Tariff:
    green_tariff = Tariff.objects.create(
        subgroup=dict["subgroup"],
        start_date=dict["start_date"],
        end_date=dict["start_date"],
        peak_tusd_in_reais_per_mwh=dict["peak_tusd_in_reais_per_mwh"],
        peak_te_in_reais_per_mwh=dict["peak_te_in_reais_per_mwh"],
        off_peak_tusd_in_reais_per_mwh=dict["off_peak_tusd_in_reais_per_mwh"],
        off_peak_te_in_reais_per_mwh=dict["off_peak_te_in_reais_per_mwh"],
        na_tusd_in_reais_per_kw=dict["na_tusd_in_reais_per_kw"],
        power_generation_tusd_in_reais_per_kw=dict["power_generation_tusd_in_reais_per_kw"],
        distributor_id=distributor.id,
        flag=Tariff.GREEN,
    )

    return green_tariff


# ---------------------------------------
# Users


def create_test_super_user(dict: dict) -> CustomUser:
    super_user = CustomUser.objects.create(
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        type=CustomUser.Type.SUPER_USER,
        is_staff=True,
    )
    super_user.set_password(dict["password"])
    super_user.save()

    return super_user


def create_test_university_user(dict: dict, university: University) -> UniversityUser:
    university_user = UniversityUser.objects.create(
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        password=dict["password"],
        type=CustomUser.Type.UNIVERSITY_USER,
        university=university,
    )

    return university_user


def create_test_university_admin_user(dict: dict, university: University) -> UniversityUser:
    university_admin_user = UniversityUser.objects.create(
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        password=dict["password"],
        university=university,
        type=CustomUser.Type.UNIVERSITY_ADMIN,
    )

    return university_admin_user
