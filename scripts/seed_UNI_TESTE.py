#!/usr/local/bin/python

from random import random
from datetime import date, timedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff
from contracts.models import Contract, EnergyBill
from users.models import UniversityUser

TODAY = date.today()
YEAR_LATER = TODAY + timedelta(days=2*365)

##########################################################################
# Funções Auxiliares
##########################################################################

def create_bills_from_table(contract, uc, table):
    for row in table:
        EnergyBill.objects.create(contract=contract, consumer_unit=uc, \
            date=row[0],\
            peak_consumption_in_kwh=row[1],\
            off_peak_consumption_in_kwh=row[2],\
            peak_measured_demand_in_kw=row[3],\
            off_peak_measured_demand_in_kw=row[4],\
            invoice_in_reais=row[5],\
            is_atypical=(False if len(row) < 7 else row[6]))

########################################################################## 

# Universidade

university = University.objects.create(
    name='Universidade de Teste',
    acronym='UniTeste',
    cnpj='16494737000148'
)

# Usuários

admin_university_user = UniversityUser.objects.create(
    university=university,
    type=UniversityUser.university_admin_user_type,
    password='teste',
    email='admin@teste.br',
    first_name="João",
    last_name="da Silva",
    is_seed_user=True
)

university_user = UniversityUser.objects.create(
    university=university,
    password='teste',
    email='usuario@teste.br',
    first_name="José",
    last_name="Santos",
    is_seed_user=True
)

# Distribuidoras

distributor_teste = Distributor.objects.create(
    name='EnergoTeste',
    cnpj='27643777000120',
    university=university,
)

# Tarifas
blue = {
    "peak_tusd_in_reais_per_kw": 29.84,
    "peak_tusd_in_reais_per_mwh": 127.2,
    "peak_te_in_reais_per_mwh": 620.43,
    "off_peak_tusd_in_reais_per_kw": 12.0,
    "off_peak_tusd_in_reais_per_mwh": 127.2,
    "off_peak_te_in_reais_per_mwh": 392.71,
    "power_generation_tusd_in_reais_per_kw": 10.00
}
green = {
    "peak_tusd_in_reais_per_mwh": 852.45,
    "peak_te_in_reais_per_mwh": 620.43,
    "off_peak_tusd_in_reais_per_mwh": 127.2,
    "off_peak_te_in_reais_per_mwh": 392.71,
    "na_tusd_in_reais_per_kw": 13.0,
    "power_generation_tusd_in_reais_per_kw": 10.00
}

a3_start_date = date(2023,1,1)
a3_end_date   = date(2024,10,5)
a4_start_date = date(2023,1,1)
a4_end_date   = date(2024,5,12)

Tariff.objects.bulk_create([
    Tariff(subgroup='A3', distributor=distributor_teste, flag=Tariff.BLUE, **blue, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A3', distributor=distributor_teste, flag=Tariff.GREEN, **green, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A4', distributor=distributor_teste, flag=Tariff.BLUE, **blue, start_date=a4_start_date, end_date=a4_end_date),
    Tariff(subgroup='A4', distributor=distributor_teste, flag=Tariff.GREEN, **green, start_date=a4_start_date, end_date=a4_end_date),
])

# Unidades Consumidoras


uc_453683 = ConsumerUnit.objects.create(
    name='CENTRO OLIMPICO - 466.513-9',
    code='453683',
    is_active=True,
    university=university,
)

contract_453683 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_453683,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=150.0,
    off_peak_contracted_demand_in_kw=150.0,
)

table_453683 = [['2023-09-01', 6279, 50511, 0.0, 158.0, 0, 'False'], 
                ['2023-10-01', 7278, 62297, 0.0, 158.0, 0, 'False'], 
                ['2023-11-01', 6373, 58602, 0.0, 170.0, 0, 'False'], 
                ['2023-12-01', 7409, 60526, 0.0, 150.0, 0, 'False'], 
                ['2024-01-01', 6151, 60944, 0.0, 167.0, 0, 'False'], 
                ['2024-02-01', 7708, 61340, 0.0, 153.0, 0, 'False'], 
                ['2024-03-01', 7710, 59322, 0.0, 158.0, 0, 'False'], 
                ['2024-04-01', 9189, 73533, 0.0, 288.0, 0, 'False'], 
                ['2024-05-01', 10272, 72838, 0.0, 343.0, 0, 'False'], 
                ['2024-06-01', 8501, 72022, 0.0, 357.0, 0, 'False'], 
                ['2024-07-01', 7737, 60690, 0.0, 294.0, 0, 'False'], 
                ['2024-08-01', 6843, 59805, 0.0, 196.0, 0, 'False']]

create_bills_from_table(contract_453683, uc_453683, table_453683)


uc_1417666 = ConsumerUnit.objects.create(
    name='DARCY SG 12 - ID - 492.479-7',
    code='1417666',
    is_active=True,
    university=university,
)

contract_1417666 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_1417666,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=2850.0,
    off_peak_contracted_demand_in_kw=4000.0,
)

table_1417666 = [['2023-09-01', 133638.0, 1189065.0, 2700.0, 3506.0, 0, 'False'], 
                 ['2023-10-01', 146999.0, 1268124.0, 2780.0, 3587.0, 0, 'False'], 
                 ['2023-11-01', 135792.0, 1238839.0, 3156.0, 4216.0, 0, 'False'], 
                 ['2023-12-01', 139044.0, 1258993.0, 2830.0, 3836.0, 0, 'False'], 
                 ['2024-01-01', 134637.0, 1267405.0, 2892.0, 3725.0, 0, 'False'], 
                 ['2024-02-01', 156686.0, 1280663.0, 2872.0, 3425.0, 0, 'False'], 
                 ['2024-03-01', 43094.0, 51926.0, 2850.0, 4000.0, 0, 'False'], 
                 ['2024-04-01', 31090.0, 43356.0, 2850.0, 4000.0, 0, 'False'], 
                 ['2024-05-01', 142509.0, 1160235.0, 3026.0, 4176.0, 0, 'False'], 
                 ['2024-06-01', 166429.0, 1443096.0, 3683.0, 4581.0, 0, 'False'], 
                 ['2024-07-01', 182242.0, 1590852.0, 3748.0, 4677.0, 0, 'False'], 
                 ['2024-08-01', 159377.0, 1520489.0, 3629.0, 5061.0, 0, 'False']]

create_bills_from_table(contract_1417666, uc_1417666, table_1417666)


uc_886483 = ConsumerUnit.objects.create(
    name='UnB CEILANDIA - 1.013.615-0',
    code='886483',
    is_active=True,
    university=university,
)

contract_886483 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_886483,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=35.0,
    off_peak_contracted_demand_in_kw=35.0,
)

table_886483 = [['2023-09-01', 301.0, 3808.0, 0.0, 25.0, 0, 'False'], 
                ['2023-10-01', 274.0, 3154.0, 0.0, 14.0, 0, 'False'], 
                ['2023-11-01', 288.0, 4301.0, 0.0, 34.0, 0, 'False'], 
                ['2023-12-01', 338.0, 5843.0, 0.0, 21.0, 0, 'False'], 
                ['2024-01-01', 274.0, 4231.0, 0.0, 20.0, 0, 'False'], 
                ['2024-02-01', 297.0, 4082.0, 0.0, 35.0, 0, 'False'], 
                ['2024-03-01', 289.0, 4100.0, 0.0, 35.0, 0, 'False'], 
                ['2024-04-01', 256.0, 3234.0, 0.0, 35.0, 0, 'False'], 
                ['2024-05-01', 401.0, 5478.0, 0.0, 35.0, 0, 'False'], 
                ['2024-06-01', 363.0, 5918.0, 0.0, 35.0, 0, 'False'], 
                ['2024-07-01', 387.0, 6411.0, 0.0, 35.0, 0, 'False'], 
                ['2024-08-01', 367.0, 6051.0, 0.0, 35.0, 0, 'False']]

create_bills_from_table(contract_886483, uc_886483, table_886483)


uc_1511891 = ConsumerUnit.objects.create(
    name='L4 N - E.E. BIOLOGIA -466.508-2',
    code='1511891',
    is_active=True,
    university=university,
)

contract_1511891 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_1511891,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=90.0,
    off_peak_contracted_demand_in_kw=90.0,
)

table_1511891 = [['2023-09-01', 503.0, 5415.0, 0.0, 30.0, 0, 'False'], 
                 ['2023-10-01', 528.0, 5845.0, 0.0, 30.0, 0, 'False'], 
                 ['2023-11-01', 577.0, 5966.0, 0.0, 30.0, 0, 'False'], 
                 ['2023-12-01', 562.0, 5993.0, 0.0, 31.0, 0, 'False'], 
                 ['2024-01-01', 509.0, 5864.0, 0.0, 31.0, 0, 'False'], 
                 ['2024-02-01', 588.0, 6089.0, 0.0, 28.0, 0, 'False'], 
                 ['2024-03-01', 434.0, 5011.0, 0.0, 90.0, 0, 'False'], 
                 ['2024-04-01', 432.0, 4766.0, 0.0, 90.0, 0, 'False'], 
                 ['2024-05-01', 519.0, 5374.0, 0.0, 90.0, 0, 'False'], 
                 ['2024-06-01', 579.0, 6300.0, 0.0, 90.0, 0, 'False'], 
                 ['2024-07-01', 563.0, 6608.0, 0.0, 90.0, 0, 'False'], 
                 ['2024-08-01', 548.0, 6194.0, 0.0, 90.0, 0, 'False']]

create_bills_from_table(contract_1511891, uc_1511891, table_1511891)


uc_1042178 = ConsumerUnit.objects.create(
    name='AD CEIL ST LEST - 1.414.317-8',
    code='1042178',
    is_active=True,
    university=university,
)

contract_1042178 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_1042178,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=150.0,
    off_peak_contracted_demand_in_kw=150.0,
)

table_1042178 = [['2023-09-01', 3482.0, 12530.0, 0.0, 91.0, 0, 'False'], 
                 ['2023-10-01', 3789.0, 15765.0, 0.0, 107.0, 0, 'False'], 
                 ['2023-11-01', 3381.0, 14153.0, 0.0, 114.0, 0, 'False'], 
                 ['2023-12-01', 3642.0, 12057.0, 0.0, 144.0, 0, 'False'], 
                 ['2024-01-01', 3800.0, 20259.0, 0.0, 140.0, 0, 'False'], 
                 ['2024-02-01', 4256.0, 15727.0, 0.0, 107.0, 0, 'False'], 
                 ['2024-03-01', 3410.0, 12680.0, 0.0, 150.0, 0, 'False'], 
                 ['2024-04-01', 3347.0, 10624.0, 0.0, 150.0, 0, 'False'], 
                 ['2024-05-01', 3734.0, 11833.0, 0.0, 150.0, 0, 'False'], 
                 ['2024-06-01', 4212.0, 22540.0, 0.0, 167.0, 0, 'False'], 
                 ['2024-07-01', 4874.0, 31848.0, 0.0, 206.0, 0, 'False'], 
                 ['2024-08-01', 4053.0, 29436.0, 0.0, 186.0, 0, 'False']]

create_bills_from_table(contract_1042178, uc_1042178, table_1042178)


uc_12451274 = ConsumerUnit.objects.create(
    name='UnB PLANALTINA -  1.245.127-4',
    code='12451274',
    is_active=True,
    university=university,
)

contract_12451274 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_12451274,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=140.0,
    off_peak_contracted_demand_in_kw=140.0,
)

table_12451274 = [['2023-09-01', 4194.0, 22866.0, 0.0, 102.0, 0, 'False'], 
                  ['2023-10-01', 4854.0, 25256.0, 0.0, 109.0, 0, 'False'], 
                  ['2023-11-01', 3845.0, 20318.0, 0.0, 110.0, 0, 'False'], 
                  ['2023-12-01', 3651.0, 18404.0, 0.0, 105.0, 0, 'False'], 
                  ['2024-01-01', 4944.0, 39626.0, 0.0, 127.0, 0, 'False'], 
                  ['2024-02-01', 6047.0, 29355.0, 0.0, 129.0, 0, 'False'], 
                  ['2024-03-01', 5178.0, 26269.0, 0.0, 102.0, 0, 'False'], 
                  ['2024-04-01', 4514.0, 25111.0, 0.0, 140.0, 0, 'False'], 
                  ['2024-05-01', 4119.0, 20860.0, 0.0, 140.0, 0, 'False'], 
                  ['2024-06-01', 5650.0, 29869.0, 0.0, 140.0, 0, 'False'], 
                  ['2024-07-01', 5550.0, 31340.0, 0.0, 164.0, 0, 'False'], 
                  ['2024-08-01', 5667.0, 33393.0, 0.0, 149.0, 0, 'False']]

create_bills_from_table(contract_12451274, uc_12451274, table_12451274)


uc_1007165 = ConsumerUnit.objects.create(
    name='UnB GAMA LESTE - 1.245.173-8',
    code='1007165',
    is_active=True,
    university=university,
)

contract_1007165 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_1007165,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=150.0,
    off_peak_contracted_demand_in_kw=150.0,
)

table_1007165 = [['2023-09-01', 4004.0, 5142.0, 0.0, 132.0, 0, 'False'], 
                 ['2023-10-01', 4670.0, 6902.0, 0.0, 130.0, 0, 'False'], 
                 ['2023-11-01', 2274.0, 0.0, 0.0, 149.0, 0, 'False'], 
                 ['2023-12-01', 4384.0, 3967.0, 0.0, 145.0, 0, 'False'], 
                 ['2024-01-01', 5125.0, 2234.0, 0.0, 156.0, 0, 'False'], 
                 ['2024-02-01', 6086.0, 5717.0, 0.0, 156.0, 0, 'False'], 
                 ['2024-03-01', 5306.0, 4764.0, 0.0, 153.0, 0, 'False'], 
                 ['2024-04-01', 5082.0, 2979.0, 0.0, 150.0, 0, 'False'], 
                 ['2024-05-01', 1904.0, 0.0, 0.0, 164.0, 0, 'False'], 
                 ['2024-06-01', 6081.0, 10813.0, 0.0, 197.0, 0, 'False'], 
                 ['2024-07-01', 7491.0, 24653.0, 0.0, 230.0, 0, 'False'], 
                 ['2024-08-01', 6769.0, 23757.0, 0.0, 255.0, 0, 'False']]

create_bills_from_table(contract_1007165, uc_1007165, table_1007165)


uc_454523 = ConsumerUnit.objects.create(
    name='FAZ.AGUA LIMPA - 466793-X004545',
    code='454523',
    is_active=True,
    university=university,
)

contract_454523 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_454523,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=65.0,
    off_peak_contracted_demand_in_kw=65.0,
)

table_454523 = [['2023-09-01', 143.0, 1558.0, 0.0, 65.0, 0, 'False'], 
                ['2023-10-01', 143.0, 1558.0, 0.0, 34.0, 0, 'False'], 
                ['2023-11-01', 885.0, 9827.0, 0.0, 41.0, 0, 'False'], 
                ['2023-12-01', 988.0, 9596.0, 0.0, 40.0, 0, 'False'], 
                ['2024-01-01', 742.0, 9657.0, 0.0, 46.0, 0, 'False'], 
                ['2024-02-01', 1019.0, 12027.0, 0.0, 52.0, 0, 'False'], 
                ['2024-03-01', 1018.0, 11733.0, 0.0, 65.0, 0, 'False'], 
                ['2024-04-01', 1218.0, 13889.0, 0.0, 65.0, 0, 'False'], 
                ['2024-05-01', 1266.0, 13244.0, 0.0, 65.0, 0, 'False'], 
                ['2024-06-01', 1031.0, 12456.0, 0.0, 65.0, 0, 'False'], 
                ['2024-07-01', 906.0, 11372.0, 0.0, 65.0, 0, 'False'], 
                ['2024-08-01', 844.0, 10623.0, 0.0, 66.0, 0, 'False']]

create_bills_from_table(contract_454523, uc_454523, table_454523)


uc_1258045 = ConsumerUnit.objects.create(
    name='GB A CP DARCY RIBEIRO-2.0873581',
    code='1258045',
    is_active=True,
    university=university,
)

contract_1258045 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_1258045,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=30.0,
    off_peak_contracted_demand_in_kw=30.0,
)

table_1258045 = [['2023-09-01', 731.0, 6950.0, 0.0, 30.0, 0, 'False'], 
                 ['2023-10-01', 815.0, 7914.0, 0.0, 33.0, 0, 'False'], 
                 ['2023-11-01', 763.0, 7645.0, 0.0, 36.0, 0, 'False'], 
                 ['2023-12-01', 845.0, 8037.0, 0.0, 32.0, 0, 'False'], 
                 ['2024-01-01', 732.0, 7496.0, 0.0, 36.0, 0, 'False'], 
                 ['2024-02-01', 0.0, 0.0, 0.0, 0.0, 0, 'False'], 
                 ['2024-03-01', 0.0, 0.0, 0.0, 0.0, 0, 'False'], 
                 ['2024-04-01', 0.0, 0.0, 0.0, 0.0, 0, 'False'], 
                 ['2024-05-01', 939.0, 8782.0, 0.0, 41.0, 0, 'False'], 
                 ['2024-06-01', 875.0, 8049.0, 0.0, 44.0, 0, 'False'], 
                 ['2024-07-01', 1257.0, 12366.0, 0.0, 57.0, 0, 'False'], 
                 ['2024-08-01', 1217.0, 12120.0, 0.0, 54.0, 0, 'False']]

create_bills_from_table(contract_1258045, uc_1258045, table_1258045)


uc_625205 = ConsumerUnit.objects.create(
    name='HVET - 673.751-x',
    code='625205',
    is_active=True,
    university=university,
)

contract_625205 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_625205,
    distributor=distributor_teste,
    start_date=date(2022,1,1),
    supply_voltage=13.8,
    peak_contracted_demand_in_kw=95.0,
    off_peak_contracted_demand_in_kw=95.0,
)

table_625205 = [['2023-09-01', 1430.0, 15786.0, 0.0, 61.0, 0, 'False'], 
                ['2023-10-01', 1689.0, 18307.0, 0.0, 80.0, 0, 'False'], 
                ['2023-11-01', 1537.0, 17667.0, 0.0, 89.0, 0, 'False'], 
                ['2023-12-01', 1700.0, 16986.0, 0.0, 69.0, 0, 'False'], 
                ['2024-01-01', 1419.0, 17248.0, 0.0, 76.0, 0, 'False'], 
                ['2024-02-01', 1738.0, 17355.0, 0.0, 72.0, 0, 'False'], 
                ['2024-03-01', 1571.0, 14740.0, 0.0, 95.0, 0, 'False'], 
                ['2024-04-01', 1558.0, 14961.0, 0.0, 95.0, 0, 'False'], 
                ['2024-05-01', 1266.0, 13244.0, 0.0, 95.0, 0, 'False'], 
                ['2024-06-01', 1886.0, 22515.0, 0.0, 110.0, 0, 'False'], 
                ['2024-07-01', 2360.0, 26189.0, 0.0, 111.0, 0, 'False'], 
                ['2024-08-01', 2055.0, 24498.0, 0.0, 110.0, 0, 'False']]

create_bills_from_table(contract_625205, uc_625205, table_625205)


