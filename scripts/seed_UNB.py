#!/usr/local/bin/python

from random import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff
from contracts.models import Contract, EnergyBill

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

def data_size(list):
    size = len(list)

    return size

def update_data(list, size):
    current_date = datetime.now().date()
    n_months = size - 1

    for i in range(size):
        new_date = current_date - relativedelta(months=n_months - i)
        list[i][0] = new_date.strftime('%Y-%m-%d')

    return list

##########################################################################

# Universidade

university = University.objects.create(
    name='Universidade de Brasília',
    acronym='UnB',
    cnpj='00038174000143'
)

# Usuários

admin_university_user = UniversityUser.objects.create(
    university=university,
    type=UniversityUser.Type.UNIVERSITY_ADMIN,
    password='unb',
    email='admin@unb.br',
    first_name="João",
    last_name="da Silva",
    is_seed_user=True
)

university_user = UniversityUser.objects.create(
    university=university,
    type=UniversityUser.Type.UNIVERSITY_USER,
    password='unb',
    email='usuario@unb.br',
    first_name="José",
    last_name="Santos",
    is_seed_user=True
)

# Distribuidoras

distributor_neoenergia = Distributor.objects.create(
    name='Neoenergia',
    cnpj='07522669000192',
    university=university,
)

distributor_ceb = Distributor.objects.create(
    name='CEB',
    cnpj='00070698000111',
    university=university,
)

# Tarifas
blue = {
    "peak_tusd_in_reais_per_kw": 89.29,
    "peak_tusd_in_reais_per_mwh": 117.13,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_kw": 31.53,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02,
    "power_generation_tusd_in_reais_per_kw": 10.00
}
green = {
    "peak_tusd_in_reais_per_mwh": 2280.15,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02,
    "na_tusd_in_reais_per_kw": 31.53,
    "power_generation_tusd_in_reais_per_kw": 10.00
}

a3_start_date = date(2022,10,2)
a3_end_date   = date(2023,10,5)
a4_start_date = date(2023,6,17)
a4_end_date   = date(2024,5,12)

Tariff.objects.bulk_create([
    Tariff(subgroup='A3', distributor=distributor_neoenergia, flag=Tariff.BLUE, **blue, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A3', distributor=distributor_neoenergia, flag=Tariff.GREEN, **green, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A4', distributor=distributor_neoenergia, flag=Tariff.BLUE, **blue, start_date=a4_start_date, end_date=a4_end_date),
    Tariff(subgroup='A4', distributor=distributor_neoenergia, flag=Tariff.GREEN, **green, start_date=a4_start_date, end_date=a4_end_date),
])

# Unidades Consumidoras

uc_campus_darcy = ConsumerUnit.objects.create(
    name='Campus Darcy Ribeiro',
    code='3410000019',
    is_active=True,
    university=university,
)

contract_campus_darcy = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_darcy,
    distributor=distributor_neoenergia,
    start_date=date(2022,11,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=1000,
    off_peak_contracted_demand_in_kw=1680,
)

uc_campus_ceilandia = ConsumerUnit.objects.create(
    name='Campus Ceilândia',
    code='3410000020',
    is_active=True,
    university=university,
)

contract_campus_ceilandia = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_ceilandia,
    distributor=distributor_neoenergia,
    start_date=date(2022,11,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=1000,
    off_peak_contracted_demand_in_kw=1680,
)

uc_campus_planaltina = ConsumerUnit.objects.create(
    name='Campus Planaltina',
    code='3410000021',
    is_active=True,
    university=university,
)

contract_campus_planaltina = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_campus_planaltina,
    distributor=distributor_neoenergia,
    start_date=date(2022,9,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=300,
    off_peak_contracted_demand_in_kw=300,
)

uc_campus_gama = ConsumerUnit.objects.create(
    name='Campus Gama',
    code='3410000022',
    is_active=True,
    university=university,
)

contract_campus_gama = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_gama,
    distributor=distributor_neoenergia,
    start_date=date(2022,8,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=100,
    off_peak_contracted_demand_in_kw=250,
)

uc_fazenda_agua_limpa = ConsumerUnit.objects.create(
    name='Fazenda Água Limpa',
    code='3410000023',
    is_active=True,
    university=university,
)

contract_fazenda_agua_limpa = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_fazenda_agua_limpa,
    distributor=distributor_neoenergia,
    start_date=date(2022,8,1),
    subgroup="A3",
    peak_contracted_demand_in_kw=100,
    off_peak_contracted_demand_in_kw=250,
)

uc_estacao = ConsumerUnit.objects.create(
    name='Estação Meteorológica',
    code='3410000024',
    is_active=False,
    university=university,
)

contract_estacao = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_estacao,
    distributor=distributor_ceb,
    start_date=date(2022,3,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=100,
    off_peak_contracted_demand_in_kw=250,
)


# Formato da Tabela de Faturas: Data, peak_consumption_in_kwh, off_peak_consumption_in_kwh, peak_measured_demand_in_kw, off_peak_measured_demand_in_kw, invoice_in_reais
table_campus_darcy = [['2022-11-01', 20707.0, 281450.0, 538.00, 1306.62, 211121.14],
                      ['2022-12-01', 29836.0, 343275.0, 665.28, 1319.22, 237945.24],
                      ['2023-01-01', 45102.0, 365256.0, 1094.94, 1863.54, 282474.49],
                      ['2023-02-01', 49273.0, 405235.0, 1115.10, 1799.28, 306234.71],
                      ['2023-03-01', 43034.0, 363988.0, 1049.58, 1501.92, 293856.63],
                      ['2023-04-01', 36692.0, 294456.0, 946.26, 1324.26, 266057.91],
                      ['2023-05-01', 23281.0, 216430.0, 635.04, 1014.30, 209543.13],
                      ['2023-06-01', 34557.0, 278715.0, 811.44, 1326.78, 249685.69],
                      ['2023-07-01', 53644.0, 399173.0, 1278.90, 1929.06, 385557.59],
                      ['2023-08-01', 46293.0, 371087.0, 1113.84, 1842.12, 328455.38],
                      ['2023-09-01', 53072.0, 434993.0, 1362.06, 2055.06, 436850.05]]

size_darcy = data_size(table_campus_darcy)
table_campus_darcy = update_data(table_campus_darcy, size_darcy)
create_bills_from_table(contract_campus_darcy, uc_campus_darcy, table_campus_darcy)

table_campus_ceilandia = [['2022-11-01', 20707.0, 281450.0, 538.00, 1306.62, 211121.14, False],
                      ['2022-12-01', 29836.0, 343275.0, 665.28, 1319.22, 237945.24, False],
                      ['2023-01-01', 45102.0, 365256.0, 1094.94, 1863.54, 282474.49, True],
                      ['2023-02-01', 49273.0, 405235.0, 1115.10, 1799.28, 306234.71, False],
                      ['2023-03-01', 43034.0, 363988.0, 1049.58, 1501.92, 293856.63, False],
                      ['2023-04-01', 36692.0, 294456.0, 946.26, 1324.26, 266057.91, False],
                      ['2023-05-01', 23281.0, 216430.0, 635.04, 1014.30, 209543.13, False],
                      ['2023-06-01', 34557.0, 278715.0, 811.44, 1326.78, 249685.69, False],
                      ['2023-07-01', 53644.0, 399173.0, 1278.90, 1929.06, 385557.59, False],
                      ['2023-08-01', 46293.0, 371087.0, 1113.84, 1842.12, 328455.38, False],
                      ['2023-09-01', 53072.0, 434993.0, 1362.06, 2055.06, 436850.05, False],
                      ['2023-01-01', 52841.0, 503043.0, 1525.06, 1988.06, 525010.05, False]]

size_ceilandia = data_size(table_campus_ceilandia)
table_campus_ceilandia = update_data(table_campus_ceilandia, size_ceilandia)
create_bills_from_table(contract_campus_ceilandia, uc_campus_ceilandia, table_campus_ceilandia)

table_campus_planaltina = [['2022-09-01', 0707.0, 81450.0, 38.00, 306.62, 11121.14],
                            ['2022-10-01', 0707.0, 81450.0, 38.00, 306.62, 11121.14],
                            ['2022-11-01', 0707.0, 81450.0, 38.00, 306.62, 11121.14],
                            ['2022-12-01', 9836.0, 43275.0, 65.28, 319.22, 37945.24],
                            ['2023-01-01', 5102.0, 65256.0, 094.94, 863.54, 82474.49],
                            ['2023-02-01', 9273.0, 05235.0, 115.10, 799.28, 06234.71],
                            ['2023-03-01', 3034.0, 63988.0, 049.58, 501.92, 93856.63],
                            ['2023-04-01', 6692.0, 94456.0, 46.26, 324.26, 66057.91],
                            ['2023-05-01', 3281.0, 16430.0, 35.04, 014.30, 09543.13],
                            ['2023-06-01', 4557.0, 78715.0, 11.44, 326.78, 49685.69],
                            ['2023-07-01', 3644.0, 99173.0, 278.90, 929.06, 85557.59],
                            ['2023-08-01', 6293.0, 71087.0, 113.84, 842.12, 28455.38],
                            ['2023-09-01', 3072.0, 34993.0, 362.06, 055.06, 36850.05],
                            ['2023-10-01', 2841.0, 3043.0, 525.06, 988.06, 25010.05],
                            ['2023-11-01', 2954.0, 3243.0, 499.6, 1010, 23010.05],
                            ['2023-12-01', 3144.0, 3543.0, 485.3, 975.6, 23010.05]]

size_planaltina = data_size(table_campus_planaltina)
table_campus_planaltina = update_data(table_campus_planaltina, size_planaltina)
create_bills_from_table(contract_campus_planaltina, uc_campus_planaltina, table_campus_planaltina)

table_campus_gama = [['2022-08-01', 0707.0, 81450.0, 38.00, 306.62, 11121.14],
                            ['2022-09-01', 794.0, 1450.0, 38.00, 306.62, 11121.14],
                            ['2022-10-01', 785.0, 1450.0, 33.00, 302.5, 11121.14],
                            ['2022-11-01', 707.0, 1450.0, 39.00, 300.35, 11121.14],
                            ['2022-12-01', 9836.0, 3275.0, 65.28, 319.22, 37945.24],
                            ['2023-01-01', 5102.0, 5256.0, 094.94, 863.54, 82474.49],
                            ['2023-02-01', 232.0, 3445.0, 11.93, 35.05, 6234.71],
                            ['2023-03-01', 230.0, 3665.0, 7.13,  52.52, 93856.63],
                            ['2023-04-01', 299.0, 4193.0, 13.89, 42.68, 66057.91],
                            ['2023-05-01', 312.0, 3821.0, 11.93, 30.38, 09543.13],
                            ['2023-06-01', 311.0, 3550.0, 20.17, 36.77, 49685.69],
                            ['2023-07-01', 365.0, 3105.0, 17.71, 29.76, 85557.59],
                            ['2023-08-01', 311.0, 2268.0, 17.58, 23.49, 28455.38],
                            ['2023-09-01', 248.0, 2040.0, 9.96,  21.77, 36850.05],
                            ['2023-10-01', 408.0, 2573.0, 22.26, 23.24, 25010.05],
                            ['2023-11-01', 453.0, 3447.0, 19.68, 34.80, 25010.05],
                            ['2023-12-01', 495.0, 3753.0, 27.06, 47.84, 23010.05],
                            ['2023-01-01', 342.0, 3580.0, 15.37, 31.36, 23010.05]]

size_gama = data_size(table_campus_gama)
table_campus_gama = update_data(table_campus_gama, size_gama)
create_bills_from_table(contract_campus_gama, uc_campus_gama, table_campus_gama)

table_fazenda_agua_limpa = [['2023-09-01', 248.0, 2040.0, 9.96,  21.77, 36850.05],
                            ['2023-10-01', 408.0, 2573.0, 22.26, 23.24, 25010.05],
                            ['2023-11-01', 453.0, 3447.0, 19.68, 34.80, 25010.05],
                            ['2023-12-01', 495.0, 3753.0, 27.06, 47.84, 23010.05],
                            ['2023-01-01', 342.0, 3580.0, 15.37, 31.36, 23010.05]]

size_fazenda_agua_limpa = data_size(table_fazenda_agua_limpa)
table_fazenda_agua_limpa = update_data(table_fazenda_agua_limpa, size_fazenda_agua_limpa)
create_bills_from_table(contract_fazenda_agua_limpa, uc_fazenda_agua_limpa, table_fazenda_agua_limpa)

table_estacao = [['2022-03-01', 248.0, 2040.0, 9.96,  21.77, 36850.05],
                 ['2022-04-01', 408.0, 2573.0, 22.26, 23.24, 25010.05],
                 ['2022-05-01', 342.0, 3580.0, 15.37, 31.36, 23010.05]]

size_estacao = data_size(table_estacao)
table_estacao = update_data(table_estacao, size_estacao)
create_bills_from_table(contract_estacao, uc_estacao, table_estacao)
